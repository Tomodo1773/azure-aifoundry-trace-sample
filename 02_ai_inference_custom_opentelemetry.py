import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.ai.inference.tracing import AIInferenceInstrumentor
from azure.ai.projects import AIProjectClient
from azure.core.credentials import AzureKeyCredential
from azure.core.settings import settings
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor

load_dotenv()

settings.tracing_implementation = "opentelemetry"

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

application_insights_connection_string = project_client.telemetry.get_connection_string()

exporter = AzureMonitorTraceExporter.from_connection_string(application_insights_connection_string)

tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)

span_processor = BatchSpanProcessor(exporter, schedule_delay_millis=60000)
tracer_provider.add_span_processor(span_processor)
tracer_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
tracer = trace.get_tracer(__name__)

AIInferenceInstrumentor().instrument()

client = ChatCompletionsClient(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"]),
    model="DeepSeek-V3",
)

message = [
    SystemMessage("You are a helpful assistant."),
    UserMessage("Hello"),
]

with tracer.start_as_current_span("AIInference_AzureMonitor_Otel"):
    response = client.complete(messages=message)
    print(f"Response: {response}")
