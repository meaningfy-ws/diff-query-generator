import pathlib
import shutil

from dqgen.adapters.ap_reader import read_ap_from_csv
from dqgen.adapters.resource_fetcher import get_file_content
from dqgen.entrypoints.cli.query_generator import generate_class_level_queries, generate_from_csv

OUTPUT_FOLDER_PATH = "../test_data/output"
PATH_TO_APS = pathlib.Path(__file__).parent.parent / "test_data" / "aps"
PATH_TO_CSV_FILE = PATH_TO_APS / "skos_core.csv"


def test_generate_class_level_queries():
    expected_query_text = """  FILTER NOT EXISTS {
    GRAPH ?oldVersionGraph {
      ?instance ?p [] .
    }"""
    processed_csv_file = read_ap_from_csv(PATH_TO_CSV_FILE)
    generate_class_level_queries(processed_csv_file=processed_csv_file, output_folder_path=OUTPUT_FOLDER_PATH)
    generated_file_content = get_file_content("../test_data/output/added_instance_concept_scheme.rq")

    assert pathlib.Path(OUTPUT_FOLDER_PATH + "/added_instance_concept_scheme.rq").is_file()
    assert isinstance(generated_file_content, str)
    assert expected_query_text in generated_file_content
    # delete the generated test output folder
    shutil.rmtree(pathlib.Path(OUTPUT_FOLDER_PATH).resolve(), ignore_errors=True)


def test_generate_from_csv():
    generate_from_csv(ap_file_name="skos_core.csv",output_base_dir=OUTPUT_FOLDER_PATH, aps_folder_path=PATH_TO_APS)

    assert pathlib.Path(OUTPUT_FOLDER_PATH).is_dir()
    assert pathlib.Path(OUTPUT_FOLDER_PATH + "/skos_core").is_dir()
    assert pathlib.Path(OUTPUT_FOLDER_PATH + "/skos_core/" + "added_instance_concept_scheme.rq").is_file()

    # delete the generated test output folder
    shutil.rmtree(pathlib.Path(OUTPUT_FOLDER_PATH).resolve(), ignore_errors=True)