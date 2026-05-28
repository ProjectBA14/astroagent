from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from graph import astro_graph

from schemas import (
    ChatRequest,
    ChatResponse
)

from fastapi.responses import StreamingResponse

from langchain_core.messages import HumanMessage

import json


from memory_store import sessions

api = FastAPI()

api.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


@api.get("/")
def root():

    return {
        "message": "AstroAgent API running"
    }

async def stream_agent_response(
    session_id: str,
    message: str
):

    if session_id not in sessions:

        sessions[session_id] = {

            "messages": [],

            "birth_details": {},

            "natal_chart": {},

            "tool_outputs": [],

            "final_response": ""
        }

    current_state = sessions[session_id]

    current_state["messages"].append(

        HumanMessage(
            content=message
        )
    )

    result = astro_graph.invoke(
        current_state
    )

    sessions[session_id] = result

    messages = result["messages"]

    final_response = ""

    for msg in reversed(messages):

        if isinstance(msg, AIMessage):

            if msg.content:

                final_response = msg.content

                break

    words = final_response.split()

    for word in words:

        chunk = {
            "token": word + " "
        }

        yield f"data: {json.dumps(chunk)}\n\n"


@api.post("/chat/stream")
async def stream_chat(
    request: ChatRequest
):

    generator = stream_agent_response(

        session_id=request.session_id,

        message=request.message
    )

    return StreamingResponse(
        generator,
        media_type="text/event-stream"
    )

@api.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    session_id = request.session_id

    if session_id not in sessions:

        sessions[session_id] = {

            "messages": [],

            "birth_details": {},

            "natal_chart": {},

            "tool_outputs": [],

            "final_response": ""
        }

    current_state = sessions[session_id]

    current_state["messages"].append(

        HumanMessage(
            content=request.message
        )
    )

    result = astro_graph.invoke(
        current_state
    )

    sessions[session_id] = result

    messages = result["messages"]

    final_response = ""

    for message in reversed(messages):

        if isinstance(message, AIMessage):

            if message.content:

                final_response = message.content

                break

    return ChatResponse(
        response=final_response
    )