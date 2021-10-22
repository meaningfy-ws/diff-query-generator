import pathlib
from pathlib import Path

import pytest

from dqgen.adapters.resource_fetcher import get_file_content
from dqgen.services.html_generator import HtmlGenerator
from dqgen.services.html_template_registry import HtmlTemplateRegistry
from dqgen.services.html_templates_generator import generate_html_templates_from_csv
from tests.unit.test_queries_generator import PATH_TO_APS


def test_instance_html_generator(tmp_path):
    expected_text = """<h2 class="ui header">Added concepts</h2>"""
    html_generator = HtmlGenerator(cls="skos:Concept", operation="added_instance", class_name="concept",
                                   output_folder_path=str(tmp_path),
                                   template=HtmlTemplateRegistry().INSTANCES)

    generated_file_path = html_generator.build_file_path(file_extension="html")
    print(generated_file_path)
    html_generator.to_file()

    generated_file_content = get_file_content(generated_file_path)
    assert Path(generated_file_path).is_file()
    assert isinstance(generated_file_content, str)
    assert expected_text in generated_file_content


def test_generate_html_templates_from_csv(tmp_path):

    generate_html_templates_from_csv(ap_file_name="src_ap_mod.csv", output_base_dir=tmp_path,
                                     aps_folder_path=PATH_TO_APS)
    assert pathlib.Path(tmp_path).is_dir()
    assert pathlib.Path(tmp_path / "src_ap_mod" / "html").is_dir()
    assert pathlib.Path(tmp_path / "src_ap_mod" / "html" / "main.html").is_file()

    with pytest.raises(Exception):
        generate_html_templates_from_csv(ap_file_name="skos_core.csv", output_base_dir=tmp_path,
                                         aps_folder_path=PATH_TO_APS)



