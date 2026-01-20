from django.test import TestCase
from apps.courses.models import Course
from apps.students.models import Student
from apps.students.service import StudentService
from apps.courses.service import CourseService

class StudentServiceTest(TestCase):
    def setUp(self):
        self.student_service = StudentService()
        self.course_service = CourseService()
        self.course = Course.objects.create(name="Course 1")
        self.course2 = Course.objects.create(name="Course 2")
        self.student = Student.objects.create(name="Student 1")

    def test_get_student_courses(self):
        self.course_service.join_course(self.student.id, self.course.id)
        self.course_service.set_student_grade(self.student.id, self.course.id, 100)

        self.assertEqual(self.student_service.get_courses(self.student.id).count(), 1)

    def test_get_student_courses_numeric_grades(self):
        self.course_service.join_course(self.student.id, self.course.id)
        self.course_service.set_student_grade(self.student.id, self.course.id, 80)

        numeric_grades = self.student_service.get_course_numeric_grades(self.student.id, self.course.id)

        self.assertEqual(len(numeric_grades), 1)

        self.assertEqual(numeric_grades[0], 80)

    def test_get_student_courses_letter_grades(self):
        self.course_service.join_course(self.student.id, self.course.id)
        self.course_service.set_student_grade(self.student.id, self.course.id, 80)

        letter_grades = self.student_service.get_course_letter_grades(self.student.id, self.course.id)

        self.assertEqual(len(letter_grades), 1)

        self.assertEqual(letter_grades[0], 'B-')

    def test_get_student_courses_average_grade(self):
        self.course_service.join_course(self.student.id, self.course.id)
        self.course_service.set_student_grade(self.student.id, self.course.id, 80)
        self.course_service.set_student_grade(self.student.id, self.course.id, 90)
        self.course_service.set_student_grade(self.student.id, self.course.id, 60)
        self.course_service.set_student_grade(self.student.id, self.course.id, 'B-')

        average_grade = self.student_service.get_numerical_average_grade(self.student.id, self.course.id)

        self.assertEqual(average_grade, 78)

        average_grade_letter = self.student_service.get_letter_average_grade(self.student.id, self.course.id)

        self.assertEqual(average_grade_letter, 'C+')

    def test_consolidated_grade_report(self):
        self.course_service.join_course(self.student.id, self.course.id)
        self.course_service.join_course(self.student.id, self.course2.id)

        self.course_service.set_student_grade(self.student.id, self.course.id, 80)
        self.course_service.set_student_grade(self.student.id, self.course.id, 90)
        self.course_service.set_student_grade(self.student.id, self.course.id, 60)
        self.course_service.set_student_grade(self.student.id, self.course.id, 'B-')

        self.course_service.set_student_grade(self.student.id, self.course2.id, 50)
        self.course_service.set_student_grade(self.student.id, self.course2.id, 62)
        self.course_service.set_student_grade(self.student.id, self.course2.id, 40)
        self.course_service.set_student_grade(self.student.id, self.course2.id, 'F')

        report = self.student_service.consolidated_grade_report(self.student.id)

        self.assertEqual(len(report), 2)

        self.assertEqual(report[0]['course'], 'Course 1')
        self.assertEqual(report[0]['recorded_grades'], [80, 90, 60, 82])
        self.assertEqual(report[0]['average'], 78)
        self.assertEqual(report[0]['letter_grade'], 'C+')

        self.assertEqual(report[1]['course'], 'Course 2')
        self.assertEqual(report[1]['recorded_grades'], [50, 62, 40, 59])
        self.assertEqual(report[1]['average'], 53)
        self.assertEqual(report[1]['letter_grade'], 'F')