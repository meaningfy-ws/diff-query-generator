import pathlib
from pathlib import Path

import pytest
from jinja2 import Template

from dqgen.adapters.resource_fetcher import get_file_content
from dqgen.services import HTML_TEMPLATES
from dqgen.services.html_generator import HtmlGenerator
from dqgen.services.html_templates_generator import generate_html_templates_from_csv
from tests.unit.test_queries_generator import PATH_TO_APS


def test_instance_html_generator(tmp_path):
    expected_text = """<h2 class="ui header">Added concepts</h2>"""
    html_generator = HtmlGenerator(cls="skos:Concept", operation="added_instance", class_name="concept",
                                   output_folder_path=str(tmp_path),
                                   template=HTML_TEMPLATES.get_template("instance.jinja2"))

    generated_file_path = html_generator.build_file_path()
    html_generator.to_file()

    generated_file_content = get_file_content(generated_file_path)
    assert Path(generated_file_path).is_file()
    assert isinstance(generated_file_content, str)
    assert expected_text in generated_file_content


def test_generate_html_templates_from_csv(tmp_path):

    generate_html_templates_from_csv(ap_file_path=PATH_TO_APS / "src_ap_mod.csv", output_base_dir=tmp_path,)
    assert pathlib.Path(tmp_path).is_dir()
    assert pathlib.Path(tmp_path / "src_ap_mod" / "html").is_dir()
    assert pathlib.Path(tmp_path / "src_ap_mod" / "html" / "main.html").is_file()

    with pytest.raises(ValueError):
        generate_html_templates_from_csv(ap_file_path=PATH_TO_APS / "skos_core.csv", output_base_dir=tmp_path)



