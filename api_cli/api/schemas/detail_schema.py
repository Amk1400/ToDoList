from pydantic import BaseModel


class DetailBase(BaseModel):
    title: str
    description: str