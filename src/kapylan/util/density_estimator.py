import logging
from abc import ABC, abstractmethod
from functools import cmp_to_key
from typing import TypeVar

import rdflib
from rdflib import XSD

from kapylan.annotation.component_annotation import DensityEstimatorComponent
from kapylan.annotation.ontology import ontology
from kapylan.util.comparator import SolutionAttributeComparator, Comparator

TITAN = ontology(uri="http://www.ontologies.khaos.uma.es/titan-kaplan/")

LOGGER = logging.getLogger("jmetal")

S = TypeVar("S")


class DensityEstimator(list, ABC):
    """This is the interface of any density estimator algorithm."""

    @abstractmethod
    def compute_density_estimator(self, solutions: list) -> float:
        pass

    @abstractmethod
    def sort(self, solutions: list) -> list:
        pass

    @classmethod
    def get_comparator(cls) -> Comparator:
        pass


@DensityEstimatorComponent(
    hasImplementation=TITAN.namespace.ImplementationCrowdingDistance,
    label=rdflib.Literal("Crowding Distance Density Estimator", datatype=XSD.string),
)
class CrowdingDistance(DensityEstimator):
    """This class implements a DensityEstimator based on the crowding distance of algorithm NSGA-II."""

    def compute_density_estimator(self, front: list):
        """This function performs the computation of the crowding density estimation over the solution list.

        .. note::
           This method assign the distance in the inner elements of the solution list.

        :param front: The list of solutions.
        """
        size = len(front)

        if size == 0:
            return
        elif size == 1:
            front[0].attributes["crowding_distance"] = float("inf")
            return
        elif size == 2:
            front[0].attributes["crowding_distance"] = float("inf")
            front[1].attributes["crowding_distance"] = float("inf")
            return

        for i in range(len(front)):
            front[i].attributes["crowding_distance"] = 0.0

        number_of_objectives = front[0].number_of_objectives

        for i in range(number_of_objectives):
            # Sort the population by Obj n
            front = sorted(front, key=lambda x: x.objectives[i])
            objective_minn = front[0].objectives[i]
            objective_maxn = front[len(front) - 1].objectives[i]

            # Set de crowding distance
            front[0].attributes["crowding_distance"] = float("inf")
            front[size - 1].attributes["crowding_distance"] = float("inf")

            for j in range(1, size - 1):
                distance = front[j + 1].objectives[i] - front[j - 1].objectives[i]

                # Check if minimum and maximum are the same (in which case do nothing)
                if objective_maxn - objective_minn == 0:
                    pass
                    # LOGGER.warning('Minimum and maximum are the same!')
                else:
                    distance = distance / (objective_maxn - objective_minn)

                distance += front[j].attributes["crowding_distance"]
                front[j].attributes["crowding_distance"] = distance

    def sort(self, solutions: list) -> list:
        solutions.sort(key=cmp_to_key(self.get_comparator().compare))

    @classmethod
    def get_comparator(cls) -> Comparator:
        return SolutionAttributeComparator("crowding_distance", lowest_is_best=False)

    def get_name(self) -> str:
        return "Crowding distance"
