#!/usr/bin/python3

# template_builder.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
from jinja2 import Template
import jinja2.environment


def build_template(jinja2_template: str, cls: str, prop: str = None, obj_prop: str = None, lang: str = "en",
                   version_history_graph: str = None,
                   old_version: str = None, new_version: str = None) -> jinja2.environment.TemplateStream:
    """
        given a jinja template and a set of (data) parameters render the template.
    :param old_version:
    :param new_version:
    :param version_history_graph:
    :param lang:
    :param obj_prop:
    :param prop:
    :param cls:
    :param jinja2_template:
    :return:
    """
    return Template(jinja2_template).stream(cls=cls,
                                            prop=prop,
                                            obj_prop=obj_prop,
                                            lang=lang,
                                            versionHistoryGraph=version_history_graph,
                                            oldVersion=old_version,
                                            newVersion=new_version)
