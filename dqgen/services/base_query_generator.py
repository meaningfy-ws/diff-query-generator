#!/usr/bin/python3

# base_query_generator.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
import abc
import pathlib


class BaseQueryGenerator(abc.ABC):

    @abc.abstractmethod
    def build_query(self) -> str:
        """
            This method builds a desired SPARQL query from the template
        :return: the string representation of the SPARQL query
        """

    def to_file(self, output_file_path: pathlib.PathPath):
        """
            Writes the generated query to a file.
        :param output_file_path:
        :return:
        """
        output_file_path.open('w').write(self.build_query())
