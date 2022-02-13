from typing import Optional, Tuple, overload

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, regular_array

from ...base import TypeArgsType, UFDLJSONType, InputType, OutputType, Integer, UFDLType
from ...error import expect


class Array(
    UFDLJSONType[
        Tuple[UFDLJSONType[TypeArgsType, InputType, OutputType], Integer],
        Tuple[InputType, ...],
        Tuple[OutputType, ...]
    ]
):
    @overload
    def __init__(self, element_type: UFDLJSONType): ...
    @overload
    def __init__(self, type_args: Optional[TypeArgsType] = None): ...

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], UFDLType):
            args = args,
        super().__init__(args)

    def parse_json_value(self, value: RawJSONElement) -> Tuple[InputType, ...]:
        self.validate_with_schema(value)
        element_type = self.type_args[0]
        return tuple(
            element_type.parse_json_value(element)
            for element in value
        )

    def format_python_value_to_json(self, value: Tuple[OutputType, ...]) -> RawJSONElement:
        expect(tuple, value)
        element_type, size_type = self.type_args
        if isinstance(size_type.value(), int) and len(value) != size_type.value():
            raise ValueError(f"Expected tuple of size {size_type}")
        return [
            element_type.format_python_value_to_json(element)
            for element in value
        ]

    @property
    def json_schema(self) -> JSONSchema:
        element_type, size_type = self.type_args
        kwargs = {}
        if isinstance(size_type.value(), int):
            kwargs = {
                "min_elements": size_type.value(),
                "max_elements": size_type.value()
            }
        return regular_array(
            element_type.json_schema,
            **kwargs
        )

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return UFDLJSONType(), Integer()

    @property
    def is_abstract(self) -> bool:
        return self.type_args[0].is_abstract
