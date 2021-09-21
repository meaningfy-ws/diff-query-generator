import pathlib
import shutil

from dqgen.adapters.query_file_name_builder import make_query_file_name


def test_make_query_file_name():
    file_name = make_query_file_name(output_folder_path="output/", operation="added_instance", cls="skos:Concept")
    assert file_name == "output/added_instance_concept.rq"
    shutil.rmtree(pathlib.Path("output/").resolve(), ignore_errors=True)
