import pyaudio
import numpy as np

DEVICE_INDEX = 1
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1

audio = pyaudio.PyAudio()
device_info = audio.get_device_info_by_index(DEVICE_INDEX)
rate = int(device_info["defaultSampleRate"])

stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=rate,
    input=True,
    input_device_index=DEVICE_INDEX,
    frames_per_buffer=CHUNK
)

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        # Convert audio bytes into 16-bit integers using NumPy
        audio_data = np.frombuffer(data, dtype=np.int16)
        print("Data size:", len(audio_data))
except KeyboardInterrupt:
    pass
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
