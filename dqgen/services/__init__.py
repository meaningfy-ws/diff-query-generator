#!/usr/bin/python3

# __init__.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

"""
    Defining maps between operation and necessary template for classes, proprieties and reified properties
"""
from dqgen.services.query_template_registry import QueryTemplateRegistry

CLASSES_OPERATION_TEMPLATE_MAPPING = {"added_instance": QueryTemplateRegistry().INSTANCE_ADDITIONS,
                                      "deleted_instance": QueryTemplateRegistry().INSTANCE_DELETIONS}
PROPERTIES_OPERATION_TEMPLATE_MAPPING = {"added_property": QueryTemplateRegistry().PROPERTY_ADDITIONS,
                                         "deleted_property": QueryTemplateRegistry().PROPERTY_DELETIONS,
                                         "value_update_property": QueryTemplateRegistry().PROPERTY_VALUE_UPDATES,
                                         "movement_cross_instance": QueryTemplateRegistry().PROPERTY_MOVEMENT_CROSS_INSTANCE,
                                         "movement_cross_property": QueryTemplateRegistry().PROPERTY_MOVEMENT_CROSS_PROP

                                         }
REIFIED_PROPERTIES_OPERATION_TEMPLATE_MAPPING = {"added_reified": QueryTemplateRegistry().REIFIED_PROPERTY_ADDITIONS,
                                                 "deleted_reified": QueryTemplateRegistry().REIFIED_PROPERTY_DELETIONS,
                                                 "value_update_reified": QueryTemplateRegistry().REIFIED_PROPERTY_VALUE_UPDATES,
                                                 "reified_movement_cross_instance": QueryTemplateRegistry().PROPERTY_MOVEMENT_CROSS_INSTANCE,
                                                 "reified_movement_cross_property": QueryTemplateRegistry().PROPERTY_MOVEMENT_CROSS_PROP
                                                 }
