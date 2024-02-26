from pathlib import Path

from src.oct_json_schema.generate_defaults import get_defaults_from_schema


def test_get_defaults_from_schema():
    # TODO(Alex) Remove this hard-coding
    root = Path("/Users/alexanderbuccheri/Codes/oct_json_schema")
    file = root / "data/demo_schema.json"

    defaults = get_defaults_from_schema(file)
    expected_defaults = {'MaximumIter': 200, 'EigensolverTolerance': 1e-07}

    assert set(list(defaults)) == {'MaximumIter', 'EigensolverTolerance'}, ('defaults does not contain expected keys. '
                                                                            'File has changed, or parsing a different '
                                                                            'file')
    assert defaults == expected_defaults
