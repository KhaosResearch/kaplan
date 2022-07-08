import unittest

from kapylan.core.solution import Solution
from kapylan.util.constraint_handling import overall_constraint_violation_degree


class ConstraintHandlingTestCases(unittest.TestCase):
    def test_should_constraint_violation_degree_return_zero_if_the_solution_has_no_constraints(
        self,
    ) -> None:
        solution = Solution(
            number_of_variables=2, number_of_objectives=2, number_of_constraints=0
        )

        self.assertEqual(0, overall_constraint_violation_degree(solution))

    def test_should_constraint_violation_degree_return_zero_if_the_solution_has_not_violated_constraints(
        self,
    ) -> None:
        solution = Solution(
            number_of_variables=2, number_of_objectives=2, number_of_constraints=2
        )

        self.assertEqual(0, overall_constraint_violation_degree(solution))

    def test_should_constraint_violation_degree_return_the_right_violation_degree(
        self,
    ) -> None:
        solution = Solution(
            number_of_variables=2, number_of_objectives=2, number_of_constraints=2
        )
        solution.constraints[0] = -1
        solution.constraints[1] = -2

        self.assertEqual(-3, overall_constraint_violation_degree(solution))


if __name__ == "__main__":
    unittest.main()
