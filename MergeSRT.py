import pysrt

# Paths to your SRT files
alumno_file = "../AudioPanFromRTTM/Entrevistas/Jose_Mayo2025/whisper_alumno/alumno.srt"
investigador_file = "../AudioPanFromRTTM/Entrevistas/Jose_Mayo2025/whisper_investigadora/investigadora.srt"


# Load subtitles
alumno_subs = pysrt.open(alumno_file)
investigador_subs = pysrt.open(investigador_file)

# Add label to each entry and store as tuples (start, end, label, text)
def label_subs(subs, label):
    labeled = []
    for sub in subs:
        labeled.append((sub.start.ordinal, sub.end.ordinal, label, sub.text))
    return labeled

labeled_alumno = label_subs(alumno_subs, "ALUMNO")
labeled_investigador = label_subs(investigador_subs, "INVESTIGADOR")

# Merge and sort by start time
merged = sorted(labeled_alumno + labeled_investigador, key=lambda x: x[0])

# Helper function to convert milliseconds to SRT time format
def ms_to_srt_time(ms):
    h = (ms // 3600000)
    m = (ms % 3600000) // 60000
    s = (ms % 60000) // 1000
    ms = ms % 1000
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

# Write to a new SRT file
with open("merged.srt", "w", encoding="utf-8") as f:
    for i, (start, end, label, text) in enumerate(merged, start=1):
        f.write(f"{i}\n")
        f.write(f"{ms_to_srt_time(start)} --> {ms_to_srt_time(end)}\n")
        f.write(f"[{label}] {text}\n\n")