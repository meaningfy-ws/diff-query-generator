import pathlib

from dqgen.adapters.resource_fetcher import get_file_content


def test_get_file_content():
    path = "../test_data/test_files/sparqrl_query.rq"
    result = get_file_content(path)

    assert isinstance(result, str)
    assert "?person foaf:name ?name " in result