import sqlite3
from student import Student
from course import Course
from mark import Mark

class DatabaseManager:
    def __init__(self, db_name="academic_system.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT UNIQUE NOT NULL,
                credits INTEGER NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS marks (
                mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                score INTEGER NOT NULL CHECK(score >= 0 AND score <= 100),
                date_recorded TEXT DEFAULT CURRENT_DATE,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    def add_student(self, student: Student):
        try:
            self.cursor.execute("INSERT INTO students (name, email) VALUES (?, ?)", (student.name, student.email))
            self.conn.commit()
            print("Student added successfully.")
        except sqlite3.IntegrityError:
            print("Error: Email must be unique.")

    def get_all_students(self):
        self.cursor.execute("SELECT * FROM students")
        return [Student(*row) for row in self.cursor.fetchall()]

    def search_student(self, keyword):
        self.cursor.execute("SELECT * FROM students WHERE name LIKE ? OR student_id = ?", (f"%{keyword}%", keyword if keyword.isdigit() else -1))
        return [Student(*row) for row in self.cursor.fetchall()]

    def update_student(self, student_id, new_name=None, new_email=None):
        if new_name:
            self.cursor.execute("UPDATE students SET name = ? WHERE student_id = ?", (new_name, student_id))
        if new_email:
            try:
                self.cursor.execute("UPDATE students SET email = ? WHERE student_id = ?", (new_email, student_id))
            except sqlite3.IntegrityError:
                print("Error: Email must be unique.")
                return
        self.conn.commit()
        print("Student updated.")

    def delete_student(self, student_id):
        self.cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        self.conn.commit()
        print("Student deleted.")

    def add_course(self, course: Course):
        try:
            self.cursor.execute("INSERT INTO courses (course_name, credits) VALUES (?, ?)", (course.course_name, course.credits))
            self.conn.commit()
            print("Course added.")
        except sqlite3.IntegrityError:
            print("Error: Course name must be unique.")

    def get_all_courses(self):
        self.cursor.execute("SELECT * FROM courses")
        return [Course(*row) for row in self.cursor.fetchall()]

    def search_course(self, keyword):
        self.cursor.execute("SELECT * FROM courses WHERE course_name LIKE ? OR course_id = ?", (f"%{keyword}%", keyword if keyword.isdigit() else -1))
        return [Course(*row) for row in self.cursor.fetchall()]

    def add_or_update_mark(self, mark: Mark):
        self.cursor.execute("SELECT mark_id FROM marks WHERE student_id = ? AND course_id = ?", (mark.student_id, mark.course_id))
        result = self.cursor.fetchone()
        if result:
            self.cursor.execute("UPDATE marks SET score = ?, date_recorded = CURRENT_DATE WHERE mark_id = ?", (mark.score, result[0]))
            print("Mark updated.")
        else:
            self.cursor.execute("INSERT INTO marks (student_id, course_id, score) VALUES (?, ?, ?)", (mark.student_id, mark.course_id, mark.score))
            print("Mark added.")
        self.conn.commit()

    def get_marks_for_student(self, student_id):
        self.cursor.execute("""
            SELECT c.course_name, c.credits, m.score
            FROM marks m
            JOIN courses c ON m.course_id = c.course_id
            WHERE m.student_id = ?
        """, (student_id,))
        return self.cursor.fetchall()

    def get_average_for_student(self, student_id):
        self.cursor.execute("SELECT AVG(score) FROM marks WHERE student_id = ?", (student_id,))
        return self.cursor.fetchone()[0]

    def get_weighted_average_for_student(self, student_id):
        self.cursor.execute("""
            SELECT m.score, c.credits
            FROM marks m
            JOIN courses c ON m.course_id = c.course_id
            WHERE m.student_id = ?
        """, (student_id,))
        data = self.cursor.fetchall()
        if not data:
            return None
        total_weighted_score = sum(score * credits for score, credits in data)
        total_credits = sum(credits for _, credits in data)
        return total_weighted_score / total_credits if total_credits > 0 else None

    def get_students_in_course(self, course_id):
        self.cursor.execute("""
            SELECT s.name, m.score
            FROM marks m
            JOIN students s ON m.student_id = s.student_id
            WHERE m.course_id = ?
        """, (course_id,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
