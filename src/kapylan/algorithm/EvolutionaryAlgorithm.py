from abc import ABC
import time
from pathlib import Path

from rdflib import Graph

from kapylan.algorithm.component.replacement.replacement import Replacement
from kapylan.algorithm.component.variation.variation import Variation
from kapylan.algorithm.component.evaluation.evaluation import Evaluation
from kapylan.algorithm.component.selection.selection import Selection
from kapylan.algorithm.component.solution_creation.solution_creation import SolutionCreation
from kapylan.algorithm.component.termination.termination import Termination
from kapylan.algorithm.algorithm import Algorithm
from kapylan.annotation.component_annotation import EvolutionaryAlgorithmComponent
from kapylan.annotation.repository import Virtuoso
from kapylan.config import store, settings


#@EvolutionaryAlgorithmComponent()
class EvolutionaryAlgorithm(Algorithm, ABC):

    def __init__(self,
                name: str,
                solution_creation: SolutionCreation,
                selection: Selection,
                variation: Variation,
                replacement_policy: Replacement,
                population_evaluation: Evaluation,
                termination: Termination = store.default_termination_criteria):
                
        super(EvolutionaryAlgorithm, self).__init__()

        self.name = name
        self.solution_creation = solution_creation
        self.variation = variation
        self.selection = selection
        self.termination = termination
        self.population_evaluation = population_evaluation
        self.replacement_policy = replacement_policy

    def run(self):
        """ Execute the algorithm. """
        self.start_computing_time = time.time()

        self.solutions = self.solution_creation.create()
        self.solutions = self.population_evaluation.evaluate(self.solutions)

        self.init_progress()

        while not self.termination.is_met:
            mating_population = self.selection.select(self.solutions)
            offspring_population = self.variation.variate(mating_population)
            offspring_population = self.population_evaluation.evaluate(offspring_population)

            self.solutions = self.replacement_policy.replace(self.solutions, offspring_population)
            self.update_progress()

        self.total_computing_time = time.time() - self.start_computing_time


    def get_observable_data(self) -> dict:
        return {'EVALUATIONS': self.evaluations,
                'SOLUTIONS': self.get_result(),
                'COMPUTING_TIME': time.time() - self.start_computing_time}

    def init_progress(self) -> None:
        self.evaluations = len(self.solutions)

    def update_progress(self) -> None:
        self.evaluations += self.variation.offspring_population_size
        self.termination.update(self.evaluations)

    def get_result(self):
        return self.solutions

    def get_name(self):
        return self.name

    def get_annotation(self) -> Graph:
        g = Graph()
        g_selection = self.selection.__triples__
        g_evaluation = self.population_evaluation.__triples__
        g_variation = self.variation.__triples__
        g_termination = self.termination.__triples__
        g_replacement = self.replacement_policy.__triples__
        g_solution_creation = self.solution_creation.__triples__

        g += g_selection + g_evaluation + g_termination + g_variation + g_replacement + g_solution_creation
        return g

    def store_annotation_file(self, path: str):
        graph = self.get_annotation()
        store_path = Path(path, self.get_name() + ".nt")
        graph.serialize(format='nt', encoding="utf-8", destination=store_path)

    def virtuoso_upload(self):
        try:
            graph = self.get_annotation()
            workflow_nt = graph.serialize(format='nt', encoding="utf-8")
            triples = str(workflow_nt.decode("UTF-8"))
            RDF_REPOSITORY_ENDPOINT = settings.RDF_REPOSITORY_ENDPOINT
            RDF_REPOSITORY_USERNAME = settings.RDF_REPOSITORY_USERNAME
            RDF_REPOSITORY_PASSWORD = settings.RDF_REPOSITORY_PASSWORD
            RDF_REPOSITORY_DB = settings.RDF_REPOSITORY_DB
            store = Virtuoso(endpoint=RDF_REPOSITORY_ENDPOINT, database=RDF_REPOSITORY_DB, username=RDF_REPOSITORY_USERNAME, password=RDF_REPOSITORY_PASSWORD)
            query = "INSERT DATA { GRAPH <" + store.database + "> {" + triples + "} }"

            return store.update(query)

        except Exception as err:
            print(f"Could not store workflow's RDF: {err.args[0]}")

    @property
    def label(self) -> str:
        return f"{self.get_name()}.{self.population_evaluation.get_problem().get_name()}"