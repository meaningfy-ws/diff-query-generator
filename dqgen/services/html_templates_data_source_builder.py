from re import split

import pandas as pd

from dqgen.adapters.query_file_name_builder import make_query_file_name
from dqgen.services import INSTANCE_OPERATIONS, PROPERTIES_OPERATIONS, REIFIED_PROPERTIES_OPERATIONS


# def build_datasource_for_html_template(processed_csv_file: pd.DataFrame):
#     data_source = {}
#     for index, row in processed_csv_file.iterrows():
#         class_folder = row["class"].split(":")[1].lower()
#         prop_group_folder = row["property_group"].replace(" ", "_")
#         if row["class"] not in data_source.keys():
#             data_source[row["class"]] = {"label": row["class name"], "prop_groups": {}}
#         if "instance_changes" not in data_source[row["class"]].keys():
#             data_source[row["class"]]["instance_changes"] = dict()
#             data_source[row["class"]]["instance_changes"] = {"label": row["class"]}
#             file_paths = []
#             for operation in INSTANCE_OPERATIONS:
#                 file_path = make_query_file_name(output_folder_path=class_folder, operation=operation, cls=row["class"],
#                                                  file_extension="html",
#                                                  prop=None, obj_prop=None)
#                 file_paths.append(file_path)
#                 data_source[row["class"]]["instance_changes"].update({"files": file_paths})
#
#         if not row["object property"]:
#             # file_paths = []
#             for operation in PROPERTIES_OPERATIONS:
#                 file_path = make_query_file_name(output_folder_path=class_folder + "/" + prop_group_folder,
#                                                  operation=operation, cls=row["class"],
#                                                  file_extension="html",
#                                                  prop=row["property"], obj_prop=None)
#                 if row["property_group"] not in data_source[row["class"]]["prop_groups"].keys():
#                     data_source[row["class"]]["prop_groups"][row["property_group"]] = {"label": row["property_group"]}
#                     data_source[row["class"]]["prop_groups"][row["property_group"]].update({"files": [file_path]})
#                 else:
#                     data_source[row["class"]]["prop_groups"][row["property_group"]]["files"].append(file_path)
#         if row["object property"]:
#             for operation in REIFIED_PROPERTIES_OPERATIONS:
#                 file_path = make_query_file_name(output_folder_path=class_folder + "/" + prop_group_folder,
#                                                  operation=operation, cls=row["class"],
#                                                  file_extension="html",
#                                                  prop=row["property"], obj_prop=row["object property"])
#                 if row["property_group"] not in data_source[row["class"]]["prop_groups"].keys():
#                     data_source[row["class"]]["prop_groups"][row["property_group"]] = {"label": row["property_group"]}
#                     data_source[row["class"]]["prop_groups"][row["property_group"]].update({"files": [file_path]})
#                 else:
#                     data_source[row["class"]]["prop_groups"][row["property_group"]]["files"].append(file_path)
#     print(data_source)

def camel_case_to_words(name: str):
    words = [word for word in split(r'(?=[A-Z])', name) if word]
    return ' '.join(words)


def build_datasource_for_html_template(processed_csv_file: pd.DataFrame) -> dict:
    data_source = {}
    for index, row in processed_csv_file.iterrows():
        class_name = row["class"].split(":")[1]
        class_folder_name = class_name.lower()
        prop_group_folder = row["property_group"].replace(" ", "_")
        if row["class"] not in data_source.keys():
            data_source[row["class"]] = {"label": row["class name"], "prop_groups": {}}
        if "instance_changes" not in data_source[row["class"]].keys():
            data_source[row["class"]]["instance_changes"] = dict()
            data_source[row["class"]]["instance_changes"] = {"label": camel_case_to_words(class_name).title()}
            instance_file_paths = []
            for operation in INSTANCE_OPERATIONS:
                file_path = make_query_file_name(output_folder_path=class_folder_name, operation=operation,
                                                 cls=row["class"],
                                                 file_extension="html",
                                                 prop=None, obj_prop=None)
                instance_file_paths.append(file_path)
            data_source[row["class"]]["instance_changes"].update({"files": instance_file_paths})
        prop_file_paths = []
        if not row["object property"]:
            for operation in PROPERTIES_OPERATIONS:
                file_path = make_query_file_name(output_folder_path=class_folder_name + "/" + prop_group_folder,
                                                 operation=operation, cls=row["class"],
                                                 file_extension="html",
                                                 prop=row["property"], obj_prop=None)
                prop_file_paths.append(file_path)
        else:
            for operation in REIFIED_PROPERTIES_OPERATIONS:
                file_path = make_query_file_name(output_folder_path=class_folder_name + "/" + prop_group_folder,
                                                 operation=operation, cls=row["class"],
                                                 file_extension="html",
                                                 prop=row["property"], obj_prop=row["object property"])
                prop_file_paths.append(file_path)

        if row["property_group"] not in data_source[row["class"]]["prop_groups"].keys():
            data_source[row["class"]]["prop_groups"][row["property_group"]] = {"label": row["property_group"].title()}
            data_source[row["class"]]["prop_groups"][row["property_group"]].update({"files": prop_file_paths})
        else:
            data_source[row["class"]]["prop_groups"][row["property_group"]]["files"].extend(prop_file_paths)
    return data_source
