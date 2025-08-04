# import pysrt

# # Paths to your SRT files
# alumno_file = "./Entrevistas/Jose_Nov2024/alumno.srt"
# investigador_file = "./Entrevistas/Jose_Nov2024/investigadora.srt"

# # Load subtitles
# alumno_subs = pysrt.open(alumno_file)
# investigador_subs = pysrt.open(investigador_file)

# # Add label to each entry and store as tuples (start_time, label, text)
# def label_subs(subs, label):
#     labeled = []
#     for sub in subs:
#         labeled.append((sub.start.ordinal, label, sub.text))
#     return labeled

# labeled_alumno = label_subs(alumno_subs, "ALUMNO")
# labeled_investigador = label_subs(investigador_subs, "INVESTIGADOR")

# # Merge and sort by start time
# merged = sorted(labeled_alumno + labeled_investigador, key=lambda x: x[0])

# # Write to a new SRT file
# with open("merged.srt", "w", encoding="utf-8") as f:
#     for i, (start, label, text) in enumerate(merged, start=1):
#         # Convert milliseconds to SRT time format
#         h = (start // 3600000)
#         m = (start % 3600000) // 60000
#         s = (start % 60000) // 1000
#         ms = start % 1000
#         end_time = start + 2000  # Dummy 2-second duration (adjust as needed)
#         eh = (end_time // 3600000)
#         em = (end_time % 3600000) // 60000
#         es = (end_time % 60000) // 1000
#         ems = end_time % 1000
        
#         start_str = f"{h:02}:{m:02}:{s:02},{ms:03}"
#         end_str = f"{eh:02}:{em:02}:{es:02},{ems:03}"

#         # Write entry
#         f.write(f"{i}\n{start_str} --> {end_str}\n[{label}] {text}\n\n")


import pysrt

# Paths to your SRT files
alumno_file = "./Entrevistas/Jose_Nov2024/alumno.srt"
investigador_file = "./Entrevistas/Jose_Nov2024/investigadora.srt"


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