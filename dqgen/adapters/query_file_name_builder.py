#!/usr/bin/python3

# template_builder.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com
import shutil
from pathlib import Path

from dqgen.adapters import camel_case_split


def make_query_file_name(output_folder_path, operation, cls, prop, obj_prop, file_extension):
    """ takes a prefix with operation and a short RDF URI notation (prefix:name) and returns a filename"""
    base = Path(output_folder_path)
    base.resolve().mkdir(exist_ok=True)
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
    file_name = base / file_name
    file_name.resolve()
    return str(file_name)


