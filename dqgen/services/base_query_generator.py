#!/usr/bin/python3

# base_query_generator.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
import abc


class BaseQueryGenerator(abc.ABC):

    @abc.abstractmethod
    def build_query_template(self):
        """
            This method builds a desired SPARQL query from the template
        :return: the string representation of the SPARQL query
        """
        pass

    @abc.abstractmethod
    def build_file_path(self):
        """
            This method will build the file and file path for the generated query
        :return:
        """
        pass

    def to_file(self):
        """
            Writes the generated query to a file.
        :param file_name:
        :param query:
        """
        self.build_query_template().dump(self.build_file_path())
