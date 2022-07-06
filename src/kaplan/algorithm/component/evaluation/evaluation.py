from abc import ABC, abstractmethod

from kaplan.annotation.component_annotation import EvaluationComponent


@EvaluationComponent()
class Evaluation(ABC):
    """ Class representing evaluation component """

    def __init__(self):
        pass

    @abstractmethod
    def evaluate(self, source):
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass