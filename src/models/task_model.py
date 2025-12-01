from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class Task:
    title: str
    due_time: datetime
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    is_completed: bool = False
    has_alerted_pre: bool = False
    has_alerted_due: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_time": self.due_time.isoformat(),
            "is_completed": self.is_completed,
            "has_alerted_pre": self.has_alerted_pre,
            "has_alerted_due": self.has_alerted_due
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            due_time=datetime.fromisoformat(data["due_time"]),
            is_completed=data["is_completed"],
            has_alerted_pre=data.get("has_alerted_pre", False),
            has_alerted_due=data.get("has_alerted_due", False)
        )

@dataclass
class BreakEvent:
    timestamp: datetime
    type: str = "Stand Up & Walk"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    is_acknowledged: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "type": self.type,
            "is_acknowledged": self.is_acknowledged
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            type=data.get("type", "Stand Up & Walk"),
            is_acknowledged=data.get("is_acknowledged", False)
        )
