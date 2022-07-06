import random

import rdflib
from rdflib import XSD

from kaplan.annotation.component_annotation import MutationComponent
from kaplan.annotation.decorator import merge_component
from kaplan.annotation.ontology import ontology
from kaplan.core.operator import Mutation
from kaplan.core.solution import BinarySolution
from kaplan.util.checking import Check

BIGOWL = ontology(uri="http://www.ontologies.khaos.uma.es/bigowl/")
TITAN = ontology(uri="http://www.ontologies.khaos.uma.es/titan-kaplan/")

BitFlipMutationComponent = merge_component(MutationComponent, {"hasParameterDistribution": BIGOWL.namespace.hasParameter},
                              {"hasParameterDistribution": TITAN.namespace.parameter_mutation_distribution_index})

#@BitFlipMutationComponent(hasImplementation=TITAN.namespace.ImplementationBitFlipMutation, label=rdflib.Literal('Bit Flip Mutation', datatype=XSD.string), hasSolution=BIGOWL.namespace.BinarySolution)
class BitFlipMutation(Mutation):

    def __init__(self, probability: float):
        super(BitFlipMutation, self).__init__(probability=probability)

    def execute(self, solution: BinarySolution) -> BinarySolution:
        Check.that(type(solution) is BinarySolution, "Solution type invalid")

        for i in range(solution.number_of_variables):
            for j in range(len(solution.variables[i])):
                rand = random.random()
                if rand <= self.probability:
                    solution.variables[i][j] = True if solution.variables[i][j] is False else False

        return solution

    def get_name(self):
        return 'BitFlip mutation'