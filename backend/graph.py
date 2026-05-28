from langgraph.graph import StateGraph, END

from langchain_groq import ChatGroq

from langchain_core.messages import (
    SystemMessage,
    ToolMessage
)

from state import AgentState

from prompts import SYSTEM_PROMPT

from config import (
    GROQ_API_KEY,
    MODEL_NAME
)

from tools import (
    compute_birth_chart_tool,
    generate_chart_svg_tool
)

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=MODEL_NAME
)

tools = {
    "compute_birth_chart_tool":
    compute_birth_chart_tool,

    "generate_chart_svg_tool":
    generate_chart_svg_tool
}

llm_with_tools = llm.bind_tools(
    list(tools.values())
)


def reasoning_node(state: AgentState):

    messages = state["messages"]

    natal_chart = state.get(
        "natal_chart",
        {}
    )

    chart_context = ""

    if natal_chart:

        chart_summary = natal_chart.get(
            "chart_summary",
            {}
        )

        chart_context = (
            f"\nUser Natal Chart:\n"
            f"{chart_summary}\n"
        )

    system_message = SystemMessage(

        content=(
            SYSTEM_PROMPT
            + chart_context
        )
    )

    response = llm_with_tools.invoke([

        system_message,

        *messages
    ])

    return {
        "messages": [response]
    }


def tool_node(state: AgentState):

    messages = state["messages"]

    last_message = messages[-1]

    tool_messages = []

    natal_chart = state.get(
        "natal_chart",
        {}
    )

    for tool_call in last_message.tool_calls:

        tool_name = tool_call["name"]

        tool = tools[tool_name]

        result = tool.invoke(
            tool_call["args"]
        )

        if tool_name == "compute_birth_chart_tool":

            natal_chart = result

        tool_messages.append(

            ToolMessage(
                content="Birth chart computed successfully.",
                tool_call_id=tool_call["id"]
            )
        )

    return {

        "messages": tool_messages,

        "natal_chart": natal_chart
    }


def should_continue(state: AgentState):

    messages = state["messages"]

    last_message = messages[-1]

    if last_message.tool_calls:

        return "tools"

    return END


graph_builder = StateGraph(AgentState)

graph_builder.add_node(
    "reasoning",
    reasoning_node
)

graph_builder.add_node(
    "tools",
    tool_node
)

graph_builder.set_entry_point(
    "reasoning"
)

graph_builder.add_conditional_edges(
    "reasoning",
    should_continue
)

graph_builder.add_edge(
    "tools",
    "reasoning"
)

astro_graph = graph_builder.compile()