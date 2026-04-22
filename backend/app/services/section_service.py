import csv
from pathlib import Path
from functools import lru_cache
from ..schemas import Section

_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "raw" / "testData.csv"

_DAY_INDEX = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4}


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
    course_code: str | None = None,
    instruction_mode: str | None = None,
    exclude_days: list[str] | None = None,
) -> list[Section]:
    results = load_sections()
    if course_code:
        results = [s for s in results if s.course_code.upper() == course_code.upper()]
    if instruction_mode and instruction_mode != "any":
        results = [s for s in results if s.instruction_mode == instruction_mode]
    if exclude_days:
        indices = {_DAY_INDEX[d] for d in exclude_days if d in _DAY_INDEX}
        results = [s for s in results if not any(s.days[i] == "c" for i in indices if i < len(s.days))]
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
    a_start, a_end = a.start_time, a.end_time
    b_start, b_end = b.start_time, b.end_time
    return not (a_end <= b_start or b_end <= a_start)
