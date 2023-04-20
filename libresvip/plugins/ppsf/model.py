from typing import Generic, List, Optional, TypeVar

from pydantic import Field
from pydantic.generics import GenericModel

from libresvip.model.base import BaseModel

ConstValue = TypeVar("ConstValue")


class PpsfConst(GenericModel, Generic[ConstValue]):
    const: ConstValue
    use_sequence: bool


class PpsfBaseSequence(BaseModel):
    constant: int
    name: str
    sequence: List
    use_sequence: bool


class PpsfSeqParam(BaseModel):
    base_sequence: PpsfBaseSequence = Field(alias="base-sequence")
    layers: List


class PpsfCurvePointSeq(BaseModel):
    border_type: Optional[int] = Field(alias="border-type")
    note_index: int = Field(alias="note-index")
    region_index: int = Field(alias="region-index")


class PpsfCurvePoint(BaseModel):
    plugin_descriptor: Optional[str] = Field(alias="plugin-descriptor")
    sequence: List[PpsfCurvePointSeq]
    sub_track_category: int = Field(alias="sub-track-category")
    sub_track_id: int = Field(alias="sub-track-id")


class PpsfSyllable(BaseModel):
    footer_text: str = Field(alias="footer-text")
    header_text: str = Field(alias="header-text")
    is_list_end: bool = Field(alias="is-list-end")
    is_list_top: bool = Field(alias="is-list-top")
    is_word_end: bool = Field(alias="is-word-end")
    is_word_top: bool = Field(alias="is-word-top")
    lyric_text: str = Field(alias="lyric-text")
    symbols_text: str = Field(alias="symbols-text")


class PpsfNote(BaseModel):
    language: int
    region_index: int = Field(alias="region-index")
    syllables: List[PpsfSyllable]
    event_index: Optional[int]
    length: Optional[int]
    muted: Optional[bool]
    vibrato_preset_id: Optional[int]
    voice_color_id: Optional[int]
    voice_release_id: Optional[int]
    note_env_preset_id: Optional[int]
    note_gain_value: Optional[int]
    note_param_edited_stats: Optional[int]
    portamento_length: Optional[int]
    portamento_offset: Optional[int]


class PpsfRegion(BaseModel):
    auto_expand_left: Optional[bool] = Field(alias="auto-expand-left")
    auto_expand_right: Optional[bool] = Field(alias="auto-expand-right")
    length: int
    muted: bool
    name: str
    position: int
    z_order: int = Field(alias="z-order")
    audio_event_index: Optional[int] = Field(alias="audio-event-index")


class PpsfSubTrack(BaseModel):
    height: int
    plugin_descriptor: Optional[str] = Field(alias="plugin-descriptor")
    sub_track_category: int = Field(alias="sub-track-category")
    sub_track_id: int = Field(alias="sub-track-id")


class PpsfParamPoint(BaseModel):
    curve_type: int
    pos: int
    value: int


class PpsfParameter(BaseModel):
    constant: int
    default: Optional[int]
    max: Optional[int]
    min: Optional[int]
    name: str
    sequence: List[PpsfParamPoint]
    use_sequence: bool


class PpsfFsmEffect(BaseModel):
    parameters: List[PpsfParameter]
    plugin_id: int = Field(alias="plugin-id")
    plugin_name: str = Field(alias="plugin-name")
    power_state: bool = Field(alias="power-state")
    program_name: str = Field(alias="program-name")
    program_number: int = Field(alias="program-number")
    version: str


class PpsfEventTrack(BaseModel):
    curve_points: List[PpsfCurvePoint] = Field(alias="curve-points")
    fsm_effects: Optional[List[PpsfFsmEffect]] = Field(alias="fsm-effects")
    height: int
    index: int
    mute_solo: Optional[int] = Field(alias="mute-solo")
    notes: Optional[List[PpsfNote]] = Field(default_factory=list)
    nt_envelope_preset_id: Optional[int] = Field(alias="nt-envelope-preset-id")
    regions: List[PpsfRegion]
    sub_tracks: List[PpsfSubTrack] = Field(alias="sub-tracks")
    total_height: int = Field(alias="total-height")
    track_type: int = Field(alias="track-type")
    vertical_scale: int = Field(alias="vertical-scale")
    vertical_scroll: int = Field(alias="vertical-scroll")


class PpsfTempoTrack(BaseModel):
    height: int
    vertical_scale: int = Field(alias="vertical-scale")
    vertical_scroll: int = Field(alias="vertical-scroll")


class PpsfTrackEditor(BaseModel):
    event_tracks: List[PpsfEventTrack] = Field(alias="event-tracks")
    header_width: int = Field(alias="header-width")
    height: int
    horizontal_scale: float = Field(alias="horizontal-scale")
    horizontal_scroll: int = Field(alias="horizontal-scroll")
    tempo_track: PpsfTempoTrack = Field(alias="tempo-track")
    user_markers: Optional[List] = Field(alias="user-markers", default_factory=list)
    width: int
    x: int
    y: int


