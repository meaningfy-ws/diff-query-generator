#!/usr/bin/python3

# asciidoc_templates_generator.py
# Date:  2024
# Author: Generated for AsciiDoc template support
import logging
import pathlib
from shutil import copytree, copyfile
from pathlib import Path

import numpy as np
import pandas as pd
from dqgen.adapters.ap_reader import read_ap_from_csv

from dqgen.services import INSTANCE_OPERATIONS, PROPERTIES_OPERATIONS, REIFIED_PROPERTIES_OPERATIONS, ASCII_DOC_TEMPLATES, \
    PATH_TO_ASCIIDOC_STATIC_FOLDER, TEMPLATE_AND_ASCIIDOC_FILE_NAME_MAPPING
from dqgen.services.asciidoc_generator import AsciiDocGenerator
from dqgen.services.templates_data_source_builder import build_datasource_for_template, camel_case_to_words
from dqgen.services.validate_application_profile import validate_application_profile


def generate_class_level_asciidoc_templates(processed_csv_file: pd.DataFrame, asciidoc_output_folder_path):
    """
        generate AsciiDoc templates for each class in the configuration CSV.
    """

    for cls in processed_csv_file["class"].unique():
        for operation in INSTANCE_OPERATIONS:
            class_name = cls.split(":")[1]
            class_folder_name = class_name.lower()
            output_folder_path = asciidoc_output_folder_path + "/" + class_folder_name
            pathlib.Path(output_folder_path).mkdir(parents=True, exist_ok=True)
            AsciiDocGenerator(cls=cls, operation=operation,
                          class_name=camel_case_to_words(class_name).title(),
                          output_folder_path=output_folder_path,
                          template=ASCII_DOC_TEMPLATES.get_template("instance.jinja2")).to_file()
    logging.info("Generated instance AsciiDoc templates ...")


def generate_property_level_asciidoc_templates(processed_csv_file: pd.DataFrame, asciidoc_output_folder_path):
    """
        generate AsciiDoc template for data properties and their values for each instance in the configuration CSV
    """
    for index, row in processed_csv_file.iterrows():

        if not row["object property"]:
            for operation in PROPERTIES_OPERATIONS:
                class_folder_name = row["class"].split(":")[1].lower()
                if row["property group"] and row["property group"] is not np.NaN:
                    property_group_folder = row["property group"].replace(" ", "_")
                    output_folder_path = asciidoc_output_folder_path + "/" + class_folder_name + "/" + property_group_folder
                else:
                    output_folder_path = asciidoc_output_folder_path + "/" + class_folder_name
                pathlib.Path(output_folder_path).mkdir(parents=True, exist_ok=True)
                AsciiDocGenerator(cls=row["class"],
                              prop=row["property"],
                              prop_name=camel_case_to_words(row["property"].split(":")[1]).lower(),
                              operation=operation,
                              output_folder_path=output_folder_path,
                              template=ASCII_DOC_TEMPLATES.get_template("property.jinja2")).to_file()

    logging.info("Generated property AsciiDoc templates ...")


def generate_reified_property_level_asciidoc_templates(processed_csv_file: pd.DataFrame, asciidoc_output_folder_path):
    """
        generate AsciiDoc template of reified structures for each instance in the configuration CSV
    """
    for index, row in processed_csv_file.iterrows():
        if row["object property"]:
            for operation in REIFIED_PROPERTIES_OPERATIONS:
                class_folder_name = row["class"].split(":")[1].lower()
                if row["property group"] and row["property group"] is not np.NaN:
                    property_group_folder = row["property group"].replace(" ", "_")
                    output_folder_path = asciidoc_output_folder_path + "/" + class_folder_name + "/" + property_group_folder
                else:
                    output_folder_path = asciidoc_output_folder_path + "/" + class_folder_name
                pathlib.Path(output_folder_path).mkdir(parents=True, exist_ok=True)
                AsciiDocGenerator(cls=row["class"],
                              prop=row["property"],
                              object_property=row["object property"],
                              prop_name=camel_case_to_words(row["property"].split(":")[1]).lower(),
                              operation=operation,
                              output_folder_path=output_folder_path,
                              template=ASCII_DOC_TEMPLATES.get_template("reified_property.jinja2")).to_file()

    logging.info("Generated reified property AsciiDoc templates ...")


def generate_asciidoc_template(processed_csv_file: pd.DataFrame, asciidoc_output_folder_path, template, file_name):
    """
    Builds an AsciiDoc page and puts into a specified folder
    :param file_name:
    :param template:
    :param processed_csv_file:
    :param asciidoc_output_folder_path:
    :return:
    """

    data_source = build_datasource_for_template(processed_csv_file=processed_csv_file, file_extension='adoc')
    build_template = template.stream(data_source=data_source)
    build_template.dump(asciidoc_output_folder_path + "/" + file_name)


def copy_files_from_static_folder(file_list: list, destination_folder: str):
    """
    Copy the files from the static folder to a specified destination
    :param file_list:
    :param destination_folder:
    """
    for file in file_list:
        file_name = file.name
        copyfile(file, destination_folder + "/" + file_name)


def generate_asciidoc_templates_from_csv(ap_file_path: pathlib.Path, output_base_dir: pathlib.Path):
    """
        generates a set of AsciiDoc templates from the configuration CSV
    """
    processed_csv_file = read_ap_from_csv(ap_file_path)
    validate_application_profile(application_profile_df=processed_csv_file)
    output = Path(output_base_dir) / ap_file_path.stem
    asciidoc_output = output / "asciidoc"
    asciidoc_output.mkdir(parents=True, exist_ok=True)

    generate_class_level_asciidoc_templates(processed_csv_file=processed_csv_file, asciidoc_output_folder_path=str(asciidoc_output))
    generate_property_level_asciidoc_templates(processed_csv_file=processed_csv_file,
                                           asciidoc_output_folder_path=str(asciidoc_output))
    generate_reified_property_level_asciidoc_templates(processed_csv_file=processed_csv_file,
                                                   asciidoc_output_folder_path=str(asciidoc_output))

    for file_name, template in TEMPLATE_AND_ASCIIDOC_FILE_NAME_MAPPING.items():
        generate_asciidoc_template(processed_csv_file=processed_csv_file,
                               asciidoc_output_folder_path=str(asciidoc_output), template=template, file_name=file_name)

    # copy static files into the generated asciidoc output directory
    copytree(PATH_TO_ASCIIDOC_STATIC_FOLDER, str(asciidoc_output), dirs_exist_ok=True)

