from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from openinference.instrumentation.pydantic_ai import OpenInferenceSpanProcessor
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

from src.core.config import settings

tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)


# If you are using a local instance without auth, ignore these headers
headers = {}
if settings.phoenix_api_key:
    headers = {"Authorization": f"Bearer {settings.phoenix_api_key}"}

exporter = OTLPSpanExporter(endpoint=settings.phoenix_url, headers=headers)

tracer_provider.add_span_processor(OpenInferenceSpanProcessor())
tracer_provider.add_span_processor(SimpleSpanProcessor(exporter))
