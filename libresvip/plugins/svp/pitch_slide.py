from collections.abc import Callable
from dataclasses import dataclass
from functools import partial

from . import interpolation


@dataclass
class PitchSlide:
    max_inter_time_in_secs: float
    max_inter_time_percent: float
    inter_func: Callable[[float], float]

    def apply(self, value: float) -> float:
        return self.inter_func(value)

    @classmethod
    def cosine_slide(cls):
        return cls(0.05, 0.1, interpolation.cosine_interpolation)

    @classmethod
    def cubic_slide(cls):
        return cls(0.05, 0.1, interpolation.cubic_interpolation)

    @classmethod
    def sigmoid_slide(cls):
        return cls(0.075, 0.48, partial(interpolation.sigmoid_interpolation, k=5.5))
