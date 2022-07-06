import logging
import random
from abc import ABC, abstractmethod, ABCMeta
from typing import Generic, TypeVar, List

from kaplan.core.solution import FloatSolution, MSASolution

LOGGER = logging.getLogger('jmetal')

S = TypeVar('S')

class Problem(Generic[S], ABC):
    """ Class representing problems. """

    MINIMIZE = -1
    MAXIMIZE = 1

    def __init__(self):
        self.number_of_variables: int = 0
        self.number_of_objectives: int = 0
        self.number_of_constraints: int = 0

        self.reference_front: List[S] = []

        self.directions: List[int] = []
        self.labels: List[str] = []

    @abstractmethod
    def create_solution(self) -> S:
        """ Creates a random_search solution to the problem.

        :return: Solution. """
        pass

    @abstractmethod
    def evaluate(self, solution: S) -> S:
        """ Evaluate a solution. For any new problem inheriting from :class:`Problem`, this method should be
        replaced. Note that this framework ASSUMES minimization, thus solutions must be evaluated in consequence.

        :return: Evaluated solution. """
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class FloatProblem(Problem[FloatSolution], ABC):
    """ Class representing float problems. """

    def __init__(self):
        super(FloatProblem, self).__init__()
        self.lower_bound = []
        self.upper_bound = []

    def create_solution(self) -> FloatSolution:
        new_solution = FloatSolution(
            self.lower_bound,
            self.upper_bound,
            self.number_of_objectives,
            self.number_of_constraints)
        new_solution.variables = \
            [random.uniform(self.lower_bound[i] * 1.0, self.upper_bound[i] * 1.0) for i in
             range(self.number_of_variables)]

        return new_solution


class MSAProblem(Problem[MSASolution]):
    """ Class representing MSA problems """

    __metaclass__ = ABCMeta

    def __init__(self):
        super(MSAProblem, self).__init__()
        self.number_of_constraints = 0

    @abstractmethod
    def evaluate(self, solution: MSASolution) -> MSASolution:
        pass

    def get_name(self) -> str:
        return 'Multiple Sequence Alignment problem'