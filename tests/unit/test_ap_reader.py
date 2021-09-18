import pathlib

import pandas as pd

from dqgen.adapters.ap_reader import read_ap_from_csv


def test_read_ap_from_csv():
    path_to_csv_file = pathlib.Path(__file__).parent.parent / "test_data" / "aps" / "skos_core.csv"
    result = read_ap_from_csv(path_to_csv_file)
    assert isinstance(result, pd.DataFrame)
    assert result["class"].values[1] == "skos:Concept"
    assert len(result.columns) == 5
    assert len(result) == 28

