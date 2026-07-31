import random
from ..models import Note,Settings,Track
from ..music.theory import PROGRESSIONS,chord
def generate_chords(settings,rng):
    degrees=rng.choice(PROGRESSIONS[settings.scale]); progression=[chord(settings.root,settings.scale,d) for d in degrees]
    track=Track("Chords",program=0); previous=None
    for bar in range(settings.bars):
        tones=progression[bar%4]; choices=[tones,(tones[1],tones[2],tones[0]+12),(tones[2]-12,tones[0],tones[1])]
        voiced=min(choices,key=lambda c:sum(abs(a-b) for a,b in zip(c,previous or c))); previous=voiced
        for pitch in voiced: track.notes.append(Note(pitch,bar*4,3.8,67+rng.randrange(-5,6)))
    return track,progression
