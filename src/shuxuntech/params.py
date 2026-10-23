"""接口请求参数，按 ``application/x-www-form-urlencoded`` 提交。

参数值为 ``None`` 时表示删除该参数，不会被提交；``bool`` 会转成小写的
``"true"`` / ``"false"``，其余值按 ``str()`` 转成字符串。

直接传 ``dict`` 给 :class:`~shuxuntech.client.ShuxunClient` 也可以，
本类只提供链式写法：

.. code-block:: python

    params = Params.create().put("name", "张三").put("idCard", "110101199001011234")
"""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any, Dict, Iterator, Mapping, Optional

__all__ = ["Params", "ParamsLike", "stringify_param"]

ParamsLike = Optional[Mapping[str, Any]]


def stringify_param(value: Any) -> str:
    """把参数值转成表单需要的字符串。

    ``None`` 由调用方负责过滤；``bool`` 转成小写，其余值使用 ``str()``。
    """
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (bytes, bytearray, memoryview)):
        raise TypeError("参数值不支持 bytes，请先自行解码为字符串")
    return str(value)


class Params(MutableMapping[str, str]):
    """保持插入顺序的参数集合，支持链式调用。"""

    __slots__ = ("_values",)

    def __init__(self, values: Optional[Mapping[str, Any]] = None) -> None:
        self._values: Dict[str, str] = {}
        if values:
            for name, value in values.items():
                self.put(name, value)

    @classmethod
    def create(cls) -> "Params":
        """创建空参数集合。"""
        return cls()

    @classmethod
    def of(cls, name: str, value: Any) -> "Params":
        """创建只包含一个参数的集合。"""
        return cls().put(name, value)

    def put(self, name: str, value: Any) -> "Params":
        """设置参数。

        :param name: 参数名，不能为空
        :param value: 参数值，为 ``None`` 时删除该参数
        :return: 当前对象，便于链式调用
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("参数名不能为空")
        if value is None:
            self._values.pop(name, None)
        else:
            self._values[name] = stringify_param(value)
        return self

    def remove(self, name: str) -> "Params":
        """删除参数。"""
        self._values.pop(name, None)
        return self

    def as_dict(self) -> Dict[str, str]:
        """返回参数副本，保持插入顺序。"""
        return dict(self._values)

    def __setitem__(self, key: str, value: Any) -> None:
        self.put(key, value)

    def __getitem__(self, key: str) -> str:
        return self._values[key]

    def __delitem__(self, key: str) -> None:
        del self._values[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    def __repr__(self) -> str:
        # 只输出参数名，避免把身份证号、手机号等敏感值写进日志
        return f"Params({list(self._values)!r})"
