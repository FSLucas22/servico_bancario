from datetime import datetime
from functools import wraps
from typing import Callable, Generic, Protocol, TypeAlias, TypeVar

class ParserError(Exception):
    pass


T = TypeVar('T', covariant=True)


class InputGetter(Protocol, Generic[T]):
    def __call__(self, msg: str, error_msg: str | None = None) -> T:
        ...


def input_getter(parser: Callable[[str], T]) -> InputGetter[T]:
    @wraps(parser)
    def wrapped(msg: str, error_msg: str | None = None) -> T:
        if error_msg is None:
            error_msg = msg
        
        try:
            return parser(input(msg))
        except ParserError:
            return wrapped(error_msg, error_msg)
    
    return wrapped


@input_getter
def get_float(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise ParserError


@input_getter
def get_natural(value: str) -> int:
    if value.isnumeric():
        return int(value)
    
    raise ParserError


@input_getter
def get_str(value: str) -> str:
    if value:
        return value
    raise ParserError


def get_date(msg: str, error_msg: str | None = None,
             format: str = "%d/%m/%Y") -> datetime:
    if error_msg is None:
        error_msg = msg
    
    try:
        return datetime.strptime(input(msg), format)
    except ValueError as e:
        return get_date(error_msg, error_msg, format)


@input_getter
def get_cpf(value: str) -> str:
    if value.isnumeric():
        return value
    raise ParserError


U = TypeVar("U")
Acao: TypeAlias = Callable[[U], None]
Menu: TypeAlias = dict[str, Acao[U]]


def get_from_menu(menu: Menu[U], msg: str, error_msg: str) -> Acao[U]:
    def parser(value: str) -> Acao:
        value = value.upper().strip()
        if value in menu:
            return menu[value]
        raise ParserError
    return input_getter(parser)(msg, error_msg)
