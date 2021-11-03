from re import split

import pandas as pd

from dqgen.adapters.file_name_builder import make_file_path, make_file_name
from dqgen.services import INSTANCE_OPERATIONS, PROPERTIES_OPERATIONS, REIFIED_PROPERTIES_OPERATIONS


def camel_case_to_words(name: str):
    """
    This method will take a camel case string and will break it into words
    :param name: 
    :return: 
    """
    words = [word for word in split(r'(?=[A-Z])', name) if word]
    return ' '.join(words)


def generate_file_data(cls, class_folder_name, operation, prop=None, obj_prop=None):
    """
    This method will return a query file path and a count query file name
    :param cls: 
    :param class_folder_name: 
    :param operation: 
    :param prop: 
    :param obj_prop: 
    :return: 
    """
    file_path = make_file_path(output_folder_path=class_folder_name,
                               file_name=make_file_name(operation=operation,
                                                        cls=cls,
                                                        file_extension="html",
                                                        prop=prop, obj_prop=obj_prop))
    count_file_name = make_file_name(operation="count_" + operation,
                                     cls=cls,
                                     file_extension="rq",
                                     prop=prop, obj_prop=obj_prop)
    return file_path, count_file_name


def iterate_operations(operation_list, file_paths, count_queries, cls, class_folder_name, prop=None,
                       obj_prop=None):
    """
    This method will iterate through a list of operations. It will put one query file path in the file paths list
     and one count query name in the count query list
    :param operation_list: 
    :param file_paths: 
    :param count_queries: 
    :param cls: 
    :param class_folder_name: 
    :param prop: 
    :param obj_prop: 
    :return: 
    """
    for operation in operation_list:
        file_path, count_file_name = generate_file_data(cls=cls, class_folder_name=class_folder_name,
                                                        operation=operation, prop=prop, obj_prop=obj_prop)
        file_paths.append(file_path)
        count_queries.append(count_file_name)


def add_instance_changes(data_source, cls, class_name, class_folder_name):
    """
    This method will build the necessary data at the class level and it will add it to a data source dictionary
    :param data_source: 
    :param cls: 
    :param class_name: 
    :param class_folder_name: 
    :return: 
    """
    if "instance_changes" not in data_source[cls].keys():
        data_source[cls]["instance_changes"] = dict()
        data_source[cls]["instance_changes"] = {"label": camel_case_to_words(class_name).title()}
        instance_file_paths = []
        instance_count_queries = []

        iterate_operations(operation_list=INSTANCE_OPERATIONS, file_paths=instance_file_paths,
                           count_queries=instance_count_queries, cls=cls, class_folder_name=class_folder_name)

        data_source[cls]["instance_changes"].update(
            {"files": instance_file_paths, "count_queries": instance_count_queries})


def add_prop_group_details(data_source, prop_group_value, cls, prop_name, prop_file_paths, count_prop_file_paths):
    """
    This method will build the necessary data at the prop group level and it will add it to a data source dictionary
    :param prop_group_value: 
    :param data_source: 
    :param cls: 
    :param prop_name: 
    :param prop_file_paths: 
    :param count_prop_file_paths: 
    :return: 
    """
    if prop_group_value not in data_source[cls]["prop_groups"].keys():
        data_source[cls]["prop_groups"][prop_group_value] = {"label": prop_group_value.title()}
        data_source[cls]["prop_groups"][prop_group_value].update({"query_template_file_paths": prop_file_paths})
        data_source[cls]["prop_groups"][prop_group_value].update({"count_queries": {prop_name: {}}})
        data_source[cls]["prop_groups"][prop_group_value]["count_queries"][prop_name].update(
            {"files": count_prop_file_paths, "label": prop_name})
    else:
        data_source[cls]["prop_groups"][prop_group_value]["query_template_file_paths"].extend(prop_file_paths)
        data_source[cls]["prop_groups"][prop_group_value]["count_queries"].update(
            {prop_name: {"files": count_prop_file_paths, "label": prop_name}})


def build_datasource_for_html_template(processed_csv_file: pd.DataFrame) -> dict:
    """
    This method will build a data source dictionary from a given application profile dataframe
    :param processed_csv_file: 
    :return: 
    """
    data_source = {}

    for index, row in processed_csv_file.iterrows():
        class_name = row["class"].split(":")[1]
        class_folder_name = class_name.lower()
        prop_group_folder = row["property group"].replace(" ", "_")

        if row["class"] not in data_source.keys():
            data_source[row["class"]] = {"label": camel_case_to_words(class_name).title(), "prop_groups": {}}

        add_instance_changes(data_source=data_source, cls=row["class"], class_name=class_name,
                             class_folder_name=class_folder_name)

        prop_file_paths = []
        count_queries = []

        if not row["object property"]:
            prop_name = row["property"]
            iterate_operations(operation_list=PROPERTIES_OPERATIONS, file_paths=prop_file_paths,
                               count_queries=count_queries, cls=row["class"],
                               class_folder_name=f'{class_folder_name}/{prop_group_folder}', prop=row["property"])
        else:
            prop_name = row["property"] + "/" + row["object property"]
            iterate_operations(operation_list=REIFIED_PROPERTIES_OPERATIONS, file_paths=prop_file_paths,
                               count_queries=count_queries, cls=row["class"],
                               class_folder_name=f'{class_folder_name}/{prop_group_folder}', prop=row["property"],
                               obj_prop=row["object property"])

        add_prop_group_details(data_source=data_source, prop_group_value=row["property group"], cls=row["class"],
                               prop_name=prop_name, prop_file_paths=prop_file_paths,
                               count_prop_file_paths=count_queries)

    return data_source
