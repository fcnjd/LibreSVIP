# flake8: noqa: N801, PLC2401
from typing import Any, Optional, Union

from pydantic import BaseModel, Field


class 大市唱打节拍(BaseModel):
    名称: Optional[str] = Field(default=None)
    颜色: Optional[str] = Field(default=None)
    风格: Optional[str] = Field(default=None)
    节拍乐器: Optional[str] = Field(default=None)
    打击乐器: Optional[str] = Field(default=None)


class 大市唱技巧(BaseModel):
    类型: Optional[str] = Field(default=None)
    开始: Optional[float] = Field(default=None)
    峰的时间: Optional[float] = Field(default=None)
    结束: Optional[float] = Field(default=None)
    峰值: Optional[float] = Field(default=None)
    峰尖锐: Optional[Union[int, float]] = Field(default=None)
    回音延迟: Optional[float] = Field(default=None)
    回音持续: Optional[float] = Field(default=None)
    强度增加: Optional[bool] = Field(default=None)
    频率增加: Optional[bool] = Field(default=None)


class 大市唱控制点数组(BaseModel):
    m倍频: Optional[int] = Field(default=None)
    m最大值: Optional[float] = Field(default=None)
    m最小值: Optional[float] = Field(default=None)
    m开始x: Optional[float] = Field(default=None)
    m峰的x: Optional[float] = Field(default=None)
    m结束x: Optional[float] = Field(default=None)
    m左尖锐: Optional[float] = Field(default=None)
    m右尖锐: Optional[float] = Field(default=None)
    m增加: Optional[bool] = Field(default=None)
    m峰值: Optional[float] = Field(default=None)
    m值: Optional[Union[float, int]] = Field(default=None)


class 大市唱控制点变化(BaseModel):
    最小值: Optional[float] = Field(default=None)
    最大值: Optional[float] = Field(default=None)
    只能为正: Optional[bool] = Field(default=None)
    上下对称: Optional[bool] = Field(default=None)
    控制点数组: list[大市唱控制点数组] = Field(default_factory=list)


class 大市唱自动谱曲(BaseModel):
    自然段开始: Optional[bool] = Field(default=False)
    高潮开始: Optional[bool] = Field(default=False)
    句子对开始: Optional[bool] = Field(default=False)
    整体势值: Optional[float] = Field(default=0.5)
    整体势值自动: Optional[bool] = Field(default=True)
    句子结构最高点: Optional[float] = Field(default=0.5)
    应用句子开头特色: Optional[bool] = Field(default=False)
    应用句子中间特色: Optional[bool] = Field(default=False)
    应用句子结尾特色: Optional[bool] = Field(default=False)
    句子音高音量对比开始: Optional[bool] = Field(default=False)
    句子音高音量对比值: Optional[bool] = Field(default=False)
    句子上下行对比开始: Optional[bool] = Field(default=False)
    句子上下行对比值: Optional[bool] = Field(default=False)
    句子音节数对比开始: Optional[bool] = Field(default=False)
    句子音节数对比值: Optional[bool] = Field(default=False)
    句子结尾音高高: Optional[bool] = Field(default=False)


class 大市唱音符自动谱曲(BaseModel):
    节拍结束: Optional[bool] = Field(default=False)
    前面的音节音高高: Optional[bool] = Field(default=False)
    前面的音节音量大: Optional[bool] = Field(default=False)
    第一个音节是爆破音较重或者送气清擦音较重: Optional[bool] = Field(default=False)
    最后一个音节时值长: Optional[bool] = Field(default=False)
    最后一个音节结束后停顿: Optional[bool] = Field(default=False)
    节拍持续时长: Optional[str] = Field(default="半拍")


class 大市唱谱曲(BaseModel):
    句子开头的节拍停顿: Optional[bool] = Field(default=False)
    句子开头两次上行: Optional[bool] = Field(default=False)
    句子最高的地方变慢突出: Optional[bool] = Field(default=False)
    上行下行之间停顿: Optional[bool] = Field(default=False)
    倒数第二个音节滑音: Optional[bool] = Field(default=False)
    倒数第二个音节上滑音下滑音交替: Optional[bool] = Field(default=False)
    倒数第二个音节变快: Optional[bool] = Field(default=False)
    倒数第二个音节加重: Optional[bool] = Field(default=False)
    最后一个节拍上行: Optional[bool] = Field(default=False)


