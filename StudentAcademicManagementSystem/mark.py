class Mark:
    def __init__(self, mark_id, student_id, course_id, score, date_recorded=None):
        self.mark_id = mark_id
        self.student_id = student_id
        self.course_id = course_id
        self.score = score
        self.date_recorded = date_recorded

    def __repr__(self):
        return f"Mark({self.mark_id}, {self.student_id}, {self.course_id}, {self.score}, {self.date_recorded})"
