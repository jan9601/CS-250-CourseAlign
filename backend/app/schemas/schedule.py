from pydantic import BaseModel, Field
from typing import Literal
from .section import Section


class ScheduleBuildRequest(BaseModel):
    courses: list[str] = Field(
        ...,
        description="List of course codes to include, e.g. ['CS 250', 'MATH 245']",
        min_length=1,
    )
    instruction_mode: Literal["in-person", "online", "any"] = "any"
    exclude_days: list[Literal["MON", "TUE", "WED", "THU", "FRI"]] = Field(
        default_factory=list,
        description="Days the student cannot attend",
    )


class ConflictDetail(BaseModel):
    section_a: Section
    section_b: Section
    reason: str


class ScheduleResponse(BaseModel):
    sections: list[Section]
    conflicts: list[ConflictDetail] = Field(default_factory=list)
    total_units: int
