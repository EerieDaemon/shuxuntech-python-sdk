"""文字识别返回模型。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .base import Model


@dataclass
class IdCardOcrResult(Model):
    """身份证OCR。"""

    #: 1: 识别成功，有数据 2: 识别成功，无数据 3：识别失败，无法正确解析、未按要求传入参数、下载图片超时
    result: Optional[int] = None

    #: 识别结果描述
    result_desc: Optional[str] = None

    info: Optional[IdCardOcrInfo] = None


@dataclass
class IdCardOcrInfo(Model):
    side: Optional[str] = None

    type: Optional[int] = None

    front: Optional[IdCardOcrFront] = None

    back: Optional[IdCardOcrBack] = None


@dataclass
class IdCardOcrFront(Model):
    birthday: Optional[str] = None

    address: Optional[str] = None

    gender: Optional[str] = None

    race: Optional[str] = None

    name: Optional[str] = None

    id_card: Optional[str] = None


@dataclass
class IdCardOcrBack(Model):
    issued_by: Optional[str] = None

    valid_date: Optional[str] = None


@dataclass
class WordOcrResult(Model):
    """通用文字OCR。"""

    #: 1:识别成功有数据 2:参数错误未识别到数据
    result: Optional[int] = None

    text_info: Optional[List[WordOcrTextInfo]] = field(default=None, metadata={"json": "text_info"})


@dataclass
class WordOcrTextInfo(Model):
    line_no: Optional[int] = field(default=None, metadata={"json": "line_no"})

    confidence: Optional[float] = None

    line_content: Optional[str] = field(default=None, metadata={"json": "line_content"})

    line_position: Optional[WordOcrLinePosition] = field(default=None, metadata={"json": "line_position"})


@dataclass
class WordOcrLinePosition(Model):
    x: Optional[int] = None

    width: Optional[int] = None

    y: Optional[int] = None

    height: Optional[int] = None

    line_direction: Optional[int] = field(default=None, metadata={"json": "line_direction"})


@dataclass
class BusinessOcrResult(Model):
    """营业执照OCR。"""

    #: 1: 识别成功，有数据 2: 识别成功，无数据 3：识别失败，无法正确解析、未按要求传入参数、下载图片超时
    result: Optional[int] = None

    #: 识别结果描述
    result_desc: Optional[str] = None

    info: Optional[BusinessOcrInfo] = None


@dataclass
class BusinessOcrInfo(Model):
    enterprise_type: Optional[str] = None

    address: Optional[str] = None

    registration_capital: Optional[str] = None

    op_to: Optional[str] = None

    org_form: Optional[str] = None

    op_scope: Optional[str] = None

    establishing_date: Optional[str] = None

    legal_name: Optional[str] = None

    registration_code: Optional[str] = None

    op_from: Optional[str] = None

    credit_code: Optional[str] = None

    op_period: Optional[str] = None

    enterprise_name: Optional[str] = None

    is_copy: Optional[int] = None


@dataclass
class DrivingOcrResult(Model):
    """驾驶证OCR。"""

    #: 1: 识别成功，有数据 2: 识别成功，无数据 3：识别失败，无法正确解析、未按要求传入参数、下载图片超时
    result: Optional[int] = None

    #: 识别结果描述
    result_desc: Optional[str] = None

    #: 主页
    main: Optional[DrivingOcrMain] = None

    #: 副页
    second: Optional[DrivingOcrSecond] = None


@dataclass
class DrivingOcrMain(Model):
    birthday: Optional[str] = None

    issued_by: Optional[str] = None

    address: Optional[str] = None

    gender: Optional[str] = None

    valid_from: Optional[str] = None

    version: Optional[str] = None

    license_number: Optional[str] = None

    valid_date: Optional[str] = None

    nationality: Optional[str] = None

    issue_date: Optional[str] = None

    name: Optional[str] = None

    category: Optional[str] = None

    valid_for: Optional[str] = None


@dataclass
class DrivingOcrSecond(Model):
    file_number: Optional[str] = None

    name: Optional[str] = None

    license_number: Optional[str] = None


@dataclass
class PlateOcrResult(Model):
    """车牌号OCR。"""

    #: 1: 识别成功，有数据 2: 识别成功，无数据 3：识别失败，无法正确解析、未按要求传入参数、下载图片超时
    result: Optional[int] = None

    #: 识别结果描述
    result_desc: Optional[str] = None

    info: Optional[PlateOcrInfo] = None


@dataclass
class PlateOcrInfo(Model):
    plate_no: Optional[str] = None

    color: Optional[str] = None


@dataclass
class VehicleOcrResult(Model):
    """行驶证OCR。"""

    #: 1: 识别成功，有数据 2: 识别成功，无数据 3：识别失败，无法正确解析、未按要求传入参数、下载图片超时
    result: Optional[int] = None

    #: 识别结果描述
    result_desc: Optional[str] = None

    #: 主页（正页）扫描信息
    info: Optional[VehicleOcrInfo] = None

    #: 副页扫描信息
    back_info: Optional[VehicleOcrBackInfo] = None


@dataclass
class VehicleOcrInfo(Model):
    #: 所有人
    owner: Optional[str] = None

    #: 发证机关
    issued_by: Optional[str] = None

    #: 证件面：front-主页，back-副页
    side: Optional[str] = None

    #: 住址
    address: Optional[str] = None

    #: 车辆类型
    vehicle_type: Optional[str] = None

    #: 注册日期
    register_date: Optional[str] = None

    #: 证件类型
    type: Optional[int] = None

    #: 发动机号
    engine_no: Optional[str] = None

    #: 发证日期
    issue_date: Optional[str] = None

    #: 号牌号码
    plate_no: Optional[str] = None

    #: 使用性质
    use_character: Optional[str] = None

    #: 品牌型号
    model: Optional[str] = None

    #: 车辆识别代号
    vin: Optional[str] = None


@dataclass
class VehicleOcrBackInfo(Model):
    #: 证件面：front-主页，back-副页
    side: Optional[str] = None

    #: 证件类型
    type: Optional[int] = None

    #: 号牌号码
    plate_no: Optional[str] = None

    #: 发证机关
    issued_by: Optional[str] = None

    #: 住址
    address: Optional[str] = None

    #: 档案编号
    file_no: Optional[str] = None

    #: 副页编号
    sub_page_code: Optional[str] = None

    #: 核定载人数
    allow_num: Optional[str] = None

    #: 总质量
    total_mass: Optional[str] = None

    #: 整备质量
    curb_weight: Optional[str] = None

    #: 核定载质量
    load_quality: Optional[str] = None

    #: 准牵引总质量
    total_quasi_mass: Optional[str] = None

    #: 外廓尺寸
    external_size: Optional[str] = None

    #: 燃油种类
    fuel_type: Optional[str] = None

    #: 备注
    marks: Optional[str] = None

    #: 检验记录
    record: Optional[str] = None


@dataclass
class VinOcrResult(Model):
    """通用文字OCR。"""

    #: 1:识别成功有数据 2:参数错误未识别到数据或不符合车架号规则
    result: Optional[int] = None

    vin: Optional[str] = None

    brand: Optional[str] = None

    #: 汽车厂商
    manufacturer: Optional[str] = None
