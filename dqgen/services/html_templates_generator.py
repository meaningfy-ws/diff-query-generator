#!/usr/bin/python3

# query_generator.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com
import logging
import pathlib
from pathlib import Path
from shutil import copyfile

import numpy as np
import pandas as pd
from jinja2 import Template

from dqgen.adapters.ap_reader import read_ap_from_csv
from dqgen.adapters.resource_fetcher import get_static_folder_file_paths

from dqgen.services import INSTANCE_OPERATIONS, PROPERTIES_OPERATIONS,REIFIED_PROPERTIES_OPERATIONS
from dqgen.services.html_template_registry import HtmlTemplateRegistry
from dqgen.services.html_generator import HtmlGenerator
from dqgen.services.html_templates_data_source_builder import build_datasource_for_html_template, camel_case_to_words
from dqgen.services.queries_generator import OUTPUT_FOLDER_PATH, APS_FOLDER_PATH
from dqgen.services.validate_application_profile import is_valid_ap


def generate_class_level_html_templates(processed_csv_file: pd.DataFrame,html_output_folder_path):
    """
        generate html templates for each class in the configuration CSV.
    """

    for cls in processed_csv_file["class"].unique():
        for operation in INSTANCE_OPERATIONS:
            class_name = cls.split(":")[1]
            class_folder_name = class_name.lower()
            output_folder_path = html_output_folder_path + "/" + class_folder_name
            pathlib.Path(output_folder_path).mkdir(parents=True, exist_ok=True)
            HtmlGenerator(cls=cls, operation=operation,
                          class_name=camel_case_to_words(class_name).title(),
                          output_folder_path=output_folder_path,
                          template=HtmlTemplateRegistry().INSTANCES).to_file()
    logging.info("Generated instance html templates ...")


def generate_property_level_html_templates(processed_csv_file: pd.DataFrame, html_output_folder_path):
    """
        generate html template for data properties and their values for each instance in the configuration CSV
    """
    for index, row in processed_csv_file.iterrows():

        if not row["object property"]:
            for operation in PROPERTIES_OPERATIONS:
                class_folder_name = row["class"].split(":")[1].lower()
                if row["property group"] and row["property group"] is not np.NaN:
                    property_group_folder = row["property group"].replace(" ", "_")
                    output_folder_path = html_output_folder_path + "/" + class_folder_name + "/" + property_group_folder
                else:
                    output_folder_path = html_output_folder_path + "/" + class_folder_name
                pathlib.Path(output_folder_path).mkdir(parents=True, exist_ok=True)
                HtmlGenerator(cls=row["class"],
                              prop=row["property"],
                              prop_name=camel_case_to_words(row["property"].split(":")[1]).lower(),
                              operation=operation,
                              output_folder_path=output_folder_path,
                              template=HtmlTemplateRegistry().PROPERTIES).to_file()

    logging.info("Generated property html templates ...")


def generate_reified_property_level_html_templates(processed_csv_file: pd.DataFrame, html_output_folder_path):
    """
        generate html template of reified structures for each instance in the configuration CSV
    """
    for index, row in processed_csv_file.iterrows():
        if row["object property"]:
            for operation in REIFIED_PROPERTIES_OPERATIONS:
                class_folder_name = row["class"].split(":")[1].lower()
                if row["property group"] and row["property group"] is not np.NaN:
                    property_group_folder = row["property group"].replace(" ", "_")
                    output_folder_path = html_output_folder_path + "/" + class_folder_name + "/" + property_group_folder
                else:
                    output_folder_path = html_output_folder_path + "/" + class_folder_name
                pathlib.Path(output_folder_path).mkdir(parents=True, exist_ok=True)
                HtmlGenerator(cls=row["class"],
                              prop=row["property"],
                              object_property=row["object property"],
                              prop_name=camel_case_to_words(row["property"].split(":")[1]).lower(),
                              operation=operation,
                              output_folder_path=output_folder_path,
                              template=HtmlTemplateRegistry().REIFIED_PROPERTIES).to_file()

    logging.info("Generated reified property html templates ...")


def generate_main_html(processed_csv_file: pd.DataFrame, html_output_folder_path):
    """
    Builds main.html page and puts into a specified folder
    :param processed_csv_file:
    :param html_output_folder_path:
    :return:
    """

    data_source = build_datasource_for_html_template(processed_csv_file=processed_csv_file)
    build_template = Template(HtmlTemplateRegistry().MAIN).stream(data_source=data_source)
    build_template.dump(html_output_folder_path + "/" + "main.html")


def copy_files_from_static_folder(file_list: list, destination_folder: str):
    """
    Copy the files from the static folder to a specified destination
    :param file_list:
    :param destination_folder:
    """
    for file in file_list:
        file_name = file.name
        copyfile(file, destination_folder + "/" + file_name)


def generate_html_templates_from_csv(ap_file_name: str, output_base_dir=OUTPUT_FOLDER_PATH,
                                     aps_folder_path=APS_FOLDER_PATH):
    """
        generates a set of html templates from the configuration CSV
    """
    processed_csv_file = read_ap_from_csv(aps_folder_path / ap_file_name)
    if not is_valid_ap(application_profile_df=processed_csv_file):
        raise Exception("The chosen application profile is not valid.")
    output = Path(output_base_dir) / Path(ap_file_name).stem
    html_output = output / "html"
    html_output.mkdir(parents=True, exist_ok=True)

    generate_class_level_html_templates(processed_csv_file=processed_csv_file, html_output_folder_path=str(html_output))
    generate_property_level_html_templates(processed_csv_file=processed_csv_file,
                                           html_output_folder_path=str(html_output))
    generate_reified_property_level_html_templates(processed_csv_file=processed_csv_file,
                                                   html_output_folder_path=str(html_output))
    generate_main_html(processed_csv_file=processed_csv_file,
                       html_output_folder_path=str(html_output))
    copy_files_from_static_folder(file_list=get_static_folder_file_paths(), destination_folder=str(html_output))
