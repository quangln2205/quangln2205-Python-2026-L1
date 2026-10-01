import math
from dataclasses import dataclass, field

import numpy as np

try:
    import curses
except ImportError:
    curses = None


def round_down_one_decimal(value):
    """Round a score down to one decimal place using math.floor."""
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
    marks: list = field(default_factory=list)

    def add_mark(self, subject, credit, mark):
        rounded_mark = round_down_one_decimal(mark)
        self.marks.append(CourseMark(subject, credit, rounded_mark))

    def gpa(self):
        if not self.marks:
            return 0.0

        credits = np.array([item.credit for item in self.marks], dtype=float)
        scores = np.array([item.mark for item in self.marks], dtype=float)

        return float(np.dot(credits, scores) / credits.sum())

    def __str__(self):
        return f"{self.student_id} - {self.name} - GPA: {self.gpa():.2f}"


def sort_students_by_gpa(students):
    return sorted(students, key=lambda s: s.gpa(), reverse=True)


def demo_students():
    s1 = Student("S001", "Alice")
    s1.add_mark("Math", 3, 8.78)
    s1.add_mark("Physics", 2, 7.65)
    s1.add_mark("English", 2, 9.42)

    s2 = Student("S002", "Bob")
    s2.add_mark("Math", 3, 6.91)
    s2.add_mark("Physics", 2, 8.40)
    s2.add_mark("English", 2, 7.33)

    s3 = Student("S003", "Charlie")
    s3.add_mark("Math", 3, 9.99)
    s3.add_mark("Physics", 2, 8.52)
    s3.add_mark("English", 2, 8.11)

    return [s1, s2, s3]


def show_students(students):
    if not students:
        print("No student records found.")
        return

    print("\nStudent list sorted by GPA:")
    for student in sort_students_by_gpa(students):
        print(student)
        for item in student.marks:
            print(f"  - {item.subject}: {item.mark} (credit {item.credit})")


def calculate_gpa_for_student(student):
    return student.gpa()


def run_text_menu():
    students = demo_students()

    while True:
        print("\n=== Student GPA Management ===")
        print("1. Add a student")
        print("2. Add marks for a student")
        print("3. Show students sorted by GPA")
        print("4. Show GPA of one student")
        print("5. Load demo data")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            student_id = input("Enter student ID: ")
            name = input("Enter student name: ")
            students.append(Student(student_id, name))
            print("Student added successfully!")

        elif choice == "2":
            if not students:
                print("No student available. Add a student first.")
                continue

            print("Current students:")
            for s in students:
                print(f"- {s.student_id}: {s.name}")

            student_id = input("Enter student ID to add marks: ")
            found = None
            for student in students:
                if student.student_id == student_id:
                    found = student
                    break

            if found is None:
                print("Student ID not found.")
                continue

            subject = input("Enter subject: ")
            credit = float(input("Enter credit: "))
            mark = float(input("Enter mark: "))
            found.add_mark(subject, credit, mark)
            print("Mark added successfully.")

        elif choice == "3":
            show_students(students)

        elif choice == "4":
            if not students:
                print("No student available.")
                continue

            student_id = input("Enter student ID: ")
            for student in students:
                if student.student_id == student_id:
                    print(f"{student.name}'s GPA is: {calculate_gpa_for_student(student):.2f}")
                    break
            else:
                print("Student ID not found.")

        elif choice == "5":
            students = demo_students()
            print("Demo data loaded.")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


def run_curses_menu(stdscr):
    curses.curs_set(0)
    students = demo_students()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 2, "STUDENT GPA MANAGEMENT", curses.A_BOLD)
        stdscr.addstr(2, 2, "1. Add student")
        stdscr.addstr(3, 2, "2. Add marks")
        stdscr.addstr(4, 2, "3. Show GPA ranking")
        stdscr.addstr(5, 2, "4. Show one GPA")
        stdscr.addstr(6, 2, "Q. Quit")
        stdscr.addstr(8, 2, "Press a key...")
        stdscr.refresh()

        key = stdscr.getch()
        if key in (ord('q'), ord('Q')):
            break

        stdscr.addstr(10, 2, "The curses UI is ready for decoration.")
        stdscr.refresh()
        stdscr.getch()


def main():
    print("Practical Work 3: some maths and decorations")
    print("Using math.floor for one-decimal rounding and numpy for GPA calculations.")

    if curses is not None:
        try:
            curses.wrapper(run_curses_menu)
            return
        except Exception:
            pass

    run_text_menu()


if __name__ == "__main__":
    main()