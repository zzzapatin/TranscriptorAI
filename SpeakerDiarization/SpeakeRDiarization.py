import os
HF_TOKEN = os.getenv("HF_TOKEN")

# load pretrained pipeline
from pyannote.audio import Pipeline
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", 
                                    use_auth_token=HF_TOKEN)

# (optional) send pipeline to GPU
# import torch
# pipeline.to(torch.device("cuda"))

# process audio file
output = pipeline(
    "Esteban_8vo_Basico_noviembre2024.wav",
    num_speakers=2,  # optional, only if you want exactly 2 speakers
    start=0.0,
    end=600.0
)

# print output
with open("output.rttm", "w") as rttm_file:
    output.write_rttm(rttm_file)