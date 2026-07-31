"""Generate several deterministic example projects without opening the UI."""
from pathlib import Path
from midi_forge.generators import generate_project
from midi_forge.midi import export_all
from midi_forge.models import Settings

EXAMPLES = (
    Settings("Dark Trap Example", "F#", "Minor", 142, 8, 808),
    Settings("RNB Example", "D#", "Major", 88, 8, 1998),
    Settings("Boom Bap Example", "C", "Minor", 92, 4, 1994),
)

for settings in EXAMPLES:
    print(export_all(generate_project(settings), Path("exports") / "examples"))
