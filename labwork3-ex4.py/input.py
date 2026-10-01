"""Input helpers for the student mark application."""

from .domains import Student


def demo_students():
    students = [Student("S001", "Alice"), Student("S002", "Bob"), Student("S003", "Charlie")]
    data = [
        [("Math", 3, 8.78), ("Physics", 2, 7.65), ("English", 2, 9.42)],
        [("Math", 3, 6.91), ("Physics", 2, 8.40), ("English", 2, 7.33)],
        [("Math", 3, 9.99), ("Physics", 2, 8.52), ("English", 2, 8.11)],
    ]
    for student, marks in zip(students, data):
        for subject, credit, mark in marks:
            student.add_mark(subject, credit, mark)
    return students


def add_student(students):
    student_id = input("Enter student ID: ")
    name = input("Enter student name: ")
    students.append(Student(student_id, name))


def add_mark(students):
    if not students:
        print("No student available. Add a student first.")
        return

    for student in students:
        print(f"- {student.student_id}: {student.name}")
    student_id = input("Enter student ID to add marks: ")
    student = next((item for item in students if item.student_id == student_id), None)
    if student is None:
        print("Student ID not found.")
        return

    subject = input("Enter subject: ")
    credit = float(input("Enter credit: "))
    mark = float(input("Enter mark: "))
    student.add_mark(subject, credit, mark)
    print("Mark added successfully.")
