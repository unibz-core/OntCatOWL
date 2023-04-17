""" Implementation of rules of group UFO Some. """

from scior.modules.dataclass_definitions_ontology import OntologyDataClass
from scior.modules.logger_config import initialize_logger
from scior.modules.rules_type_implementations import register_incompleteness
from scior.modules.utils_dataclass import get_dataclass_by_uri

LOGGER = initialize_logger()


def treat_result_ufo_some(ontology_dataclass_list: list[OntologyDataClass], selected_dataclass: OntologyDataClass,
                          can_classes_list: list[str], is_classes_list: list[str], types_to_set_list: list[str],
                          rule_code: str, arguments: dict) -> None:
    """ Treats the results from all rules from the group UFO Some. """

    length_is_list = len(is_classes_list)
    length_can_list = len(can_classes_list)

    # GENERAL CASES

    if length_is_list > 0:
        LOGGER.debug(f"Rule {rule_code} satisfied. No action is required.")

    elif length_can_list > 1:
        # Incompleteness found. Reporting incompleteness and possibilities.
        register_incompleteness(rule_code, selected_dataclass)
        LOGGER.info(f"Solution: set one or more classes from {can_classes_list} as {types_to_set_list}.")

    elif length_can_list == 1:
        # Set single candidate as desired types.
        candidate_dataclass = get_dataclass_by_uri(ontology_dataclass_list, can_classes_list[0])

        if candidate_dataclass is None:
            LOGGER.error(f"Unexpected situation. Searched URI {can_classes_list[0]} "
                         f"not found in ontology_dataclass_list. Program aborted.")
            raise ValueError(f"INVALID VALUE!")

        candidate_dataclass.move_list_of_elements_to_is_list(types_to_set_list)

    elif length_can_list == 0:
        # Report incompleteness
        if arguments["is_owa"]:
            register_incompleteness(rule_code, selected_dataclass)
            LOGGER.info(f"There are no known classes that can be set as {types_to_set_list} to satisfy the rule.")

        # Report inconsistency
        if arguments["is_cwa"]:
            LOGGER.error(f"Error detected in rule {rule_code} for class {selected_dataclass.uri}. "
                         f"There are no asserted classes that satisfy the rule. Program aborted.")
            raise ValueError(f"INCONSISTENCY FOUND IN RULE {rule_code}!")

    else:
        LOGGER.error(f"Error detected in rule {rule_code}. Unexpected else clause reached. Program aborted.")
        raise ValueError(f"UNEXPECTED BEHAVIOUR IN RULE {rule_code}!")


def run_r24rg(ontology_dataclass_list, ontology_graph, arguments):
    """ Executes rule R24Rg from group UFO.

    Code: R24Rg
    Definition: AntiRigidType(x) ^ Sortal(x) ^ Category(y) ^ subClassOf(x,y) ->
                    E z (RigidType(z) ^ Sortal(z) ^ subClassOf(x,z) ^ subClassOf(z,y))
    Description: AntiRigid Sortals cannot "only directly specialize" Categories.
    """

    rule_code = "R24Rg"

    LOGGER.debug(f"Starting rule {rule_code}")

    query_string = """
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        SELECT DISTINCT ?class_x ?class_y ?class_z
        WHERE {
            ?class_x rdf:type gufo:AntiRigidType .
            ?class_x rdf:type gufo:Sortal .
            ?class_y rdf:type gufo:Category .
            ?class_x rdfs:subClassOf ?class_y .
            ?class_x rdfs:subClassOf ?class_z .
            ?class_z rdfs:subClassOf ?class_y .
        } """

    query_result = ontology_graph.query(query_string)

    is_list = []
    can_list = []

    for row in query_result:

        for ontology_dataclass in ontology_dataclass_list:
            if ontology_dataclass.uri == row.class_z.toPython():
                # Creating IS List
                if "RigidType" in ontology_dataclass.is_type and "Sortal" in ontology_dataclass.is_type:
                    is_list.append(ontology_dataclass.uri)
                # Creating CAN List
                elif "RigidType" not in ontology_dataclass.not_type and "Sortal" not in ontology_dataclass.not_type:
                    can_list.append(ontology_dataclass.uri)

                treat_result_ufo_some(ontology_dataclass_list, ontology_dataclass, can_list, is_list,
                                      ["RigidType", "Sortal"], rule_code, arguments)

    LOGGER.debug(f"Rule {rule_code} concluded")


def execute_rules_ufo_specific(ontology_dataclass_list, ontology_graph, arguments):
    """Call execution all rules from the group UFO Some."""

    LOGGER.debug("Starting execution of all rules from group UFO Some.")

    run_r24rg(ontology_dataclass_list, ontology_graph, arguments)

    LOGGER.debug("Execution of all rules from group UFO Some completed.")
