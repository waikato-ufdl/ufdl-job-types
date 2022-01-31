from typing import Tuple

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, regular_array

from ...base import TypeArgsType, UFDLJSONType, PythonType, Integer, UFDLType


class Array(
    UFDLJSONType[
        Tuple[UFDLJSONType[TypeArgsType, PythonType], Integer],
        Tuple[PythonType, ...]
    ]
):
    def parse_json_value(self, value: RawJSONElement) -> Tuple[PythonType]:
        self.validate_with_schema(value)
        element_type = self.type_args[0]
        return tuple(
            element_type.parse_json_value(element)
            for element in value
        )

    def format_python_value_to_json(self, value: Tuple[PythonType]) -> RawJSONElement:
        if not isinstance(value, tuple):
            raise ValueError(f"Expected tuple, got {type(value)}")
        element_type, size_type = self.type_args
        if isinstance(size_type, int) and len(value) != size_type:
            raise ValueError(f"Expected tuple of size {size_type}")
        return [
            element_type.format_python_value_to_json(element)
            for element in value
        ]

    @property
    def json_schema(self) -> JSONSchema:
        element_type, size_type = self.type_args
        if not isinstance(element_type, UFDLJSONType):
            element_type = element_type.type_base_equivalent()
        kwargs = {}
        if isinstance(size_type, int):
            kwargs = {
                "min_elements": size_type,
                "max_elements": size_type
            }
        return regular_array(
            element_type.json_schema,
            **kwargs
        )

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return UFDLJSONType.type_base_equivalent(), Integer()
