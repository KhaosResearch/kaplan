from abc import ABC, abstractmethod

from kaplan.core.problem import Problem

class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, solution_list: list, problem: Problem) -> list:
        pass

    @staticmethod
    def evaluate_solution(solution, problem: Problem) -> None:
        problem.evaluate(solution)

class SequentialEvaluator(Evaluator):
    def evaluate(self, solution_list: list, problem: Problem) -> list:
        for solution in solution_list:
            Evaluator.evaluate_solution(solution, problem)

        return solution_list