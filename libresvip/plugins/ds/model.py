from typing import Literal, Optional, Union

from pydantic import (
    SerializationInfo,
    ValidationInfo,
    field_serializer,
    field_validator,
    model_serializer,
    model_validator,
)

from libresvip.model.base import BaseModel, Field


class DsItem(BaseModel):
    text: Union[str, list[str]]
    ph_seq: Union[str, list[str]]
    note_seq: Union[str, list[str]]
    note_dur_seq: Union[str, list[float]]
    is_slur_seq: Union[str, list[int]]
    ph_dur: Union[str, list[float]]
    f0_timestep: float
    f0_seq: Union[str, list[float]]
    input_type: Literal["phoneme"]
    offset: Union[str, float]
    seed: Optional[int] = None
    spk_mix: Optional[dict[str, list[float]]] = None
    spk_mix_timestep: Optional[float] = None
    gender: Optional[dict[str, list[float]]] = None
    gender_timestep: Optional[float] = None

    @field_validator("text", "note_seq", "ph_seq", mode="before")
    @classmethod
    def _validate_str_list(cls, value, _info):
        return None if value is None else value.split()

    @field_validator("f0_seq", "ph_dur", "note_dur_seq", mode="before")
    @classmethod
    def _validate_float_list(cls, value, _info):
        return None if value is None else [float(x) for x in value.split()]

    @field_validator("is_slur_seq", mode="before")
    @classmethod
    def _validate_int_list(cls, value, _info):
        return None if value is None else [int(x) for x in value.split()]

    @field_serializer(
        "f0_seq",
        "ph_dur",
        "note_dur_seq",
        "is_slur_seq",
        "text",
        "note_seq",
        "ph_seq",
        when_used="json-unless-none",
    )
    @classmethod
    def _serialize_list(cls, value, _info):
        return " ".join(str(x) for x in value)

    @field_validator("spk_mix", "gender", mode="before")
    @classmethod
    def _validate_nested_dict(cls, value, _info):
        if value is None:
            return None

        for key in value:
            value[key] = [float(x) for x in value[key].split()]
        return value

    @field_serializer("spk_mix", "gender", when_used="json-unless-none")
    @classmethod
    def _serialize_nested_dict(cls, value, _info):
        return {key: " ".join(str(x) for x in value[key]) for key in value}


class DsProject(BaseModel):
    root: list[DsItem] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def populate_root(cls, values, _info: ValidationInfo):
        return {"root": values} if isinstance(values, list) else values

    @model_serializer(mode="wrap")
    def _serialize(self, handler, info: SerializationInfo):
        data = handler(self)
        return data["root"] if info.mode == "json" and isinstance(data, dict) else data

    @classmethod
    def model_modify_json_schema(cls, json_schema):
        return json_schema["properties"]["root"]