class 大市唱音量包络(BaseModel):
    开始位置x: Optional[float] = Field(default=None)
    开始位置y: Optional[Union[float, int]] = Field(default=None)
    开始方向相对x: Optional[float] = Field(default=None)
    开始方向相对y: Optional[float] = Field(default=None)
    中间位置x: Optional[float] = Field(default=None)
    中间位置y: Optional[float] = Field(default=None)
    中间左方向相对x: Optional[float] = Field(default=None)
    中间左方向相对y: Optional[float] = Field(default=None)
    中间右方向相对x: Optional[float] = Field(default=None)
    中间右方向相对y: Optional[float] = Field(default=None)
    结束位置x: Optional[int] = Field(default=None)
    结束位置y: Optional[float] = Field(default=None)
    结束方向相对x: Optional[float] = Field(default=None)
    结束方向相对y: Optional[float] = Field(default=None)


class 大市唱附属发音小段数组(BaseModel):
    开始音标: Optional[str] = Field(default=None)
    开始音标_非音节性的影响者: Optional[str] = Field(default=None)
    开始音标_非音节性被影响的程度: Optional[float] = Field(default=None)
    𝓅清擦音最前面时域爆破: Optional[float] = Field(default=None)
    开始辅音音标: Optional[str] = Field(default=None)
    结束音标: Optional[str] = Field(default=None)
    结束音标_非音节性的影响者: Optional[str] = Field(default=None)
    结束音标_非音节性被影响的程度: Optional[float] = Field(default=None)
    持续时间: Optional[float] = Field(default=None)
    开始控制点时间: Optional[float] = Field(default=None)
    开始控制点频率: Optional[float] = Field(default=None)
    结束控制点时间: Optional[float] = Field(default=None)
    结束控制点频率: Optional[float] = Field(default=None)
    类型: Optional[str] = Field(default=None)
    继续: Optional[bool] = Field(default=None)
    待续: Optional[bool] = Field(default=None)
    结束音符是爆破音不参与参数渐变: Optional[bool] = Field(default=None)
    开始音符是爆破音不参与参数渐变: Optional[bool] = Field(default=None)
    清擦音实际长度: Optional[int] = Field(default=None)
    用于过度时使能: Optional[bool] = Field(default=None)
    用于过度时本音节的时间: Optional[int] = Field(default=None)
    浊辅音前声带音实际长度: Optional[int] = Field(default=None)
    音量包络: Optional[大市唱音量包络] = Field(default=None)


class 大市唱后面的音节过度发音小段(BaseModel):
    开始音标: Optional[str] = Field(default=None)
    开始音标_非音节性的影响者: Optional[str] = Field(default=None)
    开始音标_非音节性被影响的程度: Optional[float] = Field(default=None)
    清擦音最前面时域爆破: Optional[float] = Field(default=None, alias="𝓅清擦音最前面时域爆破")
    开始辅音音标: Optional[str] = Field(default=None)
    结束音标: Optional[str] = Field(default=None)
    结束音标_非音节性的影响者: Optional[str] = Field(default=None)
    结束音标_非音节性被影响的程度: Optional[float] = Field(default=None)
    持续时间: Optional[int] = Field(default=None)
    开始控制点时间: Optional[float] = Field(default=None)
    开始控制点频率: Optional[float] = Field(default=None)
    结束控制点时间: Optional[float] = Field(default=None)
    结束控制点频率: Optional[float] = Field(default=None)
    类型: Optional[str] = Field(default=None)
    继续: Optional[bool] = Field(default=None)
    待续: Optional[bool] = Field(default=None)
    结束音符是爆破音不参与参数渐变: Optional[bool] = Field(default=None)
    开始音符是爆破音不参与参数渐变: Optional[bool] = Field(default=None)
    清擦音实际长度: Optional[int] = Field(default=None)
    用于过度时使能: Optional[bool] = Field(default=None)
    用于过度时本音节的时间: Optional[int] = Field(default=None)
    浊辅音前声带音实际长度: Optional[int] = Field(default=None)
    音量包络: Optional[大市唱音量包络] = Field(default=None)


