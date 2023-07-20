import os

from langchain.chat_models import AzureChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate)

API_BASE = "https://eastus.api.cognitive.microsoft.com/"
API_DEPLOYMENT = "gpt-testopenai-dev-eastus-001"
API_KEY = os.getenv("OPENAI_API_KEY")
API_TYPE = "azure"
API_VERSION = "2023-03-15-preview"

templates_list = ['event_briefing.txt', 'race_briefing.txt', 
                  'range_briefing.txt', 'session_briefing.txt']

templates_path = 'prompts/'

def create_prompt(file_name: str) -> ChatPromptTemplate:
    with open(file_name) as f:
        template = f.read()

    system_message, user_message = template.split("\n")

    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_message),
        HumanMessagePromptTemplate.from_template(user_message)])

event_prompt = create_prompt(templates_path + templates_list[0])
race_prompt = create_prompt(templates_path + templates_list[1])
range_prompt = create_prompt(templates_path + templates_list[2])
session_prompt = create_prompt(templates_path + templates_list[3])

model = AzureChatOpenAI(openai_api_base=API_BASE,
                        deployment_name=API_DEPLOYMENT,
                        openai_api_key=API_KEY,
                        openai_api_type=API_TYPE,
                        openai_api_version=API_VERSION,
                        temperature=0.95)