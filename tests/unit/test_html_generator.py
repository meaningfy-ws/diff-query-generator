from pathlib import Path

from dqgen.adapters.resource_fetcher import get_file_content
from dqgen.services.html_generator import HtmlGenerator
from dqgen.services.html_template_registry import HtmlTemplateRegistry


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
