import random

import rdflib
from rdflib import XSD

from kapylan.annotation.component_annotation import MutationComponent
from kapylan.annotation.decorator import merge_component
from kapylan.annotation.ontology import ontology
from kapylan.core.operator import Mutation
from kapylan.core.solution import MSASolution

BIGOWL = ontology(uri="http://www.ontologies.khaos.uma.es/bigowl/")
TITAN = ontology(uri="http://www.ontologies.khaos.uma.es/titan-kaplan/")

ShiftClosedGapGroupsMutationComponent = merge_component(
    MutationComponent,
    {"hasParameterDistribution": BIGOWL.namespace.hasParameter},
    {"hasParameterDistribution": TITAN.namespace.parameter_mutation_remove_gap_columns},
)

# @ShiftClosedGapGroupsMutationComponent(hasImplementation=TITAN.namespace.ImplementationShiftClosedGapGroupsMutation, label=rdflib.Literal('Shift Closed Gap Groups Mutation', datatype=XSD.string),
#                                       hasSolution=BIGOWL.namespace.MSASolution)
class ShiftClosedGapGroupsMutation(Mutation):
    """For every sequence, selects a random group and shift it with the closest gap group."""

    def __init__(self, probability: float, remove_gap_columns: bool = True) -> None:
        super(ShiftClosedGapGroupsMutation, self).__init__(probability=probability)
        self.remove_full_of_gap_columns = remove_gap_columns

    def execute(self, solution: MSASolution) -> MSASolution:
        if solution is None:
            raise Exception("Solution is none")

        return self.do_mutation(solution)

    def do_mutation(self, solution: MSASolution) -> MSASolution:
        if random.random() <= self.probability:
            for i in range(solution.number_of_variables):
                gaps_group = solution.gaps_groups[i]

                if len(gaps_group) >= 4:
                    random_gaps_group = random.randrange(0, len(gaps_group) - 2, 2)
                    right_is_closest = False

                    if not right_is_closest:
                        diff = (
                            gaps_group[random_gaps_group + 3]
                            - gaps_group[random_gaps_group + 2]
                        ) - (
                            gaps_group[random_gaps_group + 1]
                            - gaps_group[random_gaps_group]
                        )

                        if diff < 0:
                            # diff < 0 means that gaps group 2 is shorter than gaps group 1, thus we need to decrease
                            # the length of the gaps group 1
                            diff = -1 * diff
                            gaps_group[random_gaps_group + 1] -= diff

                            gaps_group[random_gaps_group + 3] += diff

                            # displace gaps group 2 one position to the left
                            gaps_group[random_gaps_group + 2] -= diff
                            gaps_group[random_gaps_group + 3] -= diff
                        elif diff > 0:
                            # diff > 0 means that gaps group 2 is larger than gaps group 1, thus we need to increase
                            # the length of the gaps group 1
                            gaps_group[random_gaps_group + 1] += diff

                            gaps_group[random_gaps_group + 3] -= diff

                            # displace gaps group 2 one position to the right
                            gaps_group[random_gaps_group + 2] += diff
                            gaps_group[random_gaps_group + 3] += diff

            if self.remove_full_of_gap_columns:
                solution.remove_full_of_gaps_columns()

            # Sanity check: alignment is valid (same length for all sequences)
            if not solution.is_valid_msa():
                raise Exception(
                    "Mutated solution is not valid! {0}".format(
                        solution.decode_alignment_as_list_of_pairs()
                    )
                )

        return solution

    def get_name(self) -> str:
        return "Shift closed gap group"
