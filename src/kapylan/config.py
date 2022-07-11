from pathlib import Path
from kapylan.algorithm.operator.mutation import PolynomialMutation, BitFlipMutation
from kapylan.util.comparator import DominanceComparator
from kapylan.algorithm.component.evaluation.impl.SequentialEvaluation import (
    SequentialEvaluation,
)
from kapylan.algorithm.component.termination.impl.StoppingByEvaluations import (
    StoppingByEvaluations,
)
from kapylan.util.generator import RandomGenerator
from kapylan.util.observable import DefaultObservable

from pydantic import BaseSettings


class _Store:
    @property
    def default_observable(self):
        return DefaultObservable()

    # @property
    # def default_evaluator(self):
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
            "real": PolynomialMutation(probability=0.15, distribution_index=20),
            "binary": BitFlipMutation(0.15),
        }


store = _Store()


class _Settings(BaseSettings):

    RDF_REPOSITORY_ENDPOINT = "<Removed by BFG>"
    RDF_REPOSITORY_USERNAME = "<Removed by BFG>in"
    RDF_REPOSITORY_PASSWORD = "<Removed by BFG>"
    RDF_REPOSITORY_DB = "<Removed by BFG>"

    class Config:
        env_file = "algorithm/.env"
        file_path = Path(env_file)
        if not file_path.is_file():
            print("⚠️ `.env` not found in current directory")
            print("⚙️ Loading settings from environment")
        else:
            print(f"⚙️ Loading settings from dotenv @ {file_path.absolute()}")


settings = _Settings()
