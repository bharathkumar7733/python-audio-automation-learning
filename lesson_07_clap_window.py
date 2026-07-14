import time
import numpy as np
import pyaudio

DEVICE_INDEX = 1
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
CLAP_THRESHOLD = 25
PEAK_THRESHOLD = 10
DEBOUNCE_TIME = 0.25
WINDOW_DURATION = 5.0

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

last_clap_time = 0
window_start_time = 0
clap_count = 0
previous_volume = 0

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
        audio_float = audio_data.astype(np.float32)
        rms_volume = np.sqrt(np.mean(audio_float ** 2))
        current_time = time.time()
        delta = rms_volume - previous_volume
        
        clap_detected = (rms_volume > CLAP_THRESHOLD and delta > PEAK_THRESHOLD and current_time - last_clap_time > DEBOUNCE_TIME)
        
        if clap_detected:
            last_clap_time = current_time
            clap_count += 1
            if clap_count == 1:
                window_start_time = current_time
                print("First clap! Starting 5-second window.")
            else:
                print(f"Clap {clap_count} detected.")
                
        previous_volume = rms_volume
except KeyboardInterrupt:
    pass
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
