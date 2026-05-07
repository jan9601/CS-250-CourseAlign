import csv
from models import Section

# The CSV uses a 5-character pattern like "c-c--"
# Each position = Mon, Tue, Wed, Thu, Fri
# 'c' means class meets that day, '-' means it doesn't
DAY_MAP = {
    0: "MON",
    1: "TUE",
    2: "WED",
    3: "THU",
    4: "FRI",
}

def parse_days(day_string: str) -> list[str]:
    """
    Convert day pattern like 'c-c--' into ['MON', 'WED'].
    Returns empty list if pattern is missing or all dashes.
    """
    days = []
    for i, char in enumerate(day_string):
        if char == 'c' and i in DAY_MAP:
            days.append(DAY_MAP[i])
    return days

def parse_time(time_str: str):
    """
    Return the time string if valid, or None if it's TBD or empty.
    """
    if not time_str or time_str.strip().upper() == "TBD":
        return None
    return time_str.strip()

def load_sections(filepath: str) -> list[Section]:
    """
    Load all course sections from a CSV file.
    Returns a list of Section objects.
    Skips rows with missing required fields.
    """
    sections = []

    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row_number, row in enumerate(reader, start=2):  # start=2 because row 1 is header
            try:
                section = Section(
                    semester=row["semester"].strip(),
                    course_code=row["course_code"].strip(),
                    course_title=row["course_title"].strip(),
                    section_id=row["section_id"].strip(),
                    component=row["component"].strip(),
                    instructor=row["instructor"].strip(),
                    days=parse_days(row["days"].strip()),
                    start_time=parse_time(row["start_time"]),
                    end_time=parse_time(row["end_time"]),
                    units=int(row["units"].strip()),
                    instruction_mode=row["instruction_mode"].strip(),
                )
                sections.append(section)

            except (KeyError, ValueError) as e:
                # Don't crash — just warn and skip the bad row
                print(f"Warning: Skipping row {row_number} due to error: {e}")
                continue

    return sections


def get_sections_by_course(sections: list[Section], course_code: str) -> list[Section]:
    """
    Filter sections by course code (case-insensitive).
    Example: get_sections_by_course(sections, "CS 210")
    """
    course_code = course_code.strip().upper()
    return [s for s in sections if s.course_code.upper() == course_code]


def get_all_course_codes(sections: list[Section]) -> list[str]:
    """
    Return a sorted list of unique course codes.
    Useful for the /courses endpoint.
    """
    codes = sorted(set(s.course_code for s in sections))
    return codes
