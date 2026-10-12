from pydantic import BaseModel, Field


class ImproveDescriptionRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    notes: str = Field(default="", max_length=2000)


class ImproveDescriptionResponse(BaseModel):
    description: str