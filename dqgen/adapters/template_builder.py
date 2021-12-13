#!/usr/bin/python3

# template_builder.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
from jinja2 import Template
import jinja2.environment


def build_query_template(jinja2_template: Template, cls: str, prop: str, obj_prop: str, languages: list,
                         version_history_graph: str, old_version: str, new_version: str, preview_property: str,
                         type_of_action: str) -> jinja2.environment.TemplateStream:
    """
        given a jinja template and a set of (data) parameters render the template.
    :param type_of_action:
    :param preview_property:
    :param old_version:
    :param new_version:
    :param version_history_graph:
    :param languages:
    :param obj_prop:
    :param prop:
    :param cls:
    :param jinja2_template:
    :return:
    """
    return jinja2_template.stream(cls=cls,
                                  prop=prop,
                                  obj_prop=obj_prop,
                                  languages=languages,
                                  versionHistoryGraph=version_history_graph,
                                  oldVersion=old_version,
                                  newVersion=new_version,
                                  preview_property=preview_property,
                                  type_of_action=type_of_action)


def build_html_template(jinja2_template: Template, query_file: str, cls: str, prop: str, obj_prop: str,
                        operation: str, class_name: str, prop_name: str,
                        obj_prop_name: str, data_source: dict = None) -> jinja2.environment.TemplateStream:
    """
        given a jinja template and a set of (data) parameters render the template.
    :param data_source:
    :param obj_prop_name:
    :param prop_name:
    :param class_name:
    :param operation:
    :param query_file:
    :param obj_prop:
    :param prop:
    :param cls:
    :param jinja2_template:
    :return:
    """
    return jinja2_template.stream(query_file=query_file,
                                  property=prop,
                                  object_property=obj_prop,
                                  operation=operation,
                                  cls=cls,
                                  class_name=class_name,
                                  property_name=prop_name,
                                  object_prop_name=obj_prop_name,
                                  data_source=data_source)
