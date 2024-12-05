from typing import Any, Awaitable, Callable, Dict, Optional, TypeVar

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Status, StatusCode

from ..constants import DEFAULT_CONFIG, ENDPOINTS
from ..types import TelemetryConfig

T = TypeVar("T")


class TracingService:
    """
    A service class that provides distributed tracing capabilities using OpenTelemetry.

    This service handles trace creation, span management, and automatic instrumentation.
    It supports batch processing of spans and exports them to an OTLP endpoint.
    The service provides capabilities for HTTP request tracing and manual instrumentation
    for custom operations.

    Args:
        config (TelemetryConfig): Configuration object containing tracing settings
            such as service name and OTLP endpoint.
        resource (Resource): OpenTelemetry resource object containing service attributes
            and other metadata.
    """

    def __init__(self, config: TelemetryConfig, resource: Resource):
        """
        Initialize the tracing service with the provided configuration and resource.

        Sets up the tracer provider with batch processing capabilities, configures
        the OTLP exporter, and initializes request instrumentation.
        """
        self.config = config
        trace_exporter = OTLPSpanExporter(
            endpoint=f"{config.otlp_endpoint or DEFAULT_CONFIG['otlp_endpoint']}"
        )

        self.tracer_provider = TracerProvider(resource=resource)
        self.tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
        trace.set_tracer_provider(self.tracer_provider)

        # Auto-instrument HTTP requests
        RequestsInstrumentor().instrument()

    def instrument_fastapi(self, app):
        """
        Add OpenTelemetry instrumentation to a FastAPI application.

        Automatically creates spans for incoming HTTP requests, including timing
        information, request details, and response status.

        Args:
            app: The FastAPI application instance to instrument.
        """
        FastAPIInstrumentor.instrument_app(app)

    async def create_span(
        self,
        name: str,
        operation: Callable[[], Awaitable[T]],
        attributes: Optional[Dict[str, Any]] = None,
    ) -> T:
        """
        Create a new span and execute an async operation within its context.

        This method creates a new span, sets provided attributes, executes the
        operation, and automatically handles success and error states. It ensures
        proper span status setting and error recording.

        Args:
            name (str): Name of the span to create.
            operation (Callable[[], Awaitable[T]]): Async operation to execute
                within the span context.
            attributes (Optional[Dict[str, Any]]): Key-value pairs to set as
                span attributes.

        Returns:
            T: The result of the executed operation.

        Raises:
            Exception: Any exception raised by the operation is recorded in the
                span and re-raised.
        """
        tracer = trace.get_tracer("default")

        with tracer.start_as_current_span(name) as span:
            try:
                if attributes:
                    for key, value in attributes.items():
                        span.set_attribute(key, value)

                result = await operation()
                span.set_status(Status(StatusCode.OK))
                return result

            except Exception as error:
                span.record_exception(error)
                span.set_status(Status(StatusCode.ERROR, description=str(error)))
                raise

    def add_attributes(self, attributes: Dict[str, Any]) -> None:
        """
        Add attributes to the current active span.

        If there is no active span, this method does nothing. Attributes are
        key-value pairs that provide additional context to the span.

        Args:
            attributes (Dict[str, Any]): Dictionary of attributes to add to
                the current span.
        """
        span = trace.get_current_span()
        if span and attributes:
            for key, value in attributes.items():
                span.set_attribute(key, value)

    def record_error(self, error: Exception) -> None:
        """
        Record an error in the current active span.

        Records the exception details in the current span and sets its status
        to ERROR. If there is no active span, this method does nothing.

        Args:
            error (Exception): The exception to record in the current span.
        """
        span = trace.get_current_span()
        if span:
            span.record_exception(error)
            span.set_status(Status(StatusCode.ERROR, description=str(error)))

    async def shutdown(self) -> None:
        """
        Shutdown the tracing service gracefully.

        Ensures all pending spans are flushed and resources are properly cleaned up.
        This method should be called when shutting down the application to ensure
        all traces are properly exported.
        """
        await self.tracer_provider.shutdown()
