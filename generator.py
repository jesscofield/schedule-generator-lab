import random
from models import ScheduleAssignment
from constraints import ConstraintEvaluator


class ScheduleGenerator:
    def __init__(self, lessons, timeslots, rooms, evaluator: ConstraintEvaluator):
        self.lessons = lessons
        self.timeslots = timeslots
        self.rooms = rooms
        self.evaluator = evaluator

    def generate_random_schedule(self) -> list[ScheduleAssignment]:
        assignments = []
        for lesson in self.lessons:
            random_timeslot = random.choice(self.timeslots)
            random_room = random.choice(self.rooms)
            assignments.append(ScheduleAssignment(lesson, random_timeslot, random_room))
        return assignments

    def solve_genetic(self, population_size: int = 50, generations: int = 500, mutation_rate: float = 0.1) -> list[ScheduleAssignment]:
        population = [self.generate_random_schedule() for _ in range(population_size)]

        best_schedule = None
        best_fitness = -1.0

        for generation in range(generations):
            evaluated_population = []
            for individual in population:
                hard, soft, fitness = self.evaluator.evaluate(individual)
                evaluated_population.append((individual, fitness, hard))

                if fitness > best_fitness:
                    best_fitness = fitness
                    best_schedule = individual

                if hard == 0 and soft == 0:
                    return individual

            evaluated_population.sort(key=lambda x: x[1], reverse=True)
            survivors = [ind[0] for ind in evaluated_population[:population_size // 2]]

            new_population = list(survivors)
            while len(new_population) < population_size:
                parent1 = random.choice(survivors)
                parent2 = random.choice(survivors)
                child = self._crossover(parent1, parent2)
                child = self._mutate(child, mutation_rate)
                new_population.append(child)

            population = new_population

        return best_schedule

    def _crossover(self, parent1: list[ScheduleAssignment], parent2: list[ScheduleAssignment]) -> list[ScheduleAssignment]:
        crossover_point = random.randint(0, len(parent1) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child

    def _mutate(self, schedule: list[ScheduleAssignment], mutation_rate: float) -> list[ScheduleAssignment]:
        mutated_schedule = []
        for assignment in schedule:
            if random.random() < mutation_rate:
                new_timeslot = random.choice(self.timeslots)
                new_room = random.choice(self.rooms)
                mutated_schedule.append(ScheduleAssignment(assignment.lesson, new_timeslot, new_room))
            else:
                mutated_schedule.append(assignment)
        return mutated_schedule