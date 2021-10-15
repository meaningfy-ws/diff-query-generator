#!/usr/bin/python3

# query_generator.py
# Date:  30/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com
from dqgen.adapters import query_file_name_builder, template_builder


class QueryGenerator:
    """
    This class will generate a SPARQL query file from a query template file
    """
    def __init__(self, cls: str, operation: str, output_folder_path: str, template: str,
                 prop: str = None,
                 object_property: str = None,
                 new_version_graph: str = None,
                 old_version_graph: str = None,
                 version_history_graph: str = None,
                 language: str = "en"):
        self.cls = cls
        self.operation = operation
        self.output_folder_path = output_folder_path
        self.prop = prop
        self.object_property = object_property
        self.template = template
        self.new_version_graph = new_version_graph
        self.old_version_graph = old_version_graph
        self.version_history_graph = version_history_graph
        self.language = language
        self.file_extension = "rq"

    def build_query_template(self):
        """
            This method builds a desired SPARQL query from the template
        :return: the string representation of the SPARQL query
        """
        return template_builder.build_query_template(jinja2_template=self.template, cls=self.cls, prop=self.prop,
                                                     obj_prop=self.object_property, new_version=self.new_version_graph,
                                                     old_version=self.old_version_graph,
                                                     version_history_graph=self.version_history_graph, lang=self.language)

    def build_file_path(self, file_extension):
        """
            This method will build the file and file path for the generated query
        :return:
        """
        return query_file_name_builder.make_query_file_name(output_folder_path=self.output_folder_path,
                                                            operation=self.operation,
                                                            cls=self.cls,
                                                            prop=self.prop,
                                                            obj_prop=self.object_property,
                                                            file_extension=file_extension)

    def to_file(self):
        """
            Writes the generated query to a file.
        :param file_name:
        :param query:
        """
        self.build_query_template().dump(self.build_file_path(file_extension=self.file_extension))
