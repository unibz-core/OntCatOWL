""" Implementation of rules for types. """

from modules.logger_config import initialize_logger
from modules.user_interactions import select_class_from_list, print_class_types, set_interactively_class_as_gufo_type
from modules.utils_dataclass import get_list_gufo_classification, external_move_to_is_list, \
    external_move_list_to_is_list, get_element_list, return_dataclass_from_class_name
from modules.utils_graph import get_all_related_nodes, get_all_superclasses, get_subclasses, get_superclasses

# Frequent GUFO types
GUFO_KIND = "gufo:Kind"


def treat_rule_n_r_t(rule_code, ontology_dataclass, configurations):
    """ Implements rule n_r_t for types."""
    logger = initialize_logger()

    if configurations["is_complete"]:
        if GUFO_KIND in ontology_dataclass.can_type:
            logger.warning(f"Incompleteness detected during rule {rule_code}! "
                           f"There is not identity principle associated to class {ontology_dataclass.uri}. "
                           f"The class was set as a gufo:Kind.")
            ontology_dataclass.move_element_to_is_list(GUFO_KIND)
        else:
            logger.error(f"Inconsistency detected! Class {ontology_dataclass.uri} must be a gufo:Kind, "
                         f"however it cannot be. Program aborted.")
            print_class_types(ontology_dataclass)
            exit(1)
    else:
        logger.warning(f"Incompleteness detected during rule {rule_code}! "
                       f"There is not identity principle associated to class {ontology_dataclass.uri}.")
        if (not configurations["is_automatic"]) and (GUFO_KIND in ontology_dataclass.can_type):
            set_interactively_class_as_gufo_type(ontology_dataclass, GUFO_KIND)


def interaction_rule_ns_s_spe(list_ontology_dataclasses, ontology_dataclass, number_related_kinds,
                              related_can_kinds_list):
    """ Implements the user interaction for rule ns_s_spe for types. """

    print(f"\nAs a gufo:NonSortal, the class {ontology_dataclass.uri} must aggregate entities with "
          f"at least two different identity principles, which are provided by gufo:Kinds. "
          f"Currently, there is/are {number_related_kinds} gufo:Kind(s) related to this class. ")

    print(f"\nThe following list presents all classes that are related to {ontology_dataclass.uri} and that "
          f"can possibly be classified as gufo:Kinds.")

    selected_class = select_class_from_list(list_ontology_dataclasses, related_can_kinds_list)

    if selected_class != "skipped":
        external_move_to_is_list(list_ontology_dataclasses, selected_class, GUFO_KIND)


def decide_action_rule_ns_s_spe(configurations, number_possibilities, number_necessary):
    """ Returns the action to be performed for rule ns_s_spe. """

    ni = not (configurations["is_complete"] or configurations["is_automatic"])
    ci = configurations["is_complete"] and not configurations["is_automatic"]

    if number_possibilities <= 0:
        action = "report_incompleteness"
    elif configurations["is_complete"] and number_possibilities <= number_necessary:
        action = "set_all_as_kinds"
    elif ni or (ci and number_possibilities > number_necessary):
        action = "user_can_set"
    else:
        action = "report_incompleteness"

    return action


