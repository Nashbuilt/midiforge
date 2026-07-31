"""Small, dependency-free music theory toolkit."""
ROOTS={"C":0,"C#":1,"D":2,"D#":3,"E":4,"F":5,"F#":6,"G":7,"G#":8,"A":9,"A#":10,"B":11}
INTERVALS={"Major":(0,2,4,5,7,9,11),"Minor":(0,2,3,5,7,8,10)}
PROGRESSIONS={"Major":((0,4,5,3),(0,5,3,4),(5,3,0,4),(0,3,4,0)),"Minor":((0,5,2,6),(0,3,5,4),(0,6,5,6),(0,4,5,3))}
def pitch_classes(root,scale): return tuple((ROOTS[root]+i)%12 for i in INTERVALS[scale])
def scale_notes(root,scale,low,high): return [p for p in range(low,high+1) if p%12 in pitch_classes(root,scale)]
def is_scale_note(pitch,root,scale): return pitch%12 in pitch_classes(root,scale)
def chord(root,scale,degree,octave=4):
    steps=INTERVALS[scale]; degree%=7; base=12*(octave+1)+ROOTS[root]; out=[]
    for third in (0,2,4):
        index=degree+third; out.append(base+steps[index%7]+12*(index//7))
    return tuple(out)
def bar_beats(numerator=4,denominator=4):
    if numerator<=0 or denominator<=0: raise ValueError("Invalid time signature")
    return numerator*4.0/denominator
