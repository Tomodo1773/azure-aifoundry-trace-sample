import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.ai.projects import AIProjectClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry import configure_azure_monitor
from dotenv import load_dotenv
from opentelemetry.trace import get_tracer

load_dotenv()

tracer = get_tracer(__name__)

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

application_insights_connection_string = project_client.telemetry.get_connection_string()

if application_insights_connection_string:
    configure_azure_monitor(connection_string=application_insights_connection_string)

client = ChatCompletionsClient(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=AzureKeyCredential(
        os.environ["AZURE_INFERENCE_CREDENTIAL"],
    ),
    model="DeepSeek-V3",
)

message = [
    SystemMessage("You are a helpful assistant."),
    UserMessage("Hello"),
]

with tracer.start_as_current_span("AIInference_AzureMonitor_Dist"):
    response = client.complete(messages=message)
    print(f"Response: {response}")