class 大市唱核心发音小段数组(BaseModel):
    开始音标: Optional[str] = Field(default=None)
    开始音标_非音节性的影响者: Optional[str] = Field(default=None)
    开始音标_非音节性被影响的程度: Optional[float] = Field(default=None)
    清擦音最前面时域爆破: Optional[float] = Field(default=None, alias="𝓅清擦音最前面时域爆破")
    开始辅音音标: Optional[str] = Field(default=None)
    结束音标: Optional[str] = Field(default=None)
    结束音标_非音节性的影响者: Optional[str] = Field(default=None)
    结束音标_非音节性被影响的程度: Optional[float] = Field(default=None)
    持续时间: Optional[Union[float, int]] = Field(default=None)
    开始控制点时间: Optional[float] = Field(default=None)
    开始控制点频率: Optional[float] = Field(default=None)
    结束控制点时间: Optional[float] = Field(default=None)
    结束控制点频率: Optional[float] = Field(default=None)
    类型: Optional[str] = Field(default=None)
    继续: Optional[bool] = Field(default=None)
    待续: Optional[bool] = Field(default=None)
    结束音符是爆破音不参与参数渐变: Optional[bool] = Field(default=None)
    开始音符是爆破音不参与参数渐变: Optional[bool] = Field(default=None)
    清擦音实际长度: Optional[Union[int, float]] = Field(default=None)
    用于过度时使能: Optional[bool] = Field(default=None)
    用于过度时本音节的时间: Optional[int] = Field(default=None)
    浊辅音前声带音实际长度: Optional[int] = Field(default=None)
    音量包络: Optional[大市唱音量包络] = Field(default=None)


class 大市唱发音详细参数(BaseModel):
    左附属发音小段数组: list[大市唱附属发音小段数组] = Field(default_factory=list)
    核心发音小段数组: list[大市唱核心发音小段数组] = Field(default_factory=list)
    右附属发音小段数组: list[大市唱附属发音小段数组] = Field(default_factory=list)
    后面的音节过度发音小段: Optional[大市唱后面的音节过度发音小段] = Field(default=None)


class 大市唱音色属性(BaseModel):
    振幅变化: Optional[大市唱控制点变化] = Field(default=None)
    振幅变化速度: Optional[大市唱控制点变化] = Field(default=None)
    振幅变化随机分布: Optional[大市唱控制点变化] = Field(default=None)
    频率变化: Optional[大市唱控制点变化] = Field(default=None)
    频率变化速度: Optional[大市唱控制点变化] = Field(default=None)
    频率变化随机分布: Optional[大市唱控制点变化] = Field(default=None)


class 大市唱音色(BaseModel):
    签名: Optional[str] = Field(default=None)
    类型: Optional[str] = Field(default=None)
    名称: Optional[str] = Field(default=None)
    颜色: Optional[str] = Field(default=None)
    身高: Optional[Union[float, int]] = Field(default=None)
    身高自动: Optional[bool] = Field(default=None)
    滤波: Optional[大市唱控制点变化] = Field(default=None)
    滤波跟随频率: Optional[bool] = Field(default=None)
    保留一倍频: Optional[bool] = Field(default=None)
    一倍频振幅: Optional[float] = Field(default=None)
    共振峰宽度: Optional[int] = Field(default=None)
    高阶共振峰频谱位置: Optional[float] = Field(default=None)
    音色: Optional[大市唱音色属性] = Field(default=None)
    振幅变化: Optional[大市唱控制点变化] = Field(default=None)
    振幅变化速度: Optional[大市唱控制点变化] = Field(default=None)
    频率变化: Optional[大市唱控制点变化] = Field(default=None)
    频率变化速度: Optional[大市唱控制点变化] = Field(default=None)
    数据: Optional[str] = Field(default=None)


class 大市唱音节发音(BaseModel):
    休止符: Optional[bool] = Field(default=False)
    后面连音数量: Optional[int] = Field(default=None)
    左附属辅音: Optional[str] = Field(default=None)
    左核心辅音: Optional[str] = Field(default=None)
    核心元音: Optional[str] = Field(default=None)
    右核心辅音: Optional[str] = Field(default=None)
    右附属辅音: Optional[str] = Field(default=None)
    原生表音法的音节: Optional[str] = Field(default=None)
    音符显示: Optional[str] = Field(default=None)
    辅助显示: Optional[str] = Field(default=None)
    原文: Optional[str] = Field(default=None)
    分身: Optional[int] = Field(default=None)
    原文重复序号: Optional[int] = Field(default=None)
    句子中的位置: Optional[int] = Field(default=None)
    词的结束: Optional[bool] = Field(default=None)
    发音详细参数: Optional[大市唱发音详细参数] = Field(default=None)
    右附属辅音可以借出: Optional[bool] = Field(default=None)
    右附属辅音已经借出: Optional[bool] = Field(default=None)
    右附属辅音可以去掉: Optional[bool] = Field(default=None)
    右附属辅音已经去掉: Optional[bool] = Field(default=None)
    核心左辅音可以借入: Optional[bool] = Field(default=None)
    核心左辅音是借入的: Optional[bool] = Field(default=None)
    核心左辅音可以借入的字符: Optional[str] = Field(default=None)
    左附属辅音可以去掉: Optional[bool] = Field(default=None)
    左附属辅音已经去掉: Optional[bool] = Field(default=None)


