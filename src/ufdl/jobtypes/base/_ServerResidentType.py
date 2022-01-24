from abc import abstractmethod
from typing import Dict, List

from wai.json.raw import RawJSONElement, RawJSONObject

from ..initialise import list_function
from ._UFDLJSONType import UFDLJSONType, TypeArgsType


class ServerResidentType(
    UFDLJSONType[TypeArgsType, RawJSONObject],
    abstract=True
):
    @abstractmethod
    def server_table_name(self) -> str:
        raise NotImplementedError(self.server_table_name.__name__)

    @abstractmethod
    def filter_rules(self) -> Dict[str, str]:
        raise NotImplementedError(self.filter_rules.__name__)

    def list_all_values(self) -> List[RawJSONObject]:
        """
        Gets a list of all applicable values from the server.
        """
        return [
            self.parse_json_value(value)
            for value in list_function(self.server_table_name(), self.filter_rules())
        ]

    def parse_json_value(self, value: RawJSONElement) -> RawJSONObject:
        self.validate_with_schema(value)
        return value

    def format_python_value_to_json(self, value: RawJSONObject) -> RawJSONElement:
        self.validate_with_schema(value)
        return value
