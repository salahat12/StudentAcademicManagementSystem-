class Student:
    def __init__(self, student_id, name, email):
        self.student_id = student_id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"Student({self.student_id}, {self.name}, {self.email})"
