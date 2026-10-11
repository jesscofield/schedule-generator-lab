class Teacher:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Teacher({self.name})"


class Group:
    def __init__(self, id: int, name: str, student_count: int):
        self.id = id
        self.name = name
        self.student_count = student_count

    def __repr__(self):
        return f"Group({self.name})"


class Subject:
    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title

    def __repr__(self):
        return f"Subject({self.title})"


class Room:
    def __init__(self, id: int, name: str, capacity: int, is_lab: bool = False):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.is_lab = is_lab

    def __repr__(self):
        return f"Room({self.name}, cap={self.capacity})"


class Timeslot:
    def __init__(self, day: str, pair_number: int):
        self.day = day  # Наприклад: "Пн", "Вт"
        self.pair_number = pair_number  # 1, 2, 3, 4, 5

    def __repr__(self):
        return f"Timeslot({self.day}, пара {self.pair_number})"


class Lesson:
    def __init__(self, id: int, subject: Subject, teacher: Teacher, group: Group, is_lab_required: bool = False):
        self.id = id
        self.subject = subject
        self.teacher = teacher
        self.group = group
        self.is_lab_required = is_lab_required

    def __repr__(self):
        return f"Lesson({self.subject.title} - {self.group.name})"

class ScheduleAssignment:
    def __init__(self, lesson, timeslot, room):
        self.lesson = lesson
        self.timeslot = timeslot
        self.room = room