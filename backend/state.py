from typing import TypedDict, List, Dict, Any

from langchain_core.messages import BaseMessage


class AgentState(TypedDict):

    messages: List[BaseMessage]

    birth_details: Dict[str, Any]

    natal_chart: Dict[str, Any]

    tool_outputs: List[Dict[str, Any]]

    final_response: str