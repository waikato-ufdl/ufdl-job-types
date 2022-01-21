from typing import Dict, Type

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, standard_object

from ufdl.jobtypes.base import TypeArgType, UFDLJSONType, PythonType


class Map(UFDLJSONType[UFDLJSONType[TypeArgType, PythonType], Dict[str, PythonType]]):
    def parse_json_value(self, value: RawJSONElement) -> Dict[str, PythonType]:
        if not isinstance(value, dict):
            raise ValueError("value is not a dict")
        for key in value:
            if not isinstance(key, str):
                raise ValueError(f"value contains non-string key '{key}' ({type(key)})")

        return {
            key: self.type_arg.parse_json_value(sub_value)
            for key, sub_value in value.items()
        }

    def format_python_value_to_json(self, value: Dict[str, PythonType]) -> RawJSONElement:
        return {
            key: self.type_arg.format_python_value_to_json(sub_value)
            for key, sub_value in value
        }

    @property
    def json_schema(self) -> JSONSchema:
        return standard_object(
            additional_properties=self.type_arg.json_schema
        )

    @classmethod
    def type_arg_expected_base_type(cls) -> Type[UFDLJSONType]:
        return UFDLJSONType
