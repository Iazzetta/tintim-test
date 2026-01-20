from dataclasses import dataclass
from typing import List

@dataclass
class StudentGradeReport:
    course_name: str
    recorded_grades: List[int]
    average: int
    letter_grade: str