from typing import Final

DEFAULT_CONFIG: Final = {
    "otlp_endpoint": "http://opentelemetry-kube-stack-dev-collector.monitoring.svc.cluster.local:4318",
    "metric_interval_ms": 5000,
    "version": "1.0.0",
}

RESOURCE_ATTRIBUTES: Final = {
    "SERVICE_NAME": "service.name",
    "DEPLOYMENT_ENVIRONMENT": "deployment.environment",
    "SERVICE_VERSION": "service.version",
}

ENDPOINTS: Final = {
    "METRICS": "/v1/metrics",
    "LOGS": "/v1/logs",
    "TRACES": "/v1/traces",
}
