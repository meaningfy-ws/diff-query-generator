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

CLASSES_OPERATION_TEMPLATE_MAPPING = {
    "added_instance": QUERIES_TEMPLATES.get_template("instance_additions.rq"),
    "deleted_instance": QUERIES_TEMPLATES.get_template("instance_deletions.rq"),
    "count_added_instance": QUERIES_TEMPLATES.get_template("count_instance_additions.rq"),
    "count_deleted_instance": QUERIES_TEMPLATES.get_template("count_instance_deletions.rq")
}
PROPERTIES_OPERATION_TEMPLATE_MAPPING = {
    "added_property": QUERIES_TEMPLATES.get_template("property_additions.rq"),
    "deleted_property": QUERIES_TEMPLATES.get_template("property_deletions.rq"),
    "updated_property": QUERIES_TEMPLATES.get_template("property_value_updates.rq"),
    "moved_property": QUERIES_TEMPLATES.get_template("movement_cross_instance.rq"),
    "changed_property": QUERIES_TEMPLATES.get_template("movement_cross_property.rq"),
    "count_added_property": QUERIES_TEMPLATES.get_template("count_property_additions.rq"),
    "count_deleted_property": QUERIES_TEMPLATES.get_template("count_property_deletions.rq"),
    "count_updated_property": QUERIES_TEMPLATES.get_template("count_property_value_updates.rq"),
    "count_moved_property": QUERIES_TEMPLATES.get_template("count_movement_cross_instance.rq"),
    "count_changed_property": QUERIES_TEMPLATES.get_template("count_movement_cross_property.rq")
}
REIFIED_PROPERTIES_OPERATION_TEMPLATE_MAPPING = {
    "added_reified": QUERIES_TEMPLATES.get_template("reified_properties_additions.rq"),
    "deleted_reified": QUERIES_TEMPLATES.get_template("reified_properties_deletions.rq"),
    "updated_reified": QUERIES_TEMPLATES.get_template("reified_property_value_updates.rq"),
    "moved_reified": QUERIES_TEMPLATES.get_template("reified_movement_cross_instance.rq"),
    "changed_reified": QUERIES_TEMPLATES.get_template("reified_movement_cross_property.rq"),
    "count_added_reified": QUERIES_TEMPLATES.get_template("count_reified_properties_additions.rq"),
    "count_deleted_reified": QUERIES_TEMPLATES.get_template("count_reified_properties_deletions.rq"),
    "count_updated_reified": QUERIES_TEMPLATES.get_template("count_reified_property_value_updates.rq"),
    "count_moved_reified": QUERIES_TEMPLATES.get_template("count_reified_movement_cross_instance.rq"),
    "count_changed_reified": QUERIES_TEMPLATES.get_template("count_reified_movement_cross_property.rq")
}

TYPE_OF_ACTION_MAPPING = {
    "added_instance": "addition",
    "deleted_instance": "deletion",
    "count_added_instance": "count",
    "count_deleted_instance": "count",
    "added_property": "addition",
    "deleted_property": "deletion",
    "updated_property": "updated",
    "moved_property": "moved",
    "changed_property": "changed",
    "count_added_property": "count",
    "count_deleted_property": "count",
    "count_updated_property": "count",
    "count_moved_property": "count",
    "count_changed_property": "count",
    "added_reified": "addition",
    "deleted_reified": "deletion",
    "updated_reified": "updated",
    "moved_reified": "moved",
    "changed_reified": "changed",
    "count_added_reified": "count",
    "count_deleted_reified": "count",
    "count_updated_reified": "count",
    "count_moved_reified": "count",
    "count_changed_reified": "count"
}

INSTANCE_OPERATIONS = ["added_instance", "deleted_instance"]
PROPERTIES_OPERATIONS = ["added_property", "deleted_property", "updated_property", "moved_property", "changed_property"]
REIFIED_PROPERTIES_OPERATIONS = ["added_reified", "deleted_reified", "updated_reified", "moved_reified",
                                 "changed_reified"]

TEMPLATE_AND_HTML_FILE_NAME_MAPPING = {"main.html": HTML_TEMPLATES.get_template("main.jinja2"),
                                       "statistics.html": HTML_TEMPLATES.get_template("statistics.jinja2")}

QUERY_FALLBACK_LANGUAGES = ["en"]