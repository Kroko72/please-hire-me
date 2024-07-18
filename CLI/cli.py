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
        print(f"Schema is invalid: {e}")
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
                                if key == "pattern":
                                    str_to_add += f'{key}=r"{val}",'
                                else:
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

    with open(f"{out_dir}/generated_model.py", "w") as file:
        file.write(model_definition)


def create_rest(path_to_json: str, out_dir: str) -> None:
    """
    generating rest controllers to model in path and save code in out_dir/generated-rest.py
    :param path_to_json: path to json that describes model
    :param out_dir: directory where code will be saved
    :return: None
    """
    with open(path_to_json, "r") as f:
        data = json.load(f)
    kind = data["kind"]
    name = data["name"]
    version = data["version"]
    description = data["description"]
    configuration = data["configuration"]
    configuration_strings = list()
    engine_string = "{user}:{password}@{host}:{port}/{db_name}"
    uuid_string = "{uuid}"
    for key, value in configuration.items():
        string = f"""\
@app.put("/{kind}/{uuid_string}/{key}", response_model=dict)
def update_configuration(uuid: UUID, {key}: dict):
    with engine.connect() as conn:
        statement = update(App).where(App.uuid==uuid).values({key}={key})
        conn.execute(statement)
        conn.commit()
    return {key}
""" + "\n"
        configuration_strings.append(string)
    rest_file = f"""\
from uuid import UUID
from db.create_table import App
from fastapi import FastAPI
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, insert, select, delete, update
from db.config import host, user, password, db_name, port
from generated_model import {name}

app = FastAPI()
Base = declarative_base()
engine = create_engine(f'postgresql://{engine_string}', future=True)

@app.post("/{kind}/", response_model={name})
def save_item(item: {name}):
    with engine.connect() as conn:
        statement = insert(App).values(kind=item.kind, name=item.name, version=item.version,
                                          description=item.description, json=item.model_dump_json())
        conn.execute(statement)
        conn.commit()
    return item

@app.get("/{kind}/{uuid_string}/")
def get_item(uuid: UUID):
    with engine.connect() as conn:
        statement = select(App).where(App.uuid==uuid)
        res = conn.execute(statement).fetchall()
    return res

@app.get("/{kind}/{uuid_string}/state")
def get_item_state(uuid: UUID):
    with engine.connect() as conn:
        statement = select(App.state).where(App.uuid==uuid)
        res = conn.execute(statement).fetchall()
    return res
    
@app.delete("/{kind}/{uuid_string}/")
def delete_item(uuid: UUID):
    with engine.connect() as conn:
        statement = delete(App).where(App.uuid==uuid)
        res = conn.execute(statement)
        conn.commit()
    return res
    
@app.put("/{kind}/{uuid_string}/state", response_model=str)
def update_state(uuid: UUID, state: str):
    with engine.connect() as conn:
        statement = update(App).where(App.uuid==uuid).values(state=state)
        conn.execute(statement)
        conn.commit()
    return state
    
@app.put("/{kind}/{uuid_string}/configuration", response_model=dict)
def update_configuration(uuid: UUID, configuration: dict):
    with engine.connect() as conn:
        statement = update(App).where(App.uuid==uuid).values(configuration=configuration)
        conn.execute(statement)
        conn.commit()
    return configuration
    
{"".join(configuration_strings)}
    """

    with open(f"{out_dir}/generated_rest.py", "w") as file:
        file.write(rest_file)


if __name__ == "__main__":
    create_pydantic_model("example_schema.json", "..")
    create_rest("example_rest_schema.json", "..")
