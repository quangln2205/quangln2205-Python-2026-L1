"""Domain objects and GPA calculations."""

import math
from dataclasses import dataclass, field

import numpy as np


def round_down_one_decimal(value):
    """Round a score down to one decimal place."""
    return math.floor(value * 10) / 10


@dataclass
class CourseMark:
    subject: str
    credit: float
    mark: float


@dataclass
class Student:
    student_id: str
    name: str
    marks: list[CourseMark] = field(default_factory=list)

    def add_mark(self, subject, credit, mark):
        self.marks.append(
            CourseMark(subject, float(credit), round_down_one_decimal(float(mark)))
        )

    def gpa(self):
        if not self.marks:
            return 0.0

        credits = np.array([item.credit for item in self.marks], dtype=float)
        scores = np.array([item.mark for item in self.marks], dtype=float)
        return float(np.dot(credits, scores) / credits.sum())

    def __str__(self):
        return f"{self.student_id} - {self.name} - GPA: {self.gpa():.2f}"


def sort_students_by_gpa(students):
    """Return students ordered by GPA from highest to lowest."""
    return sorted(students, key=lambda student: student.gpa(), reverse=True)
