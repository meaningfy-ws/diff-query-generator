#!/usr/bin/python3

# __init__.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
import re


def camel_case_split(identifier):
    """
        detects camel case components in a string and retouns a list of them.
        nice solution from: https://stackoverflow.com/questions/29916065/how-to-do-camelcase-split-in-python

    """
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]
