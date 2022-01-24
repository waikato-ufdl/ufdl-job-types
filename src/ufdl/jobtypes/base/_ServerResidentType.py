from abc import abstractmethod
from typing import Dict, List

from wai.json.raw import RawJSONElement

from ..initialise import list_function
from ._UFDLJSONType import UFDLJSONType, TypeArgsType, PythonType


class ServerResidentType(
    UFDLJSONType[TypeArgsType, PythonType],
    abstract=True
):
    @abstractmethod
    def server_table_name(self) -> str:
        raise NotImplementedError(self.server_table_name.__name__)

    @abstractmethod
    def filter_rules(self) -> Dict[str, str]:
        raise NotImplementedError(self.filter_rules.__name__)

    def list_all_values(self) -> List[RawJSONElement]:
        """
        Gets a list of all applicable values from the server.
        """
        return [
            self.parse_json_value(value)
            for value in list_function(self.server_table_name(), self.filter_rules())
        ]
