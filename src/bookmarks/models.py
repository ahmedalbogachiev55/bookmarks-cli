"""Bookmark data model."""

from dataclasses import dataclass, field


@dataclass
class Bookmark:
    id: int
    url: str
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"id": self.id, "url": self.url, "tags": self.tags}

    @classmethod
    def from_dict(cls, data: dict) -> "Bookmark":
        return cls(id=data["id"], url=data["url"], tags=data.get("tags", []))
