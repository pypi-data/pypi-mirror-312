import traceback
from typing import Any, Dict, Optional, cast

from opentelemetry import trace
from opentelemetry._logs.severity import SeverityNumber
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LogRecord
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.util.types import Attributes

from ..constants import DEFAULT_CONFIG, ENDPOINTS
from ..types import TelemetryConfig


class LoggingService:
    """
    A service class that provides structured logging capabilities using OpenTelemetry.

    This service handles log emission with different severity levels and automatically
    correlates logs with traces when available. It supports batch processing of logs
    and exports them to an OTLP endpoint.

    Args:
        config (TelemetryConfig): Configuration object containing logging settings
            such as service name and OTLP endpoint.
        resource (Resource): OpenTelemetry resource object containing service attributes
            and other metadata.
    """

    def __init__(self, config: TelemetryConfig, resource: Resource):
        """
        Initialize the logging service with the provided configuration and resource.

        Sets up the logger provider with batch processing capabilities and configures
        the OTLP exporter for sending logs to the specified endpoint.
        """
        self.config = config
        log_exporter = OTLPLogExporter(
            endpoint=f"{config.otlp_endpoint or DEFAULT_CONFIG['otlp_endpoint']}"
        )

        self.logger_provider = LoggerProvider(resource=resource)
        self.logger_provider.add_log_record_processor(
            BatchLogRecordProcessor(log_exporter)
        )
        self.logger = self.logger_provider.get_logger(config.service_name)

    def _emit_log(
        self,
        severity: SeverityNumber,
        message: str,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Internal method to emit a log record with the specified severity level.

        Automatically correlates the log with the current trace context if available
        by including trace_id and span_id in the attributes.

        Args:
            severity (SeverityNumber): The severity level of the log.
            message (str): The log message to emit.
            attributes (Optional[Dict[str, Any]]): Additional attributes to include
                with the log record.
        """
        if attributes is None:
            attributes = {}

        span = trace.get_current_span()
        if span:
            context = span.get_span_context()
            attributes["trace_id"] = format(context.trace_id, "032x")
            attributes["span_id"] = format(context.span_id, "016x")

        self.logger.emit(
            LogRecord(
                timestamp=None,
                severity_number=severity,
                severity_text=severity.name,
                body=message,
                attributes=cast(Attributes, attributes),
            )
        )

    def info(self, message: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """
        Emit an informational log message.

        Args:
            message (str): The information message to log.
            attributes (Optional[Dict[str, Any]]): Additional attributes to include
                with the log record.
        """
        self._emit_log(SeverityNumber.INFO, message, attributes)

    def error(
        self,
        message: str,
        error: Optional[Exception] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Emit an error log message with optional exception details.

        When an exception is provided, automatically includes error type, message,
        and stack trace in the log attributes.

        Args:
            message (str): The error message to log.
            error (Optional[Exception]): The exception object to include in the log.
            attributes (Optional[Dict[str, Any]]): Additional attributes to include
                with the log record.
        """
        if attributes is None:
            attributes = {}

        if error:
            attributes.update(
                {
                    "error.type": error.__class__.__name__,
                    "error.message": str(error),
                    "error.stack_trace": (
                        traceback.format_exc()
                        if traceback.format_exc() != "NoneType: None\n"
                        else None
                    ),
                }
            )

        self._emit_log(SeverityNumber.ERROR, message, attributes)

    def warn(self, message: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """
        Emit a warning log message.

        Args:
            message (str): The warning message to log.
            attributes (Optional[Dict[str, Any]]): Additional attributes to include
                with the log record.
        """
        self._emit_log(SeverityNumber.WARN, message, attributes)

    def debug(self, message: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """
        Emit a debug log message.

        Args:
            message (str): The debug message to log.
            attributes (Optional[Dict[str, Any]]): Additional attributes to include
                with the log record.
        """
        self._emit_log(SeverityNumber.DEBUG, message, attributes)

    async def shutdown(self) -> None:
        """
        Shutdown the logging service gracefully.

        Ensures all pending logs are flushed and resources are properly cleaned up.
        This method should be called when shutting down the application.
        """
        await self.logger_provider.shutdown()
