from fastapi import APIRouter, HTTPException
from ..schemas import ScheduleBuildRequest, SectionOut, ScheduleOut
from ..services.section_service import filter_sections, parse_days, parse_time, sections_conflict

router = APIRouter(prefix="/generate-schedule", tags=["schedule"])


@router.post("/", response_model=list[ScheduleOut])
def build_schedule(req: ScheduleBuildRequest):
    candidates = []

    for code in req.classes:
        matches = filter_sections(
            course_id=code,
            earliest_start=req.earliestStart,
            latest_end=req.latestEnd,
        )

        if not matches:
            return []

        candidates.append(matches)

    selected = [group[0] for group in candidates]

    for i in range(len(selected)):
        for j in range(i + 1, len(selected)):
            if sections_conflict(selected[i], selected[j]):
                raise HTTPException(
                    status_code=400,
                    detail="Selected sections conflict with each other",
                )

    response_sections = [
        SectionOut(
            course=section.course_code.replace(" ", ""),
            section=section.section_id,
            days=parse_days(section.days),
            startTime=parse_time(section.start_time),
            endTime=parse_time(section.end_time),
        )
        for section in selected
    ]

    return [
        ScheduleOut(
            scheduleId=1,
            sections=response_sections,
        )
    ]