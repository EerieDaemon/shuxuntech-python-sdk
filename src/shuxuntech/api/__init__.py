"""按业务分类的强类型接口。"""

from .bankcard import BankcardApi
from .enterprise import EnterpriseApi
from .express import ExpressApi
from .identity import IdentityApi
from .ip import IpApi
from .mobile import MobileApi
from .ocr import OcrApi
from .vehicle import VehicleApi

__all__ = [
    "BankcardApi",
    "EnterpriseApi",
    "ExpressApi",
    "IdentityApi",
    "IpApi",
    "MobileApi",
    "OcrApi",
    "VehicleApi",
]
