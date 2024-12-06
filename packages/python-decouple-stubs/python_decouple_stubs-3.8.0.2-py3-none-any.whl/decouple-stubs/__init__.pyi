# coding: utf-8
import string
from collections import Iterable
from enum import Enum
from pathlib import Path
from typing import (
    Callable,
    Generic,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
    overload,
)

from typing_extensions import override

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E", bound=Enum)

def strtobool(value: Union[bool, str]) -> bool: ...

class UndefinedValueError(Exception): ...
class Undefined(object): ...

undefined: Undefined
DEFAULT_ENCODING: str

class Config(object):
    def __init__(self, repository: RepositoryEmpty) -> None: ...
    def _cast_boolean(self, value: str) -> bool: ...
    @staticmethod
    def _cast_do_nothing(value: T) -> T: ...
    @overload
    def get(
        self,
        option: str,
        default: Undefined = undefined,
        cast: Undefined = undefined,
    ) -> str: ...
    # HACK:
    # I don't know why, if I remove Enum overloads, Pyright thinks the return type is type[Enum] and not the instance.
    @overload
    def __call__(
        self,
        option: str,
        default: E,
        cast: type[E],
    ) -> E: ...
    @overload
    def __call__(
        self,
        option: str,
        default: Undefined = undefined,
        cast: type[E] = Enum,
    ) -> E: ...
    @overload
    def get(
        self,
        option: str,
        default: T,
        cast: Callable[[str], T],
    ) -> T: ...
    @overload
    def get(
        self,
        option: str,
        default: Undefined = undefined,
        cast: Callable[[str], T] = str,
    ) -> T: ...
    @overload
    def get(
        self,
        option: str,
        default: T,
        cast: Undefined = undefined,
    ) -> T | str: ...
    @overload
    def __call__(
        self,
        option: str,
        default: Undefined = undefined,
        cast: Undefined = undefined,
    ) -> str: ...
    @overload
    def __call__(
        self,
        option: str,
        default: T,
        cast: Callable[[str], U],
    ) -> T | U: ...
    @overload
    def __call__(
        self,
        option: str,
        default: Undefined = undefined,
        cast: Callable[[str], T] = str,
    ) -> T: ...
    @overload
    def __call__(
        self,
        option: str,
        default: T,
        cast: Undefined = undefined,
    ) -> T | str: ...

class RepositoryEmpty(object):
    def __init__(
        self, source: Union[str, Path] = "", encoding: str = DEFAULT_ENCODING
    ) -> None: ...
    def __contains__(self, key: str) -> bool: ...
    def __getitem__(self, key: str) -> str: ...

class RepositoryIni(RepositoryEmpty):
    @override
    def __init__(
        self, source: Union[str, Path], encoding: str = DEFAULT_ENCODING
    ) -> None: ...

class RepositoryEnv(RepositoryEmpty):
    @override
    def __init__(
        self, source: Union[str, Path], encoding: str = DEFAULT_ENCODING
    ) -> None: ...

class RepositorySecret(RepositoryEmpty):
    @override
    def __init__(self, source: Union[str, Path] = "/run/secrets/") -> None: ...

class AutoConfig(object):
    def __init__(self, search_path: Union[str, Path, None] = None) -> None: ...
    def _find_file(self, path: Union[str, Path]) -> str: ...
    def _load(self, path: Union[str, Path]) -> None: ...
    def _caller_path(self) -> str: ...
    @overload
    def __call__(
        self,
        option: str,
        default: Undefined = undefined,
        cast: Undefined = undefined,
    ) -> str: ...
    # HACK:
    # I don't know why, if I remove Enum overloads, Pyright thinks the return type is type[Enum] and not the instance.
    @overload
    def __call__(
        self,
        option: str,
        default: E,
        cast: type[E],
    ) -> E: ...
    @overload
    def __call__(
        self,
        option: str,
        default: Undefined = undefined,
        cast: type[E] = Enum,
    ) -> E: ...
    @overload
    def __call__(
        self,
        option: str,
        default: T,
        cast: Callable[[str], U],
    ) -> T | U: ...
    @overload
    def __call__(
        self,
        option: str,
        default: Undefined = undefined,
        cast: Callable[[str], T] = str,
    ) -> T: ...
    @overload
    def __call__(
        self,
        option: str,
        default: T,
        cast: Undefined = undefined,
    ) -> T | str: ...

config: AutoConfig

# TODO:
# I'm still undecided on how to type hint those implementations without using Higher Kinded Types.
# For now, I'm using Enums and lambda functions in my projects for simplicity's sake.
class Csv(Generic[T]):
    def __init__(
        self,
        cast: Callable[[str], T] = str,
        delimiter: str = ",",
        strip: str = string.whitespace,
        post_process: type[Iterable[T]] = list,
    ) -> None: ...
    def __call__(self, value: str) -> Iterable[T]: ...

class Choices(Generic[T]):
    def __init__(
        self,
        flat: Optional[List[T]] = None,
        cast: Callable[[str], T] = str,
        choices: Optional[Tuple[str, T]] = None,
    ) -> None: ...
    def __call__(self, value: str) -> T: ...
