from typing import Optional

from ufdl.json.core.filter import FilterExpression
from wai.json.raw import RawJSONObject

from ._ServerResidentType import ServerResidentType, TypeArgsType
from ._UFDLJSONType import PythonType


class NamedServerType(
    ServerResidentType[TypeArgsType, PythonType]
):
    """
    Server types from which we can extract a unique name.
    """
    def extract_name_from_json(self, value: RawJSONObject) -> str:
        """
        Gets the name of the value from its JSON representation.

        :param value:
                    The value to extract the name from.
        :return:
                    The name.
        """
        raise NotImplementedError(self.extract_name_from_json.__name__)

    def name_filter(self, name: str) -> FilterExpression:
        """
        Gets a filter spec which filters only the instance with the given name.

        :param name:
                    The name to filter for.
        :return:
                    The filter spec.
        """
        raise NotImplementedError(self.name_filter.__name__)

    def get_json_value_by_name(self, name: str) -> Optional[RawJSONObject]:
        """
        Gets the JSON representation of the value with the specified name.

        :param name:
                    The name to look for.
        :return:
                    The JSON object representing the value on the server,
                    or None if not found.
        """
        results = self.get_filtered_list_of_json_values(self.name_filter(name))
        if len(results) == 0:
            return None
        return results[0]
