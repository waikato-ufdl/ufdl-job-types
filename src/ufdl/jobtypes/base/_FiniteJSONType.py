from typing import List

from wai.json.raw import RawJSONElement

from ._UFDLJSONType import UFDLJSONType, TypeArgsType, InputType, OutputType


class FiniteJSONType(
    UFDLJSONType[TypeArgsType, InputType, OutputType]
):
    def list_all_json_values(self) -> List[RawJSONElement]:
        """
        Gets a list of all applicable values from the server.
        """
        raise NotImplementedError(self.list_all_json_values.__name__)
