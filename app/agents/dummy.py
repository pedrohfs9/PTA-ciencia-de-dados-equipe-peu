from agno.agent import Agent
from app.tools import dummy_toolkit

dummy_agent = Agent(
    name="Dummy Agent",
    description="A dummy agent for testing purposes.",
    role="This agent provides dummy responses for testing.",
    tools=[dummy_toolkit]
)