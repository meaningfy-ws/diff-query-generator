#!/usr/bin/python3

# resource_fetcher.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

"""
    This module is responsible for reading a project resource file, given certain resource path.
"""


def get_template(resource_path: str) -> str:
    """
        Given a resource path read the file and return it as a string.
    :param resource_path:
    :return:
    """
