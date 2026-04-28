from fastapi import APIRouter, Query
from ..schemas import Section
from ..services.section_service import filter_sections

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/", response_model=list[Section])
def list_sections(
    course_code: str | None = Query(None, description="Filter by course code, e.g. 'CS 250'"),
    instruction_mode: str | None = Query(None, description="'in-person' or 'online'"),
):
    return filter_sections(course_code=course_code, instruction_mode=instruction_mode)
