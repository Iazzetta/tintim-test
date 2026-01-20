from apps.courses.models import Course
from apps.students.models import Student

class CoreService:
    def __init__(self):
        pass

    def get_course(self, course_id: int):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise Course.DoesNotExist("Course does not exist")
        return course

    def get_student(self, student_id: int):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise Student.DoesNotExist("Student does not exist")
        return student