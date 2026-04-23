from typing import Any, List

from azure.core.exceptions import ResourceNotFoundError
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from dotenv import load_dotenv

load_dotenv()

def build_prompt_agent_definition(model: str, instructions: str, tools: List[Any]) -> PromptAgentDefinition:
    return PromptAgentDefinition(
        model=model,
        instructions=instructions,
        tools=tools,
    )


def agent_exists(project_client: AIProjectClient, name: str) -> bool:
    try:
        project_client.agents.get(name)
        return True
    except ResourceNotFoundError:
        return False


def initialize_agent(
    project_client: AIProjectClient,
    model: str,
    name: str,
    description: str,
    instructions: str,
    tools: List[Any] | None = None,
    definition: Any | None = None,
):
    agent_definition = definition or build_prompt_agent_definition(
        model=model,
        instructions=instructions,
        tools=tools or [],
    )

    with project_client:
        exists = agent_exists(project_client, name)
        agent = project_client.agents.create_version(
            agent_name=name,
            description=description,
            definition=agent_definition,
        )
        action = "Updated existing" if exists else "Created new"
        print(f"{action} {name} agent version, ID: {agent.id}")
        return agent
