from pydantic import BaseModel


class SessionInitRequest(BaseModel):

    birth_date: str

    birth_time: str

    birth_place: str


class SessionInitResponse(BaseModel):

    session_id: str

    message: str


class ChatRequest(BaseModel):

    session_id: str

    message: str


class ChatResponse(BaseModel):

    response: str