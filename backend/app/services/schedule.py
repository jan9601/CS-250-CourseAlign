from dataclasses import dataclass, field
from app.adapters.load_sections import Section

MAX_UNITS = 21


def conflicts(a: Section, b: Section) -> bool:
    if a.start_time == "00:00" or a.end_time == "00:00":
        return False
    if b.start_time == "00:00" or b.end_time == "00:00":
        return False
    if not a.days & b.days:
        return False
    return a.start_time < b.end_time and b.start_time < a.end_time


@dataclass
class Schedule:
    _sections: list[Section] = field(default_factory=list)

    def can_add(self, section: Section) -> bool:
        total_units = sum(s.units for s in self._sections)
        if total_units + section.units > MAX_UNITS:
            return False
        for s in self._sections:
            if conflicts(s, section):
                return False
            if s.section_id == section.section_id:
                return False
            if s.course_title == section.course_title and s.component == section.component:
                return False
        return True

    def add(self, section: Section) -> None:
        self._sections.append(section)

    def copy(self) -> "Schedule":
        return Schedule(_sections=list(self._sections))

    @property
    def sections(self) -> list[Section]:
        return list(self._sections)
