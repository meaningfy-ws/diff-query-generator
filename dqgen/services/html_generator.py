from jinja2 import Template

from dqgen.adapters import template_builder
from dqgen.services import QUERY_FALLBACK_LANGUAGES
from dqgen.services.base_generator import BaseGenerator


class HtmlGenerator(BaseGenerator):
    """
    This class will generate a html template file from a html meta-template
    """
    def __init__(self, cls: str, operation: str, output_folder_path: str, template: Template, prop: str = None,
                 object_property: str = None, new_version_graph: str = None, old_version_graph: str = None,
                 version_history_graph: str = None, languages: list = QUERY_FALLBACK_LANGUAGES, class_name: str = "", prop_name: str = "",
                 obj_prop_name: str = ""):
        super().__init__(cls, operation, output_folder_path, template, prop, object_property, new_version_graph,
                         old_version_graph, version_history_graph, languages)
        self.file_extension = "html"
        self.class_name = class_name
        self.prop_name = prop_name
        self.obj_prop_name = obj_prop_name

    def build_template(self):
        """
            This method builds a desired html template from the a meta-template
        :return: html template
        """
        query_file = self.build_file_name(file_extension='rq')
        operation = self.operation.split("_")[0]
        return template_builder.build_html_template(jinja2_template=self.template, query_file=query_file,
                                                    operation=operation, cls=self.cls, prop=self.prop,
                                                    obj_prop=self.object_property, class_name=self.class_name,
                                                    prop_name=self.prop_name,
                                                    obj_prop_name=self.obj_prop_name)
