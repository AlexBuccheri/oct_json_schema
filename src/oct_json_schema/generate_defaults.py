""" Generate a fortran module that contains all option defaults, present in the schema

One should investigate quicktype and c iso-bindings for fully automating this.
Or any package that goes from JSON schema to source code.
"""
import json
import sys


def get_defaults_from_schema(file) -> dict:
    """
    Parse the JSON schema and write the defaults to a fortran module

    Note, there should be no reason to do type casting if the JSON
    has been written correctly.
    """
    try:
        with open(file, "r") as file:
            schema = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f'{file} not found')

    def traverse(subschema, full_key: list):
        for key, value in subschema.items():
            # Log child key per iteration, to keep track of nesting
            full_key += [key]
            if isinstance(value, dict):
                traverse(value, full_key)
                full_key = full_key[:-1]
            else:
                if key == "default":
                    # Convert parent + child keys into a label
                    # Note, this drops the innermost key, "default"
                    # as I don't need to store it
                    label = "".join(s for s in full_key[:-1])
                    defaults[label] = subschema["default"]
            # Removes current child key, having iterated over it
            full_key = full_key[:-1]

    # Take top-level properties
    options = schema["properties"]

    # Fill defaults
    defaults = {}
    traverse(options, full_key=[])

    return defaults


def schema_defaults_to_fortran(defaults: dict):
    """Generate a fortran module file, containing schema defaults

    TODO This needs expanding to all data types

    :param defaults: Option defaults of the form {'option': default_value}
    """
    type_conversion = {int: 'integer(int32)',
                       float: 'real(real64)',
                       bool: 'logical'}

    suffix = {int: '_int32',
              float: '_real66',
              bool: ''}

    m_string = """module input_defaults_oct_m
   implicit none
"""
    indent = "   "
    for option, default in defaults.items():
        d_type = type(default)
        declaration = (indent + type_conversion[d_type] + ' :: ' + option + "_default = " +
                       str(default) + suffix[d_type])
        m_string += declaration + '\n'

    m_string += "end module input_defaults_oct_m"

    return m_string


if __name__ == "__main__":

    # Expect one CL arg
    if len(sys.argv) == 2:
        schema_path = sys.argv[1]
    else:
        raise ValueError("Need to pass location of JSON schema: python generate_defaults path/2/schema.json")

    defaults = get_defaults_from_schema(schema_path)
    module_str = schema_defaults_to_fortran(defaults)
    print(module_str)
