import csv
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Section:
    course_code: str
    course_title: str
    section_id: str
    component: str
    instructor: str
    days: frozenset[str]
    start_time: str
    end_time: str
    units: int
    instruction_mode: str


def _normalize_time(raw: str) -> str:
    raw = raw.strip()
    if not raw or raw.upper() == "TBD":
        return "00:00"
    if len(raw) == 4:  # H:MM → HH:MM
        return "0" + raw
    return raw


def _parse_days(raw: str) -> frozenset[str]:
    mapping = {0: "M", 1: "T", 2: "W", 3: "Th", 4: "F"}
    return frozenset(mapping[i] for i, ch in enumerate(raw[:5]) if ch == "c")


def load_sections(path: Path | str) -> list[Section]:
    sections: list[Section] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for lineno, row in enumerate(reader, start=2):
            if len(row) < 11:
                continue
            days = _parse_days(row[6])
            start = _normalize_time(row[7]) if days else "00:00"
            end = _normalize_time(row[8]) if days else "00:00"
            try:
                units = int(row[9]) if row[9].strip() else 0
            except ValueError:
                units = 0
            sections.append(Section(
                course_code=row[1].strip(),
                course_title=row[2].strip(),
                section_id=row[3].strip(),
                component=row[4].strip(),
                instructor=row[5].strip(),
                days=days,
                start_time=start,
                end_time=end,
                units=units,
                instruction_mode=row[10].strip(),
            ))
    return sections
