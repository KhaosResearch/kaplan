import rdflib
from rdflib import XSD

from kapylan.annotation.component_annotation import TerminationComponent
from kapylan.annotation.decorator import merge_component
from kapylan.annotation.ontology import ontology
from kapylan.util.termination_criterion import TerminationCriterion

BIGOWL = ontology(uri="http://www.ontologies.khaos.uma.es/bigowl/")
TITAN = ontology(uri="http://www.ontologies.khaos.uma.es/titan-kaplan/")

TerminationByEvaluationsComponent = merge_component(
    TerminationComponent,
    {"hasParameterNumber": BIGOWL.namespace.hasParameter},
    {"hasParameterNumber": TITAN.namespace.parameter_max_number_of_evaluations},
)


@TerminationByEvaluationsComponent(
    hasImplementation=TITAN.namespace.ImplementationStoppingByEvaluations,
    label=rdflib.Literal("Stopping By Evaluations", datatype=XSD.string),
)
class StoppingByEvaluations(TerminationCriterion):
    def __init__(self, max_evaluations: int):
        super(StoppingByEvaluations, self).__init__()
        self.max_evaluations = max_evaluations
        self.evaluations = 0

    def update(self, iteration: int):
        self.evaluations = iteration

    def get_name(self):
        return "Stopping by evaluations"

    @property
    def is_met(self):
        return self.evaluations >= self.max_evaluations
