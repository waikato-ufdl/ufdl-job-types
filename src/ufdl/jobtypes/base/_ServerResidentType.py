from abc import abstractmethod
from typing import Dict, List

from ..initialise import list_function
from ._PythonType import PythonType
from ._UFDLJSONType import UFDLJSONType
from ._UFDLType import TypeArgType


class ServerResidentType(
    UFDLJSONType[TypeArgType, PythonType],
    abstract=True
):
    @abstractmethod
    def server_table_name(self) -> str:
        raise NotImplementedError(self.server_table_name.__name__)

    @abstractmethod
    def filter_rules(self) -> Dict[str, str]:
        raise NotImplementedError(self.filter_rules.__name__)

    def list_all_values(self) -> List[PythonType]:
        """
        Gets a list of all applicable values from the server.
        """
        return [
            self.parse_json_value(value)
            for value in list_function(self.server_table_name(), self.filter_rules())
        ]
