#!/usr/bin/python3

# additions_query_generator.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com

""" """
from dqgen.adapters import template_builder, query_file_name_builder
from dqgen.services.base_query_generator import BaseQueryGenerator
from dqgen.services.query_template_registry import QueryTemplateRegistry


class SimplePropertyValueUpdatesGenerator(BaseQueryGenerator):
    """
        This class will build the property value updates query as a file and
        will put the file into the defined output folder
    """

    def __init__(self, cls: str, property: str, operation, output_folder_path: str):
        self.cls = cls
        self.operation = operation
        self.output_folder_path = output_folder_path
        self.property = property

    def build_file_path(self):
        return query_file_name_builder.make_query_file_name(output_folder_path=self.output_folder_path,
                                                            operation=self.operation,
                                                            cls=self.cls,
                                                            prop=self.property)

    def build_query_template(self):
        template = QueryTemplateRegistry().PROPERTY_VALUE_UPDATES
        output = template_builder.build_template(jinja2_template=template, cls=self.cls, prop=self.property)

        return output


