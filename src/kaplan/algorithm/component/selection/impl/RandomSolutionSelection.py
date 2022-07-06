import random

import rdflib
from rdflib import XSD

from kaplan.annotation.ontology import ontology
from kaplan.algorithm.component.selection.selection import Selection
from kaplan.annotation.component_annotation import SelectionComponent

TITAN = ontology(uri="http://www.ontologies.khaos.uma.es/titan-kaplan/")

@SelectionComponent(hasImplementation=TITAN.namespace.ImplementationRandomSolutionSelection, label=rdflib.Literal('Random Solution Selection', datatype=XSD.string))
class RandomSolutionSelection(Selection):

    def __init__(self, mating_pool_size: int):
        super(RandomSolutionSelection, self).__init__()
        self.mating_pool_size = mating_pool_size

    def select(self, front: list):
        if front is None:
            raise Exception('The front is null')
        elif len(front) == 0:
            raise Exception('The front is empty')
        matingPool = []
        print(self.mating_pool_size)
        for i in range(self.mating_pool_size):
            matingPool.append(random.choice(front))
        return matingPool

    def get_name(self) -> str:
        return 'Random solution selection'