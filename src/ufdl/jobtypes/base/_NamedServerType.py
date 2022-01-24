from abc import ABC, abstractmethod

from wai.json.raw import RawJSONObject

from ._ServerResidentType import ServerResidentType, TypeArgsType


class NamedServerType(ServerResidentType[TypeArgsType], ABC):
    """
    Server types from which we can extract a unique name.
    """
    @abstractmethod
    def extract_name(self, value: RawJSONObject) -> str:
        """
        Gets the name of the value from its JSON representation.

        :param value:
                    The value to extract the name from.
        :return:
                    The name.
        """
        raise NotImplementedError(self.extract_name.__name__)

