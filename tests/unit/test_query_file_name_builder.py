import pathlib
import shutil

from dqgen.adapters.query_file_name_builder import make_query_file_name


def test_make_query_file_name(tmp_path):
    file_name = make_query_file_name(output_folder_path=tmp_path, operation="added_instance", cls="skos:Concept")
    assert file_name == str(tmp_path) + "/" + "added_instance_concept.rq"

