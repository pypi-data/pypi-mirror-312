from typing import Any, Dict, Mapping, Optional, cast

from opentelemetry.sdk.resources import Resource
from opentelemetry.util.types import AttributeValue

from autonomize_sdk.telemetry.constants import DEFAULT_CONFIG, RESOURCE_ATTRIBUTES
from autonomize_sdk.telemetry.services.logging_service import LoggingService
from autonomize_sdk.telemetry.services.metrics_service import MetricsService
from autonomize_sdk.telemetry.services.tracing_service import TracingService
from autonomize_sdk.telemetry.types import MetricOptions, TelemetryConfig


class Telemetry:
    """
    A comprehensive telemetry wrapper for OpenTelemetry that provides unified access to metrics,
    logging, and tracing capabilities.

    This class initializes and manages the core telemetry services including metrics collection,
    logging, and distributed tracing. It provides a simplified interface for instrumenting
    applications with observability features.

    Args:
        config (TelemetryConfig): Configuration object containing telemetry settings including
            service name, environment, version, and OTLP endpoint details.
    """

    def __init__(self, config: TelemetryConfig):
        """
        Initialize the Telemetry instance with the provided configuration.

        Sets up resource attributes and initializes metrics, logging, and tracing services.
        """
        version = (
            config.version if config.version is not None else DEFAULT_CONFIG["version"]
        )
        otlp_endpoint = (
            config.otlp_endpoint
            if config.otlp_endpoint is not None
            else DEFAULT_CONFIG["otlp_endpoint"]
        )
        metric_interval = (
            config.metric_interval_ms
            if config.metric_interval_ms is not None
            else DEFAULT_CONFIG["metric_interval_ms"]
        )

        self.config = TelemetryConfig(
            service_name=config.service_name,
            environment=config.environment,
            version=cast(Optional[str], version),
            otlp_endpoint=cast(Optional[str], otlp_endpoint),
            metric_interval_ms=cast(Optional[int], metric_interval),
        )

        # Create properly typed resource attributes
        resource_attrs: Mapping[str, AttributeValue] = {
            RESOURCE_ATTRIBUTES["SERVICE_NAME"]: self.config.service_name,
            RESOURCE_ATTRIBUTES["DEPLOYMENT_ENVIRONMENT"]: self.config.environment,
            RESOURCE_ATTRIBUTES["SERVICE_VERSION"]: str(self.config.version or ""),
        }

        self.resource = Resource.create(resource_attrs)

        # Initialize services
        self.metrics_service = MetricsService(self.config, self.resource)
        self.logging_service = LoggingService(self.config, self.resource)
        self.tracing_service = TracingService(self.config, self.resource)

        # Log initialization
        self.info("Telemetry SDK initialized successfully")

    def create_counter(self, options: MetricOptions):
        """
        Create a counter metric for counting occurrences of events.

        Args:
            options (MetricOptions): Configuration options for the counter including name,
                description, and unit.

        Returns:
            Counter: A counter metric instance that can be used to record values.
        """
        return self.metrics_service.create_counter(options)

    def create_histogram(self, options: MetricOptions):
        """
        Create a histogram metric for measuring distributions of values.

        Args:
            options (MetricOptions): Configuration options for the histogram including name,
                description, and unit.

        Returns:
            Histogram: A histogram metric instance that can be used to record values.
        """
        return self.metrics_service.create_histogram(options)

    def create_up_down_counter(self, options: MetricOptions):
        """
        Create an up/down counter metric that can be incremented and decremented.

        Args:
            options (MetricOptions): Configuration options for the up/down counter including name,
                description, and unit.

        Returns:
            UpDownCounter: An up/down counter metric instance that can be used to record values.
        """
        return self.metrics_service.create_up_down_counter(options)

    def info(self, message: str, attributes: Optional[Dict[str, Any]] = None):
        """
        Log an informational message.

        Args:
            message (str): The message to log.
            attributes (Optional[Dict[str, Any]], optional): Additional attributes to include
                with the log entry. Defaults to None.
        """
        self.logging_service.info(message, attributes)

    def error(
        self,
        message: str,
        error: Optional[Exception] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ):
        """
        Log an error message with optional exception details.

        Args:
            message (str): The error message to log.
            error (Optional[Exception], optional): The exception object to include. Defaults to None.
            attributes (Optional[Dict[str, Any]], optional): Additional attributes to include
                with the log entry. Defaults to None.
        """
        self.logging_service.error(message, error, attributes)

    def warn(self, message: str, attributes: Optional[Dict[str, Any]] = None):
        """
        Log a warning message.

        Args:
            message (str): The warning message to log.
            attributes (Optional[Dict[str, Any]], optional): Additional attributes to include
                with the log entry. Defaults to None.
        """
        self.logging_service.warn(message, attributes)

    def debug(self, message: str, attributes: Optional[Dict[str, Any]] = None):
        """
        Log a debug message.

        Args:
            message (str): The debug message to log.
            attributes (Optional[Dict[str, Any]], optional): Additional attributes to include
                with the log entry. Defaults to None.
        """
        self.logging_service.debug(message, attributes)

    def instrument_fastapi(self, app):
        """
        Add OpenTelemetry instrumentation to a FastAPI application.

        Args:
            app: The FastAPI application instance to instrument.
        """
        self.tracing_service.instrument_fastapi(app)

    async def create_span(
        self, name: str, operation, attributes: Optional[Dict[str, Any]] = None
    ):
        """
        Create and execute an operation within a new trace span.

        Args:
            name (str): Name of the span.
            operation: Async operation to execute within the span.
            attributes (Optional[Dict[str, Any]], optional): Attributes to add to the span.
                Defaults to None.

        Returns:
            Any: The result of the operation.
        """
        return await self.tracing_service.create_span(name, operation, attributes)

    def add_attributes(self, attributes: Dict[str, Any]):
        """
        Add attributes to the current active span.

        Args:
            attributes (Dict[str, Any]): Dictionary of attributes to add to the current span.
        """
        self.tracing_service.add_attributes(attributes)

    def record_error(self, error: Exception):
        """
        Record an error in the current active span.

        Args:
            error (Exception): The exception to record in the current span.
        """
        self.tracing_service.record_error(error)

    async def shutdown(self):
        """
        Shutdown all telemetry services gracefully.

        This method should be called when shutting down the application to ensure
        all pending telemetry data is flushed and resources are cleaned up properly.

        Raises:
            Exception: If any error occurs during shutdown.
        """
        try:
            await self.tracing_service.shutdown()
            await self.metrics_service.shutdown()
            await self.logging_service.shutdown()
            self.info("Telemetry SDK shut down successfully")
        except Exception as e:
            self.error("Error shutting down Telemetry SDK", e)
            raise
