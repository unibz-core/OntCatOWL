""" Logging configurations. """

import logging
import os

from scior.modules.utils_general import get_date_time, create_directory_if_not_exists


def initialize_logger(source="default"):
    """ Initialize Scior Logger. """

    # Create a custom logger
    new_logger = logging.getLogger("Scior")

    if source == "default":
        new_logger.setLevel(logging.DEBUG)
    elif source == "tester":
        new_logger.setLevel(logging.ERROR)
    else:
        print(f"Logger parameter unknown ({source}). Aborting execution.")

    # Creates a new logger only if Scior does not exist
    if not logging.getLogger("Scior").hasHandlers():

        # Creating CONSOLE handler
        console_handler = logging.StreamHandler()
        if source == "default":
            console_handler.setLevel(logging.INFO)
        elif source == "tester":
            console_handler.setLevel(logging.ERROR)
        else:
            print(f"Logger parameter unknown ({source}). Aborting execution.")

        # If directory "/log" does not exist, create it
        log_directory = "logs/"
        create_directory_if_not_exists(log_directory)

        # Creating FILE handler
        file_handler = logging.FileHandler(f"{log_directory}{get_date_time()}.log")
        if source == "default":
            file_handler.setLevel(logging.DEBUG)
        elif source == "tester":
            file_handler.setLevel(logging.ERROR)
        else:
            print(f"Logger parameter unknown ({source}). Aborting execution.")

        # Create formatters and add it to handlers
        console_format = logging.Formatter('%(levelname)s - %(message)s')
        file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s [func: %(funcName)s '
                                        'in %(filename)s]')
        console_handler.setFormatter(console_format)
        file_handler.setFormatter(file_format)

        # Add handlers to the logger
        new_logger.addHandler(console_handler)
        new_logger.addHandler(file_handler)

    return new_logger
