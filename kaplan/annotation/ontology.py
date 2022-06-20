import rdflib
from abc import abstractmethod
from collections import namedtuple
from rdflib import Namespace


class ontology:
    def __init__(
            self,
            uri: str,
    ):
        self.uri = rdflib.URIRef(uri)
        self.namespace = Namespace(uri)