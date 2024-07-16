from jsonschema import Draft7Validator, SchemaError
import json
from typing import Any, Dict


def validate_json(schema) -> bool:
    """
    validating json schema using Draft7Validator from jsonschema lib
    :param schema: json schema to validate
    :return: True if valid, False if not (also printing error)
    """
    try:
        Draft7Validator.check_schema(schema)
        return True
    except SchemaError as e:
        print(f"Schema is invalid: {str(e)}")
        return False


def parse_dict(d: Dict[str, Any]) -> str:
    """
    parsing dict to string-pydantic model
    :param d: dict to parse
    :return: string that contains parsed dict
    """
    def parse_properties(properties: Dict[str, Any], required_fields: set) -> list[str]:
        fields = list()
        type_mapper = {
            "string": "str",
            "integer": "int",
            "boolean": "bool",
            "number": "float",
            "array": "List",
            "object": "Dict"
        }
        for prop_name, prop_details in properties.items():
            json_type = prop_details.get('type', 'Any')
            pydantic_type = type_mapper.get(json_type, "Any")
            # print(prop_name, prop_details)
            str_fields = {"alias", "validation_alias", "serialization_alias", "title", "description", "discriminator",
                          "pattern"}  # when generating the code they need to add inverted commas
            if prop_name in required_fields:
                if len(prop_details) == 1:
                    fields.append(f"{prop_name}: {pydantic_type}")
                else:
                    str_to_add = f"{prop_name}: Annotated[{pydantic_type}, Field("
                    for key, val in prop_details.items():
                        if key != "type" and type(val) != dict and type(val) != list:  # TODO make it works with dictionaries and lists
                            if key in str_fields:
                                str_to_add += f'{key}="{val}",'
                            else:
                                str_to_add += f"{key}={val},"
                    str_to_add += ")]"
                    fields.append(str_to_add)
            else:
                if len(prop_details) == 1:
                    fields.append(f"{prop_name}: Optional[{pydantic_type}] = None")
                else:
                    str_to_add = f"{prop_name}: Optional[Annotated[{pydantic_type}, Field("
                    for key, val in prop_details.items():
                        if key != "type":
                            str_to_add += f"{key}={val},"
                    str_to_add += ")]] = None"
                    fields.append(str_to_add)
        return fields

    required_fields = set(d.get("required", []))
    properties = d.get("properties", {})
    fields = parse_properties(properties, required_fields)

    model_name = d.get("name", "GeneratedModel")
    class_definitions = list()
    class_definitions.append(f"class {model_name}(BaseModel):\n")
    if not fields:
        class_definitions.append(f"    pass\n")
    else:
        for field in fields:
            class_definitions.append(f"    {field}\n")

    return "".join(class_definitions)


def create_pydantic_model(engine_schema_path: str, out_dir: str) -> None:
    """
    generating pydantic model in file generated-model.py in out_dir folder
    :param engine_schema_path: path to generating schema
    :param out_dir: path to directory there model will be saved
    :return: None
    """
    with open(engine_schema_path, "r") as f:
        data = json.load(f)
    if not validate_json(data):
        return
    fields = parse_dict(data)

    model_definition = f"""\
from pydantic import *
from typing import *


{fields}
    """

    with open(f"{out_dir}/generated-models.py", "w") as file:
        file.write(model_definition)


def create_rest(path: str, out_dir: str) -> None:
    """
    generating rest controllers to models in path and save code in out_dir/generated-rest.py
    :param path: path to models
    :param out_dir: directory where code will be saved
    :return: None
    """
    


create_pydantic_model("example-schema.json", ".")
