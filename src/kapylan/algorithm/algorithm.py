from abc import ABC, abstractmethod


class Algorithm(ABC):
    """Class representing evaluation component"""

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def get_result(self):
        pass
