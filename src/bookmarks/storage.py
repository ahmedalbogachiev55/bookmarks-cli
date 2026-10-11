"""JSON storage for bookmarks."""

import json
from pathlib import Path

from bookmarks.models import Bookmark

DEFAULT_PATH = Path.home() / ".bookmarks.json"


class Storage:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path if path is not None else DEFAULT_PATH

    def load(self) -> list[Bookmark]:
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [Bookmark.from_dict(item) for item in raw]

    def save(self, bookmarks: list[Bookmark]) -> None:
        data = [b.to_dict() for b in bookmarks]
        self.path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def add(self, url: str, tags: list[str]) -> Bookmark:
        bookmarks = self.load()
        new_id = max((b.id for b in bookmarks), default=0) + 1
        bookmark = Bookmark(id=new_id, url=url, tags=tags)
        bookmarks.append(bookmark)
        self.save(bookmarks)
        return bookmark

    def remove(self, bookmark_id: int) -> bool:
        bookmarks = self.load()
        filtered = [b for b in bookmarks if b.id != bookmark_id]
        if len(filtered) == len(bookmarks):
            return False
        self.save(filtered)
        return True

