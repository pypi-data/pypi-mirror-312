"""Object schemas for the elements in the calendar sync flow."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from source.config import CONFIG


@dataclass
class CalendarEvent:
    """Dataclass representation of a calendar event with additional entry-specific metadata."""

    status: str
    start: str
    end: str
    summary: str
    _idx: Optional[int] = field(default=None, init=False)
    _project: str | int = field(default=CONFIG.default_noko_project)
    _tag: str = field(default=CONFIG.default_noko_tag)

    @property
    def duration(self) -> int:
        diff = datetime.fromisoformat(self.end) - datetime.fromisoformat(self.start)
        duration = diff.total_seconds() / 60
        return int(duration)

    @duration.setter
    def duration(self, duration: int) -> None:
        self.duration = duration

    @property
    def idx(self) -> int | None:
        return self._idx

    @idx.setter
    def idx(self, idx: int) -> None:
        self._idx = idx

    @property
    def project(self) -> str | int:
        return self._project

    @project.setter
    def project(self, project: str | int) -> None:
        self._project = project

    @property
    def tag(self) -> str:
        return self._tag

    @tag.setter
    def tag(self, tag: str) -> None:
        self._tag = tag
