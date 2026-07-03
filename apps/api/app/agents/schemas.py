from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    """Request schema for the AI Agent."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="User message to the AI agent.",
    )

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


class ChatResponse(BaseModel):
    """Response schema returned by the AI Agent."""

    answer: str = Field(
        ...,
        description="Natural language response.",
    )

    model_config = ConfigDict(
        extra="forbid",
    )