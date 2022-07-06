from typing import Optional

import pandas
import typer as typer

from kapylan.algorithm.EvolutionaryAlgorithm import EvolutionaryAlgorithm
from kapylan.algorithm.component.evaluation.impl.SequentialEvaluation import SequentialEvaluation
from kapylan.algorithm.component.replacement.impl.RankingAndDensityEstimatorReplacement import RankingAndDensityEstimatorReplacement
from kapylan.algorithm.component.replacement.replacement import RemovalPolicyType
from kapylan.algorithm.component.selection.impl.BinaryTournamentSelection import BinaryTournamentSelection
from kapylan.algorithm.component.selection.impl.RandomSolutionSelection import RandomSolutionSelection
from kapylan.algorithm.component.solution_creation.impl.RandomSolutionCreation import RandomSolutionCreation
from kapylan.algorithm.component.variation.impl.CrossoverAndMutationVariation import CrossoverAndMutationVariation
from kapylan.core.solution import FloatSolution
from kapylan.util.plotting import Plot
from kapylan.algorithm.operator.mutation.BitFlipMutation import BitFlipMutation
from kapylan.algorithm.operator.mutation.PolynomialMutation import PolynomialMutation
from kapylan.algorithm.operator.crossover.SBXCrossover import SBXCrossover
from kapylan.config import store
from kapylan.annotation.ontology import ontology
from kapylan.problem.zdt import ZDT1
from kapylan.util.comparator import DominanceComparator
from kapylan.util.density_estimator import CrowdingDistance
from kapylan.util.ranking import FastNonDominatedRanking
from kapylan.util.solution import read_solutions, get_non_dominated_solutions, print_function_values_to_file, \
    print_variables_to_file
from kapylan.algorithm.component.termination.impl.StoppingByEvaluations import StoppingByEvaluations

BIGOWL = ontology(uri="http://www.khaos.uma.es/perception/bigowl/")
Kaplan = ontology(uri="http://www.khaos.uma.es/kaplan/")

"""  
Program to configure and run a steady-state version of the NSGA-II algorithm (configured with standard settings).
"""

