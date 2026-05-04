import re
from datetime import datetime
import subprocess


def run_cpp_scheduler(classes, earliest_start=None, latest_end=None):
    # join classes like: "CS250 MATH150"
    class_input = " ".join(classes)

    # build input step by step
    input_lines = []

    # line 1: classes
    input_lines.append(class_input)

    # earliest start
    if earliest_start:
        input_lines.append("y")
        input_lines.append(earliest_start)
    else:
        input_lines.append("n")

    # latest end
    if latest_end:
        input_lines.append("y")
        input_lines.append(latest_end)
    else:
        input_lines.append("n")

    # final input string
    user_input = "\n".join(input_lines) + "\n"

    result = subprocess.run(
        ["./coursealign"],  # run inside cpp_backend
        input=user_input,
        text=True,
        capture_output=True,
        cwd="../cpp_backend",  # change working directory
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return result.stdout


def to_24_hour(time_text: str) -> str:
    time_text = time_text.strip().lower()
    parsed = datetime.strptime(time_text, "%I:%M%p")
    return parsed.strftime("%H:%M")


def parse_cpp_output(output: str):
    schedules = []

    lines = output.splitlines()

    current_sections = []
    schedule_id = 1
    inside_schedule = False

    for line in lines:

        # Detect start of a new schedule
        if "=== CourseAlign: Your Schedule ===" in line:
            if current_sections:
                schedules.append({
                    "scheduleId": schedule_id,
                    "sections": current_sections
                })
                schedule_id += 1
                current_sections = []

            inside_schedule = True
            continue

        if not inside_schedule:
            continue

        # Detect section rows
        if "|" in line and any(comp in line for comp in ["Lecture", "Lab", "Discussion", "Activity", "Tech Acts"]):

            parts = [p.strip() for p in line.split("|")]

            if len(parts) < 7:
                continue

            course_raw = parts[1]
            section_id_str = parts[3]
            days_raw = parts[5]
            time_raw = parts[6]

            if "-" not in time_raw:
                continue

            start_raw, end_raw = [t.strip() for t in time_raw.split("-", 1)]

            current_sections.append({
                "course": course_raw.replace(" ", ""),
                "section": section_id_str,
                "days": days_raw.split(),
                "startTime": to_24_hour(start_raw),
                "endTime": to_24_hour(end_raw),
            })

    # Add last schedule
    if current_sections:
        schedules.append({
            "scheduleId": schedule_id,
            "sections": current_sections
        })

    return schedules