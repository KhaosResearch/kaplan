from abc import ABC, abstractmethod
from kaplan.core.observer import Observer

class TerminationCriterion(Observer, ABC):

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def is_met(self):
        pass
