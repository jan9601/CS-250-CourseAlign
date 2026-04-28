from fastapi import APIRouter, HTTPException
import re

from ..schemas import (
    GenerateScheduleRequest,
    ScheduleOptionResponse,
    ScheduleSectionResponse,
)
from ..services.section_service import filter_sections, sections_conflict

router = APIRouter(prefix="/generate-schedule", tags=["schedule"])


def compact_to_spaced(code: str) -> str:
    """
    Convert API course code format like 'CS100' to dataset format like 'CS 100'.
    """
    return re.sub(r"([A-Z]+)(\d+)", r"\1 \2", code)


def spaced_to_compact(code: str) -> str:
    """
    Convert dataset format like 'CS 100' back to API format like 'CS100'.
    """
    return code.replace(" ", "")


def days_to_array(days: str) -> list[str]:
    """
    Convert internal day string like '-c-c-' into API format like ['T', 'Th'].
    Assumes 5 positions in order: M, T, W, Th, F.
    """
    labels = ["M", "T", "W", "Th", "F"]
    result = []

    for i, ch in enumerate(days):
        if i < len(labels) and ch != "-":
            result.append(labels[i])

    return result


@router.post("/", response_model=list[ScheduleOptionResponse])
def build_schedule(req: GenerateScheduleRequest):
    candidates = []

    for code in req.classes:
        spaced_code = compact_to_spaced(code)

        matches = filter_sections(
            course_code=spaced_code,
            instruction_mode="any",
            exclude_days=[],
        )

        if not matches:
            raise HTTPException(status_code=404, detail=f"No sections found for {code}")

        candidates.append(matches)

    # pick first available section per course for now
    selected = [group[0] for group in candidates]

    for i in range(len(selected)):
        for j in range(i + 1, len(selected)):
            if sections_conflict(selected[i], selected[j]):
                raise HTTPException(
                    status_code=400,
                    detail="Selected sections conflict with each other",
                )

    response_sections = [
        ScheduleSectionResponse(
            course=spaced_to_compact(section.course_code),
            section=section.section_id,
            days=days_to_array(section.days),
            startTime=section.start_time,
            endTime=section.end_time,
        )
        for section in selected
    ]

    return [
        ScheduleOptionResponse(
            scheduleId=1,
            sections=response_sections,
        )
    ]
