import random
from ..models import Note,Settings,Track
DRUM_MAP={"Kick":36,"Snare":38,"Closed Hat":42}
def generate_drums(settings,rng):
    tracks={name:Track(name,is_drum=True) for name in DRUM_MAP}
    for bar in range(settings.bars):
        base=bar*4; kicks=(0,2.5) if bar%2==0 else (0,1.75,3.25)
        for start in kicks: tracks["Kick"].notes.append(Note(36,base+start,.12,105+rng.randrange(-7,8),9))
        for start in (1,3): tracks["Snare"].notes.append(Note(38,base+start,.12,99+rng.randrange(-5,6),9))
        for eighth in range(8):
            start=base+eighth*.5
            if eighth%2: start+=settings.swing/600
            tracks["Closed Hat"].notes.append(Note(42,start,.1,69+(eighth%2)*11+rng.randrange(-5,6),9))
    return tracks
