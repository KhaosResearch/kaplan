from abc import ABC, abstractmethod
from kapylan.core.problem import Problem

class Generator(ABC):

    @abstractmethod
    def new(self, problem: Problem):
        pass


class RandomGenerator(Generator):

    def new(self, problem: Problem):
        return problem.create_solution()