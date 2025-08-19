import os
HF_TOKEN = os.getenv("HF_TOKEN")

# load pretrained pipeline
from pyannote.audio import Pipeline
import sys
import tempfile
from pydub import AudioSegment
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", 
                                    use_auth_token=HF_TOKEN)

# (optional) send pipeline to GPU
# import torch
# pipeline.to(torch.device("cuda"))

# process audio file
audio_folder = sys.argv[1]  # Get folder path from command line argument
audio_file = os.path.join(audio_folder, "Entrevista_original.mp3")

# Convert mp3 to wav using pydub
wav_temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
audio = AudioSegment.from_mp3(audio_file)
audio.export(wav_temp.name, format="wav")

# Run diarization on wav file
output = pipeline(wav_temp.name)


# print output
output_file = os.path.join(audio_folder, "output.rttm")
with open(output_file, "w") as rttm_file:
    output.write_rttm(rttm_file)