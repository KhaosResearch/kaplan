import logging
import os
from pathlib import Path
from typing import List

from kapylan.core.solution import FloatSolution, Solution
from kapylan.problem.msa import MSA
from kapylan.util.archive import Archive, NonDominatedSolutionsArchive

LOGGER = logging.getLogger('kaplan')


def get_non_dominated_solutions(solutions: list) -> list:
    archive: Archive = NonDominatedSolutionsArchive()

    for solution in solutions:
        archive.add(solution)

    return archive.solution_list

def read_solutions(filename: str) -> list:
    """ Reads a reference front from a file.

    :param filename: File path where the front is located.
    """
    front = []

    if Path(filename).is_file():
        with open(filename) as file:
            for line in file:
                vector = [float(x) for x in line.split()]

                solution = FloatSolution([], [], len(vector))
                solution.objectives = vector

                front.append(solution)
    else:
        LOGGER.warning('Reference front file was not found at {}'.format(filename))

    return front


def print_variables_to_file(solutions: list, filename: str):
    LOGGER.info('Output file (variables): ' + filename)

    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    except FileNotFoundError:
        pass

    if type(solutions) is not list:
        solutions = [solutions]

    with open(filename, 'w') as of:
        for solution in solutions:
            for variables in solution.variables:
                of.write(str(variables) + " ")
            of.write("\n")


def print_variables_to_screen(solutions):
    if type(solutions) is not list:
        solutions = [solutions]

    for solution in solutions:
        print(solution.variables[0])


def print_function_values_to_file(solutions: list, filename: str):
    LOGGER.info('Output file (function values): ' + filename)

    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    except FileNotFoundError:
        pass

    if type(solutions) is not list:
        solutions = [solutions]

    with open(filename, 'w') as of:
        for solution in solutions:
            for function_value in solution.objectives:
                of.write(str(function_value) + ' ')
            of.write('\n')

def print_function_values_to_screen(solutions: list):
    if type(solutions) is not list:
        solutions = [solutions]

    for solution in solutions:
        print(str(solutions.index(solution)) + ": ", sep='  ', end='', flush=True)
        print(solution.objectives, sep='  ', end='', flush=True)
        print()


def restore_objs(front: list, problem: MSA):
    for solution in front:
        for i in range(problem.number_of_objectives):
            if not problem.score_list[i].is_minimization():
                solution.objectives[i] = -1.0 * solution.objectives[i]

    return front

def get_representative_set(front: list):
    """ Returns three solutions from any given front: one from the middle (by sorting the front in regard to the first
    objective) and one from each extreme region.
    """
    # find extreme regions
    upper_extreme, lower_extreme = front[0], front[-1]

    # find middle
    def _obj(s):
        return s.objectives[0]
    front.sort(key=_obj)
    middle = front[len(front) // 2]

    return upper_extreme, middle, lower_extreme