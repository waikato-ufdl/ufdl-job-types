from typing import Dict, Tuple

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, standard_object

from ...base import TypeArgsType, UFDLJSONType, InputType, OutputType, UFDLType
from ...error import expect


class Map(
    UFDLJSONType[
        Tuple[UFDLJSONType[TypeArgsType, InputType, OutputType]],
        Dict[str, InputType],
        Dict[str, OutputType]
    ]
):
    def parse_json_value(self, value: RawJSONElement) -> Dict[str, InputType]:
        self.validate_with_schema(value)
        return {
            key: self.type_args[0].parse_json_value(sub_value)
            for key, sub_value in value.items()
        }

    def format_python_value_to_json(self, value: Dict[str, OutputType]) -> RawJSONElement:
        expect(dict, value)
        for key in value:
            expect(str, key)
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
