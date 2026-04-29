from pydantic import BaseModel, Field
from typing import Optional


class ScheduleBuildRequest(BaseModel):
    classes: list[str] = Field(..., min_length=1, description="Course IDs, e.g. ['CS250', 'MATH150']")
    earliestStart: Optional[str] = Field(None, description="HH:MM — exclude sections starting before this")
    latestEnd: Optional[str] = Field(None, description="HH:MM — exclude sections ending after this")


class SectionOut(BaseModel):
    course: str        # courseId format, e.g. "CS250"
    section: str       # section ID string, e.g. "01"
    days: list[str]    # e.g. ["M", "W", "F"]
    startTime: str     # "HH:MM"
    endTime: str       # "HH:MM"


class ScheduleOut(BaseModel):
    scheduleId: int
    sections: list[SectionOut]
