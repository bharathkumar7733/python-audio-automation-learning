import pyaudio

audio = pyaudio.PyAudio()

stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    frames_per_buffer=1024
)

print("Microphone is ready...")
data = stream.read(1024)
print(type(data))
print(len(data))
