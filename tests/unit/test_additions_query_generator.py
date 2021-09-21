import shutil
from pathlib import Path

from dqgen.adapters.resource_fetcher import get_file_content
from dqgen.services.additions_query_generator import InstanceAdditionsGenerator, SimplePropertyAdditionsGenerator, \
    ReifiedPropertyAdditionsGenerator


def test_instance_additions_generator():
    output_folder_path = "../test_data/output"
    expected_query_text = """  FILTER NOT EXISTS {
    GRAPH ?oldVersionGraph {
      ?instance ?p [] .
    }"""
    query_generator = InstanceAdditionsGenerator(cls="skos:Concept", operation="added_instance",
                                                 output_folder_path=output_folder_path)
    generated_file_path = query_generator.build_file_path()
    print(generated_file_path)
    query_generator.to_file()

    generated_file_content = get_file_content(generated_file_path)
    assert Path(generated_file_path).is_file()
    assert isinstance(generated_file_content, str)
    assert expected_query_text in generated_file_content
    # delete the generated test output folder
    shutil.rmtree(Path(output_folder_path).resolve(), ignore_errors=True)


def test_simple_property_additions_generator():
    output_folder_path = "../test_data/output"
    expected_query_text = """  FILTER NOT EXISTS {
    GRAPH ?deletionsGraph {
      [] ?property ?value .
    }
  }"""
    query_generator = SimplePropertyAdditionsGenerator(cls="skos:Concept", operation="added_property",
                                                       property="skos:notation",
                                                       output_folder_path=output_folder_path)
    generated_file_path = query_generator.build_file_path()
    print(generated_file_path)
    query_generator.to_file()

    generated_file_content = get_file_content(generated_file_path)
    assert Path(generated_file_path).is_file()
    assert isinstance(generated_file_content, str)
    assert expected_query_text in generated_file_content
    # delete the generated test output folder
    shutil.rmtree(Path(output_folder_path).resolve(), ignore_errors=True)


def test_reified_property_additions_generator():
    output_folder_path = "../test_data/output"
    expected_query_text = """  FILTER NOT EXISTS {
    GRAPH ?deletionsGraph {
        [] ?property ?object .
        ?object ?objProperty ?value .
    }
  }"""
    query_generator = ReifiedPropertyAdditionsGenerator(cls="skos:Concept", operation="added_reified",
                                                        property="skosxl:prefLabel",
                                                        object_property="skosxl:literalForm",
                                                        output_folder_path=output_folder_path)
    generated_file_path = query_generator.build_file_path()
    print(generated_file_path)
    query_generator.to_file()

    generated_file_content = get_file_content(generated_file_path)
    assert Path(generated_file_path).is_file()
    assert isinstance(generated_file_content, str)
    assert expected_query_text in generated_file_content
    # delete the generated test output folder
    shutil.rmtree(Path(output_folder_path).resolve(), ignore_errors=True)
