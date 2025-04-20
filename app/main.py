import os
import asyncio
from google.adk.runners import Runner
from agent import build_agent
from google.genai import types
import logging

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

async def main():
    user_id = os.getenv("AGENT_USER_ID")
    agent_name = os.getenv("AGENT_NAME")

    agent, session_service, artifact_service, exit_stack = await build_agent()

    async with exit_stack:
        runner = Runner(agent=agent, session_service=session_service, artifact_service=artifact_service, app_name=agent.name)
        session = session_service.create_session(app_name=agent.name, user_id=user_id)

        print(f"\n👋 Agent {agent.name} is running. Please write your message or type 'exit'.\n")

        while True:
            user_input = input(f"\n{user_id}: ")
            if user_input.strip().lower() in ["sair", "exit", "quit"]:
                break

            events = runner.run_async(
                session_id=session.id,
                new_message=types.Content(role='user', parts=[types.Part(text=user_input)]),
                user_id=user_id
            )

            async for event in events:
                if event.is_final_response():
                    print(f"\n{agent.name}:", event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())