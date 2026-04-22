from collections import defaultdict
from app.adapters.load_sections import Section
from app.services.schedule import Schedule


def _normalize_code(code: str) -> str:
    return code.replace(" ", "")


def get_courses(sections: list[Section], course_codes: list[str]) -> list[Section]:
    codes = {c.upper() for c in course_codes}
    return [s for s in sections if _normalize_code(s.course_code).upper() in codes]


def filter_earliest_start(sections: list[Section], earliest: str) -> tuple[list[Section], list[str]]:
    filtered, excluded_codes = [], set()
    passing_codes = set()
    for s in sections:
        if s.start_time >= earliest:
            filtered.append(s)
            passing_codes.add(_normalize_code(s.course_code))
        else:
            excluded_codes.add(_normalize_code(s.course_code))
    warnings = sorted(excluded_codes - passing_codes)
    return filtered, warnings


def filter_latest_end(sections: list[Section], latest: str) -> tuple[list[Section], list[str]]:
    filtered, excluded_codes = [], set()
    passing_codes = set()
    for s in sections:
        if s.end_time <= latest:
            filtered.append(s)
            passing_codes.add(_normalize_code(s.course_code))
        else:
            excluded_codes.add(_normalize_code(s.course_code))
    warnings = sorted(excluded_codes - passing_codes)
    return filtered, warnings


def split_by_course(sections: list[Section]) -> list[list[Section]]:
    groups: dict[str, list[Section]] = defaultdict(list)
    for s in sections:
        groups[_normalize_code(s.course_code)].append(s)
    return list(groups.values())


def _recurse(
    results: list[Schedule],
    groups: list[list[Section]],
    index: int,
    current: Schedule,
) -> None:
    if index >= len(groups):
        results.append(current)
        return
    for section in groups[index]:
        if current.can_add(section):
            next_schedule = current.copy()
            next_schedule.add(section)
            _recurse(results, groups, index + 1, next_schedule)


def create_schedules(
    sections: list[Section],
    course_codes: list[str],
    earliest_start: str | None = None,
    latest_end: str | None = None,
) -> tuple[list[Schedule], list[str]]:
    active = get_courses(sections, course_codes)
    warnings: list[str] = []

    if earliest_start:
        active, w = filter_earliest_start(active, earliest_start)
        warnings.extend(f"No sections of {c} meet earliest start {earliest_start}" for c in w)

    if latest_end:
        active, w = filter_latest_end(active, latest_end)
        warnings.extend(f"No sections of {c} meet latest end {latest_end}" for c in w)

    groups = split_by_course(active)
    if not groups:
        return [], warnings

    results: list[Schedule] = []
    _recurse(results, groups, 0, Schedule())
    return results, warnings
