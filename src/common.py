
from dataclasses import dataclass
from typing import Any


@dataclass
class Review:
    """Represents the product review provided as input."""

    text: str


@dataclass
class Message:
    """Structured message exchanged between agents."""

    sender: str
    receiver: str
    task: str
    payload: dict[str, Any]
    status: str = "completed"


def log_message(message: Message) -> None:
    """Print a structured message for execution inspection."""

    print(
        f"[MESSAGE] {message.sender} -> {message.receiver} | "
        f"task={message.task} | payload={message.payload}"
    )


def validate_message(message: Message) -> None:
    """Validate all required message fields."""

    values = {
        "sender": message.sender,
        "receiver": message.receiver,
        "task": message.task,
        "payload": message.payload,
    }

    missing = [
        key
        for key, value in values.items()
        if value is None or value == ""
    ]

    if missing:
        raise ValueError(
            f"Invalid message. Missing fields: {missing}"
        )

    if not isinstance(message.payload, dict):
        raise ValueError("Message payload must be a dictionary.")
