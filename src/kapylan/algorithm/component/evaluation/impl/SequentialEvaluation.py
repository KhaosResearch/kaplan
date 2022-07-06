import rdflib
from rdflib import XSD

from kapylan.annotation.component_annotation import EvaluationComponent
from kapylan.annotation.ontology import ontology
from kapylan.core.problem import Problem
from kapylan.algorithm.component.evaluation.evaluation import Evaluation
from kapylan.util.evaluator import SequentialEvaluator

TITAN = ontology(uri="http://www.ontologies.khaos.uma.es/titan-kaplan/")

@EvaluationComponent(hasImplementation=TITAN.namespace.ImplementationSequentialEvaluation, label=rdflib.Literal('Sequential Evaluation', datatype=XSD.string))
class SequentialEvaluation(Evaluation):
    def __init__(self, problem: Problem):
        super(SequentialEvaluation, self).__init__()
        self.evaluator = SequentialEvaluator()
        self.problem = problem

    def evaluate(self, solution_list: list) -> list:
        return self.evaluator.evaluate(solution_list, self.problem)

    def get_problem(self) -> Problem:
        return self.problem

    def get_name(self):
        return 'Sequential evaluation'