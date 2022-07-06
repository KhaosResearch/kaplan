from math import sqrt, pow, sin, pi, cos

from kaplan.core.problem import FloatProblem
from kaplan.core.solution import FloatSolution


class ZDT1(FloatProblem):
    """ Problem ZDT1.

    .. note:: Bi-objective unconstrained problem. The default number of variables is 30.
    .. note:: Continuous problem having a convex Pareto front
    """

    def __init__(self, number_of_variables: int=30):
        """ :param number_of_variables: Number of decision variables of the problem.
        """
        super(ZDT1, self).__init__()
        self.number_of_variables = number_of_variables
        self.number_of_objectives = 2
        self.number_of_constraints = 0

        self.obj_directions = [self.MINIMIZE, self.MINIMIZE]
        self.obj_labels = ['x', 'y']

        self.lower_bound = self.number_of_variables * [0.0]
        self.upper_bound = self.number_of_variables * [1.0]

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        g = self.eval_g(solution)
        h = self.eval_h(solution.variables[0], g)

        solution.objectives[0] = solution.variables[0]
        solution.objectives[1] = h * g

        return solution

    def eval_g(self, solution: FloatSolution):
        g = sum(solution.variables) - solution.variables[0]

        constant = 9.0 / (solution.number_of_variables - 1)

        return constant * g + 1.0

    def eval_h(self, f: float, g: float) -> float:
        return 1.0 - sqrt(f / g)

    def get_name(self):
        return 'ZDT1'
