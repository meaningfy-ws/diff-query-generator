from pathlib import Path

from dqgen.adapters.resource_fetcher import get_file_content
from dqgen.services.query_generator import QueryGenerator
from dqgen.services.query_template_registry import QueryTemplateRegistry


def test_instance_additions_generator(tmp_path):
    expected_query_text = """  FILTER NOT EXISTS {
    GRAPH ?oldVersionGraph {
      ?instance ?p [] .
    }"""
    query_generator = QueryGenerator(cls="skos:Concept", operation="added_instance",
                                     output_folder_path=str(tmp_path),
                                     template=QueryTemplateRegistry().INSTANCE_ADDITIONS)

    generated_file_path = query_generator.build_file_path()
    print(generated_file_path)
    query_generator.to_file()

    generated_file_content = get_file_content(generated_file_path)
    assert Path(generated_file_path).is_file()
    assert isinstance(generated_file_content, str)
    assert expected_query_text in generated_file_content


def test_simple_property_additions_generator(tmp_path):
    expected_query_text = """  FILTER NOT EXISTS {
    GRAPH ?deletionsGraph {
      [] ?property ?value .
    }
  }"""
    query_generator = QueryGenerator(cls="skos:Concept", operation="added_property",
                                     prop="skos:notation",
                                     output_folder_path=str(tmp_path),
                                     template=QueryTemplateRegistry().PROPERTY_ADDITIONS)
    generated_file_path = query_generator.build_file_path()
    print(generated_file_path)
    query_generator.to_file()

    generated_file_content = get_file_content(generated_file_path)
    assert Path(generated_file_path).is_file()
    assert isinstance(generated_file_content, str)
    assert expected_query_text in generated_file_content


def test_reified_property_additions_generator(tmp_path):
    expected_query_text = """  FILTER NOT EXISTS {
    GRAPH ?deletionsGraph {
        [] ?property ?object .
        ?object ?objProperty ?value .
    }
  }"""
    query_generator = QueryGenerator(cls="skos:Concept", operation="added_reified",
                                     prop="skosxl:prefLabel",
                                     object_property="skosxl:literalForm",
                                     output_folder_path=str(tmp_path),
                                     template=QueryTemplateRegistry().REIFIED_PROPERTY_ADDITIONS)
    generated_file_path = query_generator.build_file_path()
    print(generated_file_path)
    query_generator.to_file()

    generated_file_content = get_file_content(generated_file_path)
    assert Path(generated_file_path).is_file()
    assert isinstance(generated_file_content, str)
    assert expected_query_text in generated_file_content

