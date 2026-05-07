from dataclasses import dataclass
from typing import Optional

# This is the blueprint for one course section.
# Every row in the CSV becomes one Section object.

@dataclass
class Section:
    semester: str           # e.g. "Spring 2026"
    course_code: str        # e.g. "CS 210"
    course_title: str       # e.g. "Data Structures"
    section_id: str         # e.g. "6520"
    component: str          # e.g. "Lecture", "Lab", "Discussion"
    instructor: str         # e.g. "Patricia Kraft"
    days: list[str]         # e.g. ["MON", "WED"] — converted from "c-c--"
    start_time: Optional[str]  # e.g. "08:00" or None if TBD
    end_time: Optional[str]    # e.g. "09:15" or None if TBD
    units: int              # e.g. 3
    instruction_mode: str   # e.g. "in-person" or "online"

    def to_dict(self):
        """Convert to a plain dictionary — used when sending JSON to the API."""
        return {
            "semester": self.semester,
            "course_code": self.course_code,
            "course_title": self.course_title,
            "section_id": self.section_id,
            "component": self.component,
            "instructor": self.instructor,
            "days": self.days,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "units": self.units,
            "instruction_mode": self.instruction_mode,
        }
