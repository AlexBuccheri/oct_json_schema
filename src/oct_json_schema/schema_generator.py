""" Generate a JSON schema from scrubbing the Octopus source code.
This is designed to generate an initial schema. After which point, it should not be used again.

There are several TODOs left, such as mapping Octopus defaults to valid JSON schema types/variables.
"""
import json
from pathlib import Path


from variables import Variables


class OctopusDirs:
    def __init__(self, root):
        self.root = Path(root)
        self.src = Path(root, "src")
        self.test = Path(root, 'testsuite')
        self.tutorial = Path(root, 'doc/html/content', 'Tutorial')
        self.manual = Path(root, 'doc/html/content', 'Manual')

        # Convert all attributes to strings, as glob expects this in Martin's `variables.py`
        mutated_dict = {k: v.as_posix() for k, v in self.__dict__.items()}
        self.__dict__ = mutated_dict


def get_array_entries(schema_dict: dict):
    """ Get any options of type "array"

    :return:
    """
    array_options = []
    for name, entry in schema_dict['properties'].items():
        if entry['type'] == 'array':
            array_options.append(name)
    print(f"Found {len(array_options)} options of type array")
    return array_options


def parse_source_to_schema(root):
    """
    Generates a JSON schema from parsing documentation in Octopus source

    See here: https://json-schema.org/understanding-json-schema/reference

    Things there is not information on in the Octopus documentation:
        For "integer" and "number": "minimum", "maximum", "minItems", "exclusiveMinimum", "exclusiveMaximum"

    TODO Map defaults. 'no', 'yes', '0.1', '1', 'true', 'false' to schema-valid types

    :param root: Octopus root directory
    """
    dir = OctopusDirs(root)
    # NOTE, had to add some basic checking to parse_sources method of this object, to be more robust w.r.t.
    # path handling
    octopus = Variables(sources=dir.src, tests=dir.test, tutorials=dir.tutorial, manuals=dir.manual, verbose=False)

    # Build a JSON schema
    schema_dict = {"$schema": "https://json-schema.org/draft/2020-12/schema",
                   "title": "Octopus input options",
                   "type": "object",
                   "properties": {}}

    # Map the octopus datatypes from the manual to schema-valid type: "integer", "string", "number", "array", "boolean"
    types_manual_to_schema = {'logical': 'boolean',
                              'integer': 'integer',
                              'flag': 'string',
                              'virtual': 'null',
                              'float': 'number',
                              'string': 'string',
                              'block': 'array'
                              }
    # Could check entries in manual against the expected data types
    # octopus_types = set([entry['Type'] for entry in octopus.variables.values()])

    for entry in octopus.variables.values():
        name = entry['Name']
        type = types_manual_to_schema[entry['Type']]
        description = " ".join(s for s in entry['Description'])
        default = entry['Default']

        schema_dict['properties'][entry['Name']] = \
            {"type": type,
             "description": description
             }

        if default:
            schema_dict['properties'][name]['default'] = default[0]

    return schema_dict


if __name__ == "__main__":
    schema_dict = parse_source_to_schema('/Users/alexanderbuccheri/Codes/octopus')
    json_str = json.dumps(schema_dict, indent=4)
    print(json_str)

    # Some options to check are correctly handled: 'Debug', 'Units', 'SupercellDimensions' 'Coordinates'
    # print(schema_dict['properties']['Coordinates'])
