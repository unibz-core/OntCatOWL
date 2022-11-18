""" Provides class and functions to calculate statistics of the improvement OntCatOWL has caused on
the inputted ontology. """

from modules.logger_config import initialize_logger
from modules.results_classes import dataclass_statistics, list_classes_by_situation, classes_statistics, \
    classifications_statistics, comparission_stats
from ontcatowl import NUMBER_GUFO_TYPES, NUMBER_GUFO_INDIVIDUALS


def generates_partial_statistics_list(ontology_dataclass_list):
    """ Collects the statistics of an ontology_dataclass_list.
    Returns a list of instances of the dataclass_statistics class.
    """

    partial_statistics_list = []

    for ontology_dataclass in ontology_dataclass_list:
        partial_statistics_list.append(dataclass_statistics(ontology_dataclass))

    return partial_statistics_list


def get_values_statistics_classes(statistics_list):
    """ Receives a statistics list and returns a list for classes.
        list for classes: aggregated statistics for classes
    """

    # INITIALIZATION OF VARIABLES
    return_classes_statistics = classes_statistics()

    total_classes_number = 0

    totally_unknown_classes_types = 0
    totally_unknown_classes_individuals = 0
    totally_unknown_classes_all = 0

    totally_known_classes_types = 0
    totally_known_classes_individuals = 0
    totally_known_classes_all = 0

    partially_known_classes_types = 0
    partially_known_classes_individuals = 0
    partially_known_classes_all = 0

    # CALCULATION OF VALUES
    for element in statistics_list:

        total_classes_number += 1

        # Calculating number of classes for TYPES

        is_totally_unknown_classes_types = False
        is_totally_known_classes_types = False

        if element.number_unknown_types == NUMBER_GUFO_TYPES:
            totally_unknown_classes_types += 1
            is_totally_unknown_classes_types = True
        elif element.number_unknown_types == 0:
            totally_known_classes_types += 1
            is_totally_known_classes_types = True
        else:
            partially_known_classes_types += 1

        # Calculating number of classes for INDIVIDUALS

        is_totally_unknown_classes_individuals = False
        is_totally_known_classes_individuals = False

        if element.number_unknown_individuals == NUMBER_GUFO_INDIVIDUALS:
            totally_unknown_classes_individuals += 1
            is_totally_unknown_classes_individuals = True
        elif element.number_unknown_individuals == 0:
            totally_known_classes_individuals += 1
            is_totally_known_classes_individuals = True
        else:
            partially_known_classes_individuals += 1

        # Calculating number of classes for ALL

        if is_totally_known_classes_types and is_totally_known_classes_individuals:
            totally_known_classes_all += 1
        elif is_totally_unknown_classes_types and is_totally_unknown_classes_individuals:
            totally_unknown_classes_all += 1
        else:
            partially_known_classes_all += 1

    # GENERATING RETURN LISTS

    return_classes_statistics.total_classes_number = total_classes_number

    return_classes_statistics.tu_classes_types_v = totally_unknown_classes_types
    return_classes_statistics.tu_classes_indiv_v = totally_unknown_classes_individuals
    return_classes_statistics.tu_classes_all_v = totally_unknown_classes_all

    return_classes_statistics.pk_classes_types_v = partially_known_classes_types
    return_classes_statistics.pk_classes_indiv_v = partially_known_classes_individuals
    return_classes_statistics.pk_classes_all_v = partially_known_classes_all

    return_classes_statistics.tk_classes_types_v = totally_known_classes_types
    return_classes_statistics.tk_classes_indiv_v = totally_known_classes_individuals
    return_classes_statistics.tk_classes_all_v = totally_known_classes_all

    return return_classes_statistics


