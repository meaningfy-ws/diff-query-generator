import pathlib
from pathlib import Path

import pytest
from jinja2 import Template

from dqgen.adapters.resource_fetcher import get_file_content
from dqgen.services import ASCII_DOC_TEMPLATES
from dqgen.services.asciidoc_generator import AsciiDocGenerator
from dqgen.services.asciidoc_templates_generator import generate_asciidoc_templates_from_csv
from tests.unit.test_queries_generator import PATH_TO_APS


def test_instance_asciidoc_generator(tmp_path):
    expected_text = """== Added concepts"""
    asciidoc_generator = AsciiDocGenerator(cls="skos:Concept", operation="added_instance", class_name="concept",
                                           output_folder_path=str(tmp_path),
                                           template=ASCII_DOC_TEMPLATES.get_template("instance.jinja2"))

    generated_file_path = asciidoc_generator.build_file_path()
    asciidoc_generator.to_file()

    generated_file_content = get_file_content(generated_file_path)
    assert Path(generated_file_path).is_file()
    assert isinstance(generated_file_content, str)
    assert expected_text in generated_file_content


def test_generate_asciidoc_templates_from_csv(tmp_path):

    generate_asciidoc_templates_from_csv(ap_file_path=PATH_TO_APS / "src_ap_mod.csv", output_base_dir=tmp_path,)
    assert pathlib.Path(tmp_path).is_dir()
    assert pathlib.Path(tmp_path / "src_ap_mod" / "asciidoc").is_dir()
    assert pathlib.Path(tmp_path / "src_ap_mod" / "asciidoc" / "main.adoc").is_file()

    with pytest.raises(ValueError):
        generate_asciidoc_templates_from_csv(ap_file_path=PATH_TO_APS / "skos_core.csv", output_base_dir=tmp_path)
