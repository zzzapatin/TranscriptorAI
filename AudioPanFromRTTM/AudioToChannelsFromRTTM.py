from pydub import AudioSegment

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

# Load original audio
audio = AudioSegment.from_file("./Entrevistas/Jose_Nov2024/audio.wav")

# Create silent mono tracks
left_channel = AudioSegment.silent(duration=len(audio)).set_channels(1)
right_channel = AudioSegment.silent(duration=len(audio)).set_channels(1)

# Parse RTTM
segments = parse_rttm("./Entrevistas/Jose_Nov2024/output.rttm")


# Place each speaker's segments in the correct channel
for start, duration, speaker in segments:
    segment = audio[start*1000:(start+duration)*1000].set_channels(1)
    if speaker == "SPEAKER_00":
        left_channel = left_channel.overlay(segment, position=start*1000)
    else:
        right_channel = right_channel.overlay(segment, position=start*1000)

# Export channels separately
left_channel.export("./Entrevistas/Jose_Nov2024/Results/left_channel.wav", format="wav")
right_channel.export("./Entrevistas/Jose_Nov2024/Results/right_channel.wav", format="wav")
