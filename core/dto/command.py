from dataclasses import dataclass
from enum import StrEnum

class SamplingMode(StrEnum):
    LINEAR= "lin"
    LOGARITHMIC= "log"

@dataclass
class Command:
    input_file: str
    output_file:str
    bitrate:int
    sample_Rate:int
    level_in: float | None
    level_out: float | None
    bits:int | None
    mix:float | None
    sampling:SamplingMode | None
    overwrite:bool = True
    mono:bool = False
    has_bitcrush:bool = False

    def __post_init__(self):
        """Validation purposes"""
        if self.bits is not None and self.level_in is not None and self.level_out is not None and self.mix is not None:
            if not(1.0 <= self.bits <= 64.0):
                raise ValueError("Bit-crush value has to be between 1.0 and 64.0.")
            if not(0.2 <= self.level_in <= 64.0):
                raise ValueError("Bit-crush value has to be between 0.2 and 64.0.")
            if not(0.2 <= self.level_out <= 64.0):
                raise ValueError("Bit-crush value has to be between 0.2 and 64.0.")
            if not (0 <= self.mix <= 1):
                raise ValueError("Mix value has to be between 0 and 1.")