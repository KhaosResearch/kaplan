from abc import ABC

import rdflib
from rdflib import XSD

from kapylan.algorithm.component.variation.variation import Variation
from kapylan.annotation.component_annotation import VariationComponent
from kapylan.annotation.decorator import merge_component
from kapylan.annotation.ontology import ontology
from kapylan.core.operator import Crossover, Mutation

BIGOWL = ontology(uri="http://www.ontologies.khaos.uma.es/bigowl/")
TITAN = ontology(uri="http://www.ontologies.khaos.uma.es/titan-kaplan/")

CrossoverAndMutationVariationComponent = merge_component(
    VariationComponent,
    {
        "hasParameterMutationName": BIGOWL.namespace.hasParameter,
        "hasParameterCrossoverName": BIGOWL.namespace.hasParameter,
    },
    {
        "hasParameterMutationName": TITAN.namespace.parameter_mutation_name,
        "hasParameterCrossoverName": TITAN.namespace.parameter_crossover_name,
    },
)


@CrossoverAndMutationVariationComponent(
    hasImplementation=TITAN.namespace.ImplementationCrossoverAndMutationVariation,
    label=rdflib.Literal("Crossover and Mutation Variation", datatype=XSD.string),
)
class CrossoverAndMutationVariation(Variation, ABC):
    def __init__(
        self,
        mutation_operator: Mutation,
        crossover_operator: Crossover,
        offspring_population_size: int,
    ):
        super(CrossoverAndMutationVariation, self).__init__(
            mutation_operator, crossover_operator
        )
        self.mutation_operator = mutation_operator
        self.crossover_operator = crossover_operator
        self.offspring_population_size = offspring_population_size

        self.mating_pool_size = int(
            self.offspring_population_size
            * self.crossover_operator.get_number_of_parents()
            / self.crossover_operator.get_number_of_children()
        )

    def get_crossover(self):
        return self.crossover_operator

    def get_mutation(self):
        return self.mutation_operator

    def get_mating_pool_size(self):
        return self.mating_pool_size

    def variate(self, mating_population: list):
        offspring_pool = []
        for parents in zip(*[iter(mating_population)] * 2):
            offspring_pool.append(self.crossover_operator.execute(parents))

        offspring_population = []
        for pair in offspring_pool:
            for solution in pair:
                mutated_solution = self.mutation_operator.execute(solution)
                offspring_population.append(mutated_solution)

        return offspring_population

    def get_name(self):
        return "Crossover and mutation variation"
