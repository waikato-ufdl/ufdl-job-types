from abc import abstractmethod
from typing import Generic, Type, TypeVar, Union

from ..error import WrongNumberOfTypeArgsException, IsNotSubtypeException
from ..initialise import name_type_translate
from ..util import format_type_or_type_class

TypeArgType = TypeVar('TypeArgType', bound=Union['UFDLType', None, str, int])


class NoTypeArg:
    """
    Symbolic class representing the absence of a type-parameter
    """
    pass


class UFDLType(Generic[TypeArgType]):
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
            type_arg: TypeArgType
    ):
        type_arg_expected_base_type = self.type_arg_expected_base_type()
        if type_arg_expected_base_type is NoTypeArg:
            # No type argument expected, so error if one is given
            if type_arg is not None:
                raise WrongNumberOfTypeArgsException(name_type_translate(type(self)), 1, 0)
        else:
            if type_arg is None:
                raise WrongNumberOfTypeArgsException(name_type_translate(type(self)), 0, 1)
            elif type_arg_expected_base_type is not None:
                # A specific type of type-argument is expected
                if type_arg_expected_base_type is str or type_arg_expected_base_type is int:
                    if not isinstance(type_arg, type_arg_expected_base_type):
                        raise IsNotSubtypeException(
                            format_type_or_type_class(type_arg),
                            str(type_arg_expected_base_type)
                        )
                elif not type_arg.is_subtype_of(type_arg_expected_base_type):
                    raise IsNotSubtypeException(
                        format_type_or_type_class(type_arg),
                        format_type_or_type_class(type_arg_expected_base_type)
                    )
        self._type_arg: TypeArgType = type_arg

    @property
    def type_arg(self) -> TypeArgType:
        return self._type_arg

    @property
    def abstract(self) -> bool:
        return self._abstract

    def __eq__(self, other):
        return (
            isinstance(other, UFDLType)
            and
            type(self) == type(other)
            and
            self._type_arg == other._type_arg
        )

    def is_subtype_of(self, other: Union[Type['UFDLType'], 'UFDLType']) -> bool:
        """
        Checks if this type is a sub-type of the given type.

        :param other:
                    The type to check for inheritance.
        """
        # If a type class is given, just need to be an instance of that class
        if not isinstance(other, UFDLType):
            return isinstance(self, other)

        # Get our type argument
        type_arg = self._type_arg

        return (
                isinstance(self, type(other))
                and
                (
                        type_arg is None  # Implies other._type_arg is also None
                        or (
                                isinstance(type_arg, (str, int))
                                and type_arg == other._type_arg
                        )
                        or type_arg.is_subtype_of(other._type_arg)
                )
        )

    @classmethod
    @abstractmethod
    def type_arg_expected_base_type(cls) -> Union[
        Type[TypeArgType],
        TypeArgType,
        Type[NoTypeArg],
        Type[str],
        Type[int]
    ]:
        """
        Gets a tuple of the base-types of this type's generic type arguments.

        :return:
                    The base type for the generic type argument. One of:
                    - A type of UFDLType, indicating the given type must be an instance of this base type.
                    - A UFDLType instance, indicating that the given type must be a sub-type of this base type.
                    - NoTypeArg, indicating that this type doesn't take a type argument.
                    - str, indicating that the type argument should be a string value.
                    - int, indicating that the type argument should be an int value.
        """
        raise NotImplementedError(cls.type_arg_expected_base_type.__name__)
