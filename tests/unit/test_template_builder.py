import jinja2.environment

from dqgen.adapters.template_builder import build_template
from dqgen.services.query_template_registry import QueryTemplateRegistry


def test_template_builder():
    template = QueryTemplateRegistry().INSTANCE_ADDITIONS
    built_template = build_template(jinja2_template=template, cls="skos:Concept", old_version=None, new_version=None,
                                    version_history_graph=None, obj_prop=None, prop=None, lang="en")
    assert isinstance(built_template, jinja2.environment.TemplateStream)
