from typing import List

from wai.json.raw import RawJSONElement

from ._UFDLJSONType import UFDLJSONType, TypeArgsType, PythonType


class FiniteJSONType(
    UFDLJSONType[TypeArgsType, PythonType]
):
    def list_all_values(self) -> List[RawJSONElement]:
        """
        Gets a list of all applicable values from the server.
        """
        raise NotImplementedError(self.list_all_values.__name__)
