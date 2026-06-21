from pathlib import Path

from dqgen.adapters.resource_fetcher import get_file_content
from dqgen.services import QUERIES_TEMPLATES
from dqgen.services.query_generator import QueryGenerator


def test_instance_additions_generator(tmp_path):
    expected_query_text = """  FILTER NOT EXISTS {
    GRAPH ?oldVersionGraph {
      ?instance ?p [] .
    }"""
    query_generator = QueryGenerator(cls="skos:Concept", operation="added_instance",
                                     output_folder_path=str(tmp_path),
                                     template=QUERIES_TEMPLATES.get_template("instance_additions.rq"))

    generated_file_path = query_generator.build_file_path()
    print(generated_file_path)
    query_generator.to_file()

    generated_file_content = get_file_content(generated_file_path)
    assert Path(generated_file_path).is_file()
    assert isinstance(generated_file_content, str)
    assert expected_query_text in generated_file_content


def test_simple_property_additions_generator(tmp_path):
    expected_query_text = """
  FILTER NOT EXISTS {
    GRAPH ?deletionsGraph {
      ?instance ?property [] .
    }
  }"""
    query_generator = QueryGenerator(cls="skos:Concept", operation="added_property",
                                     prop="skos:notation",
                                     output_folder_path=str(tmp_path),
                                     template=QUERIES_TEMPLATES.get_template("property_additions.rq"))
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
                                     template=QUERIES_TEMPLATES.get_template("reified_properties_additions.rq"))
    generated_file_path = query_generator.build_file_path()
    print(generated_file_path)
    query_generator.to_file()

    generated_file_content = get_file_content(generated_file_path)
    assert Path(generated_file_path).is_file()
    assert isinstance(generated_file_content, str)
    assert expected_query_text in generated_file_content


def test_property_value_update_filter_captures_all_four_cases(tmp_path):
    # The pairing FILTER must keep the original two cases and add #142 (language-tag
    # change/removal) and #143 (datatype <-> object) — for detail and count templates alike.
    case_3 = "(str(?oldValue) = str(?newValue))"
    case_4 = "(isLiteral(?oldValue) != isLiteral(?newValue))"
    for operation, template_name in [
        ("updated_property", "property_value_updates.rq"),
        ("count_updated_property", "count_property_value_updates.rq"),
        ("updated_reified", "reified_property_value_updates.rq"),
        ("count_updated_reified", "count_reified_property_value_updates.rq"),
    ]:
        query_generator = QueryGenerator(cls="skos:Concept", operation=operation,
                                         prop="skosxl:prefLabel",
                                         object_property="skosxl:literalForm",
                                         output_folder_path=str(tmp_path),
                                         template=QUERIES_TEMPLATES.get_template(template_name))
        query_generator.to_file()
        content = get_file_content(query_generator.build_file_path())
        assert case_3 in content, template_name
        assert case_4 in content, template_name
        # Guard: comments inside the FILTER must not contain parentheses. Some SPARQL
        # endpoints (Jena/ARQ-style) match a NIL token "()" across a comment that holds a
        # stray ")", breaking the query — keep the Case 3/4 comment text paren-free.
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("# Case "):
                assert "(" not in stripped and ")" not in stripped, f"{template_name}: {stripped}"

