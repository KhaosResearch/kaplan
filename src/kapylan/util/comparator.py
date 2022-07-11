from abc import ABC, abstractmethod
from typing import List, TypeVar

from kapylan.util.constraint_handling import overall_constraint_violation_degree
from kapylan.core.solution import Solution

S = TypeVar("S")


class Comparator(ABC):
    @abstractmethod
    def compare(self, solution1: S, solution2: S) -> int:
        pass


class SolutionAttributeComparator(Comparator):
    def __init__(self, key: str, lowest_is_best: bool = True):
        self.key = key
        self.lowest_is_best = lowest_is_best

    def compare(self, solution1: Solution, solution2: Solution) -> int:
        value1 = solution1.attributes.get(self.key)
        value2 = solution2.attributes.get(self.key)

        result = 0
        if value1 is not None and value2 is not None:
            if self.lowest_is_best:
                if value1 < value2:
                    result = -1
                elif value1 > value2:
                    result = 1
                else:
                    result = 0
            else:
                if value1 > value2:
                    result = -1
                elif value1 < value2:
                    result = 1
                else:
                    result = 0

        return result

    def get_name(self):
        return "Solution attribute comparator"


class MultiComparator(Comparator):
    """
    This comparator takes a list of comparators and check all of them iteratively until a
    value != 0 is obtained or the list becomes empty
    """

    def __init__(self, comparator_list: List[Comparator]):
        self.comparator_list: List[Comparator] = comparator_list

    def compare(self, solution1: Solution, solution2: Solution) -> int:
        for comparator in self.comparator_list:
            flag = comparator.compare(solution1, solution2)
            if flag != 0:
                return flag

        return 0

    def get_comparators(self) -> List[Comparator]:
        return self.comparator_list

    def get_name(self):
        return "Multi comparator"


class OverallConstraintViolationComparator(Comparator):
    def compare(self, solution1: Solution, solution2: Solution) -> int:
        violation_degree_solution_1 = overall_constraint_violation_degree(solution1)
        violation_degree_solution_2 = overall_constraint_violation_degree(solution2)
        if violation_degree_solution_1 < 0 and violation_degree_solution_2 < 0:
            if violation_degree_solution_1 > violation_degree_solution_2:
                result = -1
            elif violation_degree_solution_2 > violation_degree_solution_1:
                result = 1
            else:
                result = 0
        elif violation_degree_solution_1 == 0 and violation_degree_solution_2 < 0:
            result = -1
        elif violation_degree_solution_2 == 0 and violation_degree_solution_1 < 0:
            result = 1
        else:
            result = 0

        return result

    def get_name(self):
        return "Overall constraint violation comparator"


class DominanceComparator(Comparator):
    def __init__(
        self, constraint_comparator: Comparator = OverallConstraintViolationComparator()
    ):
        self.constraint_comparator = constraint_comparator

    def compare(self, solution1: Solution, solution2: Solution) -> int:
        if solution1 is None:
            raise Exception("The solution1 is None")
        elif solution2 is None:
            raise Exception("The solution2 is None")

        result = self.constraint_comparator.compare(solution1, solution2)
        if result == 0:
            # result = self.__dominance_test(solution1, solution2)
            result = self.dominance_test(solution1.objectives, solution2.objectives)

        return result

    def __dominance_test(self, solution1: Solution, solution2: Solution) -> float:
        best_is_one = 0
        best_is_two = 0

        for i in range(solution1.number_of_objectives):
            value1 = solution1.objectives[i]
            value2 = solution2.objectives[i]
            if value1 != value2:
                if value1 < value2:
                    best_is_one = 1
                if value1 > value2:
                    best_is_two = 1

        if best_is_one > best_is_two:
            result = -1
        elif best_is_two > best_is_one:
            result = 1
        else:
            result = 0

        return result

    @staticmethod
    def dominance_test(vector1: List[float], vector2: List[float]) -> int:
        result = 0
        for i in range(len(vector1)):
            if vector1[i] > vector2[i]:
                if result == -1:
                    return 0
                result = 1
            elif vector2[i] > vector1[i]:
                if result == 1:
                    return 0
                result = -1

        return result

    def get_name(self):
        return "Dominance comparator"
