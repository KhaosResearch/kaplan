import unittest
from mockito import mock, never, verify, when
from kapylan.core.solution import Solution

from kapylan.util.comparator import Comparator, MultiComparator, SolutionAttributeComparator


class SolutionAttributeComparatorTestCases(unittest.TestCase):
    def setUp(self):
        self.comparator = SolutionAttributeComparator("attribute")

    def test_should_compare_return_zero_if_the_first_solution_has_no_the_attribute(self):
        solution1 = Solution(1, 1)
        solution2 = Solution(1, 1)
        solution2.attributes["attribute"] = 1.0

        self.assertEqual(0, self.comparator.compare(solution1, solution2))

    def test_should_compare_return_zero_if_the_second_solution_has_no_the_attribute(self):
        solution1 = Solution(1, 1)
        solution2 = Solution(1, 1)
        solution1.attributes["attribute"] = 1.0

        self.assertEqual(0, self.comparator.compare(solution1, solution2))

    def test_should_compare_return_zero_if_none_of_the_solutions_have_the_attribute(self):
        solution1 = Solution(1, 1)
        solution2 = Solution(1, 1)

        self.assertEqual(0, self.comparator.compare(solution1, solution2))

    def test_should_compare_return_zero_if_both_solutions_have_the_same_attribute_value(self):
        solution1 = Solution(1, 1)
        solution2 = Solution(1, 1)
        solution1.attributes["attribute"] = 1.0
        solution2.attributes["attribute"] = 1.0

        self.assertEqual(0, self.comparator.compare(solution1, solution2))

    def test_should_compare_works_properly_case1(self):
        """Case 1: solution1.attribute < solution2.attribute (lowest is best)"""
        solution1 = Solution(1, 1)
        solution2 = Solution(1, 1)
        solution1.attributes["attribute"] = 0.0
        solution2.attributes["attribute"] = 1.0

        self.assertEqual(-1, self.comparator.compare(solution1, solution2))

    def test_should_compare_works_properly_case2(self):
        """Case 2: solution1.attribute > solution2.attribute (lowest is best)"""
        solution1 = Solution(1, 1)
        solution2 = Solution(1, 1)
        solution1.attributes["attribute"] = 1.0
        solution2.attributes["attribute"] = 0.0

        self.assertEqual(1, self.comparator.compare(solution1, solution2))

    def test_should_compare_works_properly_case3(self):
        """Case 3: solution1.attribute < solution2.attribute (highest is best)"""
        comparator = SolutionAttributeComparator("attribute", False)
        solution1 = Solution(1, 1)
        solution2 = Solution(1, 1)
        solution1.attributes["attribute"] = 0.0
        solution2.attributes["attribute"] = 1.0

        self.assertEqual(1, comparator.compare(solution1, solution2))

    def test_should_compare_works_properly_case4(self):
        """Case 4: solution1.attribute > solution2.attribute (highest is best)"""
        solution1 = Solution(1, 1)
        solution2 = Solution(1, 1)
        solution1.attributes["attribute"] = 1.0
        solution2.attributes["attribute"] = 0.0

        comparator = SolutionAttributeComparator("attribute", False)
        self.assertEqual(-1, comparator.compare(solution1, solution2))

class MultiComparatorTestCases(unittest.TestCase):
    def test_should_compare_return_zero_if_the_comparator_list_is_empty(self):
        solution1 = Solution(2, 2)
        solution2 = Solution(2, 2)

        multi_comparator = MultiComparator([])
        self.assertEqual(0, multi_comparator.compare(solution1, solution2))

    def test_should_compare_work_properly_case_1(self):
        """Case 1: a comparator returning 0."""
        solution1 = Solution(2, 2)
        solution2 = Solution(2, 2)

        mocked_comparator: Comparator = mock()
        when(mocked_comparator).compare(solution1, solution2).thenReturn(0)

        comparator_list = [mocked_comparator]

        multi_comparator = MultiComparator(comparator_list)
        self.assertEqual(0, multi_comparator.compare(solution1, solution2))

        verify(mocked_comparator, times=1).compare(solution1, solution2)

    def test_should_compare_work_properly_case_2(self):
        """Case 2: two comparators; the first returns 1 and the second one returns 0.
        Expected result: 1
        """
        solution1 = Solution(2, 2)
        solution2 = Solution(2, 2)

        mocked_comparator1: Comparator = mock()
        when(mocked_comparator1).compare(solution1, solution2).thenReturn(1)
        mocked_comparator2: Comparator = mock()
        when(mocked_comparator2).compare(solution1, solution2).thenReturn(0)

        comparator_list = [mocked_comparator1, mocked_comparator2]

        multi_comparator = MultiComparator(comparator_list)
        self.assertEqual(1, multi_comparator.compare(solution1, solution2))

        verify(mocked_comparator1, times=1).compare(solution1, solution2)
        verify(mocked_comparator2, never).compare(solution1, solution2)

    def test_should_compare_work_properly_case_3(self):
        """Case 2: two comparators; the first returns 0 and the second one returns -1.
        Expected result: -1
        """
        solution1 = Solution(2, 2)
        solution2 = Solution(2, 2)

        mocked_comparator1: Comparator = mock()
        when(mocked_comparator1).compare(solution1, solution2).thenReturn(0)
        mocked_comparator2: Comparator = mock()
        when(mocked_comparator2).compare(solution1, solution2).thenReturn(-1)

        comparator_list = [mocked_comparator1, mocked_comparator2]

        multi_comparator = MultiComparator(comparator_list)
        self.assertEqual(-1, multi_comparator.compare(solution1, solution2))

        verify(mocked_comparator1, times=1).compare(solution1, solution2)
        verify(mocked_comparator2, times=1).compare(solution1, solution2)


if __name__ == "__main__":
    unittest.main()