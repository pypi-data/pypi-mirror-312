# Autonomize Telemetry SDK

A comprehensive OpenTelemetry-based SDK for application monitoring and observability in Python applications. This SDK provides unified APIs for metrics, logging, and tracing, making it easier to instrument your applications with observability features.

## Features

- **Unified Telemetry**: Seamlessly integrate metrics, logs, and traces
- **Auto-instrumentation**: Automatic instrumentation for popular frameworks (FastAPI)
- **Simple API**: Easy-to-use interface for all telemetry operations
- **Configurable**: Flexible configuration options for different environments

## Installation

Install using pip:

```bash
pip install autonomize-sdk-python
```

Or using Poetry:

```bash
poetry add autonomize-sdk-python
```

## Quick Start

Here's a simple example to get you started:

```python
from autonomize_sdk import Telemetry, TelemetryConfig, MetricOptions

# Initialize telemetry
config = TelemetryConfig(
    service_name="my-service",
    environment="production",
    otlp_endpoint="http://localhost:4317"
)

telemetry = Telemetry(config)

# Create a metric
request_counter = telemetry.create_counter(
    MetricOptions(
        name="http.requests",
        description="Number of HTTP requests"
    )
)

# Log information
telemetry.info("Application started", {"version": "1.0.0"})

# Create a span
async def my_operation():
    # Your operation logic here
    return "result"

result = await telemetry.create_span(
    "my-operation",
    my_operation,
    attributes={"custom.attribute": "value"}
)

# Don't forget to shut down when your application stops
await telemetry.shutdown()
```

## Detailed Documentation

### Prerequisites

- Python 3.8 < 3.12
- An OpenTelemetry collector endpoint (default: http://localhost:4317)

### Configuration

The SDK can be configured using the `TelemetryConfig` class:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `service_name` | `str` | Yes | - | Name of your service |
| `environment` | `str` | Yes | - | Deployment environment (e.g., production, staging, development) |
| `version` | `str` | No | `"1.0.0"` | Version of your service |
| `otlp_endpoint` | `str` | No | `"http://localhost:4317"` | OpenTelemetry collector endpoint |
| `metric_interval_ms` | `int` | No | `5000` | Interval (in milliseconds) for exporting metrics |

Example usage:
```python
config = TelemetryConfig(
    service_name="flexstore-service",
    environment="production",
    version="1.1.0",
    otlp_endpoint="http://otel-collector:4317",
    metric_interval_ms=5000
)
```

### Metrics

Create and use different types of metrics:

```python
# Counter
counter = telemetry.create_counter(
    MetricOptions(name="requests.total", description="Total requests")
)
counter.add(1)

# Histogram
latency = telemetry.create_histogram(
    MetricOptions(name="request.latency", description="Request latency")
)
latency.record(0.025)

# Up/Down Counter
active_requests = telemetry.create_up_down_counter(
    MetricOptions(name="requests.active", description="Active requests")
)
active_requests.add(1)
active_requests.add(-1)
```

### Logging

Various logging levels are available:

```python
# Info logging
telemetry.info("Operation completed", {"operation_id": "123"})

# Error logging with exception
try:
    raise ValueError("Invalid input")
except Exception as e:
    telemetry.error("Operation failed", e, {"operation_id": "123"})

# Warning logging
telemetry.warn("Resource running low", {"resource": "memory"})

# Debug logging
telemetry.debug("Processing request", {"request_id": "abc"})
```

### Tracing

Instrument your code with traces:

```python
# Create a span for an operation using decorator
@tracer.start_as_current_span("process_request")
async def process_request():
    return "processed"

# Add attributes to current span
telemetry.add_attributes({"user_id": "456"})

# Record errors in current span
try:
    raise ValueError("Invalid input")
except Exception as e:
    telemetry.record_error(e)
```

### FastAPI Integration

Automatically instrument FastAPI applications:

```python
from fastapi import FastAPI

app = FastAPI()
telemetry.instrument_fastapi(app)
```

## Best Practices

1. **Structured Logging**: Use attributes to add context to your logs:
```python
# HTTP Request Logging
telemetry.info("API request processed", attributes={
    "request_id": "req_7a8b9c",
    "method": "POST",
    "path": "/api/v1/users",
    "status_code": 200,
    "response_time_ms": 45.2,
    "user_id": "usr_123"
})

# Error Logging
telemetry.error("Database connection failed", attributes={
    "database": "users_db",
    "host": "prod-db-1",
    "connection_attempts": 3,
    "latency_ms": 5000,
    "error_code": "ETIMEDOUT"
})
```

2. **Meaningful Metrics**: Create metrics that provide business value:
```python
# Response Time Histogram
latency_histogram = telemetry.create_histogram(
    MetricOptions(
        name="http.response_time",
        description="HTTP request latency distribution",
        unit="ms"
    )
)

# Request Counter
request_counter = telemetry.create_counter(
    MetricOptions(
        name="http.requests.total",
        description="Total number of HTTP requests",
        unit="requests"
    )
)

# Active Sessions Gauge
active_sessions = telemetry.create_up_down_counter(
    MetricOptions(
        name="sessions.active",
        description="Number of currently active user sessions",
        unit="sessions"
    )
)
```

3. **Proper Shutdown**: Always shut down telemetry when your application stops:
```python
# In your FastAPI application
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    telemetry = Telemetry(
        TelemetryConfig(
            service_name="user-service",
            environment="production"
        )
    )
    yield
    # Shutdown
    await telemetry.shutdown()

app = FastAPI(lifespan=lifespan)
```

4. **Span Context**: Use spans to track operations and their context:
```python
async def process_user_request(user_id: str):
    async def operation():
        # Your business logic here
        result = await db.fetch_user(user_id)
        return result

    return await telemetry.create_span(
        "process-user-request",
        operation,
        attributes={
            "user_id": user_id,
            "service": "user-service",
            "operation_type": "read",
            "database": "users_db"
        }
    )
```

5. **Health Metrics**: Track service health and performance:
```python
# Memory Usage
memory_gauge = telemetry.create_up_down_counter(
    MetricOptions(
        name="system.memory.usage",
        description="Current memory usage",
        unit="bytes"
    )
)

# CPU Usage
cpu_utilization = telemetry.create_histogram(
    MetricOptions(
        name="system.cpu.utilization",
        description="CPU utilization percentage",
        unit="percent"
    )
)

# Database Connections
db_connections = telemetry.create_up_down_counter(
    MetricOptions(
        name="database.connections.active",
        description="Number of active database connections",
        unit="connections"
    )
)
await telemetry.shutdown()
```

## Contributing

We welcome contributions! Here's how you can help:

Please read our [**Contributing Guide**](../CONTRIBUTING.md) before making any changes.

## Acknowledgments

- Built with [OpenTelemetry](https://opentelemetry.io/docs/languages/python)
- Inspired by best practices in observability and monitoring

Together, we can make Autonomize SDK better! 🌟
