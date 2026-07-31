import random
from ..models import Note,Settings,Track
def generate_bass(settings,progression,rng):
    track=Track("Bass",program=38)
    for bar in range(settings.bars):
        root=progression[bar%4][0]
        while root>47: root-=12
        starts=(0,2.5) if bar%2==0 else (0,1.5,3)
        for i,offset in enumerate(starts):
            next_offset=starts[i+1] if i+1<len(starts) else 4
            duration=min(1.25 if i else 1.8,next_offset-offset-.05)
            track.notes.append(Note(root+(12 if i==len(starts)-1 and rng.random()<.2 else 0),bar*4+offset,duration,92+rng.randrange(-6,7)))
    return track
