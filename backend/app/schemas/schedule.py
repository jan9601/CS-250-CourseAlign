import re
from pydantic import BaseModel, Field, field_validator
from typing import Optional

_TIME_RE = re.compile(r"^\d{2}:\d{2}$")


class ScheduleBuildRequest(BaseModel):
    classes: list[str] = Field(..., min_length=1, description="Course IDs, e.g. ['CS250', 'MATH150']")
    earliestStart: Optional[str] = Field(None, description="HH:MM — exclude sections starting before this")
    latestEnd: Optional[str] = Field(None, description="HH:MM — exclude sections ending after this")
    instructionMode: Optional[str] = Field(None, description="'in-person' or 'online'")

    @field_validator("earliestStart", "latestEnd")
    @classmethod
    def must_be_hhmm(cls, v: str | None) -> str | None:
        if v is not None and not _TIME_RE.match(v):
            raise ValueError("must be in HH:MM format")
        return v

    @field_validator("classes", mode="before")
    @classmethod
    def strip_and_reject_blank(cls, v):
        cleaned = [c.strip() for c in v if isinstance(c, str) and c.strip()]
        if not cleaned:
            raise ValueError("classes must contain at least one non-empty course ID")
        return cleaned


class SectionOut(BaseModel):
    course: str
    section: str
    days: list[str]
    startTime: str
    endTime: str


class ScheduleOut(BaseModel):
    scheduleId: int
    sections: list[SectionOut]