def get_values_statistics_classifications(statistics_list):
    """ Receives a statistics list and returns a list for classifications.
        list for classifications: aggregated statistics for possible classifications (stereotypes) of classes
    """

    # INITIALIZATION OF VARIABLES
    return_classifications_statistics = classifications_statistics()

    number_unknown_classifications_types = 0
    number_unknown_classifications_individuals = 0

    number_known_classifications_types = 0
    number_known_classifications_individuals = 0

    number_unknown_classifications_total = 0
    number_known_classifications_total = 0

    # CALCULATION OF VALUES
    for element in statistics_list:
        # Calculating number of classifications for TYPES
        number_unknown_classifications_types += element.number_unknown_types
        number_known_classifications_types += element.number_known_types

        # Calculating number of classifications for INDIVIDUALS
        number_unknown_classifications_individuals += element.number_unknown_individuals
        number_known_classifications_individuals += element.number_known_individuals

    # Calculating number of classifications for TOTAL
    number_unknown_classifications_total += number_unknown_classifications_types + number_unknown_classifications_individuals
    number_known_classifications_total += number_known_classifications_types + number_known_classifications_individuals

    # GENERATING RETURN LISTS

    # Generating lists of numbers for classifications
    total_classifications_number = number_unknown_classifications_total + number_known_classifications_total
    total_classifications_types = number_unknown_classifications_types + number_known_classifications_types
    total_classifications_individuals = number_unknown_classifications_individuals + number_known_classifications_individuals

    # Generating return list
    return_classifications_statistics.total_classif_number = total_classifications_number

    return_classifications_statistics.total_classif_types_v = total_classifications_types
    return_classifications_statistics.total_classif_indiv_v = total_classifications_individuals

    return_classifications_statistics.unknown_classif_types_v = number_unknown_classifications_types
    return_classifications_statistics.unknown_classif_indiv_v = number_unknown_classifications_individuals

    return_classifications_statistics.known_classif_types_v = number_known_classifications_types
    return_classifications_statistics.known_classif_indiv_v = number_known_classifications_individuals

    return return_classifications_statistics


def get_list_totally_unknown_classes(class_statistics_list):
    """ Receives a statistics_list and generate three other lists, grouped in a list_classes_by_situation class.
        All lists there contained are already alphabetically sorted. """

    logger = initialize_logger()

    logger.debug("Generating list_totally_unknown_classes ...")

    list_classes_totally_unknown_types = []
    list_classes_totally_unknown_individuals = []
    list_classes_totally_unknown_all = []

    for element in class_statistics_list:
        if element.number_known_types == 0:
            list_classes_totally_unknown_types.append(element.uri)
        if element.number_known_individuals == 0:
            list_classes_totally_unknown_individuals.append(element.uri)
        if element.number_known_types + element.number_known_individuals == 0:
            list_classes_totally_unknown_all.append(element.uri)

    list_classes_totally_unknown_types.sort()
    list_classes_totally_unknown_individuals.sort()
    list_classes_totally_unknown_all.sort()

    list_totally_unknown_classes = list_classes_by_situation("Totally Unknown", list_classes_totally_unknown_types,
                                                             list_classes_totally_unknown_individuals,
                                                             list_classes_totally_unknown_all)

    logger.debug("list_totally_unknown_classes successfully generated.")

    return list_totally_unknown_classes


def get_list_partially_known_classes(class_statistics_list):
    """ Receives a statistics_list and generate three other lists, grouped in an list_classes_by_situation class.
        All lists there contained are already alphabetically sorted. """

    logger = initialize_logger()

    logger.debug("Generating list_partially_known_classes ...")

    list_classes_partially_known_types = []
    list_classes_partially_known_individuals = []
    list_classes_partially_known_all = []

    for element in class_statistics_list:
        if element.number_unknown_types != 0 and element.number_known_types != 0:
            list_classes_partially_known_types.append(element.uri)
        if element.number_unknown_individuals != 0 and element.number_known_individuals != 0:
            list_classes_partially_known_individuals.append(element.uri)
        if (element.number_unknown_types != 0 and element.number_known_types != 0) or (
                element.number_unknown_individuals != 0 and element.number_known_individuals != 0):
            list_classes_partially_known_all.append(element.uri)

    list_classes_partially_known_types.sort()
    list_classes_partially_known_individuals.sort()
    list_classes_partially_known_all.sort()

    list_partially_known_classes = list_classes_by_situation("Partially Known", list_classes_partially_known_types,
                                                             list_classes_partially_known_individuals,
                                                             list_classes_partially_known_all)

    logger.debug("list_partially_known_classes successfully generated.")

    return list_partially_known_classes


