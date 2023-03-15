import os
import subprocess

def Playing():
    play_audio = "temp.wav"
    if os.path.exists(play_audio):
        process = subprocess.Popen(["start", "", os.path.abspath(play_audio)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        subprocess.Popen(["taskkill", "/F", "/T", "/PID", str(process.pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        print(f"File {play_audio} not found")
