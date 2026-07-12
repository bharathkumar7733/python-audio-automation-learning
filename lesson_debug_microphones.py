import pyaudio
import numpy as np

audio = pyaudio.PyAudio()

stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    input_device_index=5,
    frames_per_buffer=1024
)

print("Listening... Press Ctrl + C to stop.")

try:
    while True:
        data = stream.read(1024, exception_on_overflow=False)

        audio_data = np.frombuffer(
            data,
            dtype=np.int16
        )

        volume = np.max(np.abs(audio_data))

        print("Volume:", volume)

except KeyboardInterrupt:
    print("\nStopped listening.")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
