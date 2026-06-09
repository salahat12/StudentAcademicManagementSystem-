from student import Student
from course import Course
from mark import Mark
from database import DatabaseManager

def main():
    db = DatabaseManager()

    while True:
        print("\n--- Student Academic Management System ---")
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student Info")
        print("5. Delete Student")
        print("6. Add New Course")
        print("7. View All Courses")
        print("8. Search Course")
        print("9. Add or Update Mark")
        print("10. View Marks for a Student")
        print("11. View Students in a Course")
        print("12. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter student name: ")
            email = input("Enter student email: ")
            db.add_student(Student(None, name, email))

        elif choice == "2":
            students = db.get_all_students()
            for s in students:
                print(s)

        elif choice == "3":
            keyword = input("Enter student name or ID: ")
            result = db.search_student(keyword)
            for s in result:
                print(s)

        elif choice == "4":
            sid = int(input("Enter student ID to update: "))
            new_name = input("New name (leave blank to skip): ")
            new_email = input("New email (leave blank to skip): ")
            db.update_student(sid, new_name if new_name else None, new_email if new_email else None)

        elif choice == "5":
            sid = int(input("Enter student ID to delete: "))
            db.delete_student(sid)

        elif choice == "6":
            course_name = input("Enter course name: ")
            credits = int(input("Enter number of credits: "))
            db.add_course(Course(None, course_name, credits))

        elif choice == "7":
            courses = db.get_all_courses()
            for c in courses:
                print(c)

        elif choice == "8":
            keyword = input("Enter course name or ID: ")
            result = db.search_course(keyword)
            for c in result:
                print(c)

        elif choice == "9":
            sid = int(input("Enter student ID: "))
            cid = int(input("Enter course ID: "))
            score = int(input("Enter score (0-100): "))
            db.add_or_update_mark(Mark(None, sid, cid, score))

        elif choice == "10":
            sid = int(input("Enter student ID: "))
            marks = db.get_marks_for_student(sid)
            for course_name, credits, score in marks:
                print(f"{course_name} ({credits} credits): {score}")
            avg = db.get_average_for_student(sid)
            w_avg = db.get_weighted_average_for_student(sid)
            if avg is not None:
                print(f"Simple Average: {avg:.2f}")
                print(f"Weighted Average: {w_avg:.2f}")
            else:
                print("No marks found.")

        elif choice == "11":
            cid = int(input("Enter course ID: "))
            students = db.get_students_in_course(cid)
            for name, score in students:
                print(f"{name}: {score}")

        elif choice == "12":
            db.close()
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
