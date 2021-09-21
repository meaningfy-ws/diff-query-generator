#!/usr/bin/python3

# query_generator.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

from pathlib import Path

import click
import pandas as pd

from dqgen.adapters.ap_reader import read_ap_from_csv
from dqgen.services.additions_query_generator import InstanceAdditionsGenerator, SimplePropertyAdditionsGenerator, \
    ReifiedPropertyAdditionsGenerator
from dqgen.services.deletions_query_generator import InstanceDeletionsGenerator, SimplePropertyDeletionsGenerator, \
    ReifiedPropertyDeletionsGenerator

OUTPUT_FOLDER_PATH = "output/"
APS_FOLDER_PATH = Path(__file__).parent.parent.parent / "resources" / "aps"


def generate_class_level_queries(processed_csv_file: pd.DataFrame, output_folder_path=OUTPUT_FOLDER_PATH):
    """
        generate queries for each class in the configuration CSV.
    """

    for cls in processed_csv_file["class"].unique():
        InstanceAdditionsGenerator(cls=cls, operation="added_instance",
                                   output_folder_path=output_folder_path).to_file()
        InstanceDeletionsGenerator(cls=cls, operation="deleted_instance",
                                   output_folder_path=output_folder_path).to_file()
    print("Generated instance queries ...")


def generate_property_level_queries(processed_csv_file: pd.DataFrame, output_folder_path=OUTPUT_FOLDER_PATH):
    """
        generate queries for data properties and their values for each instance in the configuration CSV
    """
    for index, row in processed_csv_file.iterrows():
        if not row["object property"]:
            SimplePropertyAdditionsGenerator(cls=row["class"],
                                             property=row["property"],
                                             operation="added_property",
                                             output_folder_path=output_folder_path).to_file()
            SimplePropertyDeletionsGenerator(cls=row["class"],
                                             property=row["property"],
                                             operation="deleted_property",
                                             output_folder_path=output_folder_path).to_file()
    print("Generated property queries ...")


def generate_reified_property_level_queries(processed_csv_file: pd.DataFrame, output_folder_path=OUTPUT_FOLDER_PATH):
    """
        generate queries of reified structures for each instance in the configuration CSV
    """
    for index, row in processed_csv_file.iterrows():
        if row["object property"]:
            ReifiedPropertyAdditionsGenerator(cls=row["class"],
                                              property=row["property"],
                                              object_property=row["object property"],
                                              operation="added_reified",
                                              output_folder_path=output_folder_path).to_file()
            ReifiedPropertyDeletionsGenerator(cls=row["class"],
                                              property=row["property"],
                                              object_property=row["object property"],
                                              operation="deleted_reified",
                                              output_folder_path=output_folder_path).to_file()
    print("Generated reified property queries ...")


def generate_from_csv(ap_file_name: str, output_base_dir=OUTPUT_FOLDER_PATH, aps_folder_path=APS_FOLDER_PATH):
    """
        generates a set of diff queries from the configuration CSV
    """
    output = Path(output_base_dir) / Path(ap_file_name).stem
    output.mkdir(parents=True, exist_ok=True)

    processed_csv_file = read_ap_from_csv(aps_folder_path / ap_file_name)

    generate_class_level_queries(processed_csv_file=processed_csv_file, output_folder_path=str(output))
    generate_property_level_queries(processed_csv_file=processed_csv_file, output_folder_path=str(output))
    generate_reified_property_level_queries(processed_csv_file=processed_csv_file, output_folder_path=str(output))


@click.command()
@click.argument("file_name")
def generate_queries(file_name):
    generate_from_csv(file_name)


if __name__ == '__main__':
    generate_queries()
