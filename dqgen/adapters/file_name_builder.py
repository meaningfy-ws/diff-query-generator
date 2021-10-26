#!/usr/bin/python3

# template_builder.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com
import shutil
from pathlib import Path

from dqgen.adapters import camel_case_split


def make_file_name(operation, cls, prop, obj_prop, file_extension):
    try:
        subject = str(cls).split(":")[1]
        subject = str.lower("_".join(camel_case_split(subject)))
    except:
        subject = "dummy_class"
    try:
        predicate = str(prop).split(":")[1]
        predicate = str.lower("_".join(camel_case_split(predicate)))
    except:
        predicate = None
    try:
        object_predicate = str(obj_prop).split(":")[1]
        object_predicate = str.lower("_".join(camel_case_split(object_predicate)))
    except:
        object_predicate = None
    if predicate:
        if object_predicate:
            file_name = f"{str.lower(operation)}_{subject}_{predicate}_{object_predicate}.{file_extension}"
        else:
            file_name = f"{str.lower(operation)}_{subject}_{predicate}.{file_extension}"
    else:
        file_name = f"{str.lower(operation)}_{subject}.{file_extension}"

    return file_name


def make_file_path(output_folder_path, file_name):
    """ takes a prefix with operation and a short RDF URI notation (prefix:name) and returns a filename"""
    base = Path(output_folder_path)
    file_path = base / file_name
    file_path.resolve()
    return str(file_path)
