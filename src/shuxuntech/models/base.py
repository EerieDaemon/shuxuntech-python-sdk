"""强类型响应模型的基类。

自定义模型只需继承 :class:`Model` 并用 ``@dataclass`` 声明字段：:

.. code-block:: python

    from dataclasses import dataclass
    from typing import Optional
    from shuxuntech.models import Model

    @dataclass
    class MyResult(Model):
        request_id: Optional[str] = None
        count: Optional[int] = None

    result = MyResult.from_dict({"requestId": "abc", "count": 2})

字段名使用 ``snake_case``，解析时会自动匹配平台返回的 ``camelCase`` 字段；
未知字段会被忽略，平台新增字段不会导致解析失败。
"""

from __future__ import annotations

import dataclasses
import re
import types
from typing import (
    Any,
    Dict,
    List,
    Mapping,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

__all__ = ["Model", "camel_to_snake", "snake_to_camel"]

_M = TypeVar("_M", bound="Model")


def camel_to_snake(name: str) -> str:
    """把 ``camelCase`` / ``PascalCase`` 转成 ``snake_case``。"""
    first = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", first).lower()


def snake_to_camel(name: str) -> str:
    """把 ``snake_case`` 转成 ``camelCase``。"""
    head, *tail = name.split("_")
    return head + "".join(part[:1].upper() + part[1:] for part in tail)


class Model:
    """所有强类型响应模型的基类。"""

    @classmethod
    def from_dict(cls: Type[_M], data: Mapping[str, Any]) -> _M:
        """把平台返回的 ``data`` 字典转换为模型实例。

        字段名按 ``snake_case`` 匹配，同时兼容原始 ``camelCase`` 键；
        未知字段会被忽略。
        """
        if not isinstance(data, Mapping):
            raise TypeError(f"{cls.__name__}.from_dict 需要 Mapping，收到 {type(data).__name__}")

        field_map = _field_map(cls)
        hints = _type_hints(cls)
        values: Dict[str, Any] = {}
        for key, value in data.items():
            name = field_map.get(key)
            if name is None and isinstance(key, str):
                name = field_map.get(camel_to_snake(key))
            if name is None:
                continue
            values[name] = _convert(value, hints.get(name, Any))
        return cls(**values)

    def to_dict(self) -> Dict[str, Any]:
        """转换为平台返回结构的字典，省略值为 ``None`` 的字段。"""
        result: Dict[str, Any] = {}
        for item in dataclasses.fields(self):
            value = getattr(self, item.name)
            if value is None:
                continue
            key = item.metadata.get("json") or snake_to_camel(item.name)
            result[key] = _to_json(value)
        return result


def _field_map(cls: Type[Model]) -> Dict[str, str]:
    cached = cls.__dict__.get("_model_field_map")
    if cached is not None:
        return cached

    mapping: Dict[str, str] = {}
    for item in dataclasses.fields(cls):
        if not item.init:
            continue
        json_key = item.metadata.get("json") or snake_to_camel(item.name)
        mapping[item.name] = item.name
        mapping[json_key] = item.name
        mapping[camel_to_snake(json_key)] = item.name

    setattr(cls, "_model_field_map", mapping)
    return mapping


def _type_hints(cls: Type[Model]) -> Dict[str, Any]:
    cached = cls.__dict__.get("_model_hints")
    if cached is not None:
        return cached
    hints = get_type_hints(cls)
    setattr(cls, "_model_hints", hints)
    return hints


def _convert(value: Any, hint: Any) -> Any:
    if value is None:
        return None

    origin = get_origin(hint)
    if origin is Union or origin is getattr(types, "UnionType", None):
        args = [arg for arg in get_args(hint) if arg is not type(None)]
        return _convert(value, args[0]) if args else value

    if origin in (list, List):
        args = get_args(hint)
        if not isinstance(value, (list, tuple)):
            return value
        item_hint = args[0] if args else Any
        return [_convert(item, item_hint) for item in value]

    if origin is dict or origin is Dict:
        return value

    if isinstance(hint, type) and issubclass(hint, Model):
        if isinstance(value, hint):
            return value
        return hint.from_dict(value)

    return _coerce_scalar(value, hint)


def _coerce_scalar(value: Any, hint: Any) -> Any:
    """按注解做宽松转换，尽量兼容平台把数字/布尔返回成字符串的情况。"""
    if hint is str:
        if isinstance(value, str):
            return value
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (int, float)):
            return str(value)
        return value

    if hint is bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in ("true", "1", "yes")
        if isinstance(value, (int, float)):
            return bool(value)
        return value

    if hint is int:
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, int):
            return value
        if isinstance(value, float) and value.is_integer():
            return int(value)
        if isinstance(value, str):
            try:
                return int(value.strip())
            except ValueError:
                return value
        return value

    if hint is float:
        if isinstance(value, bool):
            return float(value)
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            try:
                return float(value.strip())
            except ValueError:
                return value
        return value

    return value


def _to_json(value: Any) -> Any:
    if isinstance(value, Model):
        return value.to_dict()
    if isinstance(value, (list, tuple)):
        return [_to_json(item) for item in value]
    if isinstance(value, Mapping):
        return {key: _to_json(item) for key, item in value.items()}
    return value
