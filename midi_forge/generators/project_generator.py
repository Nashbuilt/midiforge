import random
from ..models import Project, Settings
from .bass_generator import generate_bass
from .chord_generator import generate_chords
from .drum_generator import generate_drums
from .melody_generator import generate_melody

def generate_project(settings: Settings) -> Project:
    """Generate all tracks deterministically from settings.seed."""
    settings.validate(); rng=random.Random(settings.seed)
    chords,progression=generate_chords(settings,rng); tracks={"Chords":chords}
    tracks["Melody"]=generate_melody(settings,progression,rng)
    tracks["Bass"]=generate_bass(settings,progression,rng)
    tracks.update(generate_drums(settings,rng))
    return Project(settings,tracks,progression)
