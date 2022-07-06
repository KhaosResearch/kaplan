from pathlib import Path
import platform
import tempfile
from kaplan.algorithm.operator.mutation import PolynomialMutation, BitFlipMutation
from kaplan.util.comparator import DominanceComparator
from kaplan.algorithm.component.evaluation.impl.SequentialEvaluation import SequentialEvaluation
from kaplan.algorithm.component.termination.impl.StoppingByEvaluations import StoppingByEvaluations
from kaplan.util.generator import RandomGenerator
from kaplan.util.observable import DefaultObservable

from pydantic import BaseSettings

class _Store:

    @property
    def default_observable(self):
        return DefaultObservable()

    #@property
    #def default_evaluator(self):
    #    return SequentialEvaluation()

    @property
    def default_generator(self):
        return RandomGenerator()

    @property
    def default_termination_criteria(self):
        return StoppingByEvaluations(max_evaluations=25000)

    @property
    def default_comparator(self):
        return DominanceComparator()

    @property
    def default_mutation(self):
        return {
            'real': PolynomialMutation(probability=0.15, distribution_index=20),
            'binary': BitFlipMutation(0.15)
        }


store = _Store()


class _Settings(BaseSettings):
    
    #RDF_REPOSITORY_ENDPOINT = "http://0.0.0.0:8090/sparql"
    #RDF_REPOSITORY_USERNAME = "dba"
    #RDF_REPOSITORY_PASSWORD = "myDbaPassword"
    #RDF_REPOSITORY_DB = "KaplanPrueba"

    RDF_REPOSITORY_ENDPOINT = "https://opendata.khaos.uma.es/sparql"
    RDF_REPOSITORY_USERNAME = "dbain"
    RDF_REPOSITORY_PASSWORD = "khaosdev"
    RDF_REPOSITORY_DB = "KaplanPy"

    class Config:
        env_file = "algorithm/.env"
        file_path = Path(env_file)
        if not file_path.is_file():
            print("⚠️ `.env` not found in current directory")
            print("⚙️ Loading settings from environment")
        else:
            print(f"⚙️ Loading settings from dotenv @ {file_path.absolute()}")

settings = _Settings()