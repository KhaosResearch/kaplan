import copy
import random

import rdflib
from rdflib import XSD

from kapylan.annotation.component_annotation import CrossoverComponent
from kapylan.annotation.decorator import merge_component
from kapylan.annotation.ontology import ontology
from kapylan.core.operator import Crossover
from kapylan.core.solution import FloatSolution
from kapylan.util.checking import Check

BIGOWL = ontology(uri="http://www.ontologies.khaos.uma.es/bigowl/")
TITAN = ontology(uri="http://www.ontologies.khaos.uma.es/titan-kaplan/")

SBXCrossoverComponent = merge_component(
    CrossoverComponent,
    {"hasParameterDistribution": BIGOWL.namespace.hasParameter},
    {
        "hasParameterDistribution": TITAN.namespace.parameter_crossover_distribution_index
    },
)

# @SBXCrossoverComponent(hasImplementation=TITAN.namespace.ImplementationSBXCrossoverOperator, label=rdflib.Literal('SBX Crossover', datatype=XSD.string))
class SBXCrossover(Crossover):
    __EPS = 1.0e-14

    def __init__(self, probability: float, distribution_index: float = 20.0):
        super(SBXCrossover, self).__init__(probability=probability)
        self.distribution_index = distribution_index

        if distribution_index < 0:
            raise Exception(
                "The distribution index is negative: " + str(distribution_index)
            )

    def execute(self, parents: list) -> list:
        Check.that(
            issubclass(type(parents[0]), FloatSolution),
            "Solution type invalid: " + str(type(parents[0])),
        )
        Check.that(issubclass(type(parents[1]), FloatSolution), "Solution type invalid")
        Check.that(
            len(parents) == 2,
            "The number of parents is not two: {}".format(len(parents)),
        )

        offspring = [copy.deepcopy(parents[0]), copy.deepcopy(parents[1])]
        rand = random.random()

        if rand <= self.probability:
            for i in range(parents[0].number_of_variables):
                value_x1, value_x2 = parents[0].variables[i], parents[1].variables[i]

                if random.random() <= 0.5:
                    if abs(value_x1 - value_x2) > self.__EPS:
                        if value_x1 < value_x2:
                            y1, y2 = value_x1, value_x2
                        else:
                            y1, y2 = value_x2, value_x1

                        lower_bound, upper_bound = (
                            parents[0].lower_bound[i],
                            parents[1].upper_bound[i],
                        )

                        beta = 1.0 + (2.0 * (y1 - lower_bound) / (y2 - y1))
                        alpha = 2.0 - pow(beta, -(self.distribution_index + 1.0))

                        rand = random.random()
                        if rand <= (1.0 / alpha):
                            betaq = pow(
                                rand * alpha, (1.0 / (self.distribution_index + 1.0))
                            )
                        else:
                            betaq = pow(
                                1.0 / (2.0 - rand * alpha),
                                1.0 / (self.distribution_index + 1.0),
                            )

                        c1 = 0.5 * (y1 + y2 - betaq * (y2 - y1))
                        beta = 1.0 + (2.0 * (upper_bound - y2) / (y2 - y1))
                        alpha = 2.0 - pow(beta, -(self.distribution_index + 1.0))

                        if rand <= (1.0 / alpha):
                            betaq = pow(
                                (rand * alpha), (1.0 / (self.distribution_index + 1.0))
                            )
                        else:
                            betaq = pow(
                                1.0 / (2.0 - rand * alpha),
                                1.0 / (self.distribution_index + 1.0),
                            )

                        c2 = 0.5 * (y1 + y2 + betaq * (y2 - y1))

                        if c1 < lower_bound:
                            c1 = lower_bound
                        if c2 < lower_bound:
                            c2 = lower_bound
                        if c1 > upper_bound:
                            c1 = upper_bound
                        if c2 > upper_bound:
                            c2 = upper_bound

                        if random.random() <= 0.5:
                            offspring[0].variables[i] = c2
                            offspring[1].variables[i] = c1
                        else:
                            offspring[0].variables[i] = c1
                            offspring[1].variables[i] = c2
                    else:
                        offspring[0].variables[i] = value_x1
                        offspring[1].variables[i] = value_x2
                else:
                    offspring[0].variables[i] = value_x1
                    offspring[1].variables[i] = value_x2
        return offspring

    def get_number_of_parents(self) -> int:
        return 2

    def get_number_of_children(self) -> int:
        return 2

    def get_name(self) -> str:
        return "SBX crossover"
