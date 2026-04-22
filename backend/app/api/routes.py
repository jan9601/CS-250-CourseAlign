import re
from fastapi import APIRouter, HTTPException, Request
from app.schemas.models import ScheduleRequest, ScheduleResponse, SectionOut
from app.services.schedule_build import create_schedules, _normalize_code

router = APIRouter()

TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


def _section_out(s) -> SectionOut:
    return SectionOut(
        course_code=s.course_code,
        course_title=s.course_title,
        section_id=s.section_id,
        component=s.component,
        instructor=s.instructor,
        days=sorted(s.days),
        start_time=s.start_time,
        end_time=s.end_time,
        units=s.units,
        instruction_mode=s.instruction_mode,
    )


@router.get("/courses", summary="List all available course codes")
def list_courses(request: Request) -> list[str]:
    sections = request.app.state.sections
    codes = sorted({_normalize_code(s.course_code) for s in sections})
    return codes


@router.post("/schedules", response_model=ScheduleResponse, summary="Generate valid schedules")
def generate_schedules(body: ScheduleRequest, request: Request) -> ScheduleResponse:
    sections = request.app.state.sections

    if not body.courses:
        raise HTTPException(status_code=422, detail="courses list cannot be empty")

    if body.earliest_start and not TIME_RE.match(body.earliest_start):
        raise HTTPException(status_code=422, detail="earliest_start must be HH:MM")

    if body.latest_end and not TIME_RE.match(body.latest_end):
        raise HTTPException(status_code=422, detail="latest_end must be HH:MM")

    valid_codes = {_normalize_code(s.course_code).upper() for s in sections}
    for code in body.courses:
        if code.upper() not in valid_codes:
            raise HTTPException(status_code=404, detail=f"Course not found: {code}")

    schedules, warnings = create_schedules(
        sections,
        body.courses,
        earliest_start=body.earliest_start,
        latest_end=body.latest_end,
    )

    return ScheduleResponse(
        count=len(schedules),
        schedules=[[_section_out(s) for s in sched.sections] for sched in schedules],
    )
