# Lesson 3: PyAudio Microphone Streams
# PyAudio bridges Python with physical audio input and output devices.
import pyaudio
import numpy as np

audio = pyaudio.PyAudio()

# Open a 16-bit, mono, 44100 Hz input stream with a buffer size of 1024 samples
stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    frames_per_buffer=1024
)

print("Microphone is ready...")

# Read a chunk of raw bytes from the stream
data = stream.read(1024)

print(type(data))  # Expected: <class 'bytes'>
print(len(data))   # Expected: 2048 bytes (1024 samples * 2 bytes/sample)

# Cleanup resources
stream.stop_stream()
stream.close()
audio.terminate()
