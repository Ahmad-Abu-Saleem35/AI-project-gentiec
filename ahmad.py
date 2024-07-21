#Ahmad abu saleem
import matplotlib.pyplot as plt
import random
from copy import deepcopy

# Define Operation class
class Operation:
    def __init__(self, machine, duration):
        self.machine = machine.lower()  # Normalize machine name to lowercase
        self.duration = duration

# Define Job class
class Job:
    def __init__(self, operations):
        self.operations = operations

# Function to get input from user for defin jobs and operations
def input_fun():
    jobs = []
    machines = set()
    num_jobs = int(input("Enter the number of jobs (up to 10): "))
    for i in range(num_jobs):
        num_operations = int(input(f"Enter the number of operations for job {i + 1}: "))
        operations = []
        for j in range(num_operations):
            machine = input(f"Enter machine name for operation {j + 1} of job {i + 1}: ").lower()
            machines.add(machine)
            duration = int(input(f"Enter duration for operation {j + 1} of job {i + 1}: "))
            operations.append(Operation(machine, duration))
        jobs.append(Job(operations))
    return jobs, list(machines)


# Function to generate an initial population of job schedules
def generate_initial_population(jobs, size, machine_limits):
    population = []
    for _ in range(size):
        chromosome = deepcopy(jobs)
        for job in chromosome:
            random.shuffle(job.operations)

        time_end = {machine: 0 for machine in machine_limits}
        for job in chromosome:
            start_time = 0
            for op in job.operations:
                start_time = max(start_time, time_end[op.machine])
                time_end[op.machine] = start_time + op.duration
                start_time += op.duration

        population.append(chromosome)
    return population


# Function to do the mutation on a chromosome (job schedule)
def make_the_mutation(chromosome):
    job_num = random.randint(0, len(chromosome) - 1)
    job = chromosome[job_num]
    if len(job.operations) > 1:
        op1, op2 = random.sample(range(len(job.operations)), 2)
        job.operations[op1], job.operations[op2] = job.operations[op2], job.operations[op1]
    print(f"Mutated Job {job_num + 1} Operations: {[op.machine for op in job.operations]}")


# Function to calc the fitness of a job schedule
def fitness_measure(schedule, machine_limits):
    time_end = {machine: 0 for machine in machine_limits}
    total_time = 0

    for job_id, job in enumerate(schedule):
        job_time = 0
        start_time = 0
        for op_id, op in enumerate(job.operations):
            if time_end[op.machine] > start_time:
                total_time += (time_end[op.machine] - start_time)
                start_time = time_end[op.machine]

            start_time = max(start_time, time_end[op.machine])
            time_end[op.machine] = start_time + op.duration

            job_time += start_time + op.duration
            start_time += op.duration

        total_time += job_time

    return total_time


# Function to choose two parents from the population for crossover
def choose_a_parents(population, machine_limits):
    tournament_size = 3
    selected = random.sample(population, tournament_size)
    selected.sort(key=lambda x: fitness_measure(x, machine_limits))
    return selected[0], selected[1]



# Function to do a crossover between two parent schedules
def do_cross(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = deepcopy(parent1[:point]) + deepcopy(parent2[point:])
    child2 = deepcopy(parent2[:point]) + deepcopy(parent1[point:])
    return child1, child2


# Function to draw Gantt chart representing the job schedule
def chart_draw(schedule, machines):
    schedule = sorted(schedule, key=lambda job: job.operations[0].machine)
    fig, ax = plt.subplots()
    machine_colors = {machine: plt.cm.tab20(i) for i, machine in enumerate(machines)}
    time_end = {machine: 0 for machine in machines}
    for job_id, job in enumerate(schedule):
        start_time = 0
        for operation in job.operations:
            machine = operation.machine
            start_time = max(start_time, time_end[machine])
            ax.broken_barh([(start_time, operation.duration)], (job_id * 10, 9), facecolors=(machine_colors[machine]))
            ax.text(start_time + operation.duration / 2, job_id * 10 + 5, f"{machine}[{operation.duration}]",
                    ha='center', va='center', color='white', fontsize=8)
            time_end[machine] = start_time + operation.duration
            start_time += operation.duration
    ax.set_xlabel('Time')
    ax.set_yticks([5 + i * 10 for i in range(len(schedule))])
    ax.set_yticklabels([f'Job {i + 1}' for i in range(len(schedule))])
    ax.set_title('Gantt Chart')
    plt.show()


# Function to run the genetic algorithm
def GA_run(jobs, size, generations, machine_limits):
    machines = [op.machine for job in jobs for op in job.operations]
    population = generate_initial_population(jobs, size, machine_limits)
    for generation in range(generations):
        new_population = []
        for _ in range(size):
            parent1, parent2 = choose_a_parents(population, machine_limits)
            child1, child2 = do_cross(parent1, parent2)
            make_the_mutation(child1)
            make_the_mutation(child2)
            new_population.extend([child1, child2])
        population = new_population
        top_fitness = fitness_measure(min(population, key=lambda x: fitness_measure(x, machine_limits)),
                                      machine_limits)
        print(f"Generation {generation + 1}: the best fitness is {top_fitness}")
    best_schedule = min(population, key=lambda x: fitness_measure(x, machine_limits))
    chart_draw(best_schedule, machines)

# Get user input for defining jobs and the operations
jobs, machines = input_fun()

# Example machine capacities (all in lowercase for consistency)
machine_limits = {'m1': 20, 'm2': 20, 'm3': 20, 'm4': 20, 'm5': 20, 'm6': 20, 'm7': 20, 'm8': 20, 'm9': 20, 'm10': 20}


# Parameters
population_size = 10
generations = 50

# Run the genetic algorithm
GA_run(jobs, population_size, generations, machine_limits)
