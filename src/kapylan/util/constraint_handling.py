from kapylan.core.solution import Solution


def overall_constraint_violation_degree(solution: Solution) -> float:
    """
    Returns the constraint violation degree of a solution, which is the sum of the constraint values that are not zero
    :param solution:
    :return:
    """
    return sum([value for value in solution.constraints if value < 0])
