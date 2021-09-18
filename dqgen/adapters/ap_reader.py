#!/usr/bin/python3

# ap_reader.py
# Date:  15/09/2021
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com
import pathlib

import pandas as pd

from dqgen.adapters.resource_fetcher import get_file_content

"""
    This module is responsible for reading an application profile (for diffing) from a CSV file.
"""
NA_VALUES = {"class": "", "property": "", "object property": "", "modifiable": 0, "language dependent": 0}


def read_ap_from_csv(ap_csv_file_path: pathlib.Path):
    """
    This will read the csv file and it will return a Dataframe with the file content
    :param ap_csv_file_path:
    :return:
    """
    return pd.read_csv(ap_csv_file_path).fillna(NA_VALUES)
