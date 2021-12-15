import jinja2.environment

from dqgen.adapters.template_builder import build_query_template, build_html_template
from dqgen.services import HTML_TEMPLATES


def test_query_template_builder():
    template = HTML_TEMPLATES.get_template("instance.jinja2")
    built_template = build_query_template(jinja2_template=template, cls="skos:Concept", old_version=None,
                                          new_version=None,
                                          version_history_graph=None, obj_prop=None, prop=None, languages=["en"],
                                          type_of_action="addition", preview_object_property="",
                                          preview_property="skos:prefLabel")
    assert isinstance(built_template, jinja2.environment.TemplateStream)


def test_html_template_builder():
    template = HTML_TEMPLATES.get_template("instance.jinja2")
    built_template = build_html_template(jinja2_template=template, cls="skos:Concept", class_name="concept",
                                         prop_name=None, obj_prop_name=None, obj_prop=None, prop=None,
                                         query_file="query_file.rq", operation="added")
    assert isinstance(built_template, jinja2.environment.TemplateStream)
