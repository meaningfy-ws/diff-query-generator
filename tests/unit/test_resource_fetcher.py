import pathlib

from dqgen.adapters.resource_fetcher import get_file_content, get_query_template, get_html_template


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


def test_get_query_template():
    html_template = get_html_template("instance.jinja2")
    html_template_text = """{% raw %}
{% import "macros.html" as mc %}
{% endraw %}"""
    assert isinstance(html_template, str)
    assert html_template_text in html_template
