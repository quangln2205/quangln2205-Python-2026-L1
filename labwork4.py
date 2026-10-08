"""Practical work 5: persist student data in a compressed file."""

import gzip
import pickle
from pathlib import Path

from labwork3 import Student, demo_students, show_students


DATA_FILE = Path(__file__).with_name("students.dat")


def save_students(students, filename=DATA_FILE):
    """Compress and save all student data to ``students.dat``."""
    with gzip.open(filename, "wb") as file:
        pickle.dump(students, file)


def load_students(filename=DATA_FILE):
    """Load student data if the compressed data file exists."""
    if not Path(filename).exists():
        return demo_students()

    try:
        with gzip.open(filename, "rb") as file:
            students = pickle.load(file)
        print(f"Loaded {len(students)} student(s) from {Path(filename).name}.")
        return students
    except (OSError, pickle.PickleError, EOFError, ValueError) as error:
        print(f"Could not load {filename.name}: {error}")
        print("Starting with demo data.")
        return demo_students()


def add_student(students):
    student_id = input("Enter student ID: ")
    name = input("Enter student name: ")
    students.append(Student(student_id, name))


def add_mark(students):
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


def show_student_gpa(students):
    student_id = input("Enter student ID: ")
    student = next((item for item in students if item.student_id == student_id), None)
    if student is None:
        print("Student ID not found.")
    else:
        print(f"{student.name}'s GPA is: {student.gpa():.2f}")


def run():
    students = load_students()

    while True:
        print("\n=== Student GPA Management ===")
        print("1. Add a student")
        print("2. Add marks for a student")
        print("3. Show students sorted by GPA")
        print("4. Show GPA of one student")
        print("5. Load demo data")
        print("0. Exit and save")
        choice = input("Choose an option: ")

        try:
            if choice == "1":
                add_student(students)
                print("Student added successfully!")
            elif choice == "2":
                add_mark(students)
            elif choice == "3":
                show_students(students)
            elif choice == "4":
                show_student_gpa(students)
            elif choice == "5":
                students = demo_students()
                print("Demo data loaded.")
            elif choice == "0":
                save_students(students)
                print(f"Saved {len(students)} student(s) to {DATA_FILE.name}.")
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid number. Please try again.")


if __name__ == "__main__":
    run()
