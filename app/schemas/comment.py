from pydantic import BaseModel
from datetime import datetime


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: str
    content: str
    author: str
    createdAt: datetime

    model_config = {"from_attributes": True}
