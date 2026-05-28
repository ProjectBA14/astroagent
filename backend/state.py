from typing import TypedDict
from typing import List, Dict, Any

from typing_extensions import Annotated

from langgraph.graph.message import add_messages


class AgentState(TypedDict):

    messages: Annotated[list, add_messages]

    birth_details: Dict[str, Any]

    natal_chart: Dict[str, Any]

    tool_outputs: List[Dict[str, Any]]

    final_response: str