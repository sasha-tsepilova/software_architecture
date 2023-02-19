from pydantic import BaseModel

class Message(BaseModel):
    uuid: int
    message: str