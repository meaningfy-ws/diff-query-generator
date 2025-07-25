#!/usr/bin/python3

# ap_reader.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com
import pathlib

import pandas as pd

"""
    This module is responsible for reading an application profile (for diffing) from a CSV file.
"""
NA_VALUES = {"class": "", "property": "", "object property": "", "preview property": "", "preview object property": ""}


def read_ap_from_csv(ap_csv_file_path: pathlib.Path):
    """
    This will read the csv file and it will return a Dataframe with the file content
    :param ap_csv_file_path:
    :return:
    """
    return pd.read_csv(ap_csv_file_path).fillna(NA_VALUES)
