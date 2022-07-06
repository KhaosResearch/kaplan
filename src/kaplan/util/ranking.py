from abc import ABC, abstractmethod

from kaplan.annotation.component_annotation import RankingComponent
from kaplan.annotation.decorator import merge_component
from kaplan.annotation.ontology import ontology
from kaplan.util.comparator import DominanceComparator, Comparator, SolutionAttributeComparator
import rdflib
from rdflib import XSD, RDFS

BIGOWL = ontology(uri="http://www.ontologies.khaos.uma.es/bigowl/")
TITAN = ontology(uri="http://www.ontologies.khaos.uma.es/titan-kaplan/")

FastNonDominatedSortRankingComponent = merge_component(RankingComponent, {"hasParameterComparator": BIGOWL.namespace.hasParameter},
                              {"hasParameterComparator": TITAN.namespace.parameter_comparator_name})

class Ranking(ABC):

    def __init__(self, comparator: Comparator = DominanceComparator()):
        super(Ranking, self).__init__()
        self.number_of_comparisons = 0
        self.ranked_sublists = []
        self.comparator = comparator

    @abstractmethod
    def compute_ranking(self, solutions: list, k: int = None):
        pass

    def get_nondominated(self):
        return self.ranked_sublists[0]

    def get_subfront(self, rank: int):
        if rank >= len(self.ranked_sublists):
            raise Exception('Invalid rank: {0}. Max rank: {1}'.format(rank, len(self.ranked_sublists) - 1))
        return self.ranked_sublists[rank]

    def get_number_of_subfronts(self):
        return len(self.ranked_sublists)

    @classmethod
    def get_comparator(cls) -> Comparator:
        pass


@FastNonDominatedSortRankingComponent(hasImplementation=TITAN.namespace.ImplementationFastNonDominatedRanking, label=rdflib.Literal('Fast Non Dominated Sort Ranking', datatype=XSD.string))
class FastNonDominatedRanking(Ranking):
    """ Class implementing the non-dominated ranking of NSGA-II proposed by Deb et al., see [Deb2002]_ """

    def __init__(self, comparator: Comparator = DominanceComparator()):
        super(FastNonDominatedRanking, self).__init__(comparator)

    def compute_ranking(self, solutions: list, k: int = None):
        """ Compute ranking of solutions.

        :param solutions: Solution list.
        :param k: Number of individuals.
        """
        # number of solutions dominating solution ith
        dominating_ith = [0 for _ in range(len(solutions))]

        # list of solutions dominated by solution ith
        ith_dominated = [[] for _ in range(len(solutions))]

        # front[i] contains the list of solutions belonging to front i
        front = [[] for _ in range(len(solutions) + 1)]

        for p in range(len(solutions) - 1):
            for q in range(p + 1, len(solutions)):
                dominance_test_result = self.comparator.compare(solutions[p], solutions[q])
                self.number_of_comparisons += 1

                if dominance_test_result == -1:
                    ith_dominated[p].append(q)
                    dominating_ith[q] += 1
                elif dominance_test_result == 1:
                    ith_dominated[q].append(p)
                    dominating_ith[p] += 1

        for i in range(len(solutions)):
            if dominating_ith[i] == 0:
                front[0].append(i)
                solutions[i].attributes['dominance_ranking'] = 0

        i = 0
        while len(front[i]) != 0:
            i += 1
            for p in front[i - 1]:
                if p <= len(ith_dominated):
                    for q in ith_dominated[p]:
                        dominating_ith[q] -= 1
                        if dominating_ith[q] == 0:
                            front[i].append(q)
                            solutions[q].attributes['dominance_ranking'] = i

        self.ranked_sublists = [[]] * i
        for j in range(i):
            q = [0] * len(front[j])
            for m in range(len(front[j])):
                q[m] = solutions[front[j][m]]
            self.ranked_sublists[j] = q

        if k:
            count = 0
            for i, front in enumerate(self.ranked_sublists):
                count += len(front)
                if count >= k:
                    self.ranked_sublists = self.ranked_sublists[:i + 1]
                    break

        return self.ranked_sublists

    @classmethod
    def get_comparator(cls) -> Comparator:
        return SolutionAttributeComparator('dominance_ranking')

    def get_name(self) -> str:
        return 'Fast non dominated ranking'
