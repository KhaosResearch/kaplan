from abc import ABC, abstractmethod
from enum import Enum

from kaplan.annotation.component_annotation import ReplacementComponent
from kaplan.util.density_estimator import DensityEstimator
from kaplan.util.ranking import Ranking

class RemovalPolicyType(Enum):
    SEQUENTIAL = 1
    ONE_SHOT = 2

@ReplacementComponent()
class Replacement(ABC):
    """ Class representing replacement component. """

    def __init__(self, ranking: Ranking, density_estimator: DensityEstimator, removal_policy=RemovalPolicyType.ONE_SHOT):
        pass

    @abstractmethod
    def replace(self, source):
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass
