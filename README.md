# kaplan

<a href="https://github.com/IreneSanx/kaplan"><img alt="Version: 0.5.5" src="https://img.shields.io/badge/version-1.0-success?color=0080FF&style=flat-square"></a> <a href="https://github.com/IreneSanx/kaplan"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square"></a>

*`kaplan` is a component-based evolutionary algorithm optimisation framework that includes a semantic annotation methodology.*

### 🚀 Setup

#### Installation

Before proceeding with the installation of the package, a virtual environment must be created. To create a virtual environment, go to your project’s directory and run `venv`.

```
python3 -m venv env
```

Once the environment has been created, you need to activate it in order to install the packages you want to use there.

```
source env/bin/activate
```

Now that you’re in your virtual environment you can install packages.

As `kaplan` is a package that is only available in the internal Khaos repository, it is necessary to configure a `~/.pip/pip.conf` file. This is done adding the following lines: 

```
[global]
trusted-host = 192.168.219.5
extra-index-url = http://<Removed by BFG>:<Removed by BFG>@192.168.219.5:8099/simple/
```

Once we have configured the file, we can install the package with `pip`: 

```
pip install kaplan --upgrade
```


### ✨ Getting started

Take a look at the [component](https://github.com/IreneSanx/kaplan/tree/main/kaplan/algorithm/component) for more information on the components implemented for a multiobjective algorithm.

To run a multiobjective evolutionary algorithm, the 6 components needed by the algorithm must be instantiated and the `EvolutionaryAlgorithm` function must be called with those objects: 

```
from kaplan.algorithm.EvolutionaryAlgorithm import EvolutionaryAlgorithm
from kaplan.algorithm.component.evaluation.impl.SequentialEvaluation import SequentialEvaluation
from kaplan.algorithm.component.replacement.impl.RankingAndDensityEstimatorReplacement import RankingAndDensityEstimatorReplacement
from kaplan.algorithm.component.selection.impl.BinaryTournamentSelection import BinaryTournamentSelection
from kaplan.algorithm.component.solution_creation.impl.RandomSolutionCreation import RandomSolutionCreation
from kaplan.algorithm.component.termination.impl.StoppingByEvaluations import StoppingByEvaluations
from kaplan.algorithm.component.variation.impl.CrossoverAndMutationVariation import CrossoverAndMutationVariation
from kaplan.algorithm.component.replacement.replacement import RemovalPolicyType
from kaplan.algorithm.operator.mutation.PolynomialMutation import PolynomialMutation
from kaplan.algorithm.operator.crossover.SBXCrossover import SBXCrossover
from kaplan.util.ranking import FastNonDominatedRanking
from kaplan.util.density_estimator import CrowdingDistance
from kaplan.util.generator import RandomGenerator
from kaplan.util.comparator import DominanceComparator
from kaplan.util.solution import read_solutions
from kaplan.problem.zdt import ZDT1

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

In order to use the third function, `virtuoso_upload()`, save a copy of [`.env.template`](.env.template) as `.env` and insert your own values to Virtuoso.

```
from kaplan.util.solution import print_function_values_to_file, print_variables_to_file

algorithm.store_annotation_file("../../../annotation_files")
algorithm.virtuoso_upload()
```