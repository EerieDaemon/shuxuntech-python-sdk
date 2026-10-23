"""身份核验返回模型。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .base import Model


@dataclass
class IdCardCommonResult(Model):
    """身份证解析数据。"""

    #: 生日，eg: 19930123
    birthday: Optional[str] = None

    #: 性别(1 : 男 ， 0 : 女)
    gender: Optional[int] = None

    #: 年龄
    age: Optional[int] = None

    #: 省份
    province: Optional[str] = None

    #: 城市
    city: Optional[str] = None

    #: 区县
    district: Optional[str] = None

    #: 籍贯
    area: Optional[str] = None


@dataclass
class IdCardCheckResult(IdCardCommonResult):
    """实名结果。"""

    #: 1: 一致 2: 不一致 3: 无记录，不计费
    result: Optional[int] = None

    #: 核验结果描述
    result_desc: Optional[str] = None

    def __post_init__(self) -> None:
        if self.result_desc is None and self.result is not None:
            if self.result == 1:
                self.result_desc = "核验一致"
            elif self.result == 2:
                self.result_desc = "核验不一致"
            else:
                self.result_desc = "无记录"


@dataclass
class FaceIdCardResult(IdCardCommonResult):
    """人脸身份证比对结果。"""

    #: 1: 身份证号与姓名匹配，照片系统判断为同一人 2: 身份证号与姓名匹配，照片不能确定是否为同一人 3: 身份证号与姓名匹配，照片系统判断为不同人 4: 身份证号与姓名不匹配 5:
    #: 身份证号与姓名匹配，库中无照片 6: 身份证号与姓名匹配，照片检测失败 7: 库中无此号 8: 照片质量不合格
    result: Optional[int] = None

    #: 一所分值区间 [0，600）系统判断为不同人； [600，700）不能确定是否为同一人； [700，1000]系统判断为同一人；
    hack_score: Optional[float] = None


@dataclass
class FaceCompareResult(Model):
    """人脸比对。"""

    #: 1: 比对成功，有数据 2: 比对成功，无数据 3：比对失败，无法正确解析、未按要求传入参数、下载图片超时
    result: Optional[int] = None

    #: 识别结果描述
    result_desc: Optional[str] = None

    #: 置信度
    confidence: Optional[float] = None

    #: 置信度阈值
    threshold: Optional[FaceCompareThreshold] = None


@dataclass
class FaceCompareThreshold(Model):
    threshold1: Optional[float] = None

    threshold2: Optional[float] = None

    threshold3: Optional[float] = None


@dataclass
class LivingCheckResult(Model):
    """图片活体返回结果。"""

    #: 活体检测最高分
    max_score: Optional[float] = None

    #: 是否是活体，1：是活体；0：不是活体
    is_living: Optional[int] = None

    #: 每张图片的检测情况
    faces: Optional[List[LivingCheckFace]] = None


@dataclass
class LivingCheckFace(Model):
    #: 活体检测分数
    score: Optional[float] = None

    #: 合成图打分，判断图片是否为合成图
    spoofing: Optional[float] = None

    #: 是否带眼睛 none:无眼镜，common:普通眼镜，sun:墨镜
    glasses: Optional[str] = None

    #: 性别 male:男性 female:女性
    gender: Optional[str] = None
