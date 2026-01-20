from django.test import TestCase
from apps.courses.service import CourseService
from apps.courses.models import Course, Grade
from apps.students.models import Student
from apps.courses.exceptions import (
    StudentAlreadyInCourseException, 
    StudentNotInCourseException,
    InvalidGradeException
)

class CourseServiceTest(TestCase):
    def setUp(self):
        self.course_service = CourseService()
        self.course = Course.objects.create(name="Course 1")
        self.student = Student.objects.create(name="Student 1")
        self.student2 = Student.objects.create(name="Student 2")
    
    def test_join_course(self):
        self.assertTrue(self.course_service.join_course(self.course.id, self.student.id))
    
    def test_join_course_student_already_in_course(self):
        # join course
        self.course_service.join_course(self.course.id, self.student.id)
        
        # try to join course again
        with self.assertRaises(StudentAlreadyInCourseException):
            self.course_service.join_course(self.course.id, self.student.id)

    def test_set_student_grade_letter(self):
        # join course
        self.course_service.join_course(self.course.id, self.student.id)
        
        # set grade (with letter)
        self.course_service.set_student_grade(self.student.id, self.course.id, 'A-')
        # grade needs to be the high number of the letter grade
        self.assertEqual(Grade.objects.get(student=self.student, course=self.course).grade_number, 92)

    def test_set_student_grade_number(self):
        # join course
        self.course_service.join_course(self.course.id, self.student.id)
        
        # set grade (with number)
        self.course_service.set_student_grade(self.student.id, self.course.id, 87)
        self.assertEqual(Grade.objects.get(student=self.student, course=self.course).grade_number, 87)
    
    def test_set_student_grade_student_not_in_course(self):
        with self.assertRaises(StudentNotInCourseException):
            self.course_service.set_student_grade(self.student2.id, self.course.id, 100)

    def test_set_student_grade_invalid_grade_letter(self):
        with self.assertRaises(InvalidGradeException):
            self.course_service.set_student_grade(self.student.id, self.course.id, 'invalid_grade')

    def test_set_student_grade_invalid_grade_number(self):
        with self.assertRaises(InvalidGradeException):
            self.course_service.set_student_grade(self.student.id, self.course.id, 101)

    def test_get_students_in_course(self):
        self.course_service.join_course(self.course.id, self.student.id)
        students = self.course_service.get_course_students(self.course.id)
        self.assertEqual(students.count(), 1)

        self.assertEqual(students[0].name, self.student.name)