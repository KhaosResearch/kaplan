from abc import ABC, abstractmethod

from kaplan.annotation.component_annotation import SolutionCreationComponent


@SolutionCreationComponent()
class SolutionCreation(ABC):
    """ Class representing solution creation component. """

    def __init__(self):
        pass

    @abstractmethod
    def create(self, source):
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass