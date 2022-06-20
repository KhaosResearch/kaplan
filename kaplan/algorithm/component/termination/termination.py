from abc import ABC, abstractmethod

from kaplan.annotation.component_annotation import TerminationComponent

@TerminationComponent()
class Termination(ABC):
    """ Class representing termination component. """

    def __init__(self):
        pass

    @abstractmethod
    def update(self, source):
        pass

    def get_name(self):
        pass