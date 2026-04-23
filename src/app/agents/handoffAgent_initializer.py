import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    PromptAgentDefinitionTextOptions,
    TextResponseFormatJsonSchema
) 
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from services.handoff_service import IntentClassification
from agent_initializer import initialize_agent

load_dotenv()

HANDOFF_AGENT_PROMPT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'prompts', 'HandoffAgentPrompt.txt')
with open(HANDOFF_AGENT_PROMPT_PATH, 'r', encoding='utf-8') as file:
    HANDOFF_AGENT_PROMPT = file.read()

project_endpoint = os.environ["FOUNDRY_ENDPOINT"]

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)

model = os.environ["gpt_deployment"]
name = "handoff-service"
description = "Zava Handoff Service Agent"
instructions = HANDOFF_AGENT_PROMPT

definition = PromptAgentDefinition(
    model=model,
    text=PromptAgentDefinitionTextOptions(
        format=TextResponseFormatJsonSchema(
            name="IntentClassification", schema=IntentClassification.model_json_schema()
        )
    )
    ,
    instructions=instructions,
)

initialize_agent(
    project_client=project_client,
    model=model,
    name=name,
    description=description,
    instructions=instructions,
    definition=definition,
)
