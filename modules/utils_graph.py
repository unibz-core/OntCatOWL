""" Auxiliary functions for extending and complementing RDFLib's graph functions """
from rdflib import RDF, OWL, RDFS, URIRef

from modules.utils_general import remove_duplicates, lists_subtraction


def get_list_all_classes(graph):
    """ Returns a list without repetitions with the URI of all classes in a graph. """

    list_classes = []

    for subj, pred, obj in graph.triples((None, RDF.type, OWL.Class)):
        # N3 necessary for returning string and [1:-1] necessary for removing <>
        list_classes.append(subj.n3()[1:-1])

    list_classes = remove_duplicates(list_classes)

    return list_classes


def is_root_node(graph, element):
    """ Returns if a specific element is a root node in a graph. """
    elem = URIRef(element)
    list_root = get_list_root_classes(graph)

    if elem in list_root:
        return True
    else:
        return False


def is_leaf_node(graph, element):
    """ Returns if a specific element is a leaf node in a graph. """
    elem = URIRef(element)
    list_leaf = get_list_leaf_classes(graph)

    if elem in list_leaf:
        return True
    else:
        return False


def get_list_root_classes(graph):
    """ Returns a list without repetitions with the URI of all root classes in a graph.
        Root classes are:  (1) classes that (2) have no SUPERclasses besides owl:Thing.
        Isolated classes are both root and leaf at the same time.
    """

    # List of all classes
    cond1 = get_list_all_classes(graph)

    # List of all entities that have a rdfs:subclass property with other entity (participating as source)
    cond2 = []
    for subj, pred, obj in graph.triples((None, RDFS.subClassOf, None)):
        cond2.append(subj.n3()[1:-1])

    list_root_classes = lists_subtraction(cond1, cond2)

    return list_root_classes


def get_list_leaf_classes(graph):
    """ Returns a list without repetitions with the URI of all leaf classes in a graph.
        Leaf classes are:  (1) classes that (2) have no SUBclasses.
        Isolated classes are both root and leaf at the same time.
    """

    # List of all classes
    cond1 = get_list_all_classes(graph)

    # List of all entities that have a rdfs:subclass property with other entity (participating as target)
    cond2 = []
    for subj, pred, obj in graph.triples((None, RDFS.subClassOf, None)):
        cond2.append(obj.n3()[1:-1])

    # List of root classes
    cond3 = get_list_root_classes(graph)

    partial = lists_subtraction(cond1, cond2)
    list_leaf_nodes = lists_subtraction(partial, cond3)

    return list_leaf_nodes


def get_superclasses(graph, element):
    """ Returns a list of all superclasses of the given element of a graph. """

    elem = URIRef(element)
    superclasses = []

    for obj in graph.objects(elem, RDFS.subClassOf):
        superclasses.append(obj.n3()[1:-1])

    return superclasses


def get_subclasses(graph, element):
    """ Returns a list of all subclasses of the given element of a graph. """

    elem = URIRef(element)
    subclasses = []

    for subj in graph.subjects(RDFS.subClassOf, elem):
        subclasses.append(subj.n3()[1:-1])

    return subclasses
