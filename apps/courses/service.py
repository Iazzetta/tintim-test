from apps.courses.models import Course, Grade
from apps.students.models import Student
from apps.courses.exceptions import (
    StudentAlreadyInCourseException, 
    StudentNotInCourseException, 
    GradeFormatException
)
from academy.utils import get_grade_number

class CourseService:

    def get_student(self, student_id: int):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise Student.DoesNotExist("Student does not exist")
        return student

    def get_course(self, course_id: int):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise Course.DoesNotExist("Course does not exist")
        return course

    def join_course(self, student_id: int, course_id: int):
        student = self.get_student(student_id)
        course = self.get_course(course_id)

        # check if student already in course
        if course.students.filter(id=student.id).exists():
            raise StudentAlreadyInCourseException("Student already in course")

        course.students.add(student)
        return True

    def set_student_grade(self, student_id: int, course_id: int, grade: int|str):
        student = self.get_student(student_id)
        course = self.get_course(course_id)

        # grade can be 1 or 2 letters (A+, A, B-, etc) or a number between 0 and 100
        if not isinstance(grade, int) and not isinstance(grade, str):
            raise GradeFormatException("Grade must be a number or a string.")
        
        if isinstance(grade, int):
            if grade < 0 or grade > 100:
                raise GradeFormatException("Grade must be between 0 and 100.")
        
        if isinstance(grade, str):
            if len(grade) != 2 and len(grade) != 1:
                raise GradeFormatException("Grade must be 1 or 2 letters (A+, B, C-).")

        if isinstance(grade, str):
            if grade not in ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]:
                raise GradeFormatException("Grade must be one of the following options: A+, A, A-, B+, B, B-, C+, C, C-, D and F.")
        
        grade_number = get_grade_number(grade) if isinstance(grade, str) else grade 

        # check if student already in course
        if not course.students.filter(id=student.id).exists():
            raise StudentNotInCourseException("Student not in course")

        grade = Grade.objects.create(student=student, course=course, grade_number=grade_number)
        return grade

    def get_course_students(self, course_id: int):
        course = self.get_course(course_id)
        return course.students.all()