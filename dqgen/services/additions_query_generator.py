#!/usr/bin/python3

# additions_query_generator.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
from dqgen.adapters import template_builder, query_file_name_builder
from dqgen.services.base_query_generator import BaseQueryGenerator
from dqgen.services.query_template_registry import QueryTemplateRegistry


class InstanceAdditionsGenerator(BaseQueryGenerator):
    """
        This class will build the instance additions query as a file and
        will put the file into the defined output folder
    """

    def __init__(self, cls: str, operation, output_folder_path: str):
        self.cls = cls
        self.operation = operation
        self.output_folder_path = output_folder_path

    def build_file_path(self):
        return query_file_name_builder.make_query_file_name(output_folder_path=self.output_folder_path,
                                                            operation=self.operation,
                                                            cls=self.cls)

    def build_query_template(self):
        template = QueryTemplateRegistry().INSTANCE_ADDITIONS
        output = template_builder.build_template(jinja2_template=template, cls=self.cls)

        return output

# class SimplePropertyAdditionsGenerator(BaseQueryGenerator):
#     """
#         TBD
#     """
#
#     def build_query_template(self) -> str:
#         pass
