from pydantic import BaseModel


class ChatRequest(BaseModel):

    birth_date: str

    birth_time: str

    birth_place: str

    message: str


class ChatResponse(BaseModel):

    response: str