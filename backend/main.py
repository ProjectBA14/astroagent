import json
import uuid
import os

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import StreamingResponse

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from graph import astro_graph

from memory_store import sessions

from schemas import (
    SessionInitRequest,
    SessionInitResponse,
    ChatRequest,
    ChatResponse
)

api = FastAPI()

DEV_MODE = True

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


def create_dev_session():

    initial_state = {

        "messages": [],

        "birth_details": {

            "birth_date": "2005-07-18",

            "birth_time": "09:45",

            "birth_place": "Thiruvananthapuram"
        },

        "natal_chart": {},

        "tool_outputs": [],

        "final_response": ""
    }

    result = astro_graph.invoke(
        initial_state
    )

    return result

@api.post(
    "/session/init",
    response_model=SessionInitResponse
)
def initialize_session(
    request: SessionInitRequest
):

    session_id = str(uuid.uuid4())

    initial_state = {

        "messages": [],

        "birth_details": {

            "birth_date": request.birth_date,

            "birth_time": request.birth_time,

            "birth_place": request.birth_place
        },

        "natal_chart": {},

        "tool_outputs": [],

        "final_response": ""
    }

    result = astro_graph.invoke(
        initial_state
    )

    sessions[session_id] = result

    return SessionInitResponse(

        session_id=session_id,

        message=(
            "Birth chart initialized successfully."
        )
    )


@api.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest
):

    session_id = request.session_id

    if session_id not in sessions:

        if DEV_MODE:

            sessions[session_id] = create_dev_session()

        else:

            return ChatResponse(
                response=(
                    "Session not found. "
                    "Please initialize your birth chart first."
                )
            )

    current_state = sessions[session_id]

    if not current_state.get("natal_chart"):

        return ChatResponse(
            response=(
                "Your birth chart hasn't been initialized yet. "
                "Please complete the onboarding form first."
            )
        )

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


async def stream_agent_response(
    session_id: str,
    message: str
):

    if session_id not in sessions:

        if DEV_MODE:

            sessions[session_id] = create_dev_session()

        else:

            chunk = {
                "token": (
                    "Session not found. "
                    "Please initialize your birth chart first."
                )
            }

            yield f"data: {json.dumps(chunk)}\n\n"

            return

    current_state = sessions[session_id]

    if not current_state.get("natal_chart"):

        chunk = {
            "token": (
                "Your birth chart hasn't been initialized yet. "
                "Please complete the onboarding form first."
            )
        }

        yield f"data: {json.dumps(chunk)}\n\n"

        return

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