from ninja import Router, Schema
from django.shortcuts import get_object_or_404
from .models import Course, Enrollment
from users.auth import AuthBearer
from users.permissions import is_admin, is_instructor

router = Router(tags=["courses"])

# =====================
# SCHEMA
# =====================
class CourseSchema(Schema):
    title: str
    description: str


# =====================
# PUBLIC
# =====================
@router.get("/")
def list_courses(request, search: str = None):
    courses = Course.objects.all()

    if search:
        courses = courses.filter(title__icontains=search)

    return [
        {
            "id": c.id,
            "title": c.title
        }
        for c in courses
    ]


@router.get("/{course_id}")
def course_detail(request, course_id: int):
    c = get_object_or_404(Course, id=course_id)

    return {
        "id": c.id,
        "title": c.title,
        "description": c.description,
        "instructor": c.instructor.username
    }


# =====================
# PROTECTED (RBAC)
# =====================
@router.post("/", auth=AuthBearer())
def create_course(request, payload: CourseSchema):
    user = request.auth

    if not is_instructor(user):
        return {"error": "Only instructor can create course"}

    course = Course.objects.create(
        title=payload.title,
        description=payload.description,
        instructor=user
    )

    return {"id": course.id}


@router.patch("/{course_id}", auth=AuthBearer())
def update_course(request, course_id: int, payload: CourseSchema):
    user = request.auth
    course = get_object_or_404(Course, id=course_id)

    if course.instructor != user:
        return {"error": "Only owner can update"}

    course.title = payload.title
    course.description = payload.description
    course.save()

    return {"message": "updated"}


@router.delete("/{course_id}", auth=AuthBearer())
def delete_course(request, course_id: int):
    user = request.auth

    if not is_admin(user):
        return {"error": "Only admin can delete"}

    course = get_object_or_404(Course, id=course_id)
    course.delete()

    return {"message": "deleted"}


# =====================
# ENROLLMENTS
# =====================
@router.post("/enroll", auth=AuthBearer())
def enroll_course(request, course_id: int):
    user = request.auth

    if Enrollment.objects.filter(user=user, course_id=course_id).exists():
        return {"message": "Already enrolled"}

    Enrollment.objects.create(user=user, course_id=course_id)

    return {"message": "Enrolled"}


@router.get("/my-courses", auth=AuthBearer())
def my_courses(request):
    user = request.auth

    enrollments = Enrollment.objects.select_related("course").filter(user=user)

    return [
        {
            "enrollment_id": e.id,
            "course_id": e.course.id,
            "course": e.course.title,
            "completed": e.completed
        }
        for e in enrollments
    ]


@router.post("/progress/{enroll_id}", auth=AuthBearer())
def mark_complete(request, enroll_id: int):
    user = request.auth

    enrollment = get_object_or_404(Enrollment, id=enroll_id, user=user)

    enrollment.completed = True
    enrollment.save()

    return {"message": "Completed"}