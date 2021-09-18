#!/usr/bin/python3

# query_template_registry.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com

"""
    This modules provides an easy access to the SPARQL queries templates from resources
"""
from dqgen.adapters.resource_fetcher import get_query_template


class QueryTemplateRegistry:

    @property
    def INSTANCE_ADDITIONS(self) -> str:
        return get_query_template("instance_additions.rq")

    @property
    def PROPERTY_ADDITIONS(self) -> str:
        return get_query_template("property_additions.rq")

    @property
    def REIFIED_PROPERTY_ADDITIONS(self) -> str:
        return get_query_template("reified_properties_additions.rq")
