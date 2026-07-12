import pyaudio
import numpy as np

DEVICE_INDEX = 1
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
CLAP_THRESHOLD = 25

audio = pyaudio.PyAudio()

device_info = audio.get_device_info_by_index(DEVICE_INDEX)
rate = int(device_info["defaultSampleRate"])

print("Using microphone:", device_info["name"])
print("Sample rate:", rate)

stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=rate,
    input=True,
    input_device_index=DEVICE_INDEX,
    frames_per_buffer=CHUNK
)

print("Listening... Press Ctrl + C to stop.")

try:
    while True:
        data = stream.read(
            CHUNK,
            exception_on_overflow=False
        )

        audio_data = np.frombuffer(
            data,
            dtype=np.int16
        )

        # Convert to float before squaring to avoid int16 overflow
        audio_float = audio_data.astype(np.float32)

        # RMS represents the average energy/loudness of the whole chunk
        rms_volume = np.sqrt(
            np.mean(audio_float ** 2)
        )

        minimum = np.min(audio_data)
        maximum = np.max(audio_data)

        if rms_volume > CLAP_THRESHOLD:
            print(f"👏 Loud Sound! RMS = {int(rms_volume)}")
        else:
            print(f"Listening... RMS = {int(rms_volume)}")
except KeyboardInterrupt:
    print("\nListening stopped.")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("Microphone closed safely.")