def treat_rule_ns_s_spe(rule_code, ontology_dataclass, list_ontology_dataclasses, graph, nodes_list, configurations):
    """ Implements rule ns_s_spe for types."""

    logger = initialize_logger()

    # Get all ontology dataclasses that are reachable from the ontologies dataclass
    list_all_related_nodes = get_all_related_nodes(graph, nodes_list, ontology_dataclass.uri)

    logger.debug(f"Related nodes of {ontology_dataclass.uri} are: {list_all_related_nodes}")

    # From the previous list, get all the ones that ARE gufo:Kinds
    related_is_kinds_list = get_list_gufo_classification(list_ontology_dataclasses, list_all_related_nodes, "IS",
                                                         GUFO_KIND)
    number_related_kinds = len(related_is_kinds_list)

    logger.debug(f"Related nodes of {ontology_dataclass.uri} that ARE Kinds: {list_all_related_nodes}")

    # Get all related classes that CAN be classified as gufo:Kinds
    related_can_kinds_list = get_list_gufo_classification(list_ontology_dataclasses, list_all_related_nodes, "CAN",
                                                          GUFO_KIND)

    logger.debug(f"Related nodes of {ontology_dataclass.uri} that CAN BE Kinds: {list_all_related_nodes}")

    number_can_kinds_list = len(related_can_kinds_list)

    number_possibilities = number_can_kinds_list
    number_necessary = 2 - number_related_kinds

    logger.debug(f"For {ontology_dataclass.uri}: K = {number_related_kinds}, "
                 f"P = {number_possibilities}, N = {number_necessary} "
                 f"K list = {related_is_kinds_list} "
                 f"P list = {related_can_kinds_list} ")

    # The rule is already accomplished, so there is no need to do any action.
    if number_necessary <= 0:
        return

    action = decide_action_rule_ns_s_spe(configurations, number_possibilities, number_necessary)

    logger.warning(f"Incompleteness detected during rule {rule_code}! "
                   f"The class {ontology_dataclass.uri} "
                   f"is associated to {2 - number_necessary} Kind(s), "
                   f"but it should be related to at least 2 Kinds. ")

    if action == "report_incompleteness":
        if number_can_kinds_list > 0:
            logger.info(f"Classes that are associated with {ontology_dataclass.uri} and that "
                        f"can be Kinds are: {related_can_kinds_list}.")
        else:
            logger.debug(f"There are no classes associated with {ontology_dataclass.uri} and that can be set as Kinds.")
    elif action == "set_all_as_kinds":
        logger.info(f"The following classes are going to be set as Kinds "
                    f"to solve the incompleteness: {related_can_kinds_list}.")
        external_move_list_to_is_list(list_ontology_dataclasses, related_can_kinds_list, GUFO_KIND)
    elif action == "user_can_set":
        interaction_rule_ns_s_spe(list_ontology_dataclasses, ontology_dataclass, number_related_kinds,
                                  related_can_kinds_list)
    else:
        logger.error("Unexpected evaluation result! Program aborted.")
        exit(1)


def interaction_rule_nk_k_sup(list_ontology_dataclasses, list_possibilities):
    """ User interaction for rule nk_k_sup. """

    logger = initialize_logger()

    print(f"The following classes were identified as possible identity providers:")
    selected_class = select_class_from_list(list_ontology_dataclasses, list_possibilities)

    if selected_class != "skipped":
        external_move_to_is_list(list_ontology_dataclasses, selected_class, GUFO_KIND)
        logger.info(f"Class {selected_class} was correctly set as gufo:Kind.")


def treat_rule_nk_k_sup(rule_code, ontology_dataclass, list_ontology_dataclasses, graph, nodes_list, configurations):
    """ Implements rule nk_k_sup for types."""

    logger = initialize_logger()

    # Get all ontology dataclasses that are directly or indirectly superclasses of ontology_dataclass
    list_superclasses = get_all_superclasses(graph, nodes_list, ontology_dataclass.uri)
    logger.debug(f"Superclasses of {ontology_dataclass.uri} are: {list_superclasses}")

    # Verify if there is a Kind in the superclass list
    kind_sortals = get_list_gufo_classification(list_ontology_dataclasses, list_superclasses, "IS", GUFO_KIND)

    # CONDITION 2: Kind not found in list of superclasses (i.e., if a Kind is found, the rule execution is interrupted)
    if len(kind_sortals) != 0:
        return

    list_possibilities = []
    # select which can be kind (can_type)
    for possible_kind in list_superclasses:

        possible_kind_can = get_element_list(list_ontology_dataclasses, possible_kind, "can_type")

        if GUFO_KIND in possible_kind_can:
            list_possibilities.append(possible_kind)

    logger.warning(f"Incompleteness detected during rule {rule_code}! "
                   f"The class {ontology_dataclass.uri} does not have an identity provider. "
                   f"It must have exactly one gufo:Kind as direct or indirect supertype, but has none.")

    # If no identity provider available, report incompleteness for all configurations
    if len(list_possibilities) == 0:
        logger.info(f"No classes were identified as possible candidates for "
                    f"identity provider for {ontology_dataclass.uri}.")
    elif len(list_possibilities) == 1:
        if configurations["is_complete"]:
            external_move_to_is_list(list_ontology_dataclasses, list_possibilities[0], GUFO_KIND)
            logger.info(f"Class {list_possibilities[0]} is the unique possible identity provider "
                        f"for {ontology_dataclass.uri}. Hence, it was automatically asserted as gufo:Kind.")
        elif configurations["is_automatic"]:
            logger.info(f"The following classes were identified as possible identity providers "
                        f"for {ontology_dataclass.uri}: {list_possibilities}.")
        else:
            interaction_rule_nk_k_sup(list_ontology_dataclasses, list_possibilities)
    elif len(list_possibilities) > 1:
        if configurations["is_automatic"]:
            logger.info(f"The following classes were identified as possible identity providers: {list_possibilities}.")
        else:
            interaction_rule_nk_k_sup(list_ontology_dataclasses, list_possibilities)


