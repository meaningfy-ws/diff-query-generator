from dqgen.services.html_template_registry import HtmlTemplateRegistry


def test_html_template_registry():
    for template in [HtmlTemplateRegistry().INSTANCES, HtmlTemplateRegistry().PROPERTIES,
                     HtmlTemplateRegistry().REIFIED_PROPERTIES]:
        assert "macros.html" in template
        assert "{% raw %}" in template
        assert isinstance(template, str)
