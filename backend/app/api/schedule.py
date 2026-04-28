from fastapi import APIRouter, HTTPException
from ..schemas import ScheduleBuildRequest, ScheduleResponse, ConflictDetail
from ..services.section_service import filter_sections, sections_conflict

router = APIRouter(prefix="/generate-schedule", tags=["schedule"])


@router.post("/", response_model=ScheduleResponse)
def build_schedule(req: ScheduleBuildRequest):
    candidates = []
    for code in req.courses:
        matches = filter_sections(
            course_code=code,
            instruction_mode=req.instruction_mode,
            exclude_days=req.exclude_days or [],
        )
        if not matches:
            raise HTTPException(status_code=404, detail=f"No sections found for {code}")
        candidates.append(matches)

    # pick first available section per course, then detect conflicts
    selected = [group[0] for group in candidates]
    conflicts: list[ConflictDetail] = []
    for i in range(len(selected)):
        for j in range(i + 1, len(selected)):
            if sections_conflict(selected[i], selected[j]):
                conflicts.append(ConflictDetail(
                    section_a=selected[i],
                    section_b=selected[j],
                    reason="Time overlap on shared day(s)",
                ))

    return ScheduleResponse(
        sections=selected,
        conflicts=conflicts,
        total_units=sum(s.units for s in selected),
    )
