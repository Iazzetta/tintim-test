from apps.courses.models import Course, Grade
from apps.students.models import Student
from django.db.models import Avg
from django.db.models.functions import Round
from academy.utils import get_grade_letter
from collections import defaultdict

class StudentService:

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

    def get_courses(self, student_id: int):
        student = self.get_student(student_id)
        return Grade.objects.filter(student=student).values_list('course', flat=True)

    def get_course_numeric_grades(self, student_id: int, course_id: int):
        student = self.get_student(student_id)
        course = self.get_course(course_id)
        return Grade.objects.filter(student=student, course=course).values_list('grade_number', flat=True)

    def get_course_letter_grades(self, student_id: int, course_id: int):
        student = self.get_student(student_id)
        course = self.get_course(course_id)
        return [grade.get_grade_letter() for grade in Grade.objects.filter(student=student, course=course)]

    def get_numerical_average_grade(self, student_id: int, course_id: int):
        student = self.get_student(student_id)
        course = self.get_course(course_id)
        result = Grade.objects.filter(student=student, course=course).aggregate(
            average=Round(Avg('grade_number'))
        )
        
        return result['average'] or 0

    def get_letter_average_grade(self, student_id: int, course_id: int):
        result = self.get_numerical_average_grade(student_id, course_id)
        return get_grade_letter(result)

    def consolidated_grade_report(self, student_id: int):
        student = self.get_student(student_id)
        
        grades_queryset = Grade.objects.filter(student=student).select_related('course').order_by('created_at')
        
        if not grades_queryset.exists():
            return []

        course_data = defaultdict(lambda: {"name": "", "grades": []})
        
        for grade in grades_queryset:
            course_id = grade.course.id
            course_data[course_id]["name"] = grade.course.name
            course_data[course_id]["grades"].append(grade.grade_number)
        
        report = []
        for course_id, data in course_data.items():
            all_grades = data["grades"]
            
            avg_numeric = round(sum(all_grades) / len(all_grades)) if all_grades else 0
            
            report.append({
                "course": data["name"],
                "recorded_grades": all_grades,
                "average": avg_numeric,
                "letter_grade": get_grade_letter(avg_numeric)
            })
            
        return report