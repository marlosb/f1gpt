import os

from langchain.chat_models import AzureChatOpenAI

API_BASE = "https://eastus.api.cognitive.microsoft.com/"
API_DEPLOYMENT = "gpt-testopenai-dev-eastus-001"
API_KEY = os.getenv("OPENAI_API_KEY")
API_TYPE = "azure"
API_VERSION = "2023-03-15-preview"

model = AzureChatOpenAI(openai_api_base=API_BASE,
                        deployment_name=API_DEPLOYMENT,
                        openai_api_key=API_KEY,
                        openai_api_type=API_TYPE,
                        openai_api_version=API_VERSION,
                        temperature=0.95,)