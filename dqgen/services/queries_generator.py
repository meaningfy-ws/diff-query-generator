#!/usr/bin/python3

# query_generator.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com
import logging
from pathlib import Path


import pandas as pd

from dqgen.adapters.ap_reader import read_ap_from_csv
from dqgen.services import CLASSES_OPERATION_TEMPLATE_MAPPING, PROPERTIES_OPERATION_TEMPLATE_MAPPING, \
    REIFIED_PROPERTIES_OPERATION_TEMPLATE_MAPPING
from dqgen.services.query_generator import QueryGenerator


OUTPUT_FOLDER_PATH = "output/"
APS_FOLDER_PATH = Path(__file__).parent.parent / "resources" / "aps"


def generate_class_level_queries(processed_csv_file: pd.DataFrame, output_folder_path=OUTPUT_FOLDER_PATH):
    """
        generate queries for each class in the configuration CSV.
    """

    for cls in processed_csv_file["class"].unique():
        for operation, template in CLASSES_OPERATION_TEMPLATE_MAPPING.items():
            QueryGenerator(cls=cls, operation=operation,
                           output_folder_path=output_folder_path, template=template).to_file()

    logging.info("Generated instance queries ...")


def generate_property_level_queries(processed_csv_file: pd.DataFrame, output_folder_path=OUTPUT_FOLDER_PATH):
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
                               template=template).to_file()

    logging.info("Generated property queries ...")


def generate_reified_property_level_queries(processed_csv_file: pd.DataFrame, output_folder_path=OUTPUT_FOLDER_PATH):
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
                               template=template).to_file()

    logging.info("Generated reified property queries ...")


def generate_from_csv(ap_file_name: str, output_base_dir=OUTPUT_FOLDER_PATH, aps_folder_path=APS_FOLDER_PATH):
    """
        generates a set of diff queries from the configuration CSV
    """
    output = Path(output_base_dir) / Path(ap_file_name).stem
    queries_output = output / "queries"
    queries_output.mkdir(parents=True, exist_ok=True)

    processed_csv_file = read_ap_from_csv(aps_folder_path / ap_file_name)

    generate_class_level_queries(processed_csv_file=processed_csv_file, output_folder_path=str(queries_output))
    generate_property_level_queries(processed_csv_file=processed_csv_file, output_folder_path=str(queries_output))
    generate_reified_property_level_queries(processed_csv_file=processed_csv_file,
                                            output_folder_path=str(queries_output))
