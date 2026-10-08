"""Extra exercises: text files, compression, pickle, CSV and pandas queries.

This file reuses the ``Student`` and ``CourseMark`` classes from ``labwork3``.
Run it directly with ``python extra_example.py``.
"""

from __future__ import annotations

import csv
import gzip
import json
import pickle
import re
from pathlib import Path
from typing import Any

import pandas as pd

from labwork3 import Student, demo_students, show_students


BASE_DIR = Path(__file__).resolve().parent
TEXT_FILE = BASE_DIR / "students.txt"
DATA_FILE = BASE_DIR / "students.dat"


# Normal file: students.txt

def student_to_dict(student: Student) -> dict[str, Any]:
    """Convert a Student object into data that JSON can store."""
    return {
        "student_id": student.student_id,
        "name": student.name,
        "marks": [
            {"subject": item.subject, "credit": item.credit, "mark": item.mark}
            for item in student.marks
        ],
    }


def student_from_dict(data: dict[str, Any]) -> Student:
    """Create a Student object from data read from JSON."""
    student = Student(str(data["student_id"]), str(data["name"]))
    for item in data.get("marks", []):
        student.add_mark(item["subject"], item["credit"], item["mark"])
    return student


def save_students_text(students: list[Student], filename: Path = TEXT_FILE) -> None:
    """Save students in a readable UTF-8 JSON text file."""
    records = [student_to_dict(student) for student in students]
    Path(filename).write_text(
        json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def load_students_text(filename: Path = TEXT_FILE) -> list[Student]:
    """Load students from ``students.txt``."""
    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(f"Cannot find {path.name}.")
    records = json.loads(path.read_text(encoding="utf-8"))
    return [student_from_dict(record) for record in records]


# Compressed binary file: students.dat (gzip + pickle)

def save_students_dat(students: list[Student], filename: Path = DATA_FILE) -> None:
    """Pickle and gzip-compress all student objects."""
    with gzip.open(filename, "wb") as file:
        pickle.dump(students, file, protocol=pickle.HIGHEST_PROTOCOL)


def load_students_dat(filename: Path = DATA_FILE) -> list[Student]:
    """Load trusted objects from the compressed pickle file.

    Pickle can execute code while loading. Only load a file created by this
    program or received from a trusted source.
    """
    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(f"Cannot find {path.name}.")
    with gzip.open(path, "rb") as file:
        students = pickle.load(file)
    if not isinstance(students, list) or not all(
        isinstance(student, Student) for student in students
    ):
        raise ValueError("The data file does not contain a list of students.")
    return students


# CSV export

def make_course_id(subject: str) -> str:
    """Create a stable ID, for example ``Data Science`` -> ``DATA_SCIENCE``."""
    course_id = re.sub(r"[^A-Z0-9]+", "_", subject.upper()).strip("_")
    return course_id or "UNKNOWN_COURSE"


def export_csv_files(
    students: list[Student], directory: Path = BASE_DIR
) -> tuple[Path, Path, Path]:
    """Export student, course and mark information to three CSV files."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    students_file = directory / "students.csv"
    courses_file = directory / "courses.csv"
    marks_file = directory / "marks.csv"

    with students_file.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["student_id", "name"])
        writer.writeheader()
        writer.writerows(
            {"student_id": student.student_id, "name": student.name}
            for student in students
        )

    courses: dict[str, dict[str, Any]] = {}
    mark_rows: list[dict[str, Any]] = []
    for student in students:
        for item in student.marks:
            course_id = make_course_id(item.subject)
            course = {
                "course_id": course_id,
                "course_name": item.subject,
                "credit": item.credit,
            }
            if course_id in courses and courses[course_id]["credit"] != item.credit:
                raise ValueError(
                    f"Course {item.subject!r} has more than one credit value."
                )
            courses[course_id] = course
            mark_rows.append(
                {
                    "student_id": student.student_id,
                    "course_id": course_id,
                    "mark": item.mark,
                }
            )

    with courses_file.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file, fieldnames=["course_id", "course_name", "credit"]
        )
        writer.writeheader()
        writer.writerows(sorted(courses.values(), key=lambda row: row["course_id"]))

    with marks_file.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file, fieldnames=["student_id", "course_id", "mark"]
        )
        writer.writeheader()
        writer.writerows(mark_rows)

    return students_file, courses_file, marks_file


# pandas DataFrames and safe query

def load_csv_dataframes(directory: Path = BASE_DIR) -> dict[str, pd.DataFrame]:
    """Use pandas to load the three CSV files into DataFrames."""
    directory = Path(directory)
    filenames = {
        "students": directory / "students.csv",
        "courses": directory / "courses.csv",
        "marks": directory / "marks.csv",
    }
    missing = [path.name for path in filenames.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing CSV file(s): " + ", ".join(missing))
    return {
        table_name: pd.read_csv(path)
        for table_name, path in filenames.items()
    }


CONDITION_PATTERN = re.compile(
    r'^\s*([A-Za-z_]\w*)\s*(==|=|!=|>=|<=|>|<)\s*(.*?)\s*$'
)


def parse_value(raw_value: str, series: pd.Series) -> Any:
    """Convert an entered value to a type suitable for a DataFrame column."""
    value = raw_value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]

    if pd.api.types.is_numeric_dtype(series):
        try:
            return float(value)
        except ValueError as error:
            raise ValueError(f"{value!r} is not a number.") from error
    if pd.api.types.is_bool_dtype(series):
        choices = {"true": True, "false": False}
        if value.lower() not in choices:
            raise ValueError("A Boolean value must be true or false.")
        return choices[value.lower()]
    return value


def query_dataframe(dataframe: pd.DataFrame, condition: str) -> pd.DataFrame:
    """Run one safe condition such as ``name = "Mr. Volunteer"``.

    Supported operators are =, ==, !=, >, >=, < and <=. The function avoids
    Python ``eval``, so user input cannot execute arbitrary Python code.
    """
    match = CONDITION_PATTERN.fullmatch(condition)
    if match is None:
        raise ValueError('Use a condition such as: name = "Mr. Volunteer"')

    column, operator, raw_value = match.groups()
    if column not in dataframe.columns:
        raise ValueError(
            f"Unknown column {column!r}. Available columns: "
            + ", ".join(dataframe.columns)
        )
    if not raw_value:
        raise ValueError("The condition needs a value.")

    series = dataframe[column]
    value = parse_value(raw_value, series)
    operations = {
        "=": lambda: series == value,
        "==": lambda: series == value,
        "!=": lambda: series != value,
        ">": lambda: series > value,
        ">=": lambda: series >= value,
        "<": lambda: series < value,
        "<=": lambda: series <= value,
    }
    try:
        mask = operations[operator]()
    except TypeError as error:
        raise ValueError(
            f"Operator {operator!r} cannot be used with column {column!r}."
        ) from error
    return dataframe.loc[mask].copy()


def query_csv_interactively(directory: Path = BASE_DIR) -> pd.DataFrame:
    """Ask for a table and condition, then display the query result."""
    frames = load_csv_dataframes(directory)
    print("Tables: students, courses, marks")
    table_name = input("Enter table name: ").strip().lower()
    if table_name not in frames:
        raise ValueError("Table must be students, courses or marks.")

    print("Columns:", ", ".join(frames[table_name].columns))
    condition = input('Enter condition (example: name = "Mr. Volunteer"): ')
    result = query_dataframe(frames[table_name], condition)
    if result.empty:
        print("No matching rows.")
    else:
        print(result.to_string(index=False))
    return result


# Main menu

def run() -> None:
    """Run all file and DataFrame exercises from one menu."""
    students = demo_students()

    while True:
        print("\n=== EXTRA FILE AND DATAFRAME EXERCISES ===")
        print("1. Show students")
        print("2. Save students.txt")
        print("3. Load students.txt")
        print("4. Save compressed pickle students.dat")
        print("5. Load compressed pickle students.dat")
        print("6. Export students.csv, courses.csv and marks.csv")
        print("7. Load CSV files and run a pandas query")
        print("8. Reset to demo data")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                show_students(students)
            elif choice == "2":
                save_students_text(students)
                print(f"Saved {len(students)} student(s) to {TEXT_FILE.name}.")
            elif choice == "3":
                students = load_students_text()
                print(f"Loaded {len(students)} student(s) from {TEXT_FILE.name}.")
            elif choice == "4":
                save_students_dat(students)
                print(f"Saved {len(students)} student(s) to {DATA_FILE.name}.")
            elif choice == "5":
                students = load_students_dat()
                print(f"Loaded {len(students)} student(s) from {DATA_FILE.name}.")
            elif choice == "6":
                files = export_csv_files(students)
                print("Exported:", ", ".join(path.name for path in files))
            elif choice == "7":
                query_csv_interactively()
            elif choice == "8":
                students = demo_students()
                print("Demo data loaded.")
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
        except (FileNotFoundError, ValueError, OSError, json.JSONDecodeError) as error:
            print(f"Error: {error}")
        except (pickle.PickleError, EOFError) as error:
            print(f"Could not read the pickle file: {error}")


if __name__ == "__main__":
    run()

