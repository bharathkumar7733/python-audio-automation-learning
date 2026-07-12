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
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # Convert to float32 to avoid int16 overflow during squaring
        audio_float = audio_data.astype(np.float32)
        # Root Mean Square (RMS) represents average signal energy/loudness
        rms_volume = np.sqrt(np.mean(audio_float ** 2))
        
        print("RMS Volume:", rms_volume)
except KeyboardInterrupt:
    pass
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
