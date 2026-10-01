"""Output helpers for courses and GPA results."""

from .domains import sort_students_by_gpa


def show_students(students):
    if not students:
        print("No student records found.")
        return
    print("\nStudent list sorted by GPA:")
    for student in sort_students_by_gpa(students):
        print(student)
        for mark in student.marks:
            print(f"  - {mark.subject}: {mark.mark} (credit {mark.credit})")


def show_student_gpa(students):
    student_id = input("Enter student ID: ")
    student = next((item for item in students if item.student_id == student_id), None)
    if student is None:
        print("Student ID not found.")
    else:
        print(f"{student.name}'s GPA is: {student.gpa():.2f}")
