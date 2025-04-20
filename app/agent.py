import os
from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from utils.tool_registry import load_mcp_toolset

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

api_key = os.getenv("LITELLM_API_KEY")
model_id = os.getenv("LITELLM_MODEL")
agent_name = os.getenv("AGENT_NAME")
agent_instruction = os.getenv("AGENT_INSTRUCTION")

if not api_key:
    raise ValueError("LITELLM_API_KEY not defined")

async def build_agent():
    tools, exit_stack = await load_mcp_toolset("config_sse_tools.yaml")
    print(f"[INFO] Agent {agent_name} created with the tools: {[tool.name for tool in tools]}")

    agent = LlmAgent(
        model=LiteLlm(model=model_id, api_key=api_key),
        name=agent_name,
        instruction=agent_instruction,
        tools=tools
    )

    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()

    return agent, session_service, artifact_service, exit_stack