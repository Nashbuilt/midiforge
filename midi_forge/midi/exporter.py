"""Standards-compliant MIDI export using mido."""
from dataclasses import asdict
import json,re
from pathlib import Path
import mido
from ..models import Project,Track
PPQ=480
def safe_name(value):
    cleaned=re.sub(r"[^A-Za-z0-9 _-]","",value).strip().replace(" ","_")
    return cleaned or "midi_forge_project"
def _mido_track(track,include_meta=False,bpm=120):
    output=mido.MidiTrack(); output.append(mido.MetaMessage("track_name",name=track.name,time=0))
    if include_meta:
        output.append(mido.MetaMessage("set_tempo",tempo=mido.bpm2tempo(bpm),time=0))
        output.append(mido.MetaMessage("time_signature",numerator=4,denominator=4,time=0))
    if not track.is_drum: output.append(mido.Message("program_change",program=max(0,min(127,track.program)),channel=0,time=0))
    events=[]
    for note in track.notes:
        start=round(note.start*PPQ); end=round(note.end*PPQ); channel=9 if track.is_drum else note.channel
        events.append((start,1,mido.Message("note_on",note=note.pitch,velocity=note.velocity,channel=channel)))
        events.append((end,0,mido.Message("note_off",note=note.pitch,velocity=0,channel=channel)))
    previous=0
    for tick,_,message in sorted(events,key=lambda event:(event[0],event[1])):
        message.time=tick-previous; output.append(message); previous=tick
    output.append(mido.MetaMessage("end_of_track",time=0)); return output
def export_track(track,path,bpm):
    path.parent.mkdir(parents=True,exist_ok=True); midi=mido.MidiFile(type=0,ticks_per_beat=PPQ)
    midi.tracks.append(_mido_track(track,True,bpm)); midi.save(path); return path
def export_combined(project,path):
    path.parent.mkdir(parents=True,exist_ok=True); midi=mido.MidiFile(type=1,ticks_per_beat=PPQ)
    for index,track in enumerate(project.tracks.values()): midi.tracks.append(_mido_track(track,index==0,project.settings.bpm))
    midi.save(path); return path
def export_all(project,base):
    folder=base/safe_name(project.settings.project_name); folder.mkdir(parents=True,exist_ok=True)
    filenames={"Melody":"melody.mid","Chords":"chords.mid","Bass":"bass.mid","Kick":"kick.mid","Snare":"snare.mid","Closed Hat":"closed_hat.mid"}
    for name,track in project.tracks.items(): export_track(track,folder/filenames[name],project.settings.bpm)
    drums=Track("Drums Combined",is_drum=True)
    for name in ("Kick","Snare","Closed Hat"): drums.notes.extend(project.tracks[name].notes)
    export_track(drums,folder/"drums_combined.mid",project.settings.bpm); export_combined(project,folder/"full_arrangement.mid")
    (folder/"project_settings.json").write_text(json.dumps(asdict(project.settings),indent=2),encoding="utf-8")
    return folder
