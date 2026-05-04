import csv
from pathlib import Path
from functools import lru_cache
from ..schemas import Section

_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "raw" / "testData.csv"

# CSV day positions → contract day strings
_DAY_NAMES = ["M", "T", "W", "Th", "F"]


def parse_days(days_str: str) -> list[str]:
    """Convert CSV day string (e.g. 'c-c-c') to contract format (e.g. ['M','W','F'])."""
    return [_DAY_NAMES[i] for i, ch in enumerate(days_str) if ch == "c"]


def parse_time(t: str) -> str:
    """Convert 'TBD' to '00:00'; pass valid HH:MM through unchanged."""
    return "00:00" if t == "TBD" else t


@lru_cache(maxsize=1)
def load_sections() -> list[Section]:
    sections: list[Section] = []
    with open(_DATA_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sections.append(Section(
                semester=row["semester"],
                course_code=row["course_code"],
                course_title=row["course_title"],
                section_id=row["section_id"],
                component=row["component"],
                instructor=row["instructor"],
                days=row["days"],
                start_time=row["start_time"],
                end_time=row["end_time"],
                units=int(row["units"]),
                instruction_mode=row["instruction_mode"],
            ))
    return sections


def filter_sections(
    course_id: str | None = None,        # contract format: "CS250" (no space)
    instruction_mode: str | None = None,
    earliest_start: str | None = None,   # "HH:MM" — exclude sections starting before this
    latest_end: str | None = None,       # "HH:MM" — exclude sections ending after this
) -> list[Section]:
    results = load_sections()
    if course_id:
        results = [s for s in results if s.course_code.replace(" ", "").upper() == course_id.upper()]
    if instruction_mode and instruction_mode != "any":
        results = [s for s in results if s.instruction_mode == instruction_mode]
    if earliest_start:
        results = [s for s in results if s.start_time == "TBD" or s.start_time >= earliest_start]
    if latest_end:
        results = [s for s in results if s.end_time == "TBD" or s.end_time <= latest_end]
    return results


def sections_conflict(a: Section, b: Section) -> bool:
    shared_days = any(
        a.days[i] == "c" and b.days[i] == "c"
        for i in range(min(len(a.days), len(b.days)))
    )
    if not shared_days:
        return False
    if a.start_time == "TBD" or b.start_time == "TBD":
        return False
    return not (a.end_time <= b.start_time or b.end_time <= a.start_time)