import pathlib

from dqgen.adapters.ap_reader import read_ap_from_csv
from dqgen.services.html_templates_data_source_builder import camel_case_to_words, build_datasource_for_html_template


def test_camel_case_to_words():
    example = "orderedCollection"
    transformed_example = camel_case_to_words(example)
    assert isinstance(transformed_example, str)
    assert transformed_example == "ordered Collection"


def test_build_datasource_for_html_template():
    path_to_csv_file = pathlib.Path(__file__).parent.parent / "test_data" / "aps" / "src_ap_mod.csv"
    df = read_ap_from_csv(path_to_csv_file)
    data_source = build_datasource_for_html_template(processed_csv_file=df)
    assert isinstance(data_source, dict)
    assert 'skos:Concept', 'skos:Collection' in data_source.keys()
    assert "label", "prop_groups" in data_source["skos:Concept"].keys()
