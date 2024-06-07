from pydantic import BaseModel, Field


class SuccessOutput(BaseModel):
    success: bool = Field(default=True, title="success")


class CreateOutput(SuccessOutput):
    id: int = Field(title="created")
