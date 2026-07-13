import time

import numpy as np
import pyaudio


DEVICE_INDEX = 1
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1

CLAP_THRESHOLD = 21
PEAK_THRESHOLD = 10
DEBOUNCE_TIME = 0.25
DOUBLE_CLAP_WINDOW = 1.5


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
first_clap_time = 0
clap_count = 0
previous_volume = 0

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

        # Difference between the current and previous audio chunk
        delta = rms_volume - previous_volume

        # If the first clap becomes too old, reset it
        if (
            clap_count == 1
            and current_time - first_clap_time > DOUBLE_CLAP_WINDOW
        ):
            clap_count = 0

        # Detect a loud, sudden audio spike
        if (
            rms_volume > CLAP_THRESHOLD
            and delta > PEAK_THRESHOLD
            and current_time - last_clap_time > DEBOUNCE_TIME
        ):
            last_clap_time = current_time

            if clap_count == 0:
                clap_count = 1
                first_clap_time = current_time

                print(
                    f"👏 First clap | "
                    f"RMS: {int(rms_volume)} | "
                    f"Delta: {int(delta)}"
                )

            elif (
                clap_count == 1
                and current_time - first_clap_time <= DOUBLE_CLAP_WINDOW
            ):
                time_difference = current_time - first_clap_time

                print(
                    f"✅ Double clap detected after "
                    f"{time_difference:.2f} seconds!"
                )

                clap_count = 0
                first_clap_time = 0

        # Save the current volume for comparison in the next loop
        previous_volume = rms_volume

except KeyboardInterrupt:
    print("\nListening stopped.")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()

    print("Microphone closed safely.")
