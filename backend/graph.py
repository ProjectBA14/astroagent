from langgraph.graph import (
    StateGraph,
    END
)

from langchain_groq import ChatGroq

from langchain_core.messages import (
    SystemMessage
)

from state import AgentState

from prompts import SYSTEM_PROMPT

from tools import (
    compute_birth_chart
)

from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7
)


def chart_generation_node(
    state: AgentState
):

    natal_chart = state.get(
        "natal_chart",
        {}
    )

    birth_details = state.get(
        "birth_details",
        {}
    )

    if natal_chart:

        return state

    chart_data = compute_birth_chart.invoke({

        "birth_date": birth_details["birth_date"],

        "birth_time": birth_details["birth_time"],

        "birth_place": birth_details["birth_place"]
    })

    state["natal_chart"] = chart_data

    return state


def reasoning_node(
    state: AgentState
):

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
            "\nUser Natal Chart Context:\n"
            f"{chart_summary}\n"
        )

    system_message = SystemMessage(

        content=(
            SYSTEM_PROMPT
            + chart_context
        )
    )

    response = llm.invoke([

        system_message,

        *messages
    ])

    state["messages"].append(
        response
    )

    return state


workflow = StateGraph(
    AgentState
)

workflow.add_node(
    "chart_generation",
    chart_generation_node
)

workflow.add_node(
    "reasoning",
    reasoning_node
)

workflow.set_entry_point(
    "chart_generation"
)

workflow.add_edge(
    "chart_generation",
    "reasoning"
)

workflow.add_edge(
    "reasoning",
    END
)

astro_graph = workflow.compile()