def treat_rule_s_nsup_k(rule_code, ontology_dataclass, graph, nodes_list, configurations):
    """ Implements the treatment of rule n_nsup_k for types. """
    logger = initialize_logger()

    # Get list of all superclasses up to leaves.
    all_superclasses = get_all_superclasses(graph, nodes_list, ontology_dataclass.uri)

    # CONDITION 2: list of superclasses must be empty
    if len(all_superclasses) != 0:
        return

    logger.warning(f"Incompleteness detected during rule {rule_code}! "
                   f"The class {ontology_dataclass.uri} does not have an identity provider. ")

    if configurations["is_complete"]:
        ontology_dataclass.move_element_to_is_list(GUFO_KIND)
        logger.info(f"The class {ontology_dataclass.uri} was successfully set as a gufo:Kind.")
    elif not configurations["is_automatic"]:
        set_interactively_class_as_gufo_type(ontology_dataclass, GUFO_KIND)


def treat_rule_ns_sub_r(list_ontology_dataclasses, ontology_dataclass, graph, nodes_list):
    """ Implements the treatment of rule ns_sub_r for types. """

    logger = initialize_logger()

    # Get list of all direct subclasses of the ontolgy_dataclass
    direct_subclasses = get_subclasses(graph, nodes_list["all"], ontology_dataclass.uri)

    # CONDITION 2: list of subclasses cannot be empty
    if len(direct_subclasses) == 0:
        return

    for subclass_name in direct_subclasses:
        subclass = return_dataclass_from_class_name(list_ontology_dataclasses, subclass_name)

        # If one of the subclasses is not a RigidType, nothing can be asserted for the superclass.
        if "gufo:RigidType" not in subclass.is_type:
            break
    else:
        # Only executed when the loop had no break. All subclasses were RigidTypes.
        logger.debug(f"The NonSortal class {ontology_dataclass.uri} "
                     f"is only specialized into RigidTypes and, hence, was set as a gufo:Category.")
        ontology_dataclass.move_element_to_is_list("gufo:Category")


def treat_rule_nrs_ns_r(rule_code, ontology_dataclass, graph, nodes_list, configurations):
    """ Implements the treatment of rule nrs_ns_r for types. """

    logger = initialize_logger()

    # Get all direct superclasses
    superclasses_list = get_superclasses(graph, nodes_list["all"], ontology_dataclass.uri)

    # For each superclass, verify the number of direct subclasses. If only one, perform action (else, do nothing).
    for superclass in superclasses_list:
        superclass_children = get_subclasses(graph, nodes_list["all"], superclass)
        number_children = len(superclass_children)

        if number_children > 1:
            return
        elif number_children == 1:
            break
        else:
            logger.error("Unexpected number of children. At least one subclass was expected. Program aborted.")
            exit(1)

    # All conditions are met. Perform possible actions.
    if configurations["is_complete"]:
        logger.info(f"The class {ontology_dataclass.uri} is a NonRigid Sortal without siblings, "
                    f"hence it was set as gufo:Role.")
        ontology_dataclass.move_element_to_is_list("gufo:Role")
    else:
        # Report incompleteness.
        logger.warning(f"Incompleteness detected during rule {rule_code}! "
                       f"The class {ontology_dataclass.uri} is a NonRigid Sortal without siblings. "
                       f"This class must be set as a gufo:Role. If it is a gufo:Phase, "
                       f"at least another gufo:Phase sibling class is missing, representing an incompleteness.")
        if not configurations["is_automatic"]:
            set_interactively_class_as_gufo_type(ontology_dataclass, "gufo:Role")


def treat_rule_ks_sf_in(rule_code, ontology_dataclass, graph, nodes_list, configurations):
    """ Implements the treatment of rule ks_sf_in for types. """

    logger = initialize_logger()

    # If a class (i) has only known direct subtypes and (ii) if only one of these is a phase, it represents an incompleteness.

    # Get class subclasses
    # Count number of subclasses and how many of them are phases

    pass
