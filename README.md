# kapylan

<a href="https://github.com/KhaosResearch/kapylan"><img alt="Version: 0.5.5" src="https://img.shields.io/badge/version-1.0-success?color=0080FF&style=flat-square"></a> <a href="https://github.com/IreneSanx/kaplan"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square"></a>

*`kapylan` is a component-based evolutionary algorithm optimisation framework that includes a semantic annotation methodology.*

### 🚀 Setup

#### Installation

```
pip install kapylan
```

### ✨ Getting started

Take a look at the [component](https://github.com/IreneSanx/kaplan/tree/main/kaplan/algorithm/component) for more information on the components implemented for a multiobjective algorithm.

To run a multiobjective evolutionary algorithm, the 6 components needed by the algorithm must be instantiated and the `EvolutionaryAlgorithm` function must be called with those objects: 

```
from kapylan.algorithm.EvolutionaryAlgorithm import EvolutionaryAlgorithm
from kapylan.algorithm.component.evaluation.impl.SequentialEvaluation import SequentialEvaluation
from kapylan.algorithm.component.replacement.impl.RankingAndDensityEstimatorReplacement import RankingAndDensityEstimatorReplacement
from kapylan.algorithm.component.selection.impl.BinaryTournamentSelection import BinaryTournamentSelection
from kapylan.algorithm.component.solution_creation.impl.RandomSolutionCreation import RandomSolutionCreation
from kapylan.algorithm.component.termination.impl.StoppingByEvaluations import StoppingByEvaluations
from kapylan.algorithm.component.variation.impl.CrossoverAndMutationVariation import CrossoverAndMutationVariation
from kapylan.algorithm.component.replacement.replacement import RemovalPolicyType
from kapylan.algorithm.operator.mutation.PolynomialMutation import PolynomialMutation
from kapylan.algorithm.operator.crossover.SBXCrossover import SBXCrossover
from kapylan.util.ranking import FastNonDominatedRanking
from kapylan.util.density_estimator import CrowdingDistance
from kapylan.util.generator import RandomGenerator
from kapylan.util.comparator import DominanceComparator
from kapylan.util.solution import read_solutions
from kapylan.problem.zdt import ZDT1

problem = ZDT1()
problem.reference_front = read_solutions(filename="resources/reference_front/ZDT1.pf")

max_evaluations = 25000
population_size = 100
offspring_population_size = 100

mutation = PolynomialMutation(probability = 1/problem.number_of_variables, distribution_index = 20)
crossover = SBXCrossover(probability = 0.9, distribution_index = 20)
variation = CrossoverAndMutationVariation(mutation, crossover, offspring_population_size)
solution_creation = RandomSolutionCreation(problem, population_size, RandomGenerator())
termination = StoppingByEvaluations(max_evaluations = max_evaluations)
replacement_policy = RankingAndDensityEstimatorReplacement(FastNonDominatedRanking(DominanceComparator()), CrowdingDistance(), RemovalPolicyType.ONE_SHOT)
selection = BinaryTournamentSelection(variation.get_mating_pool_size(), DominanceComparator())
population_evaluation = SequentialEvaluation(problem)

algorithm = EvolutionaryAlgorithm(
    name="NSGA-II",
    solution_creation=solution_creation,
    selection=selection,
    variation=variation,
    replacement_policy=replacement_policy,
    termination=termination,
    population_evaluation=population_evaluation
)

algorithm.run()

front = algorithm.get_result()

# Save results to file
print_function_values_to_file(front, "FUN.csv")
print_variables_to_file(front, "VAR.csv")

print(f"Algorithm: {algorithm.get_name()}")
print(f"Problem: {problem.get_name()}")
print(f"Computing time: {algorithm.total_computing_time}")
```

*(This script is complete, it should run "as is")*

When using `print_function_values_to_file()` and `print_variables_to_file()` functions, two files are generated, *FUN.csv* where the function values are included and *VAR.csv* which contains the variables.

If we want to access the semantic annotation, we can make use of the `get_annotation()`, `store_annotation_file()` and `virtuoso_upload()` functions. The `get_annotation()` function collects all the semantic information of the running algorithm into a single graph. The `store_annotation_file()` function calls the first function and stores the information in a n-triplets file. Finally, function `virtuoso_upload()` also calls first function and uploads the annotated information to a Virtuoso repository.

In order to use the third function, `virtuoso_upload()`, it is necessary to insert your own values for Virtuoso. They can be written directly into the function or a virtual environment can be created beforehand, save a copy of [`.env.template`](.env.template) as `.env` and insert the values there.

```
from kapylan.util.solution import print_function_values_to_file, print_variables_to_file

algorithm.store_annotation_file("../../../annotation_files")
algorithm.virtuoso_upload()
```