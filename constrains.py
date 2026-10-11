class ScheduleAssignment:
    def __init__(self, lesson, timeslot, room):
        self.lesson = lesson
        self.timeslot = timeslot
        self.room = room


class ConstraintEvaluator:
    def __init__(self, hard_penalty_weight: int = 1000, soft_penalty_weight: int = 1):
        self.hard_penalty_weight = hard_penalty_weight
        self.soft_penalty_weight = soft_penalty_weight

    def evaluate(self, assignments: list[ScheduleAssignment]) -> tuple[int, int, float]:
        hard_penalties = 0
        soft_penalties = 0

        for i in range(len(assignments)):
            a1 = assignments[i]

            if a1.lesson.group.student_count > a1.room.capacity:
                hard_penalties += 1

            if a1.lesson.is_lab_required and not a1.room.is_lab:
                hard_penalties += 1

            for j in range(i + 1, len(assignments)):
                a2 = assignments[j]

                if (a1.timeslot.day == a2.timeslot.day and 
                    a1.timeslot.pair_number == a2.timeslot.pair_number):

                    if a1.lesson.teacher.id == a2.lesson.teacher.id:
                        hard_penalties += 1

                    if a1.lesson.group.id == a2.lesson.group.id:
                        hard_penalties += 1

                    if a1.room.id == a2.room.id:
                        hard_penalties += 1

        soft_penalties += self._count_windows_and_overload(assignments)

        total_penalty = (hard_penalties * self.hard_penalty_weight) + (soft_penalties * self.soft_penalty_weight)
        fitness_score = 1.0 / (1.0 + total_penalty)

        return hard_penalties, soft_penalties, fitness_score

    def _count_windows_and_overload(self, assignments: list[ScheduleAssignment]) -> int:
        soft_penalties = 0
        schedule_by_group = {}

        for a in assignments:
            g_id = a.lesson.group.id
            day = a.timeslot.day
            pair_num = a.timeslot.pair_number

            if g_id not in schedule_by_group:
                schedule_by_group[g_id] = {}
            if day not in schedule_by_group[g_id]:
                schedule_by_group[g_id][day] = []

            schedule_by_group[g_id][day].append(pair_num)

        for g_id, days in schedule_by_group.items():
            for day, pairs in days.items():
                sorted_pairs = sorted(pairs)

                for k in range(len(sorted_pairs) - 1):
                    gap = sorted_pairs[k+1] - sorted_pairs[k] - 1
                    if gap > 0:
                        soft_penalties += gap

                if len(sorted_pairs) > 4:
                    soft_penalties += (len(sorted_pairs) - 4)

        return soft_penalties