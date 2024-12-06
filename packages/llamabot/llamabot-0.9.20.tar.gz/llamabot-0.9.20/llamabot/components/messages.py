"""Definitions for the different types of messages that can be sent."""

from pydantic import BaseModel, Field


class BaseMessage(BaseModel):
    """A base message class."""

    role: str
    content: str
    prompt_hash: str | None = Field(default=None)

    # Implement slicing for message contents so that I can get content[:-i].
    def __getitem__(self, index):
        """Get the content of the message at the given index."""
        return self.__class__(content=self.content[index], role=self.role)

    def __len__(self):
        """Get the length of the message."""
        return len(self.content)

    def __radd__(self, other: str) -> "BaseMessage":
        """Right add operation for BaseMessage.

        :param other: The string to add to the content.
        :returns: A new BaseMessage with the updated content.
        """
        if isinstance(other, str):
            return self.__class__(content=other + self.content, role=self.role)

    def __add__(self, other: str) -> "BaseMessage":
        """Left add operation for BaseMessage.

        :param other: The string to add to the content.
        :returns: A new BaseMessage with the updated content.
        """
        if isinstance(other, str):
            return self.__class__(content=self.content + other, role=self.role)


class SystemMessage(BaseMessage):
    """A message from the system."""

    content: str
    role: str = "system"


class HumanMessage(BaseMessage):
    """A message from a human."""

    content: str
    role: str = "user"


class AIMessage(BaseMessage):
    """A message from the AI."""

    content: str
    role: str = "assistant"


class ToolMessage(BaseMessage):
    """A message from the AI."""

    content: str
    role: str = "tool"


class RetrievedMessage(BaseMessage):
    """A message retrieved from the history."""

    content: str
    role: str = "system"


def retrieve_messages_up_to_budget(
    messages: list[BaseMessage], character_budget: int
) -> list[BaseMessage]:
    """Retrieve messages up to the character budget.

    :param messages: The messages to retrieve.
    :param character_budget: The character budget to use.
    :returns: The retrieved messages.
    """
    used_chars = 0
    retrieved_messages = []
    for message in messages:
        if not isinstance(message, (BaseMessage, str)):
            raise ValueError(
                f"Expected message to be of type BaseMessage or str, got {type(message)}"
            )
        used_chars += len(message)
        if used_chars > character_budget:
            # append whatever is left
            retrieved_messages.append(message[: used_chars - character_budget])
            break
        retrieved_messages.append(message)
    return retrieved_messages
