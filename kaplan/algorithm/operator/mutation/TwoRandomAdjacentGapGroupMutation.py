import random
import rdflib
from rdflib import XSD

from kaplan.annotation.component_annotation import MutationComponent
from kaplan.annotation.decorator import merge_component
from kaplan.annotation.ontology import ontology
from kaplan.core.operator import Mutation
from kaplan.core.solution import MSASolution

BIGOWL = ontology(uri="http://www.ontologies.khaos.uma.es/bigowl/")
TITAN = ontology(uri="http://www.ontologies.khaos.uma.es/titan-kaplan/")

TwoRandomAdjacentGapGroupMutationComponent = merge_component(MutationComponent, {"hasParameterDistribution": BIGOWL.namespace.hasParameter},
                              {"hasParameterDistribution": TITAN.namespace.parameter_mutation_remove_gap_columns})

#@TwoRandomAdjacentGapGroupMutationComponent(hasImplementation=TITAN.namespace.ImplementationTwoRandomAdjacentGapGroupMutation, label=rdflib.Literal('Two Random Adjacent Gap Group Mutation', datatype=XSD.string),
#                                            hasSolution=BIGOWL.namespace.MSASolution)
class TwoRandomAdjacentGapGroupMutation(Mutation):
    """ Selects a random gap group and merges it with the adjacent gaps group. """

    def __init__(self, probability: float, remove_gap_columns: bool = True) -> None:
        super(TwoRandomAdjacentGapGroupMutation, self).__init__(probability=probability)
        self.remove_full_of_gap_columns = remove_gap_columns

    def execute(self, solution: MSASolution) -> MSASolution:
        if solution is None:
            raise Exception("Solution is none")

        return self.do_mutation(solution)

    def do_mutation(self, solution: MSASolution) -> MSASolution:
        if random.random() <= self.probability:
            if solution.number_of_variables >= 1:
                seq = random.randint(0, solution.number_of_variables - 1)
            else:
                seq = 0

            gaps_group = solution.gaps_groups[seq]

            if len(gaps_group) >= 4:
                random_gaps_group = random.randrange(0, len(gaps_group) - 2, 2)
                right_is_closest = False

                if not right_is_closest:
                    to_add = gaps_group[random_gaps_group + 3] - gaps_group[random_gaps_group + 2] + 1
                    gaps_group[random_gaps_group + 1] += to_add

                    del gaps_group[random_gaps_group + 3]
                    del gaps_group[random_gaps_group + 2]

            solution.merge_gaps_groups()

            if self.remove_full_of_gap_columns:
                solution.remove_full_of_gaps_columns()

            # Sanity check: alignment is valid (same length for all sequences)
            if not solution.is_valid_msa():
                raise Exception(
                    "Mutated solution is not valid! {0}".format(solution.decode_alignment_as_list_of_pairs()))

        return solution

    def get_name(self) -> str:
        return 'Two random adjacent gap group mutation'