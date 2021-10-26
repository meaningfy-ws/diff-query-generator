#!/usr/bin/python3

# query_generator.py
# Date:  30/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com
from jinja2 import Template

from dqgen.adapters import template_builder
from dqgen.services.base_generator import BaseGenerator


class QueryGenerator(BaseGenerator):
    """
    This class will generate a SPARQL query file from a query template file
    """

    def __init__(self, cls: str, operation: str, output_folder_path: str, template: Template, prop: str = None,
                 object_property: str = None, new_version_graph: str = None, old_version_graph: str = None,
                 version_history_graph: str = None, language: str = "en"):
        super().__init__(cls, operation, output_folder_path, template, prop, object_property, new_version_graph,
                         old_version_graph, version_history_graph, language)
        self.file_extension = "rq"

    def build_template(self):
        """
            This method builds a desired SPARQL query from the template
        :return: the string representation of the SPARQL query
        """
        return template_builder.build_query_template(jinja2_template=self.template, cls=self.cls, prop=self.prop,
                                                     obj_prop=self.object_property, new_version=self.new_version_graph,
                                                     old_version=self.old_version_graph,
                                                     version_history_graph=self.version_history_graph,
                                                     lang=self.language)