def get_list_totally_known_classes(class_statistics_list):
    """ Receives a statistics_list and generate three other lists, grouped in an list_classes_by_situation class.
    All lists there contained are already alphabetically sorted. """

    logger = initialize_logger()

    logger.debug("Generating list_totally_known_classes ...")

    list_classes_totally_known_types = []
    list_classes_totally_known_individuals = []
    list_classes_totally_known_all = []

    for element in class_statistics_list:
        if element.number_unknown_types == 0:
            list_classes_totally_known_types.append(element.uri)
        if element.number_unknown_individuals == 0:
            list_classes_totally_known_individuals.append(element.uri)
        if element.number_unknown_types + element.number_unknown_individuals == 0:
            list_classes_totally_known_all.append(element.uri)

    list_classes_totally_known_types.sort()
    list_classes_totally_known_individuals.sort()
    list_classes_totally_known_all.sort()

    list_totally_known_classes = list_classes_by_situation("Totally Known", list_classes_totally_known_types,
                                                           list_classes_totally_known_individuals,
                                                           list_classes_totally_known_all)

    logger.debug("list_totally_known_classes successfully generated.")

    return list_totally_known_classes


def generate_result_classes_lists(before_statistics, after_statistics):
    """ Receives 'before' and 'after' statistics and generates lists of improved and solved classes."""

    lists_before = []
    lists_after = []

    # Getting lists with classes names
    list_totally_unknown_classes_before = get_list_totally_unknown_classes(before_statistics)
    list_partially_known_classes_before = get_list_partially_known_classes(before_statistics)
    list_totally_known_classes_before = get_list_totally_known_classes(before_statistics)

    list_totally_unknown_classes_after = get_list_totally_unknown_classes(after_statistics)
    list_partially_known_classes_after = get_list_partially_known_classes(after_statistics)
    list_totally_known_classes_after = get_list_totally_known_classes(after_statistics)

    lists_before.append("Before")
    lists_before.append(list_totally_unknown_classes_before)
    lists_before.append(list_partially_known_classes_before)
    lists_before.append(list_totally_known_classes_before)

    lists_after.append("After")
    lists_after.append(list_totally_unknown_classes_after)
    lists_after.append(list_partially_known_classes_after)
    lists_after.append(list_totally_known_classes_after)

    return lists_before, lists_after


def calculate_final_statistics(before_statistics, after_statistics):
    """ Receives 'before' and 'after' statistic lists and calculates final statistics.
    The 'before' and 'after' statistic lists are lists of statistics of all classes. I.e., it contains instances of
    the class dataclass_statistics.
    """

    statistics_classes_before = get_values_statistics_classes(before_statistics)
    statistics_classes_before.calculate()
    statistics_classes_before.validate()

    statistics_classifications_before = get_values_statistics_classifications(before_statistics)
    statistics_classifications_before.calculate()
    statistics_classifications_before.validate()

    statistics_classes_after = get_values_statistics_classes(after_statistics)
    statistics_classes_after.calculate()
    statistics_classes_after.validate()

    statistics_classifications_after = get_values_statistics_classifications(after_statistics)
    statistics_classifications_after.calculate()
    statistics_classifications_after.validate()

    comparisson_statistics = comparission_stats(statistics_classes_before,
                                                statistics_classifications_before,
                                                statistics_classes_after,
                                                statistics_classifications_after)
    comparission_stats.calculate()

    return comparisson_statistics
