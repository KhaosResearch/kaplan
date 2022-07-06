from abc import ABC, abstractmethod
from kapylan.core.operator import Crossover, Mutation

class Variation(ABC):
    """ Class representing variation component. """

    def __init__(self, mutation_operator: Mutation, crossover_operator: Crossover):
        pass

    @abstractmethod
    def variate(self, source):
        pass

    def get_mutation(self):
        pass

    def get_crossover(self):
        pass
