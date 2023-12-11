from pathlib import Path

from dqgen.adapters.resource_fetcher import get_file_content

ROOT_DIR = Path(__file__).parent.parent

def test_get_file_content():
    path = ROOT_DIR / "test_data/test_files/sparqrl_query.rq"
    result = get_file_content(str(path))

    assert isinstance(result, str)
    assert "?person foaf:name ?name " in result