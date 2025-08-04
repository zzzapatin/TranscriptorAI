from pydub import AudioSegment
import numpy as np

# --- Function to parse RTTM ---
def parse_rttm(rttm_file):
    segments = []
    with open(rttm_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 8:
                continue
            start = float(parts[3])
            duration = float(parts[4])
            speaker = parts[7]
            segments.append((start, duration, speaker))
    return segments

# --- Function to pan audio ---
def pan_audio(segment, pan):
    # pan=-1 full left, 0 center, +1 full right
    return segment.pan(pan)

# --- Main ---
audio = AudioSegment.from_file("original_audio.wav")
segments = parse_rttm("output.rttm")

output = AudioSegment.silent(duration=len(audio))

for start, duration, speaker in segments:
    segment = audio[start*1000:(start+duration)*1000]  # convert to ms
    if speaker == "SPEAKER_00":
        panned = pan_audio(segment, -1)  # Left
    else:
        panned = pan_audio(segment, 1)   # Right
    output = output.overlay(panned, position=start*1000)

output.export("panned_audio.wav", format="wav")
