"""IP 归属地返回模型。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .base import Model


@dataclass
class IpQueryCityResult(Model):
    """ip归属地查询。"""

    continent: Optional[str] = None

    country: Optional[str] = None

    country_code: Optional[str] = None

    province: Optional[str] = None

    city: Optional[str] = None

    lng: Optional[str] = None

    lat: Optional[str] = None

    ad_code: Optional[str] = None

    post_code: Optional[str] = None

    timezone: Optional[str] = None

    isp: Optional[str] = None

    accuracy: Optional[str] = None
