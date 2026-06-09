import tkinter as tk
from tkinter import messagebox, ttk
from student import Student
from course import Course
from mark import Mark
from database import DatabaseManager

db = DatabaseManager()

class StudentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Academic Management System")

        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()

        self.setup_widgets()

    def setup_widgets(self):
        # Entry form
        tk.Label(self.root, text="Student Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Student Email:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.email_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Add Student", command=self.add_student).grid(row=2, column=0, columnspan=2, pady=10)

        # Treeview to show students
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Email"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.refresh_students()

    def add_student(self):
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        if not name or not email:
            messagebox.showerror("Input Error", "Both name and email are required.")
            return
        db.add_student(Student(None, name, email))
        self.name_var.set("")
        self.email_var.set("")
        self.refresh_students()

    def refresh_students(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for student in db.get_all_students():
            self.tree.insert("", "end", values=(student.student_id, student.name, student.email))

if __name__ == "__main__":
    root = tk.Tk()
    gui = StudentGUI(root)
    root.mainloop()
