"""Main module for OntCatOWL"""
if __name__ == "__main__":

    import logging
    from rdflib import Graph
    from modules.data_loading import get_list_of_types, get_list_of_individuals

    # TODO (@pedropaulofb): Set base level for printing log
    logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)

    gufo = Graph()
    ontology = Graph()

    # Input GUFO ontology
    # TODO (@pedropaulofb): Change for the complete version of GUFO after the tests are finished.
    try:
        gufo.parse("resources/gufoEndurantsOnly.ttl")
    except OSError:
        logging.error("Could not load resources/gufoEndurantsOnly.ttl file. Exiting program.")
        exit(1)

    # TODO (@pedropaulofb): Read from argument
    # Input ontology to be evaluated
    try:
        ontology.parse("resources/d3fend.ttl")
    except OSError:
        logging.error("Could not load resources/d3fend.ttl file. Exiting program.")
        exit(1)

    # TODO (@pedropaulofb): Read all classes from input ontology and create a list with no repetitions

    # logging.debug("Initializing RDFS reasoning. This may take a while...")
    # st = time.time()
    # DeductiveClosure(RDFS_Semantics).expand(ontology)  # Performs RDFS inferences
    # et = time.time()
    # elapsed_time = round((et - st), 2)
    # logging.debug(f"Reasoning process completed in {elapsed_time} seconds.")

    logging.debug("Initializing list of GUFO concepts.")
    gufo_types = get_list_of_types()
    gufo_individuals = get_list_of_individuals()

# TODO (@pedropaulofb): Create log file parallel to logs printed on std.out  #  (e.g., https://github.com/borntyping/jsonlog)
# TODO (@pedropaulofb): Use different colors for logs levels printed on std.out (e.g. https://betterstack.com/community/questions/how-to-color-python-logging-output/)
# TODO (@pedropaulofb): Future argument options: save in one file (ont + gufo), save inferences as assertions
# TODO (@pedropaulofb): Verify possibility to check consistency using a reasoner.
# TODO (@pedropaulofb): Evaluate on Linux before release first version
# TODO (@pedropaulofb): Update requirements.txt
# TODO (@pedropaulofb): OntCatOWL can became a generic mapper tool!
