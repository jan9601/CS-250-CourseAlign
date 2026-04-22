from pydantic import BaseModel
from typing import Optional


class SectionOut(BaseModel):
    course_code: str
    course_title: str
    section_id: str
    component: str
    instructor: str
    days: list[str]
    start_time: str
    end_time: str
    units: int
    instruction_mode: str


class ScheduleRequest(BaseModel):
    courses: list[str]
    earliest_start: Optional[str] = None  # "HH:MM" or omit
    latest_end: Optional[str] = None      # "HH:MM" or omit


class ScheduleResponse(BaseModel):
    count: int
    schedules: list[list[SectionOut]]
