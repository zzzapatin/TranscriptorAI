import sys
import subprocess
import os

def run(cmd):
    print(f">>> Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def main(folder_path):
    os.makedirs(folder_path, exist_ok=True)

    left_channel_path = os.path.join(folder_path, "left_channel.wav")
    right_channel_path = os.path.join(folder_path, "right_channel.wav")

    # 1. Run Speaker Diarization
    run(["python", "diarize.py", audio_path])

    # 2. Run Audio Splitter
    run(["python", "split.py", audio_path])

    # 3. Run Whisper Transcriber for Left Channel
    run(["Whisper", left_channel_path,  '--language Spanish --model turbo'])

    # 4. Run Whisper Transcriber for Right Channel
    run(["Whisper", right_channel_path, '--language Spanish --model turbo'])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: pipeline.py <EntrevistaFolder>")
        sys.exit(1)

    audio_path = sys.argv[1]
    main(audio_path)
