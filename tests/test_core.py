from pathlib import Path
import mido
import pytest
from midi_forge.generators import generate_project
from midi_forge.midi import export_all
from midi_forge.models import Note,Settings
from midi_forge.music.theory import bar_beats,chord,is_scale_note

def test_scale_validation():
    for pitch in (60,62,63,65,67,68,70): assert is_scale_note(pitch,"C","Minor")
    assert not is_scale_note(61,"C","Minor")
def test_chord_construction():
    assert chord("C","Major",0)==(60,64,67)
    assert chord("A","Minor",0)==(69,72,76)
def test_note_validation():
    with pytest.raises(ValueError): Note(128,0,1)
    with pytest.raises(ValueError): Note(60,0,0)
def test_seed_reproducibility():
    a=generate_project(Settings(seed=123)); b=generate_project(Settings(seed=123)); assert a.tracks==b.tracks
def test_bass_is_monophonic():
    bass=sorted(generate_project(Settings(seed=77)).tracks["Bass"].notes,key=lambda n:n.start)
    assert all(left.end<=right.start for left,right in zip(bass,bass[1:]))
def test_bar_and_time_signature_math():
    assert bar_beats(4,4)==4; assert bar_beats(3,4)==3; assert generate_project(Settings(bars=8)).length_beats==32
def test_export_files_and_midi_values(tmp_path:Path):
    project=generate_project(Settings(project_name="Test",seed=5)); folder=export_all(project,tmp_path)
    expected=("melody.mid","chords.mid","bass.mid","kick.mid","snare.mid","closed_hat.mid","drums_combined.mid","full_arrangement.mid")
    for name in expected:
        path=folder/name; assert path.exists(); midi=mido.MidiFile(path)
        active=set()
        for track in midi.tracks:
            active.clear()
            for message in track:
                if message.type=="note_on" and message.velocity:
                    assert 0<=message.note<=127; active.add((message.channel,message.note))
                elif message.type in ("note_off","note_on") and hasattr(message,"note"): active.discard((message.channel,message.note))
            assert not active
