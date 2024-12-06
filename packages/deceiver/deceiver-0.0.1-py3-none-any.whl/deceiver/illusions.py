from __future__ import annotations

import typing

from . import log


class IllusionNamespace(dict):
    def __setitem__(self, key: str, value: object) -> None:
        if not key.startswith('__') or key == '__init__':
            value = log.AttrLogger(name=key, attr=value)
        super().__setitem__(key, value)


class IllusionMeta(type):
    @classmethod
    def __prepare__(
        metacls: typing.Type[type], name: str, bases: tuple[type, ...], /, **kwargs
    ) -> typing.Mapping[str, object]:
        return IllusionNamespace()


class Illusion(metaclass=IllusionMeta):
    __deceiver_log__: log.Log
    __deceiver_prefix__: str = ''

    def __new__(
        cls,
        *args,
        _deceiver_log: log.Log | None = None,
        _prefix: str | None = None,
        **kwargs,
    ) -> typing.Self:
        self = super().__new__(cls, *args, **kwargs)
        if _deceiver_log is None:
            _deceiver_log = log.Log()
        self.__deceiver_log__ = _deceiver_log
        if _prefix is not None:
            self.__deceiver_prefix__ = f'{_prefix}.'
        return self
