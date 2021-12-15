#!/usr/bin/python3

# query_generator.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com
import logging
import pathlib
from pathlib import Path


import pandas as pd

from dqgen.adapters.ap_reader import read_ap_from_csv
from dqgen.services import CLASSES_OPERATION_TEMPLATE_MAPPING, PROPERTIES_OPERATION_TEMPLATE_MAPPING, \
    REIFIED_PROPERTIES_OPERATION_TEMPLATE_MAPPING, TYPE_OF_ACTION_MAPPING
from dqgen.services.query_generator import QueryGenerator
from dqgen.services.validate_application_profile import validate_application_profile


def generate_class_level_queries(processed_csv_file: pd.DataFrame, output_folder_path):
    """
        generate queries for each class in the configuration CSV.
    """

    for cls in processed_csv_file["class"].unique():
        preview_property = processed_csv_file[(processed_csv_file["class"] == cls)]["preview property"].values[0]
        preview_object_property = processed_csv_file[(processed_csv_file["class"] == cls)]["preview object property"].values[0]
        for operation, template in CLASSES_OPERATION_TEMPLATE_MAPPING.items():
            QueryGenerator(cls=cls, operation=operation,
                           output_folder_path=output_folder_path, template=template,
                           type_of_action=TYPE_OF_ACTION_MAPPING[operation],
                           preview_property=preview_property,
                           preview_object_property=preview_object_property).to_file()

    logging.info("Generated instance queries ...")


def generate_property_level_queries(processed_csv_file: pd.DataFrame, output_folder_path):
    """
        generate queries for data properties and their values for each instance in the configuration CSV
    """
    for index, row in processed_csv_file.iterrows():
        if not row["object property"]:
            for operation, template in PROPERTIES_OPERATION_TEMPLATE_MAPPING.items():
                QueryGenerator(cls=row["class"],
                               prop=row["property"],
                               operation=operation,
                               output_folder_path=output_folder_path,
                               template=template,
                               preview_property=row["preview property"],
                               preview_object_property=row["preview object property"],
                               type_of_action=TYPE_OF_ACTION_MAPPING[operation]).to_file()

    logging.info("Generated property queries ...")


def generate_reified_property_level_queries(processed_csv_file: pd.DataFrame, output_folder_path):
    """
        generate queries of reified structures for each instance in the configuration CSV
    """
    for index, row in processed_csv_file.iterrows():
        if row["object property"]:
            for operation, template in REIFIED_PROPERTIES_OPERATION_TEMPLATE_MAPPING.items():
                QueryGenerator(cls=row["class"],
                               prop=row["property"],
                               object_property=row["object property"],
                               operation=operation,
                               output_folder_path=output_folder_path,
                               template=template,
                               preview_property=row["preview property"],
                               preview_object_property=row["preview object property"],
                               type_of_action=TYPE_OF_ACTION_MAPPING[operation]).to_file()

    logging.info("Generated reified property queries ...")


def generate_from_csv(ap_file_path:pathlib.Path, output_base_dir:pathlib.Path):
    """
        generates a set of diff queries from the configuration CSV
    """
    output = Path(output_base_dir) / ap_file_path.stem
    queries_output = output / "queries"
    queries_output.mkdir(parents=True, exist_ok=True)

    processed_csv_file = read_ap_from_csv(ap_file_path)
    validate_application_profile(application_profile_df=processed_csv_file)

    generate_class_level_queries(processed_csv_file=processed_csv_file, output_folder_path=str(queries_output))
    generate_property_level_queries(processed_csv_file=processed_csv_file, output_folder_path=str(queries_output))
    generate_reified_property_level_queries(processed_csv_file=processed_csv_file,
                                            output_folder_path=str(queries_output))