def nsgaii_parameters(
    problem_name: str = typer.Option(..., help="Type of selection"),
    reference_front_file_name: str = typer.Option(..., help="Type of selection"),
    algorithm_result: str = typer.Option(..., help="Type of selection"),
    selection_type: str = typer.Option(..., help="Type of selection"),
    variation_type: str = typer.Option(..., help="Type of variation"),
    replacement_type: str = typer.Option(..., help="Type of replacement"),
    evaluation_type: str = typer.Option(..., help="Type of evaluation"),
    solution_creator_type: str = typer.Option(..., help="Type of solution creator"),
    termination_type: str = typer.Option(..., help="Type of termination"),
    ranking_name: str = typer.Option("Fast non dominated ranking", help="Name of ranking"),
    density_estimator_name: str = typer.Option("Crowding distance", help="Name of density estimator"),
    comparator_ranking: str = typer.Option("Dominance comparator", help="Name of the comparator for the ranking"),
    removal_policy: str = typer.Option("One shot", help="Removal Policy"),
    comparator_selection: str = typer.Option("Dominance comparator", help="Name of the comparator for the selection"),
    tournament_size: Optional[int] = typer.Option(None, help="Tournament size"),
    mating_pool_size: Optional[int] = typer.Option(None, help="Mating pool size"),
    max_evaluations: int = typer.Option(..., help="Max number of evaluations"),
    population_size: int = typer.Option(..., help="Population size"),
    offspring_population_size: int = typer.Option(..., help="Offspring population size"),
    mutation_name: str = typer.Option(..., help="Name of mutation"),
    crossover_name: str = typer.Option(..., help="Name of crossover"),
    probability_mutation: float = typer.Option(..., help="Probability mutation"),
    probability_crossover: float = typer.Option(..., help="Probability crossover"),
    distribution_index_mutation: float = typer.Option(..., help="Distribution index mutation"),
    distribution_index_crossover: float = typer.Option(..., help="Distribution index crossover")
):

    problem = ZDT1()
    problem.reference_front = read_solutions(filename="resources/reference_front/ZDT1.pf")

    max_evaluations = int(max_evaluations)
    population_size = int(population_size)
    offspring_population_size = int(offspring_population_size)

    mutation = ""
    crossover = ""

    if mutation_name in "PolynomialMutation":
        mutation = PolynomialMutation(probability=float(probability_mutation) / problem.number_of_variables,
                                  distribution_index=float(distribution_index_mutation))
    elif mutation_name in "BitFlipMutation":
        mutation = BitFlipMutation(probability=float(probability_mutation) / problem.number_of_variables)

    if crossover_name in "SBXCrossover":
        crossover = SBXCrossover(probability=float(probability_crossover),
                                 distribution_index=float(distribution_index_crossover))

    if variation_type in "CrossoverAndMutationVariation":
        variation = CrossoverAndMutationVariation(mutation, crossover, offspring_population_size)

    if solution_creator_type in "RandomSolutionCreation":
        solution_creation = RandomSolutionCreation(problem, population_size, store.default_generator)

    if termination_type in "StoppingByEvaluations":
        termination = StoppingByEvaluations(max_evaluations=max_evaluations)

    if removal_policy == "OneShot":
        removal_policy_type = RemovalPolicyType.ONE_SHOT
    elif removal_policy == "Sequential":
        removal_policy_type = RemovalPolicyType.SEQUENTIAL

    if comparator_ranking in "DominanceComparator":
        comparator_ranking_type = DominanceComparator()

    if ranking_name in "FastNonDominatedSortRanking":
        ranking_type = FastNonDominatedRanking(comparator_ranking_type)

    if density_estimator_name in "CrowdingDistance":
        density_type = CrowdingDistance()

    if replacement_type in "RankingAndDensityEstimatorReplacement":
        replacement_policy = RankingAndDensityEstimatorReplacement(ranking_type, density_type, removal_policy_type)

    if comparator_selection in "DominanceComparator":
        comparator_selection_type = DominanceComparator()

    if selection_type in "BinaryTournamentSelection":
        if mating_pool_size != None:
            selection = BinaryTournamentSelection(mating_pool_size, comparator_selection_type)
        else:
            selection = BinaryTournamentSelection(variation.get_mating_pool_size(), comparator_selection_type)
    elif selection_type in "RandomSolutionSelection":
        if mating_pool_size != None:
            selection = RandomSolutionSelection(mating_pool_size)
        else:
            selection = RandomSolutionSelection(variation.get_mating_pool_size())

    if evaluation_type in "SequentialEvaluation":
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
    print("NSGA-II")
    #print(algorithm.get_observable_data())
    #algorithm.store_annotation_file("../../../annotation_files")
    #print(algorithm.virtuoso_upload())
    #print(algorithm.termination.__triples__.serialize(format='nt', encoding="utf-8", destination="../../../annotation_files/prueba.nt"))
    front = algorithm.get_result()
    sol = front[1]
    print(sol.__dict__)
    print(front[0])

    # Save results to file
    print_function_values_to_file(front, "FUN.csv")
    print_variables_to_file(front, "VAR.csv")
    #print_variables_to_screen(front)

    # Plot front
    data = pandas.read_csv("FUN2.csv", sep=",", header=None)

    list_objectives = []
    for index, row in data.iterrows():
        obj = [row[0], row[1]]
        list_objectives.append(obj)

    solutions = []
    for element in list_objectives:
        solution = FloatSolution(lower_bound=[], upper_bound=[], number_of_objectives=2, number_of_constraints=0)
        solution.number_of_variables = 30
        solution.objectives = element
        solutions.append(solution)

    plot_front = Plot(
        title="Pareto front approximation. Problem: " + problem.get_name(),
        reference_front=problem.reference_front,
        axis_labels=problem.obj_labels,
    )

    plot_front.plot(solutions, label=algorithm.label, filename=algorithm.get_name())

    print(f"Algorithm: {algorithm.get_name()}")
    print(f"Problem: {problem.get_name()}")
    print(f"Computing time: {algorithm.total_computing_time}")

if __name__ == "__main__":
    typer.run(nsgaii_parameters)

