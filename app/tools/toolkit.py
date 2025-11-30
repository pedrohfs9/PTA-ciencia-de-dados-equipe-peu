from .dummy import dummy_tool
from agno.tools import Toolkit

dummy_toolkit = Toolkit(
    name="App Toolkit",
    tools=[dummy_tool]
)