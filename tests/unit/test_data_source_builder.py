import pathlib

from dqgen.adapters.ap_reader import read_ap_from_csv
from dqgen.services.templates_data_source_builder import camel_case_to_words, build_datasource_for_template, \
    generate_file_data, iterate_operations, add_instance_changes, add_prop_group_details


def test_camel_case_to_words():
    example = "orderedCollection"
    transformed_example = camel_case_to_words(example)
    assert isinstance(transformed_example, str)
    assert transformed_example == "ordered Collection"


def test_generate_file_data():
    file_path, count_file_name = generate_file_data(cls="skos:Concept", class_folder_name="test_folder",
                                                    operation="added_instance")
    assert file_path == "test_folder/added_instance_concept.html"
    assert count_file_name == "count_added_instance_concept.rq"


def test_iterate_operations():
    file_paths = []
    count_queries = []
    iterate_operations(operation_list=["added_instance", "deleted_instance"],
                       class_folder_name="test_folder", cls="skos:Collection",
                       file_paths=file_paths, count_queries=count_queries)
    assert len(file_paths) == 2
    assert len(count_queries) == 2
    assert "test_folder/added_instance_collection.html" in file_paths
    assert "count_added_instance_collection.rq" in count_queries


def test_add_instance_changes():
    data = {"skos:Concept": {"label": camel_case_to_words("concept").title()}}
    add_instance_changes(data_source=data, class_folder_name="test_folder", cls="skos:Concept", class_name="concept")
    assert "instance_changes" in data["skos:Concept"].keys()
    assert "count_queries" in data["skos:Concept"]["instance_changes"].keys()


def test_add_prop_group_details():
    data = {"skos:Concept": {"label": camel_case_to_words("concept").title(), "prop_groups": {}}}
    file_paths = []
    count_queries = []
    add_prop_group_details(prop_group_value="preferred labels", prop_name="skosxl:prefLabel/skosxl:literalForm",
                           cls="skos:Concept", data_source=data, prop_file_paths=file_paths,
                           count_prop_file_paths=count_queries)
    assert "preferred labels" in data["skos:Concept"]["prop_groups"].keys()
    assert ["label", "query_template_file_paths", "count_queries"] == list(data["skos:Concept"]["prop_groups"][
                                                                               "preferred labels"].keys())


def test_build_datasource_for_hmtl_template():
    path_to_csv_file = pathlib.Path(__file__).parent.parent / "test_data" / "aps" / "src_ap_mod.csv"
    df = read_ap_from_csv(path_to_csv_file)
    data_source = build_datasource_for_template(processed_csv_file=df)
    print(data_source)
    assert isinstance(data_source, dict)
    assert 'skos:Concept', 'skos:Collection' in data_source.keys()
    assert "label", "prop_groups" in data_source["skos:Concept"].keys()

    # check at least one class-level instance file uses .html
    instance_files = data_source.get("skos:Concept", {}).get("instance_changes", {}).get("files", [])
    assert any(f.endswith('.html') for f in instance_files)

    # check a property-level file uses .html
    prop_groups = data_source.get("skos:Concept", {}).get("prop_groups", {})
    found = False
    for group in prop_groups.values():
        paths = group.get("query_template_file_paths", [])
        if any(p.endswith('.html') for p in paths):
            found = True
            break
    assert found, "No .html file paths found in property groups"


def test_build_datasource_for_adoc_template():
    # Ensure the data source builder emits .adoc file paths when requested
    path_to_csv_file = pathlib.Path(__file__).parent.parent / "test_data" / "aps" / "src_ap_mod.csv"
    df = read_ap_from_csv(path_to_csv_file)
    data_source = build_datasource_for_template(processed_csv_file=df, file_extension="adoc")

    # check at least one class-level instance file uses .adoc
    instance_files = data_source.get("skos:Concept", {}).get("instance_changes", {}).get("files", [])
    assert any(f.endswith('.adoc') for f in instance_files)

    # check a property-level file uses .adoc
    prop_groups = data_source.get("skos:Concept", {}).get("prop_groups", {})
    # find any prop group entry and check its query template file paths
    found = False
    for group in prop_groups.values():
        paths = group.get("query_template_file_paths", [])
        if any(p.endswith('.adoc') for p in paths):
            found = True
            break
    assert found, "No .adoc file paths found in property groups"
