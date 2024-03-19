import abc
from typing import Annotated, Any, Literal, Optional, Union

from pydantic import Field

from libresvip.model.base import BaseModel


class DspxMetadata(BaseModel):
    version: Optional[str] = None
    name: str
    author: str


class DspxControl(BaseModel):
    gain: float = 1.0
    mute: bool = False


class DspxLoop(BaseModel):
    start: int = 0
    length: int = 0
    enabled: bool = True


class DspxMaster(BaseModel):
    control: DspxControl = Field(default_factory=DspxControl)
    loop: DspxLoop = Field(default_factory=DspxLoop)


class DspxLabel(BaseModel):
    pos: int = 0
    text: str = ""


class DspxTempo(BaseModel):
    pos: int = 0
    value: float = 0.0


class DspxTimeSignature(BaseModel):
    index: int = 0
    numerator: int = 0
    denominator: int = 0


class DsTimeline(BaseModel):
    time_signatures: list[DspxTimeSignature] = Field(default_factory=list, alias="timeSignatures")
    tempos: list[DspxTempo] = Field(default_factory=list)
    labels: list[DspxLabel] = Field(default_factory=list)


class DspxTime(BaseModel):
    start: int = 0
    length: int = 0
    clip_start: int = Field(0, alias="clipStart")
    clip_len: int = Field(0, alias="clipLen")


class DspxParamNode(BaseModel):
    x: int = 0
    y: int = 0
    interp: Literal["linear", "hermite", "none"] = "linear"


class DspxParamFree(BaseModel):
    type_: Literal["free"] = Field("free", alias="type")
    start: int = 0
    step: int = 0
    values: list[int] = Field(default_factory=list)


class DspxParamAnchor(BaseModel):
    type_: Literal["anchor"] = Field("anchor", alias="type")
    start: int = 0
    nodes: list[DspxParamNode] = Field(default_factory=list)


DsParamCurve = Annotated[Union[DspxParamFree, DspxParamAnchor], Field(discriminator="type_")]


class DspxParam(BaseModel):
    original: list[DsParamCurve] = Field(default_factory=list)
    edited: list[DsParamCurve] = Field(default_factory=list)
    envelope: list[DsParamCurve] = Field(default_factory=list)


class DspxParams(BaseModel):
    pitch: DspxParam = Field(default_factory=DspxParam)
    energy: DspxParam = Field(default_factory=DspxParam)


class DspxVibratoPoint(BaseModel):
    x: float = 0.0
    y: float = 0.0


class DspxVibrato(BaseModel):
    start: float = 0.0
    end: float = 0.0
    freq: float = 0.0
    phase: float = 0.0
    amp: float = 0.0
    offset: float = 0.0
    points: list[DspxVibratoPoint] = Field(default_factory=list)


class DspxPhoneme(BaseModel):
    type_: Literal["ahead", "normal", "final"] = Field("normal", alias="type")
    token: str = ""
    start: int = 0


class DspxPhonemes(BaseModel):
    original: list[DspxPhoneme] = Field(default_factory=list)
    edited: list[DspxPhoneme] = Field(default_factory=list)


class DspxNote(BaseModel):
    pos: int = 0
    length: int = 0
    key_num: int = Field(0, alias="keyNum")
    lyric: str = ""
    phonemes: DspxPhonemes = Field(default_factory=DspxPhonemes)
    vibrato: DspxVibrato = Field(default_factory=DspxVibrato)
    extra: dict[str, dict[Any, Any]] = Field(default_factory=dict)


class DspxClipMixin(abc.ABC, BaseModel):
    time: DspxTime = Field(default_factory=DspxTime)
    name: str = ""
    control: DspxControl = Field(default_factory=DspxControl)


class DspxAudioClip(DspxClipMixin, BaseModel):
    type_: Literal["audio"] = Field("audio", alias="type")
    path: str = ""


class DspxSingingClip(DspxClipMixin, BaseModel):
    type_: Literal["singing"] = Field("singing", alias="type")
    sources: dict[Any, Any] = Field(default_factory=dict)
    notes: list[DspxNote] = Field(default_factory=list)
    params: DspxParams = Field(default_factory=DspxParams)


DspxClip = Annotated[Union[DspxAudioClip, DspxSingingClip], Field(discriminator="type_")]


class DspxTrackControl(BaseModel):
    gain: float = 1.0
    mute: bool = False
    solo: bool = False
    pan: float = 0.0


class DspxTrackColor(BaseModel):
    color_id: Optional[int] = Field(None, alias="id")
    value: Optional[str] = None


class DspxTrack(BaseModel):
    name: str = ""
    color: DspxTrackColor = Field(default_factory=DspxTrackColor)
    control: DspxTrackControl = Field(default_factory=DspxTrackControl)
    clips: list[DspxClip] = Field(default_factory=list)


class DspxContent(BaseModel):
    metadata: DspxMetadata
    master: DspxMaster = Field(default_factory=DspxMaster)
    timeline: DsTimeline = Field(default_factory=DsTimeline)
    params: DspxParams = Field(default_factory=DspxParams)
    tracks: list[DspxTrack] = Field(default_factory=list)


class DspxModel(BaseModel):
    version: str = "1.0.0"
    content: DspxContent = Field(default_factory=DspxContent)
    workspace: dict[str, dict[Any, Any]] = Field(default_factory=dict)
