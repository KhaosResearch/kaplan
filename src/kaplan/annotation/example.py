import rdflib
from kaplan.annotation.decorator import component
from kaplan.annotation.ontology import ontology

BIGOWL = ontology(uri="http://www.khaos.uma.es/perception/bigowl#")
Kaplan = ontology(uri="http://www.khaos.uma.es/kaplan#")

Algorithm = component(Kaplan.uri, {"output": BIGOWL.namespace.output, "type": rdflib.URIRef("rdf:type")},
                                  {"output": Kaplan.namespace.Population, "type": BIGOWL.namespace.EvolutionaryAlgorithm})

#AlgorithmComponent = Algorithm({"comparator": BIGOWL.namespace.comparator}, {"comparator": Kaplan.namespace.Comparator})


#@RandomSelectionOperator()
def nsgaii():
    pass

#@RandomOperator()
#def prueba(nsgaii):
#    pass

if __name__ == "__main__":
    g = nsgaii.__triples__
    # raw triples
    for s, p, o in g:
        print((s, p, o))
    # n-triples
    print(g.serialize(format='n3'))