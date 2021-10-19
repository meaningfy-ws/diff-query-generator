#!/usr/bin/python3

# query_template_registry.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com

"""
    This modules provides an easy access to the html templates from resources
"""
from dqgen.adapters.resource_fetcher import get_html_template


class HtmlTemplateRegistry:
    """
    This class holds a registry to the SPARQL template queries files
    """
    @property
    def INSTANCES(self) -> str:
        return get_html_template("instance.jinja2")

    @property
    def PROPERTIES(self) -> str:
        return get_html_template("property.jinja2")

    @property
    def REIFIED_PROPERTIES(self) -> str:
        return get_html_template("reified_property.jinja2")
    @property
    def MAIN(self) -> str:
        return get_html_template("main.jinja2")

    @property
    def PROP_GROUP_SECTION(self) -> str:
        return get_html_template("prop_group_section.jinja2")

