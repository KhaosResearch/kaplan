import rdflib
from rdflib import XSD

from kaplan.annotation.component_annotation import SolutionCreationComponent
from kaplan.annotation.ontology import ontology
from kaplan.core.problem import Problem
from kaplan.util.generator import Generator
from kaplan.config import store

TITAN = ontology(uri="http://www.ontologies.khaos.uma.es/titan-kaplan/")

@SolutionCreationComponent(hasImplementation=TITAN.namespace.ImplementationRandomSolutionCreation, label=rdflib.Literal('Random Solution Creation', datatype=XSD.string))
class RandomSolutionCreation():
    def __init__(self,
                 problem: Problem,
                 population_size: int,
                 population_generator: Generator = store.default_generator):
        
        self.problem = problem
        self.population_size = population_size
        self.population_generator = population_generator

    def create(self) -> list:
        return [self.population_generator.new(self.problem) for _ in range(self.population_size)]

    def get_name(self) -> str:
        return 'Random solution creation'