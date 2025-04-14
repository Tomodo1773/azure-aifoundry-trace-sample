import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from langchain_azure_ai.callbacks.tracers import AzureAIInferenceTracer
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)

application_insights_connection_string = project_client.telemetry.get_connection_string()

tracer = AzureAIInferenceTracer(
    connection_string=application_insights_connection_string,
    enable_content_recording=True,
)

model = AzureAIChatCompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    model_name="DeepSeek-V3",
    client_kwargs={"logging_enable": True},
)


system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([("system", system_template), ("user", "{text}")])

parser = StrOutputParser()

chain = prompt_template | model | parser
chain_config = chain.with_config(callbacks=[tracer], run_name="Langchain_AzureAIInferenceTracer")

response = chain_config.invoke({"language": "italian", "text": "hi"})

print("***Print Raw response***")
print(response)
print("***End of Raw response***")
