from agno.team import Team

from .another import another_agent
from .dummy import dummy_agent

team = Team(
    name="Example Team",
    mode="route",
    members=[dummy_agent, another_agent],
    instructions="This team is designed to handle example tasks.",
    show_members_responses=True
)