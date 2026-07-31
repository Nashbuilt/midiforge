# MIDI Forge

MIDI Forge is a fully local Windows desktop application that generates deterministic, coordinated MIDI ideas for FL Studio. It uses musical rules rather than unconstrained random note selection: scale-aware motifs, chord-tone anchors, phrase variation, smooth chord voice-leading, harmonic bass, intentional rests, and structured drums.

## Windows setup

```powershell
py -m pip install -r requirements.txt
py main.py
```

Run tests with `py -m pytest -q`. Build with `.\build_windows.bat`.

The portable application is written to `dist\MIDI Forge Portable\MIDI Forge Portable.exe`. Keep the entire folder together. Folder mode avoids unpacking runtime files into `%TEMP%` on every launch.

## Included MVP features

- Major/minor keys, 40–240 BPM, 4/8 bars, deterministic seeds
- Motif-based melody, voice-led chords, monophonic bass
- Separate kick, snare and closed-hat tracks
- Swing, density, complexity and humanisation settings
- Piano-roll visualisation and separate/combined MIDI export at 480 PPQ
- JSON presets, automated tests and portable Windows packaging

## Next stage

Local playback, editable piano roll, A/B sections, instrument presets, ADSR, glide, drive, chorus, delay, reverb and EQ are planned next.
