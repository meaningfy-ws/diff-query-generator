import pathlib

from dqgen.adapters.ap_reader import read_ap_from_csv
from dqgen.services.validate_application_profile import is_valid_ap


def test_is_valid_ap():
    path_to_csv_file_1 = pathlib.Path(__file__).parent.parent / "test_data" / "aps" / "skos_core.csv"
    path_to_csv_file_2 = pathlib.Path(__file__).parent.parent / "test_data" / "aps" / "src_ap_mod.csv"
    ap1 = read_ap_from_csv(path_to_csv_file_1)
    ap2 = read_ap_from_csv(path_to_csv_file_2)

    assert not is_valid_ap(ap1)
    assert is_valid_ap(ap2)
