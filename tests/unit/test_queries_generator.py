import pathlib
import shutil

from dqgen.adapters.ap_reader import read_ap_from_csv
from dqgen.adapters.resource_fetcher import get_file_content
from dqgen.services.queries_generator import generate_class_level_queries, generate_from_csv

PATH_TO_APS = pathlib.Path(__file__).parent.parent / "test_data" / "aps"
PATH_TO_CSV_FILE = PATH_TO_APS / "skos_core.csv"


def test_generate_class_level_queries(tmp_path):
    expected_query_text = """  FILTER NOT EXISTS {
    GRAPH ?oldVersionGraph {
      ?instance ?p [] .
    }"""
    processed_csv_file = read_ap_from_csv(PATH_TO_CSV_FILE)
    generate_class_level_queries(processed_csv_file=processed_csv_file, output_folder_path=tmp_path)
    generated_file_content = get_file_content(tmp_path/"added_instance_concept_scheme.rq")

    assert pathlib.Path(tmp_path / "added_instance_concept_scheme.rq").is_file()
    assert isinstance(generated_file_content, str)
    assert expected_query_text in generated_file_content


def test_generate_from_csv(tmp_path):
    generate_from_csv(ap_file_name="skos_core.csv",output_base_dir=tmp_path, aps_folder_path=PATH_TO_APS)

    assert pathlib.Path(tmp_path).is_dir()
    assert pathlib.Path(tmp_path / "skos_core").is_dir()
    assert pathlib.Path(tmp_path / "skos_core" / "added_instance_concept_scheme.rq").is_file()
