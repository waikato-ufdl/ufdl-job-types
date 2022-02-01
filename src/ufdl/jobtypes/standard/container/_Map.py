from typing import Dict, Tuple, Type

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, standard_object

from ufdl.jobtypes.base import TypeArgsType, UFDLJSONType, PythonType, UFDLType


class Map(UFDLJSONType[Tuple[UFDLJSONType[TypeArgsType, PythonType]], Dict[str, PythonType]]):
    def parse_json_value(self, value: RawJSONElement) -> Dict[str, PythonType]:
        if not isinstance(value, dict):
            raise ValueError("value is not a dict")
        for key in value:
            if not isinstance(key, str):
                raise ValueError(f"value contains non-string key '{key}' ({type(key)})")

        return {
            key: self.type_args[0].parse_json_value(sub_value)
            for key, sub_value in value.items()
        }

    def format_python_value_to_json(self, value: Dict[str, PythonType]) -> RawJSONElement:
        return {
            key: self.type_args[0].format_python_value_to_json(sub_value)
            for key, sub_value in value
        }

    @property
    def json_schema(self) -> JSONSchema:
        return standard_object(
            additional_properties=self.type_args[0].json_schema
        )

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return UFDLJSONType(),

    @property
    def is_abstract(self) -> bool:
        return self.type_args[0].is_abstract
