import dataclasses
import operator
from typing import Optional

import more_itertools

from libresvip.core.tick_counter import (
    shift_beat_list,
    shift_tempo_list,
    skip_beat_list,
    skip_tempo_list,
)
from libresvip.core.time_sync import TimeSynchronizer
from libresvip.model.base import (
    InstrumentalTrack,
    Note,
    Project,
    SingingTrack,
    SongTempo,
    TimeSignature,
)

from .constants import OCTAVE_OFFSET, TICK_RATE
from .model import (
    VoiSonaAudioTrackItem,
    VoiSonaPointData,
    VoiSonaProject,
    VoiSonaSingingTrackItem,
)
from .options import InputOptions
from .voisona_pitch import (
    VoiSonaPitchEvent,
    VoiSonaTrackPitchData,
    pitch_from_voisona_track,
)


@dataclasses.dataclass
class VoiSonaParser:
    options: InputOptions
    time_synchronizer: TimeSynchronizer = dataclasses.field(init=False)

    def parse_project(self, voisona_project: VoiSonaProject) -> Project:
        time_signatures = []
        tempos = []
        tracks = []
        for track in voisona_project.tracks:
            for item in track.track:
                if isinstance(item, VoiSonaSingingTrackItem):
                    if parse_result := self.parse_singing_track(item):
                        singing_track, tempo_part, time_signature_part = parse_result
                        tracks.append(singing_track)
                        tempos.extend(tempo_part)
                        time_signatures.extend(time_signature_part)
        tempos = self.merge_tempos(tempos)
        self.time_synchronizer = TimeSynchronizer(tempos)
        for track in voisona_project.tracks:
            for item in track.track:
                if (
                    isinstance(item, VoiSonaAudioTrackItem)
                    and item.audio_event is not None
                ):
                    for i, event in enumerate(item.audio_event):
                        tracks.append(
                            InstrumentalTrack(
                                title=f"{item.name} {i + 1}",
                                audio_file_path=event.path,
                                offset=int(
                                    self.time_synchronizer.get_actual_ticks_from_secs(
                                        event.offset
                                    )
                                ),
                            )
                        )
        time_signatures = self.merge_time_signatures(time_signatures)
        return Project(
            time_signature_list=skip_beat_list(time_signatures, 0),
            song_tempo_list=skip_tempo_list(tempos, 0),
            track_list=tracks,
        )

    def merge_tempos(self, tempos: list[SongTempo]) -> list[SongTempo]:
        buckets = more_itertools.bucket(tempos, key=operator.attrgetter("position"))
        return [next(buckets[key]) for key in buckets] or [SongTempo()]

    def merge_time_signatures(
        self, time_signatures: list[TimeSignature]
    ) -> list[TimeSignature]:
        buckets = more_itertools.bucket(
            time_signatures, key=operator.attrgetter("bar_index")
        )
        return [next(buckets[key]) for key in buckets] or [TimeSignature()]

    def parse_singing_track(
        self, track: VoiSonaSingingTrackItem
    ) -> Optional[tuple[SingingTrack, list[SongTempo], list[TimeSignature]]]:
        if track.plugin_data.state_information.song is None:
            return None
        time_signatures = [
            TimeSignature(bar_index=0, numerator=4, denominator=4),
        ]
        prev_tick = 0
        tempos = []
        notes = []

        tick_prefix = int(time_signatures[0].bar_length())
        for song in track.plugin_data.state_information.song:
            for beat in song.beat:
                for time_node in beat.time:
                    tick = time_node.clock // TICK_RATE
                    numerator = time_node.beats
                    denominator = time_node.beat_type

                    if (
                        tick is not None
                        and numerator is not None
                        and denominator is not None
                    ):
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
            for tempo in song.tempo:
                for tempo_node in tempo.sound:
                    tick = tempo_node.clock // TICK_RATE
                    bpm = (
                        float(tempo_node.tempo)
                        if tempo_node.tempo is not None
                        else None
                    )
                    if tick is not None and bpm is not None:
                        tempos.append(SongTempo(position=tick, bpm=bpm))
            for score in song.score:
                for note_node in score.note:
                    pitch_octave = note_node.pitch_octave - OCTAVE_OFFSET
                    notes.append(
                        Note(
                            key_number=note_node.pitch_step + pitch_octave * 12,
                            lyric="-" if note_node.lyric == "ー" else note_node.lyric,
                            start_pos=(note_node.clock // TICK_RATE),
                            length=note_node.duration // TICK_RATE,
                        )
                    )
        tempos = shift_tempo_list(tempos, tick_prefix)
        voisona_track_pitch_data = None
        if track.plugin_data.state_information.parameter is not None:
            for parameter in track.plugin_data.state_information.parameter:
                if parameter.log_f0 is not None:
                    for curve in parameter.log_f0:
                        pitch_data_nodes: list[VoiSonaPointData] = curve.data
                        pitch_datas = []
                        for data_node in pitch_data_nodes:
                            if pitch_data := self.parse_pitch_data(data_node):
                                pitch_datas.append(pitch_data)
                        voisona_track_pitch_data = VoiSonaTrackPitchData(
                            events=pitch_datas, tempos=tempos, tick_prefix=tick_prefix
                        )
        time_signatures = shift_beat_list(time_signatures, 1)
        singing_track = SingingTrack(title=track.name, note_list=notes)
        if (
            voisona_track_pitch_data is not None
            and (pitch := pitch_from_voisona_track(voisona_track_pitch_data))
            is not None
        ):
            singing_track.edited_params.pitch = pitch
        return singing_track, tempos, time_signatures

    @staticmethod
    def parse_pitch_data(data_element: VoiSonaPointData) -> Optional[VoiSonaPitchEvent]:
        value = float(data_element.value) if data_element.value is not None else None
        if value is not None:
            index = data_element.index or None
            repeat = data_element.repeat or None
            return VoiSonaPitchEvent(index=index, repeat=repeat, value=value)
