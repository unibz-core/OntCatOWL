""" Argument Treatments """

import argparse

from modules.logger_config import initialize_logger


def treat_arguments(software_version):
    """ Treats user input arguments. """

    logger = initialize_logger()
    logger.debug("Parsing arguments...")

    # PARSING ARGUMENTS
    arguments_parser = argparse.ArgumentParser(prog="OntCatOWL",
                                               description="Identification of ontological categories for "
                                                           "OWL ontologies.",
                                               allow_abbrev=False,
                                               epilog="https://github.com/unibz-core/OntCatOWL/")

    arguments_parser.version = software_version

    # OPTIONAL ARGUMENTS

    # Automation level

    automation_group = arguments_parser.add_mutually_exclusive_group()

    automation_group.add_argument("-i", "--interactive", action='store_true',
                                  help="Executes automatic rules whenever possible. "
                                       "Executes interactive rules only if necessary.")

    automation_group.add_argument("-a", "--automatic",
                                  action='store_true',
                                  help="Executes only automatic rules. Interactive rules are not performed.")

    # Ontology completeness arguments

    completeness_group = arguments_parser.add_mutually_exclusive_group()

    completeness_group.add_argument("-n", "--incomplete", action='store_true',
                                    help="The loaded ontology is an incomplete model.")

    completeness_group.add_argument("-c", "--complete", action='store_true',
                                    help="The loaded ontology is a complete model.")

    # General arguments
    arguments_parser.add_argument("-t", "--times", action='store_true',
                                  help="Prints the execution times of all functions.")

    # TODO (@pedropaulofb): Arguments -p and -g are not implemented yet.
    arguments_parser.add_argument("-p", "--partial", action='store_true',
                                  help="Saves in files the partial ontology and reports before any user interaction.")

    arguments_parser.add_argument("-g", "--gufo", action='store_true',
                                  help="Imports GUFO ontology in the output ontology file.")

    # Automatic arguments
    arguments_parser.add_argument("-v", "--version", action="version", help="Prints the software version and exit.")

    # POSITIONAL ARGUMENT
    arguments_parser.add_argument("ontology_file", type=str, action="store", help="The ontology file to be loaded.")

    # Execute arguments parser
    arguments = arguments_parser.parse_args()

    global_configurations = {"partial_results": arguments.partial,
                             "import_gufo": arguments.gufo,
                             "is_automatic": arguments.automatic,
                             "is_complete": arguments.complete,
                             "print_time": arguments.times,
                             "ontology_path": arguments.ontology_file}

    logger.debug(f"Arguments Parsed. Obtained values are: {global_configurations}")

    print(vars(arguments))

    return global_configurations
