from abc import abstractmethod
from typing import Generic, Tuple, Type, TypeVar, Union

from ..error import WrongNumberOfTypeArgsException, IsNotSubtypeException
from ..initialise import name_type_translate

TypeArgsType = TypeVar(
    'TypeArgsType',
    bound=Tuple[Union['UFDLType', str, int, Type['UFDLType'], Type[str], Type[int]], ...]
)

# The Python type that is used to represent values of a UFDLType on a worker node
PythonType = TypeVar('PythonType')


class UFDLType(Generic[TypeArgsType, PythonType]):
    """
    Base class for all types used by the UFDL system.
    """
    # Whether this type is abstract (should not be instantiated)
    _abstract: bool = True

    def __init_subclass__(cls, **kwargs):
        cls._abstract = kwargs.pop("abstract", False)
        if not isinstance(cls._abstract, bool):
            cls._abstract = bool(cls._abstract)

    def __init__(
            self,
            type_args: TypeArgsType
    ):
        # Get the base types of our type parameters
        type_params_expected_base_types = self.type_params_expected_base_types()

        # Make sure the correct number of type arguments were passed
        num_type_args = len(type_args)
        num_type_params = len(type_params_expected_base_types)
        if num_type_args != num_type_params:
            raise WrongNumberOfTypeArgsException(name_type_translate(type(self)), num_type_args, num_type_params)

        # Check each type argument is a sub-type of its expected base type
        from ..util import is_subtype, format_type_or_type_class
        for type_arg, type_param_expected_base_type in zip(type_args, type_params_expected_base_types):
            if not is_subtype(type_arg, type_param_expected_base_type):
                raise IsNotSubtypeException(
                    format_type_or_type_class(type_arg),
                    format_type_or_type_class(type_param_expected_base_type)
                )

        self._type_args: TypeArgsType = type_args

    @property
    def type_args(self) -> TypeArgsType:
        return self._type_args

    @property
    def abstract(self) -> bool:
        return self._abstract or any(
            isinstance(type_arg, UFDLType)
            and type_arg.abstract
            for type_arg in self._type_args
        )

    def __eq__(self, other):
        return (
            isinstance(other, UFDLType)
            and
            type(self) == type(other)
            and
            self._type_args == other._type_args
        )

    def is_subtype_of(self, other: 'UFDLType') -> bool:
        """
        Checks if this type is a sub-type of the given type.

        :param other:
                    The type to check for inheritance.
        """
        from ..util import is_subtype
        return (
                isinstance(self, type(other))
                and
                all(
                        is_subtype(type_arg, other_type_arg)
                        for type_arg, other_type_arg in zip(self._type_args, other._type_args)
                )
        )

    @classmethod
    def type_base_equivalent(cls) -> 'UFDLType[TypeArgsType]':
        return cls(cls.type_params_expected_base_types())

    @classmethod
    @abstractmethod
    def type_params_expected_base_types(cls) -> Tuple[
        Union[
            Type['UFDLType'],
            'UFDLType',
            Type[str],
            Type[int]
        ],
        ...
    ]:
        """
        Gets a tuple of the base-types of this type's generic type parameters.

        :return:
                    The base types for the generic type parameters. Each is one of:
                    - A type of UFDLType, indicating the given type must be an instance of this base type.
                    - A UFDLType instance, indicating that the given type must be a sub-type of this base type.
                    - str, indicating that the type argument should be a string value.
                    - int, indicating that the type argument should be an int value.
        """
        raise NotImplementedError(cls.type_params_expected_base_types.__name__)

    @abstractmethod
    def parse_binary_value(self, value: bytes) -> PythonType:
        """
        Parses a raw value supplied as binary into the Python-type.

        :param value:
                    The value to parse, as binary.
        :return:
                    The value parsed into Python.
        """
        raise NotImplementedError(self.parse_binary_value.__name__)

    @abstractmethod
    def format_python_value(self, value: PythonType) -> bytes:
        """
        Formats a Python value into binary.

        :param value:
                    The value to format.
        :return:
                    The serialised value.
        """
        raise NotImplementedError(self.format_python_value.__name__)