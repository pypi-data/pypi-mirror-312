from __future__ import annotations

import collections
import types
import typing
from dataclasses import dataclass

from . import illusions, records


class Log(collections.deque[records.Record]):
    def append(self, record: records.Record) -> None:
        if isinstance(record, records.CallRecord):
            prev_record = self.pop()
            if not (
                isinstance(prev_record, records.GetRecord)
                and prev_record.name == record.name
            ):
                super().append(prev_record)
        return super().append(record)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, list):
            return list(self) == value
        return super().__eq__(value)


@dataclass(kw_only=True)
class AttrLogger:
    name: str
    attr: object

    def __get__(
        self, instance: illusions.Illusion, owner: typing.Type[illusions.Illusion]
    ) -> object:
        instance.__deceiver_log__.append(
            records.GetRecord(name=self.name, value=self.attr)
        )
        if isinstance(self.attr, types.FunctionType):
            return CallLogger(name=self.name, func=self.attr, instance=instance)
        return self.attr

    def __set__(self, instance: illusions.Illusion, value: typing.Callable) -> None:
        instance.__deceiver_log__.append(records.SetRecord(name=self.name, value=value))
        self.attr = value


@dataclass(kw_only=True)
class CallLogger:
    name: str
    func: types.FunctionType
    instance: illusions.Illusion

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        result = self.func(self.instance, *args, **kwargs)
        self.instance.__deceiver_log__.append(
            records.CallRecord(name=self.name, args=args, kwargs=kwargs, result=result)
        )
        return result
