from pydantic import BaseModel, Field
from typing import Optional


class GenerateScheduleRequest(BaseModel):
    classes: list[str] = Field(
        ...,
        description="List of course codes in compact API format, e.g. ['CS100', 'MATH150']",
        min_length=1,
    )
    earliestStart: Optional[str] = Field(
        default=None,
        description='Optional earliest allowed start time in HH:MM',
    )
    latestEnd: Optional[str] = Field(
        default=None,
        description='Optional latest allowed end time in HH:MM',
    )


class ScheduleSectionResponse(BaseModel):
    course: str
    section: str
    days: list[str]
    startTime: str
    endTime: str


class ScheduleOptionResponse(BaseModel):
    scheduleId: int
    sections: list[ScheduleSectionResponse]
