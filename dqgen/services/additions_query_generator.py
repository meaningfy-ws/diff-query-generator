#!/usr/bin/python3

# additions_query_generator.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
from dqgen.services.base_query_generator import BaseQueryGenerator


class InstanceAdditionsGenerator(BaseQueryGenerator):
    """
        TBD
    """

    def build_query(self) -> str:
        # template = resource_fetcher.get_template(INSTANCE_TEMPLATE)
        # output = template_builder.build(template,p1,p2,p3)
        # return output
        pass


class SimplePropertyAdditionsGenerator(BaseQueryGenerator):
    """
        TBD
    """

    def build_query(self) -> str:
        pass
