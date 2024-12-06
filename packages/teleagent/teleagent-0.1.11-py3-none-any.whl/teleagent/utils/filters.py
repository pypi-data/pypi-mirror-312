import functools
import operator
import typing as tp

__all__ = ["TelethonFilter"]

Operator = tp.Callable[[tp.Any, tp.Any], bool]
Path = list[str]
Value = tp.Any


class TelethonFilter:
    _operator_postfix_func_mapping: dict[str, Operator] = {
        "eq": operator.eq,
        "ne": operator.ne,
        "is": operator.is_,
        "is_not": operator.is_not,
        "lt": operator.lt,
        "gt": operator.gt,
        "lte": operator.le,
        "gte": operator.ge,
        "isinstance": isinstance,
    }
    _default_operator_postfix = "eq"
    _path_separator = "__"
    _self_prefix = "self"

    def __init__(self, **criteria: Value) -> None:
        self._criteria = criteria
        self._compiled_criteria = self.compile(self._criteria)

    def __call__(self, obj: tp.Any) -> bool:
        for paths, op, value in self._compiled_criteria:
            curr_obj = obj
            for attr in paths:
                if attr != self._self_prefix:
                    curr_obj = getattr(curr_obj, attr, None)
                if curr_obj is None:
                    return False
            if not op(curr_obj, value):
                return False
        return True

    @classmethod
    def compile(cls, criteria: tp.Mapping[str, Value]) -> list[tuple[Path, Operator, Value]]:
        compiled_filters = []

        for key, value in criteria.items():
            path, op = key.split(cls._path_separator), cls._default_operator_postfix
            if path[-1] in cls._operator_postfix_func_mapping:
                *path, op = path
            compiled_filters.append((path, cls._operator_postfix_func_mapping[op], value))

        return compiled_filters

    def add(self, **criteria: Value) -> tp.Self:
        return self.__class__(**(self._criteria | criteria))

    def agg(self, *filters: "TelethonFilter") -> tp.Self:
        return self.__class__(**functools.reduce(lambda acc, item: acc | item.criteria, filters, self._criteria))

    @property
    def criteria(self) -> dict[str, Value]:
        return self._criteria
