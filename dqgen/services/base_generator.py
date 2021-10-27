#!/usr/bin/python3

# base_generator.py
# Date:  30/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com
from jinja2 import Template

from dqgen.adapters import file_name_builder


class BaseGenerator:
    """
    This class will generate a file from a template file
    """

    def __init__(self, cls: str, operation: str, output_folder_path: str, template: Template,
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
        self.file_extension = "base"

    def build_template(self):
        """
            This method builds a jinja template
        """
        return Template(self.template)

    def build_file_name(self, file_extension):
        """
            This method will build the file name
        :return:
        """
        return file_name_builder.make_file_name(operation=self.operation,
                                                cls=self.cls,
                                                prop=self.prop,
                                                obj_prop=self.object_property,
                                                file_extension=file_extension)

    def build_file_path(self):
        """
            This method will build the file path for the generated template
        :return:
        """
        return file_name_builder.make_file_path(output_folder_path=self.output_folder_path,
                                                file_name=self.build_file_name(file_extension=self.file_extension))

    def to_file(self):
        """
            Writes the generated template to a file.
        """
        self.build_template().dump(self.build_file_path())
