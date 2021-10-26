#!/usr/bin/python3

# __init__.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

"""
    Defining maps between operation and necessary template for classes, proprieties and reified properties
"""
import pathlib

from jinja2 import Environment, PackageLoader

HTML_TEMPLATES = Environment(loader=PackageLoader("dqgen.resources", "html_templates"))
QUERIES_TEMPLATES = Environment(loader=PackageLoader("dqgen.resources", "query_templates"))
PATH_TO_STATIC_FOLDER = pathlib.Path(__file__).parent.parent / "resources" / "html_templates" / "static"

CLASSES_OPERATION_TEMPLATE_MAPPING = {"added_instance": QUERIES_TEMPLATES.get_template("instance_additions.rq"),
                                      "deleted_instance": QUERIES_TEMPLATES.get_template("instance_deletions.rq")}
PROPERTIES_OPERATION_TEMPLATE_MAPPING = {"added_property": QUERIES_TEMPLATES.get_template("property_additions.rq"),
                                         "deleted_property": QUERIES_TEMPLATES.get_template("property_deletions.rq")}
REIFIED_PROPERTIES_OPERATION_TEMPLATE_MAPPING = {
    "added_reified": QUERIES_TEMPLATES.get_template("reified_properties_additions.rq"),
    "deleted_reified": QUERIES_TEMPLATES.get_template("reified_properties_deletions.rq")}

INSTANCE_OPERATIONS = ["added_instance", "deleted_instance"]
PROPERTIES_OPERATIONS = ["added_property", "deleted_property"]
REIFIED_PROPERTIES_OPERATIONS = ["added_reified", "deleted_reified"]
