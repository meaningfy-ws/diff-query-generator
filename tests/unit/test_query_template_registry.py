from dqgen.services.query_template_registry import QueryTemplateRegistry


def test_query_template_registry():
    for query in [QueryTemplateRegistry().INSTANCE_ADDITIONS, QueryTemplateRegistry().PROPERTY_ADDITIONS,
                  QueryTemplateRegistry().REIFIED_PROPERTY_ADDITIONS, QueryTemplateRegistry().INSTANCE_DELETIONS,
                  QueryTemplateRegistry().PROPERTY_DELETIONS, QueryTemplateRegistry().REIFIED_PROPERTY_DELETIONS]:
        assert "SELECT" in query
        assert "FILTER" in query
        assert isinstance(query, str)
