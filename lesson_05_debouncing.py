import time

import numpy as np
import pyaudio


DEVICE_INDEX = 1
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1

CLAP_THRESHOLD = 25
DEBOUNCE_TIME = 0.25
DOUBLE_CLAP_WINDOW = 1.5
clap_count = 0
first_clap_time = 0


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

print("Listening for claps... Press Ctrl + C to stop.")

last_clap_time = 0

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

        audio_float = audio_data.astype(np.float32)

        rms_volume = np.sqrt(
            np.mean(audio_float ** 2)
        )

        current_time = time.time()

        if (rms_volume > CLAP_THRESHOLD and current_time - last_clap_time > DEBOUNCE_TIME):
            last_clap_time = current_time

            if clap_count == 0:
                clap_count = 1
                first_clap_time = current_time
                print(f"👏 First Clap at {current_time:.2f}")

            elif (
                clap_count == 1
                and current_time - first_clap_time <= DOUBLE_CLAP_WINDOW
            ):
                clap_count = 0
                print(
    f"Second clap after "
    f"{current_time - first_clap_time:.2f} sec")

            else:
                clap_count = 1
                first_clap_time = current_time

except KeyboardInterrupt:
    print("\nListening stopped.")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("Microphone closed safely.")
