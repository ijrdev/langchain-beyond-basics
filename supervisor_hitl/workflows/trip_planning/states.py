from typing import Annotated

from pydantic import BaseModel, Field
from langchain.messages import AnyMessage
from langgraph.graph.message import add_messages

class InputState(BaseModel):
    messages: list[AnyMessage]

class ExecutionState(BaseModel):
    messages: Annotated[list[AnyMessage], add_messages] = Field(default_factory=list)

class OutputState(BaseModel):
    messages: list[AnyMessage]