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
    """
    This class holds a registry to the SPARQL template queries files
    """
    @property
    def INSTANCE_ADDITIONS(self) -> str:
        return get_query_template("instance_additions.rq")

    @property
    def PROPERTY_ADDITIONS(self) -> str:
        return get_query_template("property_additions.rq")

    @property
    def REIFIED_PROPERTY_ADDITIONS(self) -> str:
        return get_query_template("reified_properties_additions.rq")

    @property
    def INSTANCE_DELETIONS(self) -> str:
        return get_query_template("instance_deletions.rq")

    @property
    def PROPERTY_DELETIONS(self) -> str:
        return get_query_template("property_deletions.rq")

    @property
    def REIFIED_PROPERTY_DELETIONS(self) -> str:
        return get_query_template("reified_properties_deletions.rq")

    @property
    def PROPERTY_VALUE_UPDATES(self) -> str:
        return get_query_template("property_value_updates.rq")

    @property
    def REIFIED_PROPERTY_VALUE_UPDATES(self) -> str:
        return get_query_template("reified_property_value_updates.rq")

    @property
    def PROPERTY_MOVEMENT_CROSS_INSTANCE(self) -> str:
        return get_query_template("movement_cross_instance.rq")

    @property
    def REIFIED_PROPERTY_MOVEMENT_CROSS_INSTANCE(self) -> str:
        return get_query_template("reified_movement_cross_instance.rq")

    @property
    def PROPERTY_MOVEMENT_CROSS_PROP(self) -> str:
        return get_query_template("movement_cross_property.rq")

    @property
    def REIFIED_PROPERTY_MOVEMENT_CROSS_PROP(self) -> str:
        return get_query_template("reified_movement_cross_property.rq")