class PpsfLoopPoint(BaseModel):
    begin: int
    enable: Optional[bool]
    enabled: Optional[bool]
    end: int


class PpsfMetronome(BaseModel):
    enable: Optional[bool]
    enabled: Optional[bool]
    wav: str


class PpsfGuiSettings(BaseModel):
    loop_point: Optional[PpsfLoopPoint]
    metronome: Optional[PpsfMetronome]
    ambient_enabled: Optional[bool] = Field(alias="ambient-enabled")
    file_fullpath: str = Field(alias="file-fullpath")
    playback_position: int = Field(alias="playback-position")
    project_length: int = Field(alias="project-length")
    track_editor: PpsfTrackEditor = Field(alias="track-editor")


class PpsfFileAudioData(BaseModel):
    file_path: str
    tempo: int


class PpsfAudioTrackEvent(BaseModel):
    file_audio_data: PpsfFileAudioData
    playback_offset_sample: int
    tick_length: int
    tick_pos: int


class PpsfMixer(BaseModel):
    gain: PpsfSeqParam
    mixer_type: str
    panpot: PpsfSeqParam


class PpsfAudioTrackItem(BaseModel):
    block_size: int
    enabled: bool
    events: List[PpsfAudioTrackEvent]
    input_channel: int
    mixer: PpsfMixer
    name: str
    output_channel: int
    sampling_rate: int


class PpsfMeter(BaseModel):
    denomi: int
    nume: int


class PpsfSingerParam(BaseModel):
    breathiness: int
    brightness: int
    clearness: int
    gender_factor: int
    opening: int


class PpsfSingerTableItem(BaseModel):
    cid1: str
    name: str
    param1: PpsfSingerParam


class PpsfVibDepthItem(BaseModel):
    curve_type: int
    pos: int
    value: int


class PpsfVibRateItem(BaseModel):
    curve_type: int
    pos: int
    value: int


class PpsfVocaloidTrackEvent(BaseModel):
    accent: int
    bend_depth: int
    bend_length: int
    decay: int
    fall_port: bool
    length: int
    lyric: str
    note_number: int
    opening: int
    pos: int
    protected: bool
    rise_port: bool
    symbols: str
    velocity: int
    vib_category: int
    vib_offset: int
    vib_depth: Optional[List[PpsfVibDepthItem]] = None
    vib_rate: Optional[List[PpsfVibRateItem]] = None


class PpsfVocaloidTrackItem(BaseModel):
    events: List[PpsfVocaloidTrackEvent]
    mixer: PpsfMixer
    name: str
    parameters: List[PpsfParameter]
    singer: int


class PpsfSinger(BaseModel):
    character_name: str
    do_extrapolation: bool
    frame_shift: float
    gender: int
    language_id: int
    library_id: str
    name: str
    singer_name: str
    stationaly_type: str
    synthesis_version: str
    tail_silent: float
    vprm_morph_mode: str


class PpsfEnvelope(BaseModel):
    length: int
    offset: int
    points: List
    use_length: bool


class PpsfDvlTrackEvent(BaseModel):
    adjust_speed: bool
    attack_speed_rate: int
    consonant_rate: int
    consonant_speed_rate: int
    enabled: bool
    length: int
    lyric: str
    note_number: int
    note_off_pit_envelope: PpsfEnvelope
    note_on_pit_envelope: PpsfEnvelope
    portamento_envelope: PpsfEnvelope
    portamento_type: int
    pos: int
    protected: bool
    release_speed_rate: int
    symbols: str
    vcl_like_note_off: bool


class PpsfDvlTrackItem(BaseModel):
    enabled: bool
    events: List[PpsfDvlTrackEvent]
    mixer: PpsfMixer
    name: str
    parameters: List[PpsfSeqParam]
    plugin_output_bus_index: int
    singer: PpsfSinger


class PpsfInnerProject(BaseModel):
    audio_track: List[PpsfAudioTrackItem]
    block_size: int
    loop_point: Optional[PpsfLoopPoint]
    meter: PpsfConst[PpsfMeter]
    metronome: Optional[PpsfMetronome]
    name: str
    sampling_rate: int
    singer_table: List[PpsfSingerTableItem]
    tempo: PpsfConst[int]
    vocaloid_track: List[PpsfVocaloidTrackItem]
    dvl_track: Optional[List[PpsfDvlTrackItem]]


class PpsfRoot(BaseModel):
    app_ver: str
    gui_settings: PpsfGuiSettings
    ppsf_ver: str
    project: PpsfInnerProject


class PpsfProject(BaseModel):
    ppsf: PpsfRoot
