import unittest
from kapylan.algorithm.EvolutionaryAlgorithm import EvolutionaryAlgorithm
from kapylan.algorithm.component.evaluation.impl.SequentialEvaluation import SequentialEvaluation
from kapylan.algorithm.component.replacement.impl.RankingAndDensityEstimatorReplacement import RankingAndDensityEstimatorReplacement
from kapylan.algorithm.component.replacement.replacement import RemovalPolicyType
from kapylan.algorithm.component.selection.impl.BinaryTournamentSelection import BinaryTournamentSelection
from kapylan.algorithm.component.solution_creation.impl.RandomSolutionCreation import RandomSolutionCreation
from kapylan.algorithm.component.termination.impl.StoppingByEvaluations import StoppingByEvaluations
from kapylan.algorithm.component.variation.impl.CrossoverAndMutationVariation import CrossoverAndMutationVariation
from kapylan.algorithm.operator.crossover.SBXCrossover import SBXCrossover
from kapylan.algorithm.operator.mutation.PolynomialMutation import PolynomialMutation
from kapylan.core.quality_indicator import HyperVolume

from kapylan.problem.zdt import ZDT1
from kapylan.util.comparator import DominanceComparator
from kapylan.util.density_estimator import CrowdingDistance
from kapylan.util.generator import RandomGenerator
from kapylan.util.ranking import FastNonDominatedRanking


class RunningAlgorithmTestCase(unittest.TestCase):
    def setUp(self):
        self.problem = ZDT1()
        self.population_size = 100
        self.offspring_size = 100
        self.max_evaluations = 25000
        self.mutation = PolynomialMutation(probability=1.0 / self.problem.number_of_variables, distribution_index=20)
        self.crossover = SBXCrossover(probability=1.0, distribution_index=20)
        self.variation = CrossoverAndMutationVariation(self.mutation, self.crossover, self.offspring_size)
        self.solution_creation = RandomSolutionCreation(self.problem, self.population_size, RandomGenerator())
        self.termination = StoppingByEvaluations(max_evaluations = self.max_evaluations)
        self.replacement_policy = RankingAndDensityEstimatorReplacement(FastNonDominatedRanking(DominanceComparator()), CrowdingDistance(), RemovalPolicyType.ONE_SHOT)
        self.selection = BinaryTournamentSelection(self.variation.get_mating_pool_size(), DominanceComparator())
        self.population_evaluation = SequentialEvaluation(self.problem)
    
    def test_EvolutionaryAlgorithm(self):
        EvolutionaryAlgorithm(
            name="NSGA-II",
            solution_creation=self.solution_creation,
            selection=self.selection,
            variation=self.variation,
            replacement_policy=self.replacement_policy,
            termination=self.termination,
            population_evaluation=self.population_evaluation,
        ).run()

class IntegrationTestCases(unittest.TestCase):
    def test_should_NSGAII_Evolutionary_Algorithm_work_when_solving_problem_ZDT1_with_standard_settings(self):
        problem = ZDT1()
        max_evaluations = 25000
        population_size = 100
        offspring_size = 100
        mutation = PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20)
        crossover = SBXCrossover(probability=1.0, distribution_index=20)
        variation = CrossoverAndMutationVariation(mutation, crossover, offspring_size)

        algorithm = EvolutionaryAlgorithm(
            name="NSGA-II",
            solution_creation=RandomSolutionCreation(problem, population_size, RandomGenerator()),
            variation=variation,
            selection=BinaryTournamentSelection(variation.get_mating_pool_size(), DominanceComparator()),
            replacement_policy=RankingAndDensityEstimatorReplacement(FastNonDominatedRanking(DominanceComparator()), CrowdingDistance(), RemovalPolicyType.ONE_SHOT),
            termination=StoppingByEvaluations(max_evaluations = max_evaluations),
            population_evaluation=SequentialEvaluation(problem),
        )

        algorithm.run()
        front = algorithm.get_result()

        hv = HyperVolume(reference_point=[1, 1])
        value = hv.compute([front[i].objectives for i in range(len(front))])

        self.assertTrue(value >= 0.65)

if __name__ == "__main__":
    unittest.main()
