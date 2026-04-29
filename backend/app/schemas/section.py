from pydantic import BaseModel
from typing import Literal


class Section(BaseModel):
    semester: str
    course_code: str
    course_title: str
    section_id: str
    component: Literal["Lecture", "Lab", "Discussion", "Activity", "Tech Acts"] | str
    instructor: str
    days: str                  # e.g. "c-c-c" — 5 chars, Mon–Fri; 'c' = has class
    start_time: str            # "HH:MM" or "TBD"
    end_time: str              # "HH:MM" or "TBD"
    units: int
    instruction_mode: Literal["in-person", "online"] | str


class CourseResponse(BaseModel):
    courseId: str  # course_code with spaces removed, e.g. "CS250"
    name: str
