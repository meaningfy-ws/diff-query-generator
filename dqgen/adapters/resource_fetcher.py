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

from dqgen.resources import query_templates, html_templates

PATH_TO_STATIC_FOLDER = pathlib.Path(__file__).parent.parent / "resources" / "html_templates" / "static"


def get_file_content(resource_path: str) -> str:
    """
        Given a resource path read the file and return the file content it as a string.
    :param resource_path:
    :return:
    """
    path = pathlib.Path(resource_path).resolve()
    return path.read_text()


def get_query_template(query_file_name: str) -> str:
    """
        Given query template file name, read the file and return it as a string.
    :param query_file_name:
    :return:
    """
    with pkg_resources.path(query_templates, query_file_name) as path:
        return path.read_text()


def get_html_template(html_template_file_name: str) -> str:
    """
        Given html template file name, read the file and return it as a string.
    :param html_template_file_name:
    :return:
    """
    with pkg_resources.path(html_templates, html_template_file_name) as path:
        return path.read_text()


def get_static_folder_file_paths() -> list:
    """
        Get all file paths from the static folder
    :return: [file_paths]
    """
    return [file_path for file_path in PATH_TO_STATIC_FOLDER.iterdir() if file_path.is_file()]
