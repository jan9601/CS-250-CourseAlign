from fastapi import APIRouter, HTTPException
from ..schemas import ScheduleBuildRequest, SectionOut, ScheduleOut
from ..services.section_service import filter_sections, load_sections, parse_days, parse_time, sections_conflict

router = APIRouter(prefix="/generate-schedule", tags=["schedule"])


@router.post(
    "/",
    response_model=list[ScheduleOut],
    responses={
        404: {"description": "One or more course IDs not found"},
        400: {"description": "No sections match the given constraints"},
        409: {"description": "Time conflict between selected sections"},
    },
)
def build_schedule(req: ScheduleBuildRequest):
    known_ids = {s.course_code.replace(" ", "").upper() for s in load_sections()}

    unknown = [c for c in req.classes if c.upper() not in known_ids]
    if unknown:
        raise HTTPException(
            status_code=404,
            detail=f"Course(s) not found: {', '.join(unknown)}",
        )

    candidates = []
    no_match = []

    for code in req.classes:
        matches = filter_sections(
            course_id=code,
            instruction_mode=req.instructionMode,
            earliest_start=req.earliestStart,
            latest_end=req.latestEnd,
        )

        if not matches:
            no_match.append(code)
        else:
            candidates.append(matches)

    if no_match:
        raise HTTPException(
            status_code=400,
            detail=f"No sections match the given constraints for: {', '.join(no_match)}",
        )

    selected = [group[0] for group in candidates]

    conflicts = []
    for i in range(len(selected)):
        for j in range(i + 1, len(selected)):
            if sections_conflict(selected[i], selected[j]):
                a_id = selected[i].course_code.replace(" ", "")
                b_id = selected[j].course_code.replace(" ", "")
                conflicts.append(f"{a_id} and {b_id}")

    if conflicts:
        raise HTTPException(
            status_code=409,
            detail=f"Time conflict(s) detected: {'; '.join(conflicts)}",
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

    return [ScheduleOut(scheduleId=1, sections=response_sections)]