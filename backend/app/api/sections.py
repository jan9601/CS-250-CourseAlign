from fastapi import APIRouter
from ..schemas import CourseResponse
from ..services.section_service import load_sections

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/", response_model=list[CourseResponse])
def list_courses():
    seen: dict[str, CourseResponse] = {}
    for s in load_sections():
        course_id = s.course_code.replace(" ", "")
        if course_id not in seen:
            seen[course_id] = CourseResponse(courseId=course_id, name=s.course_title)
    return list(seen.values())