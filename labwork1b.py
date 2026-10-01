def input_students():
    """Input student list from keyboard."""
    try:
        count = int(input("Nhap so luong sinh vien: "))
    except ValueError:
        print("So luong sinh vien phai la so nguyen!")
        return []

    students = []
    for i in range(count):
        print(f"\nSinh vien thu {i + 1}:")
        student_id = input("Nhap ma sinh vien: ")
        name = input("Nhap ten sinh vien: ")
        dob = input("Nhap ngay sinh (dd/mm/yyyy): ")
        students.append({
            "id": student_id,
            "name": name,
            "dob": dob
        })
    return students


def input_courses():
    """Input course list from keyboard."""
    try:
        count = int(input("Nhap so luong mon hoc: "))
    except ValueError:
        print("So luong mon hoc phai la so nguyen!")
        return []

    courses = []
    for i in range(count):
        print(f"\nMon hoc thu {i + 1}:")
        course_id = input("Nhap ma mon hoc: ")
        name = input("Nhap ten mon hoc: ")
        courses.append({
            "id": course_id,
            "name": name
        })
    return courses


def input_marks_for_course(students, course_id, marks):
    """Input marks for all students in one selected course."""
    if not students:
        print("Ban chua nhap danh sach sinh vien!")
        return marks

    course_marks = marks.setdefault(course_id, {})
    for student in students:
        student_id = student["id"]
        student_name = student["name"]
        try:
            point = float(input(f"Nhap diem cho sinh vien {student_name} ({student_id}): "))
        except ValueError:
            print("Diem phai la so thuc!")
            point = 0.0
        course_marks[student_id] = point
    return marks


def list_courses(courses):
    """Display all courses."""
    if not courses:
        print("Chua co mon hoc nao.")
        return
    print("\nDanh sach mon hoc:")
    for course in courses:
        print(f"- Ma mon: {course['id']} | Ten mon: {course['name']}")


def list_students(students):
    """Display all students."""
    if not students:
        print("Chua co sinh vien nao.")
        return
    print("\nDanh sach sinh vien:")
    for student in students:
        print(f"- Ma SV: {student['id']} | Ten: {student['name']} | Ngay sinh: {student['dob']}")


def show_marks_for_course(students, courses, marks):
    """Display marks for a selected course."""
    if not courses:
        print("Chua co mon hoc nao.")
        return

    course_id = input("Nhap ma mon hoc can xem diem: ")
    selected_course = None
    for course in courses:
        if course["id"] == course_id:
            selected_course = course
            break

    if selected_course is None:
        print("Ma mon hoc khong ton tai.")
        return

    print(f"\nDiem cua mon {selected_course['name']} ({selected_course['id']}):")
    if course_id not in marks or not marks[course_id]:
        print("Chua co diem nao cho mon nay.")
        return

    for student in students:
        student_id = student["id"]
        if student_id in marks[course_id]:
            print(f"- {student['name']} ({student_id}): {marks[course_id][student_id]}")


def main():
    students = []
    courses = []
    marks = {}

    print("=================================================")
    print("         PRACTICAL WORK 1: STUDENT MARK MANAGEMENT")
    print("=================================================")

    while True:
        print("\n1. Nhap danh sach sinh vien")
        print("2. Nhap danh sach mon hoc")
        print("3. Nhap diem cho mon hoc")
        print("4. Liet ke danh sach mon hoc")
        print("5. Liet ke danh sach sinh vien")
        print("6. Hien thi diem theo mon hoc")
        print("0. Thoat")

        choice = input("Chon chuc nang: ")

        if choice == "1":
            students = input_students()
        elif choice == "2":
            courses = input_courses()
        elif choice == "3":
            if not courses:
                print("Ban chua nhap danh sach mon hoc.")
                continue
            if not students:
                print("Ban chua nhap danh sach sinh vien.")
                continue

            print("\nDanh sach mon hoc hien co:")
            for course in courses:
                print(f"- {course['id']} : {course['name']}")

            course_id = input("Nhap ma mon hoc can nhap diem: ")
            valid = False
            for course in courses:
                if course["id"] == course_id:
                    valid = True
                    break

            if not valid:
                print("Ma mon hoc khong ton tai.")
                continue

            marks = input_marks_for_course(students, course_id, marks)
            print("Da nhap diem thanh cong.")
        elif choice == "4":
            list_courses(courses)
        elif choice == "5":
            list_students(students)
        elif choice == "6":
            show_marks_for_course(students, courses, marks)
        elif choice == "0":
            print("Cam on ban da su dung chuong trinh!")
            break
        else:
            print("Lua chon khong hop le, vui long chon lai!")


if __name__ == "__main__":
    main()
