from typing import Literal

from pydantic import BaseModel


class HistoryEntry(BaseModel):
    """A single entry in the chat history"""

    user_type: Literal["user", "assistant"]
    """The type of the user"""
    message: str
    """The message of the user"""
