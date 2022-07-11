from kapylan.algorithm.EvolutionaryAlgorithm import EvolutionaryAlgorithm
from kapylan.algorithm.component.evaluation.impl.SequentialEvaluation import (
    SequentialEvaluation,
)
from kapylan.algorithm.component.replacement.impl.RankingAndDensityEstimatorReplacement import (
    RankingAndDensityEstimatorReplacement,
)
from kapylan.algorithm.component.selection.impl.BinaryTournamentSelection import (
    BinaryTournamentSelection,
)
from kapylan.algorithm.component.solution_creation.impl.RandomSolutionCreation import (
    RandomSolutionCreation,
)
from kapylan.algorithm.component.termination.impl.StoppingByEvaluations import (
    StoppingByEvaluations,
)
from kapylan.algorithm.component.variation.impl.CrossoverAndMutationVariation import (
    CrossoverAndMutationVariation,
)
from kapylan.algorithm.component.replacement.replacement import RemovalPolicyType
from kapylan.algorithm.operator.mutation.PolynomialMutation import PolynomialMutation
from kapylan.algorithm.operator.crossover.SBXCrossover import SBXCrossover
from kapylan.util.ranking import FastNonDominatedRanking
from kapylan.util.density_estimator import CrowdingDistance
from kapylan.util.generator import RandomGenerator
from kapylan.util.comparator import DominanceComparator
from kapylan.util.solution import (
    read_solutions,
    print_function_values_to_file,
    print_variables_to_file,
)
from kapylan.problem.zdt import ZDT1

problem = ZDT1()
problem.reference_front = read_solutions(filename="resources/reference_front/ZDT1.pf")

max_evaluations = 25000
population_size = 100
offspring_population_size = 100

mutation = PolynomialMutation(
    probability=1 / problem.number_of_variables, distribution_index=20
)
crossover = SBXCrossover(probability=0.9, distribution_index=20)
variation = CrossoverAndMutationVariation(
    mutation, crossover, offspring_population_size
)
solution_creation = RandomSolutionCreation(problem, population_size, RandomGenerator())
termination = StoppingByEvaluations(max_evaluations=max_evaluations)
replacement_policy = RankingAndDensityEstimatorReplacement(
    FastNonDominatedRanking(DominanceComparator()),
    CrowdingDistance(),
    RemovalPolicyType.ONE_SHOT,
)
selection = BinaryTournamentSelection(
    variation.get_mating_pool_size(), DominanceComparator()
)
population_evaluation = SequentialEvaluation(problem)

algorithm = EvolutionaryAlgorithm(
    name="NSGA-II",
    solution_creation=solution_creation,
    selection=selection,
    variation=variation,
    replacement_policy=replacement_policy,
    termination=termination,
    population_evaluation=population_evaluation,
)

algorithm.run()

front = algorithm.get_result()

# Save results to file
print_function_values_to_file(front, "FUN.csv")
print_variables_to_file(front, "VAR.csv")

print(f"Algorithm: {algorithm.get_name()}")
print(f"Problem: {problem.get_name()}")
print(f"Computing time: {algorithm.total_computing_time}")
