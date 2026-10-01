"""Practical work 5: persist student data in a compressed file."""

import gzip
import pickle
import importlib
import importlib.util
import sys
from pathlib import Path


MODULE_DIR = Path(__file__).with_name("labwork3-ex4.py")
MODULE_PACKAGE = "student_modules"
if MODULE_PACKAGE not in sys.modules:
    spec = importlib.util.spec_from_file_location(
        MODULE_PACKAGE,
        MODULE_DIR / "__init__.py",
        submodule_search_locations=[str(MODULE_DIR)],
    )
    package = importlib.util.module_from_spec(spec)
    sys.modules[MODULE_PACKAGE] = package
    spec.loader.exec_module(package)

Student = importlib.import_module(f"{MODULE_PACKAGE}.domains").Student
input_module = importlib.import_module(f"{MODULE_PACKAGE}.input")
output = importlib.import_module(f"{MODULE_PACKAGE}.output")


DATA_FILE = Path(__file__).with_name("students.dat")


def save_students(students, filename=DATA_FILE):
    """Compress and save all student data to ``students.dat``."""
    with gzip.open(filename, "wb") as file:
        pickle.dump(students, file)


def load_students(filename=DATA_FILE):
    """Load student data if the compressed data file exists."""
    if not Path(filename).exists():
        return input_module.demo_students()

    try:
        with gzip.open(filename, "rb") as file:
            students = pickle.load(file)
        print(f"Loaded {len(students)} student(s) from {Path(filename).name}.")
        return students
    except (OSError, pickle.PickleError, EOFError, ValueError) as error:
        print(f"Could not load {filename.name}: {error}")
        print("Starting with demo data.")
        return input_module.demo_students()


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
                save_students(students)
                print(f"Saved {len(students)} student(s) to {DATA_FILE.name}.")
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid number. Please try again.")


if __name__ == "__main__":
    run()
