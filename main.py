from models import Teacher, Group, Subject, Room, Timeslot, Lesson
from constraints import ConstraintEvaluator
from generator import ScheduleGenerator


def create_sample_data():
    teachers = [
        Teacher(1, "Dr. Smith"),
        Teacher(2, "Prof. Johnson"),
        Teacher(3, "Dr. Williams"),
        Teacher(4, "Prof. Brown")
    ]

    groups = [
        Group(1, "CS-101", 30),
        Group(2, "CS-102", 25),
        Group(3, "SE-201", 35)
    ]

    subjects = [
        Subject(1, "Mathematics"),
        Subject(2, "Programming"),
        Subject(3, "Physics"),
        Subject(4, "Database Systems"),
        Subject(5, "Web Development")
    ]

    rooms = [
        Room(1, "101", 40, is_lab=False),
        Room(2, "102-Lab", 30, is_lab=True),
        Room(3, "103-Lab", 35, is_lab=True),
        Room(4, "201", 50, is_lab=False)
    ]

    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    timeslots = [Timeslot(day, pair) for day in days for pair in range(1, 5)]

    lessons = [
        Lesson(1, subjects[0], teachers[0], groups[0], is_lab_required=False),
        Lesson(2, subjects[1], teachers[1], groups[0], is_lab_required=True),
        Lesson(3, subjects[2], teachers[2], groups[0], is_lab_required=False),
        Lesson(4, subjects[3], teachers[3], groups[0], is_lab_required=True),
        
        Lesson(5, subjects[0], teachers[0], groups[1], is_lab_required=False),
        Lesson(6, subjects[1], teachers[1], groups[1], is_lab_required=True),
        Lesson(7, subjects[4], teachers[3], groups[1], is_lab_required=False),
        
        Lesson(8, subjects[2], teachers[2], groups[2], is_lab_required=False),
        Lesson(9, subjects[3], teachers[3], groups[2], is_lab_required=True),
        Lesson(10, subjects[4], teachers[1], groups[2], is_lab_required=False)
    ]

    return lessons, timeslots, rooms


def print_schedule(schedule, evaluator):
    hard, soft, fitness = evaluator.evaluate(schedule)
    print("\n" + "=" * 60)
    print(f"GENERATED SCHEDULE (Hard Penalties: {hard}, Soft Penalties: {soft}, Fitness: {fitness:.4f})")
    print("=" * 60)

    sorted_schedule = sorted(
        schedule, 
        key=lambda x: (x.timeslot.day, x.timeslot.pair_number, x.lesson.group.name)
    )

    for assignment in sorted_schedule:
        print(f"Day: {assignment.timeslot.day:<3} | "
              f"Pair: {assignment.timeslot.pair_number} | "
              f"Group: {assignment.lesson.group.name:<6} | "
              f"Subject: {assignment.lesson.subject.title:<18} | "
              f"Teacher: {assignment.lesson.teacher.name:<13} | "
              f"Room: {assignment.room.name}")
    print("=" * 60 + "\n")


def main():
    lessons, timeslots, rooms = create_sample_data()
    evaluator = ConstraintEvaluator()
    generator = ScheduleGenerator(lessons, timeslots, rooms, evaluator)

    print("Generating schedule using Genetic Algorithm...")
    best_schedule = generator.solve_genetic(population_size=100, generations=1000, mutation_rate=0.15)

    if best_schedule:
        print_schedule(best_schedule, evaluator)
    else:
        print("Failed to generate schedule.")


if __name__ == "__main__":
    main()