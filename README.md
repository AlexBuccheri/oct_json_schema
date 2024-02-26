# Octopus JSON Schema Demo

Demo project illustrating how one could move docuemntation and default definition out of Octopus, and into a JSON
schema. The package is currently not installable.

**Generate a JSON Schema**

To generate as yet not-complete JSON schema for Octopus, run:

```shell
python src/oct_json_schema/schema_generator.py
```

**Generate a Defaults F90 Module**

To generate a single module containing all defaults from the schema, one can run:

```shell
python src/oct_json_schema/generate_defaults.py data/demo_schema.json
```

I note one could instead try something like `quicktype`:

```shell
quicktype --lang c schema.json -o output.c
```

where the schema is directly converted to C code. Or any package that goes from JSON schema to source code.


**Generate a Webpage From the Schema**

This package allows a webpage to be created from a schema 

```shell
pip install json-schema-for-humans
```

Usage:

```shell
cd docs
generate-schema-doc ../data/demo_schema.json
```

One could go further and add this to sphinx:
1. Convert your JSON schema to a format compatible with Sphinx: Use JSON Schema Documentation 
2. Write Sphinx documentation that includes your schema.
3. Configure Sphinx to build your documentation.


**Run the Unit Tests**

From root:

```shell
# -s gives any print info
pytest -s  
```


## TODOs
* Add links to the test cases that contain these variables

* If one inspects the schema, it's clear that many defaults/type will need manual attention, either after the schema
is generated, or directly in the Octopus source.

* Investigate `quicktype`, and other packages that go directly from JSON schema to source code.

* See if `generate-schema-doc` can be replaced with nesting in sphinx


## Files

[variables.py](src/oct_json_schema/variables.py) is a python file available in the Octopus documentation repository, 
which is a rewrite of perl code designed to scrub and parse documentation from the Octopus source code.


## Motivations for Moving to a Schema

* All documentation and defaults for variables defined in one place, outside of the code
* No need to parse the source code to generate documentation
* Can trivially convert to webpage with a single command - embed with the rest of the docs
* Can reuse all the existing HTML formatting in the doc strings
* Defaults are made consistent between the code and documentation
* One can set defaults according to dependencies i.e. use different defaults depending, in the schema
* Can generate most of the schema boilerplate by scrubbing the code with the python tool Martin uses to generate the existing documentation
* Can validate inputs when using a python wrapper, like:

```shell
pip install jsonschema
```

```python
import jsonschema

try:
    # Validate the input data against the schema
    jsonschema.validate(instance=input_data, schema=schema)
    print("Validation successful!")
except jsonschema.exceptions.ValidationError as e:
    print(f"Validation failed: {e}")
```

## Issues/Annoyances 

* Will require some initial manual setup to address missing fields
* Not sure if one can split lines for schema documentation => Bit of a pain to edit
