import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from openinference.instrumentation.langchain import LangChainInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor

load_dotenv()

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)

application_insights_connection_string = project_client.telemetry.get_connection_string()

exporter = AzureMonitorTraceExporter.from_connection_string(application_insights_connection_string)

tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)

span_processor = BatchSpanProcessor(exporter, schedule_delay_millis=60000)
tracer_provider.add_span_processor(span_processor)
tracer_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

tracer = trace.get_tracer(__name__)

LangChainInstrumentor().instrument()

prompt = ChatPromptTemplate.from_messages([("system", "You are a helpful assistant."), ("user", "{text}")])

parser = StrOutputParser()


model = ChatAnthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
    model="claude-3-7-sonnet-latest",
)

chain = prompt | model | parser
chain_config = chain.with_config(run_name="Langchain_LangchainInstrumentor")
response = chain_config.invoke({"text": "What is the capital of France?"})

print(f"Response: {response}")
