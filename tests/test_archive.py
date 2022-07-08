import unittest
from kapylan.core.solution import Solution

from kapylan.util.archive import Archive, NonDominatedSolutionsArchive


class ArchiveTestCases(unittest.TestCase):
    class DummyArchive(Archive):
        def add(self, solution) -> bool:
            pass

    def setUp(self):
        self.archive = self.DummyArchive()

    def test_should_constructor_create_a_non_null_object(self):
        self.assertIsNotNone(self.archive)

    def test_should_constructor_create_an_empty_list(self):
        self.assertEqual(0, len(self.archive.solution_list))


class NonDominatedSolutionListArchiveTestCases(unittest.TestCase):
    def setUp(self):
        self.archive = NonDominatedSolutionsArchive()

    def test_should_constructor_create_a_non_null_object(self):
        self.assertIsNotNone(self.archive)

    def test_should_adding_one_solution_work_properly(self):
        solution = Solution(1, 1)
        self.archive.add(solution)
        self.assertEqual(1, self.archive.size())
        self.assertEqual(solution, self.archive.solution_list[0])

    def test_should_adding_two_solutions_work_properly_if_one_is_dominated(self):
        dominated_solution = Solution(1, 2)
        dominated_solution.objectives = [2.0, 2.0]

        dominant_solution = Solution(1, 2)
        dominant_solution.objectives = [1.0, 1.0]

        self.archive.add(dominated_solution)
        self.archive.add(dominant_solution)

        self.assertEqual(1, self.archive.size())
        self.assertEqual(dominant_solution, self.archive.solution_list[0])

    def test_should_adding_two_solutions_work_properly_if_both_are_non_dominated(self):
        solution1 = Solution(1, 2)
        solution1.objectives = [1.0, 0.0]

        solution2 = Solution(1, 2)
        solution2.objectives = [0.0, 1.0]

        self.archive.add(solution1)
        self.archive.add(solution2)

        self.assertEqual(2, self.archive.size())
        self.assertTrue(
            solution1 in self.archive.solution_list
            and solution2 in self.archive.solution_list
        )

    def test_should_adding_four_solutions_work_properly_if_one_dominates_the_others(
        self,
    ):
        solution1 = Solution(1, 2)
        solution1.objectives = [1.0, 1.0]

        solution2 = Solution(1, 2)
        solution2.objectives = [0.0, 2.0]

        solution3 = Solution(1, 2)
        solution3.objectives = [0.5, 1.5]

        solution4 = Solution(1, 2)
        solution4.objectives = [0.0, 0.0]

        self.archive.add(solution1)
        self.archive.add(solution2)
        self.archive.add(solution3)
        self.archive.add(solution4)

        self.assertEqual(1, self.archive.size())
        self.assertEqual(solution4, self.archive.solution_list[0])

    def test_should_adding_three_solutions_work_properly_if_two_of_them_are_equal(self):
        solution1 = Solution(1, 2)
        solution1.objectives = [1.0, 1.0]

        solution2 = Solution(1, 2)
        solution2.objectives = [0.0, 2.0]

        solution3 = Solution(1, 2)
        solution3.objectives = [1.0, 1.0]

        self.archive.add(solution1)
        self.archive.add(solution2)
        result = self.archive.add(solution3)

        self.assertEqual(2, self.archive.size())
        self.assertFalse(result)
        self.assertTrue(
            solution1 in self.archive.solution_list
            or solution3 in self.archive.solution_list
        )


if __name__ == "__main__":
    unittest.main()
