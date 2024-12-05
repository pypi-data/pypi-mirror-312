from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TelemetryConfig:
    service_name: str
    environment: str
    version: Optional[str] = "1.0.0"
    otlp_endpoint: Optional[str] = "http://localhost:4317"
    metric_interval_ms: Optional[int] = 5000


@dataclass
class MetricOptions:
    name: str
    description: str
    unit: str = ""
    tags: Optional[Dict[str, str]] = None


@dataclass
class LogAttributes:
    attributes: Dict[str, Any]
