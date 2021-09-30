import pathlib

from dqgen.adapters.resource_fetcher import get_file_content, get_query_template


def test_get_file_content():
    path = "../test_data/test_files/sparqrl_query.rq"
    result = get_file_content(path)

    assert isinstance(result, str)
    assert "?person foaf:name ?name " in result


def test_get_query_template():
    query = get_query_template("instance_additions.rq")
    query_text = """  FILTER NOT EXISTS {
    GRAPH ?oldVersionGraph {
      ?instance ?p [] .
    }"""
    assert isinstance(query, str)
    assert query_text in query
