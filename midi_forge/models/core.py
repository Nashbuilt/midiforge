"""Validated application data models."""
from dataclasses import asdict, dataclass, field
import json
from pathlib import Path

@dataclass(frozen=True, slots=True)
class Note:
    pitch: int
    start: float
    duration: float
    velocity: int = 90
    channel: int = 0
    def __post_init__(self) -> None:
        if not 0 <= self.pitch <= 127: raise ValueError("MIDI pitch must be 0..127")
        if self.start < 0 or self.duration <= 0: raise ValueError("Start must be non-negative and duration positive")
        if not 1 <= self.velocity <= 127 or not 0 <= self.channel <= 15: raise ValueError("Invalid velocity or channel")
    @property
    def end(self) -> float: return self.start + self.duration

@dataclass(slots=True)
class Track:
    name: str
    notes: list[Note] = field(default_factory=list)
    program: int = 0
    is_drum: bool = False

@dataclass(slots=True)
class Settings:
    project_name: str = "My Beat"
    root: str = "C"
    scale: str = "Minor"
    bpm: int = 140
    bars: int = 8
    seed: int = 42
    melody_complexity: int = 55
    melody_density: int = 55
    swing: int = 0
    humanisation: int = 0
    def validate(self) -> None:
        if self.root not in ROOT_NAMES or self.scale not in ("Major", "Minor"): raise ValueError("Choose a supported key and scale")
        if not 40 <= self.bpm <= 240 or self.bars not in (4, 8): raise ValueError("BPM must be 40..240; bars must be 4 or 8")
        for value in (self.melody_complexity, self.melody_density, self.swing, self.humanisation):
            if not 0 <= value <= 100: raise ValueError("Percentage settings must be 0..100")
    def save(self, path: Path) -> None:
        self.validate(); path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
    @classmethod
    def load(cls, path: Path) -> "Settings":
        value = cls(**json.loads(path.read_text(encoding="utf-8"))); value.validate(); return value

ROOT_NAMES = ("C","C#","D","D#","E","F","F#","G","G#","A","A#","B")

@dataclass(slots=True)
class Project:
    settings: Settings
    tracks: dict[str, Track] = field(default_factory=dict)
    progression: list[tuple[int,int,int]] = field(default_factory=list)
    @property
    def length_beats(self) -> float: return self.settings.bars * 4.0
