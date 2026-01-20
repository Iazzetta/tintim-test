from django.db import models
from academy.utils import get_grade_letter

class Course(models.Model):
    name = models.CharField(max_length=200)
    students = models.ManyToManyField('students.Student')

    def __str__(self):
        return self.name


class Grade(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    grade_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.name} - {self.course.name} - {self.grade_number}'

    def get_grade_letter(self):
        return get_grade_letter(self.grade_number)