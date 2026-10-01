"""Application coordinator for practical work 4."""

from . import input as input_module
from . import output


def run():
    students = input_module.demo_students()
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
            input_module.add_student(students)
            print("Student added successfully!")
        elif choice == "2":
            input_module.add_mark(students)
        elif choice == "3":
            output.show_students(students)
        elif choice == "4":
            output.show_student_gpa(students)
        elif choice == "5":
            students = input_module.demo_students()
            print("Demo data loaded.")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    run()
