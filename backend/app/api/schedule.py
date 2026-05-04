
from fastapi import APIRouter, HTTPException

from ..schemas import (
    GenerateScheduleRequest,
    ScheduleOptionResponse,
)

from ..services.cpp_bridge import run_cpp_scheduler, parse_cpp_output

router = APIRouter(prefix="/generate-schedule", tags=["schedule"])


@router.post("/", response_model=list[ScheduleOptionResponse])
def build_schedule(req: GenerateScheduleRequest):
    try:
        output = run_cpp_scheduler(
            classes=req.classes,
            earliest_start=req.earliestStart,
            latest_end=req.latestEnd,
        )

        schedules = parse_cpp_output(output)

        # Contract rule: no schedules → return []
        if not schedules:
            return []

        return schedules

    except Exception as e:
        # Contract rule: invalid input → standard error
        raise HTTPException(status_code=400, detail="Invalid request")