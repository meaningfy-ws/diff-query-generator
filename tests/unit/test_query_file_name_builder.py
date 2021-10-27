from dqgen.adapters.file_name_builder import make_file_path, make_file_name


def test_make_file_name_and_path(tmp_path):
    file_name = make_file_path(output_folder_path=tmp_path,
                               file_name=make_file_name(operation="added_instance", cls="skos:Concept",
                                                        obj_prop=None, prop=None, file_extension="rq"))
    assert file_name == str(tmp_path) + "/" + "added_instance_concept.rq"
