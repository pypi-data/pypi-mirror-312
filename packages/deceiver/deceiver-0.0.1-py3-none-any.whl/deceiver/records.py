from __future__ import annotations

import typing
from dataclasses import astuple, dataclass, is_dataclass


@dataclass(kw_only=True)
class Record:
    action: str
    name: str

    def __repr__(self) -> str:
        return f'[{self.action}] {self.name}'

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, str):
            return repr(self) == obj
        if is_dataclass(obj) and not isinstance(obj, type):
            return astuple(self) == astuple(obj)
        return NotImplemented


@dataclass(eq=False, kw_only=True)
class GetRecord(Record):
    action: typing.Literal['get'] = 'get'
    value: object

    def __repr__(self) -> str:
        return f'{super().__repr__()} -> {self.value!r}'


@dataclass(eq=False, kw_only=True)
class SetRecord(Record):
    action: typing.Literal['set'] = 'set'
    value: object

    def __repr__(self) -> str:
        return f'{super().__repr__()} = {self.value!r}'


@dataclass(eq=False, kw_only=True)
class CallRecord(Record):
    action: typing.Literal['call'] = 'call'
    args: tuple
    kwargs: dict
    result: object

    def __repr__(self) -> str:
        return (
            f'{super().__repr__()} (*{self.args!r}, **{self.kwargs!r})'
            f' -> {self.result!r}'
        )
