from functools import partial
from typing import Dict

import rdflib
import stringcase
from rdflib import Graph, RDFS
from rdflib.namespace import XSD
from kapylan.annotation.ontology import ontology

TITAN = "http://www.ontologies.khaos.uma.es/titan-kaplan/"
BIGOWL = ontology(uri="http://www.ontologies.khaos.uma.es/bigowl/")
RDF = ontology(uri="http://www.w3.org/1999/02/22-rdf-syntax-ns#")


def merge_component(algorithm, predict: Dict[str, str], object: Dict[str, str]):
    """
    Custom decorator that adds extra annotation to an annotation already made with the annotated_component function.
    """
    v = (predict or dict()).copy()
    v.update(algorithm.args[1])
    d = (object or dict()).copy()
    d.update(algorithm.args[2])
    return partial(annotated_component, algorithm.args[0], v, d)


def annotated_component(uri, predict: Dict[str, str], object: Dict[str, str], **kwargs):
    """
    Custom decorator to set attributes to wrapped function.
    """

    def decorator(func):
        name = rdflib.URIRef(uri + "Component" + func.__name__)
        g = Graph()
        for k, v in object.items():
            if k not in kwargs.keys():
                g.add((name, predict[k], v))
                if "parameter" in v:
                    g += parameter(v)

        for k, v in kwargs.items():
            g.add((name, predict[k], v))

        name_implementation = rdflib.URIRef(TITAN + "Implementation" + func.__name__)
        g.add(
            (
                name_implementation,
                BIGOWL.namespace.module,
                rdflib.Literal(
                    "drama_kaplan.catalog.publisher.operator.Operator",
                    datatype=XSD.string,
                ),
            )
        )
        g.add(
            (name_implementation, RDF.namespace.type, BIGOWL.namespace.Implementation)
        )
        g.add(
            (
                name_implementation,
                BIGOWL.namespace.implementationLanguage,
                rdflib.Literal("Python", datatype=XSD.string),
            )
        )
        setattr(func, "__triples__", g)
        return func

    return decorator


def component(
    uri, predict: Dict[str, str] = None, object: Dict[str, str] = None, **kwargs
):
    return partial(annotated_component, uri, predict or dict(), object or dict())


def parameter(uri):
    """
    Generates the annotation of each parameter of a component.
    """
    g = Graph()
    if "number" in uri or "size" in uri:
        g.add((uri, BIGOWL.namespace.hasDataType, BIGOWL.namespace.Integer))
    elif "distribution" in uri or "probability" in uri:
        g.add((uri, BIGOWL.namespace.hasDataType, BIGOWL.namespace.Double))
    else:
        g.add((uri, BIGOWL.namespace.hasDataType, BIGOWL.namespace.String))
    name = str(uri).split("parameter_")[1]
    g.add((uri, BIGOWL.namespace.hasName, rdflib.Literal(name, datatype=XSD.string)))
    g.add(
        (
            uri,
            RDF.namespace.type,
            rdflib.URIRef(
                "http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#Parameter"
            ),
        )
    )
    g.add(
        (
            uri,
            RDFS.label,
            rdflib.Literal(stringcase.titlecase(name), datatype=XSD.string),
        )
    )
    return g
