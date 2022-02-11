from typing import List

from ufdl.json.core.filter import FilterExpression, FilterSpec

from wai.json.raw import RawJSONElement

from ._FiniteJSONType import FiniteJSONType, TypeArgsType, InputType, OutputType


class ServerResidentType(
    FiniteJSONType[TypeArgsType, InputType, OutputType]
):
    def server_table_name(self) -> str:
        raise NotImplementedError(self.server_table_name.__name__)

    def filter_rules(self) -> List[FilterExpression]:
        raise NotImplementedError(self.filter_rules.__name__)

    def list_all_json_values(self) -> List[RawJSONElement]:
        """
        Gets a list of all applicable values from the server.
        """
        return self.get_filtered_list_of_json_values()

    def get_filtered_list_of_json_values(self, *filter_expressions: FilterExpression) -> List[RawJSONElement]:
        from ..initialise import list_function
        filter_spec = FilterSpec(expressions=[*self.filter_rules(), *filter_expressions])
        return list_function(self.server_table_name(), filter_spec)
