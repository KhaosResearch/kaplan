import unittest

from hamcrest import any_of, assert_that
from kapylan.algorithm.component.selection.impl.BinaryTournamentSelection import (
    BinaryTournamentSelection,
)
from kapylan.algorithm.component.selection.impl.RandomSolutionSelection import (
    RandomSolutionSelection,
)
from kapylan.core.solution import Solution


class BinaryTournamentTestCases(unittest.TestCase):
    def setUp(self):
        self.selection = BinaryTournamentSelection(100)

    def test_should_constructor_create_a_non_null_object(self):
        self.assertIsNotNone(self.selection)

    def test_should_execute_raise_an_exception_if_the_list_of_solutions_is_none(self):
        solution_list = None
        with self.assertRaises(Exception):
            self.selection.select(solution_list)

    def test_should_execute_raise_an_exception_if_the_list_of_solutions_is_empty(self):
        solution_list = []
        with self.assertRaises(Exception):
            self.selection.select(solution_list)

    def test_should_execute_return_the_solution_in_a_list_with_one_solution(self):
        solution = Solution(3, 2)
        solution_list = [solution]

        self.assertEqual([solution], self.selection.select(solution_list))

    def test_should_execute_work_if_the_solution_list_contains_two_non_dominated_solutions(
        self,
    ):
        solution1 = Solution(2, 2)
        solution1.variables = [1.0, 2.0]
        solution2 = Solution(2, 2)
        solution2.variables = [0.0, 3.0]

        solution_list = [solution1, solution2]

        assert_that(any_of(solution1, solution2), self.selection.select(solution_list))

    def test_should_execute_work_if_the_solution_list_contains_two_solutions_and_one_them_is_dominated(
        self,
    ):
        solution1 = Solution(2, 2)
        solution1.variables = [1.0, 4.0]
        solution2 = Solution(2, 2)
        solution2.variables = [0.0, 3.0]

        solution_list = [solution1, solution2]

        assert_that(solution2, self.selection.select(solution_list))


class RandomSolutionSelectionTestCases(unittest.TestCase):
    def setUp(self):
        self.selection = RandomSolutionSelection(100)

    def test_should_constructor_create_a_non_null_object(self):
        self.assertIsNotNone(self.selection)

    def test_should_execute_raise_an_exception_if_the_list_of_solutions_is_none(self):
        solution_list = None
        with self.assertRaises(Exception):
            self.selection.select(solution_list)

    def test_should_execute_raise_an_exception_if_the_list_of_solutions_is_empty(self):
        solution_list = []
        with self.assertRaises(Exception):
            self.selection.select(solution_list)


if __name__ == "__main__":
    unittest.main()
