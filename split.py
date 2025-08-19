from pydub import AudioSegment
import os
import sys
import tempfile

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

# process audio file
audio_folder = sys.argv[1]  # Get folder path from command line argument
audio_file = os.path.join(audio_folder, "Entrevista_original.mp3")

# Convert mp3 to wav using pydub
wav_temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
audio = AudioSegment.from_mp3(audio_file)
audio.export(wav_temp.name, format="wav") 


# Load original audio
audio = AudioSegment.from_file(wav_temp.name)

# Create silent mono tracks
left_channel = AudioSegment.silent(duration=len(audio)).set_channels(1)
right_channel = AudioSegment.silent(duration=len(audio)).set_channels(1)


# print output
rttm_file = os.path.join(audio_folder, "output.rttm")

# Parse RTTM
segments = parse_rttm(rttm_file)


# Place each speaker's segments in the correct channel
for start, duration, speaker in segments:
    segment = audio[start*1000:(start+duration)*1000].set_channels(1)
    if speaker == "SPEAKER_00":
        left_channel = left_channel.overlay(segment, position=start*1000)
    else:
        right_channel = right_channel.overlay(segment, position=start*1000)

left_audio = os.path.join(audio_folder, "left_channel.wav")
right_audio = os.path.join(audio_folder, "right_channel.wav")


# Export channels separately
left_channel.export(left_audio, format="wav")
right_channel.export(right_audio, format="wav")
