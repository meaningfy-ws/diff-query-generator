#!/usr/bin/python3

# query_generator.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com
import logging
import pathlib
from distutils.dir_util import copy_tree
from pathlib import Path
from shutil import copyfile

import numpy as np
import pandas as pd
from dqgen.adapters.ap_reader import read_ap_from_csv


from dqgen.services import INSTANCE_OPERATIONS, PROPERTIES_OPERATIONS, REIFIED_PROPERTIES_OPERATIONS, HTML_TEMPLATES, \
    PATH_TO_STATIC_FOLDER, TEMPLATE_AND_HTML_FILE_NAME_MAPPING
from dqgen.services.html_generator import HtmlGenerator
from dqgen.services.html_templates_data_source_builder import build_datasource_for_html_template, camel_case_to_words
from dqgen.services.validate_application_profile import validate_application_profile


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
                          template=HTML_TEMPLATES.get_template("instance.jinja2")).to_file()
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
                              template=HTML_TEMPLATES.get_template("property.jinja2")).to_file()

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
                              template=HTML_TEMPLATES.get_template("reified_property.jinja2")).to_file()

    logging.info("Generated reified property html templates ...")


def generate_html_template(processed_csv_file: pd.DataFrame, html_output_folder_path, template, file_name):
    """
    Builds a html page and puts into a specified folder
    :param file_name:
    :param template:
    :param processed_csv_file:
    :param html_output_folder_path:
    :return:
    """

    data_source = build_datasource_for_html_template(processed_csv_file=processed_csv_file)
    build_template = template.stream(data_source=data_source)
    build_template.dump(html_output_folder_path + "/" + file_name)


def copy_files_from_static_folder(file_list: list, destination_folder: str):
    """
    Copy the files from the static folder to a specified destination
    :param file_list:
    :param destination_folder:
    """
    for file in file_list:
        file_name = file.name
        copyfile(file, destination_folder + "/" + file_name)


def generate_html_templates_from_csv(ap_file_path: pathlib.Path, output_base_dir: pathlib.Path):
    """
        generates a set of html templates from the configuration CSV
    """
    processed_csv_file = read_ap_from_csv(ap_file_path)
    validate_application_profile(application_profile_df=processed_csv_file)
    output = Path(output_base_dir) / ap_file_path.stem
    html_output = output / "html"
    html_output.mkdir(parents=True, exist_ok=True)

    generate_class_level_html_templates(processed_csv_file=processed_csv_file, html_output_folder_path=str(html_output))
    generate_property_level_html_templates(processed_csv_file=processed_csv_file,
                                           html_output_folder_path=str(html_output))
    generate_reified_property_level_html_templates(processed_csv_file=processed_csv_file,
                                                   html_output_folder_path=str(html_output))

    for file_name, template in TEMPLATE_AND_HTML_FILE_NAME_MAPPING.items():
        generate_html_template(processed_csv_file=processed_csv_file,
                               html_output_folder_path=str(html_output), template=template, file_name=file_name)

    copy_tree(PATH_TO_STATIC_FOLDER, str(html_output))
