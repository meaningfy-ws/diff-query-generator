from dqgen.adapters import template_builder
from dqgen.services.query_generator import QueryGenerator


class HtmlGenerator(QueryGenerator):

    def __init__(self, cls: str, operation: str, output_folder_path: str, template: str, prop: str = None,
                 object_property: str = None, new_version_graph: str = None, old_version_graph: str = None,
                 version_history_graph: str = None, language: str = "en", class_name: str = "", prop_name: str = "",
                 obj_prop_name: str = ""):
        super().__init__(cls, operation, output_folder_path, template, prop, object_property, new_version_graph,
                         old_version_graph, version_history_graph, language)
        self.file_extension = "html"
        self.class_name = class_name
        self.prop_name = prop_name
        self.obj_prop_name = obj_prop_name

    def build_query_template(self):
        query_file = self.build_file_path(file_extension='rq').rsplit(sep='/', maxsplit=1)[1]
        operation = self.operation.split("_")[0]
        return template_builder.build_html_template(jinja2_template=self.template, query_file=query_file,
                                                    operation=operation, cls=self.cls, prop=self.prop,
                                                    obj_prop=self.object_property, class_name=self.class_name,
                                                    prop_name=self.prop_name,
                                                    obj_prop_name=self.obj_prop_name)