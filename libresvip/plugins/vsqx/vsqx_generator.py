import contextlib
import dataclasses
import operator

from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

from libresvip.core.lyric_phoneme.chinese import get_pinyin_series
from libresvip.core.tick_counter import shift_beat_list, shift_tempo_list
from libresvip.core.time_sync import TimeSynchronizer
from libresvip.model.base import (
    InstrumentalTrack,
    Note,
    ParamCurve,
    Project,
    SingingTrack,
    SongTempo,
    TimeSignature,
)

from .constants import BPM_RATE
from .model import (
    VocaloidStyleTypes,
    Vsq4,
    Vsq4MCtrl,
    Vsq4MonoTrack,
    Vsq4MonoUnit,
    Vsq4MusicalPart,
    Vsq4Note,
    Vsq4ParameterNames,
    Vsq4Singer,
    Vsq4StereoTrack,
    Vsq4StereoUnit,
    Vsq4Tempo,
    Vsq4TimeSig,
    Vsq4TypeParamAttr,
    Vsq4TypePhonemes,
    Vsq4VsTrack,
    Vsq4VsUnit,
    Vsq4VVoice,
    Vsq4WavPart,
)
from .options import OutputOptions
from .vocaloid_pitch import generate_for_vocaloid


@dataclasses.dataclass
class VsqxGenerator:
    options: OutputOptions
    style_params: dict = dataclasses.field(init=False)
    time_synchronizer: TimeSynchronizer = dataclasses.field(init=False)

    def generate_project(self, project: Project) -> Vsq4:
        self.style_params = VocaloidStyleTypes().model_dump(by_alias=True)
        self.time_synchronizer = TimeSynchronizer(project.song_tempo_list)
        vsqx = Vsq4()
        mixer = vsqx.mixer
        master_track = vsqx.master_track
        tick_prefix = int(project.time_signature_list[0].bar_length())
        master_track.time_sig = self.generate_time_signatures(
            project.time_signature_list, master_track.pre_measure
        )
        master_track.tempo = self.generate_tempos(project.song_tempo_list, tick_prefix)
        vsqx.v_voice_table.v_voice.append(
            Vsq4VVoice(
                comp_id=self.options.default_comp_id,
                v_voice_name=self.options.default_singer_name,
            )
        )
        vsqx.vs_track, mixer.vs_unit = self.generate_singing_tracks(
            [track for track in project.track_list if isinstance(track, SingingTrack)],
            tick_prefix,
        )
        if first_instrumental_track := next(
            (
                track
                for track in project.track_list
                if isinstance(track, InstrumentalTrack)
            ),
            None,
        ):
            self.generate_instrumental_track(
                first_instrumental_track, vsqx, tick_prefix
            )
        return vsqx

    def generate_instrumental_track(
        self, track: InstrumentalTrack, vsqx: Vsq4, tick_prefix: int
    ):
        with contextlib.suppress(CouldntDecodeError, FileNotFoundError):
            audio_segment = AudioSegment.from_file(track.audio_file_path)
            wav_part = Vsq4WavPart(
                part_name=track.title,
                file_path=track.audio_file_path,
                pos_tick=tick_prefix + track.offset,
                play_time=round(self.time_synchronizer.get_actual_ticks_from_secs_offset(
                    track.offset, audio_segment.duration_seconds
                )) - track.offset,
                sample_rate=audio_segment.frame_rate,
                sample_reso=audio_segment.sample_width * 8,
                channels=audio_segment.channels,
            )
            if audio_segment.channels == 1:
                vsqx.mixer.mono_unit = Vsq4MonoUnit(
                    mute=int(track.mute),
                    solo=int(track.solo),
                )
                vsqx.mono_track = Vsq4MonoTrack(wav_part=[wav_part])
            elif audio_segment.channels == 2:
                vsqx.mixer.stereo_unit = Vsq4StereoUnit(
                    mute=int(track.mute),
                    solo=int(track.solo),
                )
                vsqx.stereo_track = Vsq4StereoTrack(wav_part=[wav_part])

    def generate_singing_tracks(
        self, track_list: list[SingingTrack], tick_prefix: int
    ) -> tuple[list[Vsq4VsTrack], list[Vsq4VsUnit]]:
        vs_track_list = []
        vs_unit_list = []
        for track_index, track in enumerate(track_list):
            vsqx_track = Vsq4VsTrack(
                vs_track_no=track_index,
                track_name=track.title,
            )
            if track.note_list:
                musical_part = Vsq4MusicalPart(
                    pos_tick=tick_prefix,
                    play_time=track.note_list[-1].end_pos if track.note_list else 0,
                    note=self.generate_notes(track.note_list),
                    singer=[Vsq4Singer(v_bs=self.options.default_lang_id)],
                )
                musical_part.part_style.attr.extend(
                    Vsq4TypeParamAttr(
                        id=param_name,
                        value=param_value,
                    )
                    for param_name, param_value in self.style_params.items()
                    if not param_name.startswith("vib")
                )
                if pitch := self.generate_pitch(track.edited_params.pitch, track.note_list):
                    musical_part.m_ctrl = pitch
                vsqx_track.musical_part = [musical_part]
            vsqx_unit = Vsq4VsUnit(vs_track_no=track_index)
            vs_track_list.append(vsqx_track)
            vs_unit_list.append(vsqx_unit)
        return vs_track_list, vs_unit_list

    def generate_tempos(
        self, song_tempos: list[SongTempo], tick_prefix: int
    ) -> list[Vsq4Tempo]:
        song_tempos = shift_tempo_list(song_tempos, tick_prefix)
        return [
            Vsq4Tempo(
                pos_tick=song_tempo.position,
                bpm=int(song_tempo.bpm * BPM_RATE),
            )
            for song_tempo in song_tempos
        ]

    def generate_time_signatures(
        self, time_signatures: list[TimeSignature], measure_prefix: int
    ) -> list[Vsq4TimeSig]:
        time_signatures = shift_beat_list(time_signatures, measure_prefix)
        return [
            Vsq4TimeSig(
                pos_mes=time_signature.bar_index,
                nume=time_signature.numerator,
                denomi=time_signature.denominator,
            )
            for time_signature in time_signatures
        ]

    def generate_notes(self, notes: list[Note]) -> list[Vsq4Note]:
        note_list = []
        for note in notes:
            vsqx_note = Vsq4Note(
                pos_tick=note.start_pos,
                dur_tick=note.length,
                note_num=note.key_number,
                lyric=" ".join(
                    get_pinyin_series([note.lyric], filter_non_chinese=False)
                ),
            )
            vsqx_note.note_style.attr.extend(
                Vsq4TypeParamAttr(
                    id=param_name,
                    value=param_value,
                )
                for param_name, param_value in self.style_params.items()
                if param_value is not None
            )
            if note.pronunciation:
                vsqx_note.phnms = Vsq4TypePhonemes(
                    value=note.pronunciation,
                )
            note_list.append(vsqx_note)
        return note_list

    def generate_pitch(self, pitch: ParamCurve, notes: list[Note]) -> list[Vsq4MCtrl]:
        music_controls = []
        if pitch_raw_data := generate_for_vocaloid(pitch, notes):
            music_controls.extend(
                Vsq4MCtrl(
                    pos_tick=pbs_event.pos,
                    attr=Vsq4TypeParamAttr(
                        id=Vsq4ParameterNames.PBS,
                        value=pbs_event.value,
                    ),
                )
                for pbs_event in pitch_raw_data.pbs
            )
            music_controls.extend(
                Vsq4MCtrl(
                    pos_tick=pit_event.pos,
                    attr=Vsq4TypeParamAttr(
                        id=Vsq4ParameterNames.PIT,
                        value=pit_event.value,
                    ),
                )
                for pit_event in pitch_raw_data.pit
            )
            music_controls.sort(key=operator.attrgetter("pos_tick"))
        return music_controls