from typing import List

from ufdl.json.core.filter import FilterSpec

from wai.json.raw import RawJSONElement

from ._UFDLJSONType import UFDLJSONType, TypeArgsType, PythonType


class ServerResidentType(
    UFDLJSONType[TypeArgsType, PythonType]
):
    def server_table_name(self) -> str:
        raise NotImplementedError(self.server_table_name.__name__)

    def filter_rules(self) -> FilterSpec:
        raise NotImplementedError(self.filter_rules.__name__)

    def list_all_values(self) -> List[RawJSONElement]:
        """
        Gets a list of all applicable values from the server.
        """
        from ..initialise import list_function
        return list_function(self.server_table_name(), self.filter_rules())
