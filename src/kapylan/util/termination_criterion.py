from abc import ABC, abstractmethod
from kapylan.core.observer import Observer


class TerminationCriterion(Observer, ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def is_met(self):
        pass
