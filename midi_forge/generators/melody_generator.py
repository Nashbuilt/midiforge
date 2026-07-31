import random
from ..models import Note,Settings,Track
from ..music.theory import scale_notes
def generate_melody(settings,progression,rng):
    track=Track("Melody",program=81); pool=scale_notes(settings.root,settings.scale,60,79)
    motif_len=3+settings.melody_complexity//25; rhythm=[(0,.75),(1,.5),(2,.75),(3,.5)]
    anchor=min(pool,key=lambda p:min(abs(p-c) for c in progression[0])); motif=[anchor]
    for _ in range(motif_len-1):
        i=pool.index(min(pool,key=lambda p:abs(p-motif[-1]))); step=rng.choice((-2,-1,1,1,2))
        motif.append(pool[max(0,min(len(pool)-1,i+step))])
    for bar in range(settings.bars):
        phrase=bar%4
        for index,(offset,duration) in enumerate(rhythm[:motif_len]):
            if rng.random()>settings.melody_density/100*.85: continue
            pitch=motif[index%len(motif)]
            if phrase==2 and index==1: pitch=pool[max(0,pool.index(pitch)-1)]
            if phrase==3 and index==motif_len-1:
                tones=progression[bar%4]; pitch=min(pool,key=lambda p:min(abs(p-c) for c in tones))
            track.notes.append(Note(pitch,bar*4+offset,duration,86+rng.randrange(-9,10)))
    return track
