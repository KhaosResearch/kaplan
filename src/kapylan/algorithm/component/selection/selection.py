from abc import ABC, abstractmethod
from kapylan.annotation.component_annotation import SelectionComponent

@SelectionComponent()
class Selection(ABC):
    """ Class representing selection component. """

    def __init__(self):
        pass

    @abstractmethod
    def select(self, source):
        pass

    @abstractmethod
    def get_comparator(self):
        pass

