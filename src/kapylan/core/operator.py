from abc import ABC, abstractmethod

class Operator(ABC):
    """ Class representing operator """

    @abstractmethod
    def execute(self, source):
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


def check_valid_probability_value(func):
    def func_wrapper(self, probability: float):
        if probability > 1.0:
            raise Exception('The probability is greater than one: {}'.format(probability))
        elif probability < 0.0:
            raise Exception('The probability is lower than zero: {}'.format(probability))

        res = func(self, probability)
        return res
    return func_wrapper


class Mutation(Operator, ABC):
    """ Class representing mutation operator. """

    @check_valid_probability_value
    def __init__(self, probability: float):
        self.probability = probability


class Crossover(Operator, ABC):
    """ Class representing crossover operator. """

    @check_valid_probability_value
    def __init__(self, probability: float):
        self.probability = probability

    @abstractmethod
    def get_number_of_parents(self) -> int:
        pass

    @abstractmethod
    def get_number_of_children(self) -> int:
        pass