import random

import rdflib
from rdflib import XSD

from kaplan.annotation.decorator import merge_component
from kaplan.annotation.ontology import ontology
from kaplan.algorithm.component.selection.selection import Selection
from kaplan.util.comparator import Comparator, DominanceComparator
from kaplan.annotation.component_annotation import SelectionComponent

BIGOWL = ontology(uri="http://www.ontologies.khaos.uma.es/bigowl/")
TITAN = ontology(uri="http://www.ontologies.khaos.uma.es/titan-kaplan/")

BinaryTournamentSelectionComponent = merge_component(SelectionComponent, {"hasParameterComparator": BIGOWL.namespace.hasParameter},
                                                    {"hasParameterComparator": TITAN.namespace.parameter_comparator_name})

@BinaryTournamentSelectionComponent(hasImplementation=TITAN.namespace.ImplementationBinaryTournamentSelection, label=rdflib.Literal('Binary Tournament Selection', datatype=XSD.string))
class BinaryTournamentSelection(Selection):

    def __init__(self, mating_pool_size: int, comparator: Comparator = DominanceComparator()):
        super(BinaryTournamentSelection, self).__init__()
        self.comparator = comparator
        self.tournamentSize = 2
        self.mating_pool_size = mating_pool_size

    def get_comparator(self) -> Comparator:
        return self.comparator

    def select(self, front: list):
        matingPool = []

        if front is None:
            raise Exception('The front is null')
        elif len(front) == 0:
            raise Exception('The front is empty')

        if len(front) == 1:
            matingPool.append(front[0])

        else:
            for i in range(self.mating_pool_size):
                # Sampling without replacement

                i, j = random.sample(range(0, len(front)), self.tournamentSize)
                solution1 = front[i]
                solution2 = front[j]

                flag = self.comparator.compare(solution1, solution2)

                if flag == -1:
                    result = solution1
                elif flag == 1:
                    result = solution2
                else:
                    result = [solution1, solution2][random.random() < 0.5]

                matingPool.append(result)

        return matingPool

    def get_name(self) -> str:
        return 'Binary tournament selection'