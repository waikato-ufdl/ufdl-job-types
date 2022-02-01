from abc import abstractmethod
from typing import Generic, Optional, Tuple, TypeVar

from wai.common.meta import instanceoptionalmethod

from ..error import WrongNumberOfTypeArgsException, IsNotSubtypeException

TypeArgsType = TypeVar(
    'TypeArgsType',
    bound=Tuple['UFDLType', ...]
)

# The Python type that is used to represent values of a UFDLType on a worker node
PythonType = TypeVar('PythonType')


class UFDLType(Generic[TypeArgsType, PythonType]):
    """
    Base class for all types used by the UFDL system.
    """
    def __init_subclass__(cls, **kwargs):
        base_types = cls.type_params_expected_base_types()

        if not isinstance(base_types, tuple):
            raise TypeError(f"Base-types for a {UFDLType} should be a tuple; {cls} got {base_types}")

        for base_type in base_types:
            if not isinstance(base_type, UFDLType):
                raise TypeError(f"All base-types for a {UFDLType} should be instances of {UFDLType}; {cls} got {base_type}")

    def __init__(
            self,
            type_args: Optional[TypeArgsType] = None
    ):
        # Get the base types of our type parameters
        type_params_expected_base_types = self.type_params_expected_base_types()

        if type_args is not None:
            if not isinstance(type_args, tuple):
                raise TypeError(f"Expected tuple; got {type_args}")

            # Make sure the correct number of type arguments were passed
            num_type_args = len(type_args)
            num_type_params = len(type_params_expected_base_types)
            if num_type_args != num_type_params:
                raise WrongNumberOfTypeArgsException(type(self).format_type_class_name(), num_type_args, num_type_params)

            # Check each type argument is a sub-type of its expected base type
            for type_arg, type_param_expected_base_type in zip(type_args, type_params_expected_base_types):
                if not isinstance(type_arg, UFDLType):
                    raise TypeError(f"Expected {UFDLType}; got {type_arg}")

                if not type_arg.is_subtype_of(type_param_expected_base_type):
                    raise IsNotSubtypeException(
                        str(type_arg),
                        str(type_param_expected_base_type)
                    )
        else:
            type_args = type_params_expected_base_types

        self._type_args: TypeArgsType = type_args

    @property
    def type_args(self) -> TypeArgsType:
        return self._type_args

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
        return (
                isinstance(self, type(other))
                and
                all(
                        type_arg.is_subtype_of(other_type_arg)
                        for type_arg, other_type_arg in zip(self._type_args, other._type_args)
                )
        )

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple['UFDLType', ...]:
        """
        Gets a tuple of the base-types of this type's generic type parameters.

        :return:
                    The base types for the generic type parameters. Each is one of:
                    - A type of UFDLType, indicating the given type must be an instance of this base type.
                    - A UFDLType instance, indicating that the given type must be a sub-type of this base type.
                    - str, indicating that the type argument should be a string value.
                    - int, indicating that the type argument should be an int value.
        """
        return tuple()

    def parse_binary_value(self, value: bytes) -> PythonType:
        """
        Parses a raw value supplied as binary into the Python-type.

        :param value:
                    The value to parse, as binary.
        :return:
                    The value parsed into Python.
        """
        raise NotImplementedError(self.parse_binary_value.__name__)

    def format_python_value(self, value: PythonType) -> bytes:
        """
        Formats a Python value into binary.

        :param value:
                    The value to format.
        :return:
                    The serialised value.
        """
        raise NotImplementedError(self.format_python_value.__name__)

    def __str__(self) -> str:
        return self.format()

    @instanceoptionalmethod
    def format(self) -> str:
        type_name = self.format_type_class_name()
        formatted_type_args = self.format_type_args()

        return f"{type_name}{formatted_type_args}"

    @instanceoptionalmethod
    def format_type_args(self) -> str:
        args = (
            self._type_args if instanceoptionalmethod.is_instance(self)
            else self.type_params_expected_base_types()
        )

        if len(args) == 0:
            return ""

        return f"<{', '.join(str(arg) for arg in args)}>"

    @classmethod
    def format_type_class_name(cls) -> str:
        """
        Formats the name of a type-class.

        :return:
                    The name of the type-class.
        """
        # Try to get the name from the map
        from ..initialise import type_translate
        type_class_name: Optional[str] = type_translate(cls)

        # If it wasn't in the map, use the class name
        if type_class_name is None:
            raise ValueError(f"Unnamed type {cls}")

        return type_class_name

    @property
    def is_abstract(self) -> bool:
        return True
