import unittest
from kapylan.algorithm.component.evaluation.impl.SequentialEvaluation import (
    SequentialEvaluation,
)
from kapylan.core.problem import FloatProblem
from kapylan.core.solution import FloatSolution


class MockedProblem(FloatProblem):
    def __init__(self, number_of_variables: int = 3):
        super(MockedProblem, self).__init__()
        self.number_of_objectives = 2
        self.number_of_variables = number_of_variables
        self.number_of_constraints = 0

        self.lower_bound = [-5.0 for _ in range(number_of_variables)]
        self.upper_bound = [5.0 for _ in range(number_of_variables)]

        FloatSolution.lower_bound = self.lower_bound
        FloatSolution.upper_bound = self.upper_bound

    def evaluate(self, solution: FloatSolution):
        solution.objectives[0] = 1.2
        solution.objectives[1] = 2.3

        return solution

    def get_name(self) -> str:
        pass


class SequentialEvaluationTestCases(unittest.TestCase):
    def setUp(self):
        self.problem = MockedProblem()
        self.evaluation = SequentialEvaluation(self.problem)

    def test_should_constructor_create_a_non_null_object(self):
        self.assertIsNotNone(self.evaluation)

    def test_should_evaluate_a_list_of_problem_work_properly_with_a_solution(self):
        problem_list = [self.problem.create_solution() for _ in range(1)]

        self.evaluation.evaluate(problem_list)

        self.assertEqual(1.2, problem_list[0].objectives[0])
        self.assertEqual(2.3, problem_list[0].objectives[1])

    def test_should_evaluate_a_list_of_problem_work_properly(self):
        problem_list = [self.problem.create_solution() for _ in range(10)]

        self.evaluation.evaluate(problem_list)

        for i in range(10):
            self.assertEqual(1.2, problem_list[i].objectives[0])
            self.assertEqual(2.3, problem_list[i].objectives[1])


if __name__ == "__main__":
    unittest.main()