class 大市唱音符(BaseModel):
    音高: Optional[int] = Field(default=None)
    时长: Optional[Union[float, int]] = Field(default=None)
    左侧过度时长: Optional[float] = Field(default=None)
    右侧过度时长: Optional[float] = Field(default=None)
    左侧吐字自动: Optional[bool] = Field(default=None)
    左侧吐字延迟开始: Optional[float] = Field(default=None)
    左侧吐字建立耗时: Optional[float] = Field(default=None)
    右侧吐字自动: Optional[bool] = Field(default=None)
    右侧吐字消失耗时: Optional[float] = Field(default=None)
    右侧吐字提前结束: Optional[float] = Field(default=None)
    连音: Optional[bool] = Field(default=False)
    编曲修饰: list[str] = Field(default_factory=list)
    自动谱曲: Optional[大市唱音符自动谱曲] = Field(default=None)
    音节发音: Optional[大市唱音节发音] = Field(default=None)


class 大市唱声乐曲(BaseModel):
    角色: Optional[list[str]] = Field(default_factory=list)
    乐器: Optional[list[str]] = Field(default_factory=list)
    自动谱曲: Optional[大市唱自动谱曲] = Field(default_factory=大市唱自动谱曲)
    语种: Optional[str] = Field(default="chinese")
    音符: list[大市唱音符] = Field(default_factory=list)
    调号自动: Optional[bool] = Field(default=False)
    调号: Optional[int] = Field(default=60)
    每分钟拍数: Optional[int] = Field(default=120)
    说唱: Optional[bool] = Field(default=False)
    节拍配置名称: Optional[str] = Field(default="丁香")
    纯音乐: Optional[bool] = Field(default=True)
    纯朗读: Optional[bool] = Field(default=False)
    声乐曲音量: Optional[float] = Field(default=None)
    声乐曲清擦相对音量: Optional[float] = Field(default=1)
    编曲修饰音量: Optional[float] = Field(default=None)
    打节拍旋律音量: Optional[float] = Field(default=0.5)
    打节拍鼓音量: Optional[float] = Field(default=0.5)
    最后编辑时间: Optional[int] = Field(default=0)
    技巧: list[大市唱技巧] = Field(default_factory=list)
    声乐清擦: list[object] = Field(default_factory=list)
    声乐声带: list[object] = Field(default_factory=list)
    副声乐声带1: list[object] = Field(default_factory=list)
    副声乐声带2: list[object] = Field(default_factory=list)
    编曲修饰: list[object] = Field(default_factory=list)
    打节拍旋律: list[object] = Field(default_factory=list)
    打节拍鼓: list[object] = Field(default_factory=list)


class 大市唱文件格式(BaseModel):
    文件签名: str = Field(default="dscm")
    主版本号: int = Field(default=1)
    副版本号: int = Field(default=2)
    歌曲名称: str = Field(default="")
    文件名: str = Field(default="未命名")
    作者: str = Field(default="赵磊")
    组织: str = Field(default="没有组织是个人")
    说明: str = Field(default="这家伙很懒，什么都没留下")
    采样频率: int = Field(default=16000)
    正在编辑的行的索引: int = Field(default=-1)
    声乐曲: list[大市唱声乐曲] = Field(default_factory=list)
    音色: list[大市唱音色] = Field(default_factory=list)
    打节拍: list[大市唱打节拍] = Field(default_factory=list)
    编曲: Optional[dict[str, Any]] = Field(default=None)
    字典: list[dict[str, Any]] = Field(default_factory=list)
    谱曲: Optional[大市唱谱曲] = Field(default=None)
