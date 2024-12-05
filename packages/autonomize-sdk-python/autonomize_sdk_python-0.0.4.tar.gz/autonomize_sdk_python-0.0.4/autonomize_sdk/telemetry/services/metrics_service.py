from typing import Union, cast

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource

from ..constants import DEFAULT_CONFIG, ENDPOINTS
from ..types import MetricOptions, TelemetryConfig


class MetricsService:
    """
    A service class that provides metric collection and export capabilities using OpenTelemetry.

    This service supports creation of different types of metrics (counters, histograms,
    and up/down counters) and periodically exports them to an OTLP endpoint. It handles
    metric configuration, collection, and export with customizable intervals.

    Args:
        config (TelemetryConfig): Configuration object containing metrics settings
            including service name, OTLP endpoint, and metric export interval.
        resource (Resource): OpenTelemetry resource object containing service attributes
            and other metadata.
    """

    def __init__(self, config: TelemetryConfig, resource: Resource):
        """
        Initialize the metrics service with the provided configuration and resource.

        Sets up the meter provider with periodic metric export capabilities and configures
        the OTLP exporter for sending metrics to the specified endpoint.
        """
        self.config = config
        metric_exporter = OTLPMetricExporter(
            endpoint=f"{config.otlp_endpoint or DEFAULT_CONFIG['otlp_endpoint']}"
        )

        interval = config.metric_interval_ms or DEFAULT_CONFIG["metric_interval_ms"]
        interval_ms = float(cast(Union[int, str], interval))

        metric_reader = PeriodicExportingMetricReader(
            metric_exporter,
            interval_ms,
        )

        self.meter_provider = MeterProvider(
            resource=resource, metric_readers=[metric_reader]
        )
        metrics.set_meter_provider(self.meter_provider)
        self.meter = metrics.get_meter(config.service_name)

    def create_counter(self, options: MetricOptions):
        """
        Create a counter metric for counting occurrences or events.

        A counter is a cumulative metric that represents a single monotonically increasing value.
        Counters can only be increased, not decreased, and will only be reset when the process
        restarts.

        Args:
            options (MetricOptions): Configuration options for the counter including:
                - name: The name of the metric
                - description: A human-readable description of the metric
                - unit: The unit of measurement (optional)

        Returns:
            Counter: A counter metric instance that can be used to record values.
        """
        return self.meter.create_counter(
            name=options.name, description=options.description, unit=options.unit
        )

    def create_histogram(self, options: MetricOptions):
        """
        Create a histogram metric for recording distributions of values.

        A histogram tracks the distribution of measurements within the application, such as
        request durations or response sizes. It can be used to calculate statistics like
        percentiles, mean, and standard deviation.

        Args:
            options (MetricOptions): Configuration options for the histogram including:
                - name: The name of the metric
                - description: A human-readable description of the metric
                - unit: The unit of measurement (optional)

        Returns:
            Histogram: A histogram metric instance that can be used to record values.
        """
        return self.meter.create_histogram(
            name=options.name, description=options.description, unit=options.unit
        )

    def create_up_down_counter(self, options: MetricOptions):
        """
        Create an up/down counter metric that can be incremented and decremented.

        An up/down counter is a metric that records a value that can go up or down over time,
        such as the number of active requests or the size of a queue.

        Args:
            options (MetricOptions): Configuration options for the up/down counter including:
                - name: The name of the metric
                - description: A human-readable description of the metric
                - unit: The unit of measurement (optional)

        Returns:
            UpDownCounter: An up/down counter metric instance that can be used to record values.
        """
        return self.meter.create_up_down_counter(
            name=options.name, description=options.description, unit=options.unit
        )

    async def shutdown(self) -> None:
        """
        Shutdown the metrics service gracefully.

        Ensures all pending metrics are flushed and resources are properly cleaned up.
        This method should be called when shutting down the application to ensure
        all metrics are properly exported.
        """
        await self.meter_provider.shutdown()
