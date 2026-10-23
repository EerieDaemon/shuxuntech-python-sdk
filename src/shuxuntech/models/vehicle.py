"""交通出行返回模型。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .base import Model


@dataclass
class Vin2Result(Model):
    """VIN车架号查询精准版返回结果。"""

    #: 查询结果，1:查询成功，2:无记录
    result: Optional[int] = None

    #: 车辆信息
    info: Optional[Vin2Info] = None


@dataclass
class Vin2Info(Model):
    #: 发动机号
    engineno: Optional[str] = None

    #: 燃料种类
    fueltype: Optional[str] = None

    #: 总质量
    totalweight: Optional[str] = None

    #: 颜色
    color: Optional[str] = None

    #: 生产日期
    productiondate: Optional[str] = None

    #: 车等级，暂时没用
    carlevel: Optional[str] = None

    #: 后轮距
    reartrack: Optional[str] = None

    #: 货箱栏板内尺寸高
    boxheight: Optional[str] = None

    #: 发动机型号
    enginemodel: Optional[str] = None

    #: 油耗
    comfuelconsumption: Optional[str] = None

    #: 货箱栏板内尺寸宽
    boxwidth: Optional[str] = None

    #: 前轮距
    fronttrack: Optional[str] = None

    #: 外形尺寸(mm) 长
    len: Optional[str] = None

    #: 指导价格
    price: Optional[str] = None

    #: 车体结构
    bodytype: Optional[str] = None

    #: 排量
    displacement: Optional[str] = None

    #: 车辆型号
    model: Optional[str] = None

    #: 车架号
    vin: Optional[str] = None

    #: 车品牌
    brand: Optional[str] = None

    #: 排放标准
    environmentalstandards: Optional[str] = None

    #: 外形尺寸(mm)高
    height: Optional[str] = None

    #: 驱动方式
    drivemode: Optional[str] = None

    #: 额定载质量(kg)
    ratedloadweight: Optional[str] = None

    #: 最大功率(kW)
    maxpower: Optional[str] = None

    #: 排量(ml)
    displacementml: Optional[str] = None

    #: 货箱栏板内尺寸(mm) 长
    boxlen: Optional[str] = None

    #: 整备质量(kg)
    weight: Optional[str] = None

    #: 轮胎数
    tirenum: Optional[str] = None

    #: 轮胎规格
    tiresize: Optional[str] = None

    #: 车组
    groupname: Optional[str] = None

    #: 年款
    yeartype: Optional[str] = None

    #: 座位数
    seatnum: Optional[str] = None

    #: 轴距
    wheelbase: Optional[str] = None

    #: 轴数
    axlenum: Optional[str] = None

    #: 车系名称
    name: Optional[str] = None

    #: 外形尺寸(mm)宽
    width: Optional[str] = None


@dataclass
class Vin2_1Result(Model):
    """VIN车架号查询精准优质版返回结果。"""

    #: 品牌名称
    brand: Optional[str] = None

    #: 车系名称
    series: Optional[str] = None

    #: 车型名称
    model_name: Optional[str] = None

    #: 年款
    years: Optional[str] = None

    #: 厂商指导价
    price: Optional[str] = None

    #: 上市时间
    time_to_market: Optional[str] = None

    #: 厂商
    factory: Optional[str] = None

    #: 车辆等级
    level: Optional[str] = None

    #: 销售状态
    sales_status: Optional[str] = None

    #: 车身结构
    body: Optional[str] = None

    #: 长*宽*高
    model_size: Optional[str] = None

    #: 整备质量
    curb_weight: Optional[str] = None

    #: 车门
    door: Optional[str] = None

    #: 座位数
    seat: Optional[str] = None

    #: 排量
    displacement: Optional[str] = None

    #: 档位数
    shift_num: Optional[str] = None

    #: 发动机型号
    engine_code: Optional[str] = None

    #: 排量(L/T)
    engine: Optional[str] = None

    #: 发动机描述
    engine_desc: Optional[str] = None

    #: 最大功率
    max_power: Optional[str] = None

    #: 前制动器类型
    front_brake: Optional[str] = None

    #: 后制动器类型
    rear_brake: Optional[str] = None

    #: 助力类型
    assist_type: Optional[str] = None

    #: 轴距
    wheel_base: Optional[str] = None

    #: 前轮距
    wheel_base_font: Optional[str] = None

    #: 后轮距
    wheel_base_rear: Optional[str] = None

    #: 前轮胎规格
    front_tire: Optional[str] = None

    #: 后轮胎规格
    rear_tire: Optional[str] = None

    #: 备胎规格
    spare_tire: Optional[str] = None

    #: 驱动方式
    driver_type: Optional[str] = None

    #: 变速箱类型
    trans_type: Optional[str] = None

    #: 变速箱描述
    trans_des: Optional[str] = None

    #: 进气形式
    engine_gas_in: Optional[str] = None

    #: 每缸气门数(个)
    engine_gasin_number: Optional[str] = None

    #: 气缸排列形式
    engine_cylinder_arranged: Optional[str] = None

    #: 燃油类型
    fuel_type: Optional[str] = None

    #: 燃油标号
    fuel_grade: Optional[str] = None

    #: 供油方式
    oil_providing: Optional[str] = None

    #: 排放标准
    emission_standard: Optional[str] = None

    #: 非销售车型的其他信息，有销售车型时一般为空
    vehicle: Optional[List[Vin2_1Vehicle]] = None


@dataclass
class Vin2_1Vehicle(Model):
    """非销售车型的其他属性。"""

    #: 属性
    key: Optional[str] = None

    #: 属性值
    value: Optional[str] = None


@dataclass
class Vin5Result(Model):
    """车架号精准版带公告号返回结果。"""

    #: 车架号
    vin: Optional[str] = None

    #: 公告号
    model_code: Optional[str] = None

    #: 品牌名称
    brand: Optional[str] = None

    #: 厂商
    factory_name: Optional[str] = None

    #: 最大功率
    max_power: Optional[str] = None

    #: 气缸排列形式
    engine_cylinder_arranged: Optional[str] = None

    #: 气缸数(个)
    engine_cylinder_number: Optional[str] = None

    #: 每缸气门数(个)
    engine_gasin_number: Optional[str] = None

    #: 年款
    years: Optional[str] = None

    #: 指导价
    price: Optional[str] = None

    #: 车系
    series: Optional[str] = None

    #: 车型名称
    model_name: Optional[str] = None

    #: 前制动器类型
    front_brake: Optional[str] = None

    #: 后制动器类型
    rear_brake: Optional[str] = None

    #: 助力类型
    assist_type: Optional[str] = None

    #: 轴距(mm)
    wheel_base: Optional[str] = None

    #: 前轮胎规格
    front_tire: Optional[str] = None

    #: 后轮胎规格
    rear_tire: Optional[str] = None

    #: 备胎规格
    spare_tire: Optional[str] = None

    #: 下市时间(停售)
    time_to_halted: Optional[str] = None

    #: 上市年份
    listing_year: Optional[str] = None

    #: 上市月份
    listing_month: Optional[str] = None

    #: 生产时间
    product_time: Optional[str] = None

    #: 发动机型号
    engine_code: Optional[str] = None

    #: 驱动方式
    driver: Optional[str] = None

    #: 排放标准
    emission_standard: Optional[str] = None

    #: 车辆等级
    level: Optional[str] = None

    #: 排量
    displacement: Optional[str] = None

    #: 进气形式
    intake: Optional[str] = None

    #: 燃油类型
    fuel_type: Optional[str] = None

    #: 燃油标号
    fuel_grade: Optional[str] = None

    #: 档位数
    shift_number: Optional[str] = None

    #: 车门数
    door: Optional[str] = None

    #: 座位数
    seat: Optional[str] = None

    #: 底盘号
    chassis_code: Optional[str] = None

    #: 变速器类型
    trans_type: Optional[str] = None

    #: 变速器描述
    trans_desc: Optional[str] = None


@dataclass
class CarFiveResult(Model):
    """车五项查询返回结果。"""

    car_number: Optional[str] = None

    brand_name: Optional[str] = None

    engine_model: Optional[str] = None

    #: 发动机号码
    engine_number: Optional[str] = None

    vin_code: Optional[str] = None

    reg_date: Optional[str] = None

    vehicle_code: Optional[str] = None
