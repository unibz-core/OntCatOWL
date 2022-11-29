""" This module implements functions for validate Ontology DataClasses. """

from ontcatowl.modules.logger_config import initialize_logger
from ontcatowl.modules.utils_general import has_duplicates


def verify_duplicates_in_lists_ontology(ontology_dataclass):
    """ No same string must be in two lists at the same time. """

    logger = initialize_logger()
    merged_list = ontology_dataclass.is_type + ontology_dataclass.is_individual + ontology_dataclass.can_type + \
                  ontology_dataclass.can_individual + ontology_dataclass.not_type + ontology_dataclass.not_individual

    if has_duplicates(merged_list):
        logger.error(f"INCONSISTENCY DETECTED: Same element in two lists for {ontology_dataclass.uri}. "
                     f"Program aborted.")
        exit(1)


def verify_all_ontology_dataclasses_consistency(ontology_dataclass_list):
    """ Calls the consistency verification of all elements in a list of Ontology DataClasses. """

    logger = initialize_logger()
    logger.debug("Initializing consistency checking for all ontology dataclasses...")

    for ontology_dataclass in ontology_dataclass_list:
        ontology_dataclass.is_consistent()

    logger.debug("Consistency checking for all ontology dataclasses successfully performed.")


def updates_all_list_ontology_dataclasses(ontology_dataclass_list):
    """ Updates all the list of ontology dataclasses. """

    logger = initialize_logger()
    logger.debug("Updating all ontology elements in the dataclass list ...")

    for ontology_dataclass in ontology_dataclass_list:
        ontology_dataclass.update_all_lists_from_gufo()

    logger.debug("All ontology elements in the dataclass list were successfully updated.")
