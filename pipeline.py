import sys
import subprocess
import os
import pysrt


def run(cmd):
    print(f">>> Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def main(folder_path):
    os.makedirs(folder_path, exist_ok=True)


    # 1. Run Speaker Diarization
    run(["python", "diarize.py", folder_path])

    # 2. Run Audio Splitter
    run(["python", "split.py", folder_path])


    left_channel_path = os.path.join(folder_path, "left_channel.wav")
    right_channel_path = os.path.join(folder_path, "right_channel.wav")


    # # 3. Run Whisper Transcriber for Left Channel
    run(["Whisper", left_channel_path, "--language", "Spanish", "--model", "turbo", "--output_dir", folder_path])

    # 4. Run Whisper Transcriber for Right Channel
    run(["Whisper", right_channel_path, "--language", "Spanish", "--model", "turbo", "--output_dir", folder_path])


    # Paths to your SRT files
    left_channel_srt  = os.path.join(folder_path, "left_channel.srt")
    right_channel_srt = os.path.join(folder_path, "right_channel.srt")

    # Load subtitles
    left_subs = pysrt.open(left_channel_srt)
    right_subs = pysrt.open(right_channel_srt)

    # Add label to each entry and store as tuples (start, end, label, text)
    def label_subs(subs, label):
        labeled = []
        for sub in subs:
            labeled.append((sub.start.ordinal, sub.end.ordinal, label, sub.text))
        return labeled

    labeled_left  = label_subs(left_subs, "LEFT")
    labeled_right = label_subs(right_subs, "RIGHT")

    # Merge and sort by start time
    merged = sorted(labeled_left + labeled_right, key=lambda x: x[0])

    # Helper function to convert milliseconds to SRT time format
    def ms_to_srt_time(ms):
        h = (ms // 3600000)
        m = (ms % 3600000) // 60000
        s = (ms % 60000) // 1000
        ms = ms % 1000
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    result_path = os.path.join(folder_path, "merged.srt")

    # Write to a new SRT file
    with open(result_path, "w", encoding="utf-8") as f:
        for i, (start, end, label, text) in enumerate(merged, start=1):
            f.write(f"{i}\n")
            f.write(f"{ms_to_srt_time(start)} --> {ms_to_srt_time(end)}\n")
            f.write(f"[{label}] {text}\n\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: pipeline.py <EntrevistaFolder>")
        sys.exit(1)

    audio_path = sys.argv[1]
    main(audio_path)
