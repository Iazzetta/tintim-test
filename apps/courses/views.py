import json
from django.http import HttpResponse
from .service import CourseService
from academy.utils import get_grade_number, get_grade_letter
from .exceptions import (
    StudentAlreadyInCourseException, 
    StudentNotInCourseException, 
    InvalidGradeException
)

course_service = CourseService()

def join_course(request, course_id: int):
    data = json.loads(request.body.decode("utf-8"))
    student_id = data.get("student_id")
    if not student_id:
        return HttpResponse("Student id is required.", status=400)
    try:
        course_service.join_course(student_id, course_id)
    except StudentAlreadyInCourseException as e:
        return HttpResponse(str(e), status=400)
    return HttpResponse("Student joined course successfully.", status=200)

def set_student_grade(request, course_id):
    data = json.loads(request.body.decode("utf-8"))
    student_id = data.get("student_id")
    grade = data.get("grade")

    if not student_id:
        return HttpResponse("Student id is required.", status=400)
    
    if not grade:
        return HttpResponse("Grade is required.", status=400)
    
    try:
        course_service.set_student_grade(student_id, course_id, grade)
    except StudentNotInCourseException as e:
        return HttpResponse(str(e), status=400)
    except InvalidGradeException as e:
        return HttpResponse(str(e), status=400)

    return HttpResponse("Student grade set successfully.", status=200)