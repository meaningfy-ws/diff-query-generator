#!/usr/bin/python3

# template_builder.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

"""
    This module is responsible for reading a project resource file, given certain resource path.
"""
import pathlib

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources


def get_file_content(resource_path: str) -> str:
    """
        Given a resource path read the file and return the file content it as a string.
    :param resource_path:
    :return:
    """
    path = pathlib.Path(resource_path).resolve()
    return path.read_text()
