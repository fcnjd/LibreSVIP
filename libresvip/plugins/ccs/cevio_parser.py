import dataclasses
import operator
from typing import Optional

import more_itertools

from libresvip.core.tick_counter import skip_beat_list, skip_tempo_list
from libresvip.core.time_sync import TimeSynchronizer
from libresvip.model.base import (
    InstrumentalTrack,
    Note,
    Project,
    SingingTrack,
    SongTempo,
    TimeSignature,
    Track,
)

from .cevio_pitch import CeVIOPitchEvent, CeVIOTrackPitchData, pitch_from_cevio_track
from .constants import OCTAVE_OFFSET, TICK_RATE
from .model import CeVIOCreativeStudioProject, CeVIOData, CeVIOGroup, CeVIOUnit
from .options import InputOptions


@dataclasses.dataclass
class CeVIOParser:
    options: InputOptions
    time_synchronizer: TimeSynchronizer = dataclasses.field(init=False)
    singer_id2name: dict[str, str] = dataclasses.field(default_factory=dict)

    def parse_project(self, ccs_project: CeVIOCreativeStudioProject) -> Project:
        scene_node = ccs_project.sequence.scene
        for sound_source in ccs_project.generation.svss.sound_sources.sound_source:
            self.singer_id2name[sound_source.sound_source_id] = sound_source.name
        singing_unit_nodes = [
            unit_node
            for unit_node in scene_node.units.unit
            if unit_node.category == "SingerSong"
        ]
        audio_unit_nodes = [
            unit_node
            for unit_node in scene_node.units.unit
            if unit_node.category == "OuterAudio"
        ]
        id2group = {group.group_id: group for group in scene_node.groups.group}

        tracks: list[Track] = []
        tempos = []
        time_signatures = []
        for index, unit_node in enumerate(singing_unit_nodes):
            group_id = unit_node.group
            group = id2group.get(group_id)
            track_name = group.name if group is not None else None
            track, tempo_part, time_signature_part = self.parse_singing_track(
                index, unit_node, group, track_name
            )
            tracks.append(track)
            tempos.extend(tempo_part)
            time_signatures.extend(time_signature_part)

        tempos = self.merge_tempos(tempos)
        time_signatures = self.merge_time_signatures(time_signatures)

        self.time_synchronizer = TimeSynchronizer(tempos)

        for index, unit_node in enumerate(audio_unit_nodes):
            group_id = unit_node.group
            group = id2group.get(group_id)
            track_name = group.name if group is not None else None
            track = self.parse_instrumental_track(index, unit_node, group, track_name)
            tracks.append(track)

        return Project(
            track_list=tracks,
            time_signature_list=skip_beat_list(time_signatures, 0),
            song_tempo_list=skip_tempo_list(tempos, 0),
        )

    def merge_tempos(self, tempos: list[SongTempo]) -> list[SongTempo]:
        buckets = more_itertools.bucket(tempos, operator.attrgetter("position"))
        return [next(buckets[key]) for key in buckets]

    def merge_time_signatures(
        self, time_signatures: list[TimeSignature]
    ) -> list[TimeSignature]:
        buckets = more_itertools.bucket(
            time_signatures, operator.attrgetter("bar_index")
        )
        return [next(buckets[key]) for key in buckets]

    def parse_instrumental_track(
        self,
        index: int,
        unit_node: CeVIOUnit,
        group_node: CeVIOGroup,
        track_name: Optional[str],
    ) -> InstrumentalTrack:
        return InstrumentalTrack(
            title=track_name or f"Track {index + 1}",
            audio_file_path=unit_node.file_path,
            mute=group_node.is_muted,
            solo=group_node.is_solo,
            offset=int(
                self.time_synchronizer.get_actual_ticks_from_secs(
                    unit_node.start_time.duration
                )
            ),
        )

    def parse_singing_track(
        self,
        index: int,
        unit_node: CeVIOUnit,
        group_node: CeVIOGroup,
        track_name: Optional[str],
    ) -> tuple[SingingTrack, list[SongTempo], list[TimeSignature]]:
        time_nodes = unit_node.song.beat.time

        prev_tick = 0
        time_signatures = [
            TimeSignature(bar_index=0, numerator=4, denominator=4),
        ]
        for time_node in time_nodes:
            tick = time_node.clock // TICK_RATE
            numerator = time_node.beats
            denominator = time_node.beat_type

            if tick is not None and numerator is not None and denominator is not None:
                ticks_in_measure = time_signatures[-1].bar_length()
                tick_diff = tick - prev_tick
                measure_diff = tick_diff / ticks_in_measure
                time_signatures.append(
                    TimeSignature(
                        bar_index=int(
                            time_signatures[-1].bar_index + measure_diff,
                        ),
                        numerator=numerator,
                        denominator=denominator,
                    )
                )
                prev_tick = tick

        time_signatures = [
            time_signature.model_copy(
                update={"bar_index": time_signature.bar_index - 4}
            )
            for time_signature in time_signatures
        ]

        tick_prefix = int(time_signatures[0].bar_length())

        tempos = []
        tempo_nodes = unit_node.song.tempo.sound
        for tempo_node in tempo_nodes:
            tick = (
                tempo_node.clock // TICK_RATE - tick_prefix
                if tempo_node.clock is not None
                else None
            )
            bpm = float(tempo_node.tempo) if tempo_node.tempo is not None else None
            if tick is not None and bpm is not None:
                tempos.append(SongTempo(position=tick, bpm=bpm))

        notes = []
        note_nodes = unit_node.song.score.note
        for note_node in note_nodes:
            tick_on = (
                (note_node.clock // TICK_RATE) - tick_prefix
                if note_node.clock is not None
                else None
            )
            duration = (
                (note_node.duration // TICK_RATE)
                if note_node.duration is not None
                else None
            )
            pitch_step = (
                note_node.pitch_step if note_node.pitch_step is not None else None
            )
            pitch_octave = (
                note_node.pitch_octave - OCTAVE_OFFSET
                if note_node.pitch_octave is not None
                else None
            )
            key = (
                pitch_step + pitch_octave * 12
                if pitch_step is not None and pitch_octave is not None
                else None
            )
            lyric = note_node.lyric or None
            if (
                tick_on is not None
                and duration is not None
                and key is not None
                and lyric is not None
            ):
                notes.append(
                    Note(
                        key_number=key, lyric=lyric, start_pos=tick_on, length=duration
                    )
                )

        cevio_track_pitch_data = None
        if (
            unit_node.song.parameter is not None
            and unit_node.song.parameter.log_f0 is not None
        ):
            pitch_data_nodes: list[CeVIOData] = unit_node.song.parameter.log_f0.data
            pitch_datas = []
            for data_node in pitch_data_nodes:
                if pitch_data := self.parse_pitch_data(data_node):
                    pitch_datas.append(pitch_data)
            cevio_track_pitch_data = CeVIOTrackPitchData(
                events=pitch_datas, tempos=tempos, tick_prefix=tick_prefix
            )

        track_name = track_name or f"Track {index + 1}"
        track = SingingTrack(
            ai_singer_name=self.singer_id2name.get(unit_node.cast_id, ""),
            title=track_name,
            note_list=notes,
            mute=group_node.is_muted,
            solo=group_node.is_solo,
        )
        if (
            cevio_track_pitch_data is not None
            and (pitch := pitch_from_cevio_track(cevio_track_pitch_data)) is not None
        ):
            track.edited_params.pitch = pitch
        return track, tempos, time_signatures

    @staticmethod
    def parse_pitch_data(data_element: CeVIOData) -> Optional[CeVIOPitchEvent]:
        value = float(data_element.value) if data_element.value is not None else None
        if value is not None:
            index = data_element.index or None
            repeat = data_element.repeat or None
            return CeVIOPitchEvent(index=index, repeat=repeat, value=value)
