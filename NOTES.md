# Python Audio Automation Learning Notes

## Overview

This repository documents my step-by-step learning journey while building a clap-controlled desktop automation system using Python.

Instead of directly copying a finished clap detector, I first learned the important concepts individually:

- Python modules
- Operating system automation
- Processes and subprocesses
- PyAudio
- Microphone streams
- Audio buffers
- NumPy arrays
- RMS loudness
- Threshold detection
- Debouncing
- Peak detection
- Clap counting
- Time-window gesture recognition

The final goal is to use clap patterns to control desktop applications.

Example:

- One clap → Open VS Code
- Two claps → Open YouTube

---

# 1. Python Modules

## What is a module?

A module is a Python file that contains reusable code such as:

- functions
- classes
- variables
- constants

Modules allow us to reuse existing code instead of writing everything from scratch.

Example:

```python
import webbrowser
```

The webbrowser module provides functions for opening websites.

```python
webbrowser.open("https://www.google.com")
```

Understanding the dot operator

In:

```python
webbrowser.open()
```

- `webbrowser` is the module
- `open` is a function inside the module
- `.` means access something inside the module
- `()` calls the function

Built-in and external modules

Built-in modules

These come with Python:

- `math`
- `time`
- `random`
- `webbrowser`
- `subprocess`

They do not need installation.

External modules

These are installed using pip.

- `numpy`
- `pyaudio`
- `fastapi`

Example:

```bash
pip install numpy
pip install pyaudio
```

# 2. Opening Websites

The webbrowser module is used to open URLs in the default browser.

```python
import webbrowser

webbrowser.open("https://www.youtube.com")
```

The URL is passed as an argument to the open() function.

The browser that opens depends on the default browser configured in the operating system.

# 3. Processes and Subprocesses

What is a process?

A process is a running instance of a program.

Examples:

- `chrome.exe`
- `code.exe`
- `python.exe`
- `notepad.exe`

When a Python file runs, Windows creates a python.exe process.

What is a subprocess?

A subprocess is a new process started by another process.

Example:

```
Python process
      ↓
Starts VS Code
      ↓
VS Code becomes another process
```

Python uses the subprocess module to start other programs.

```python
import subprocess

subprocess.Popen(["code"])
```

Understanding Popen

Popen means opening or starting a new process.

```python
subprocess.Popen(["notepad"])
```

This asks Windows to start Notepad.

Why commands are passed as a list

A command may contain multiple parts.

Command:

```bash
python app.py
```

Python representation:

```python
["python", "app.py"]
```

Command:

```bash
git status
```

Python representation:

```python
["git", "status"]
```

Each command-line argument becomes one list element.

# 4. PATH

PATH is an operating system environment variable containing folders where Windows searches for executable programs.

When this runs:

```python
subprocess.Popen(["code"])
```

Windows searches the PATH folders for the VS Code command.

Commands such as these can be used to inspect PATH resolution:

```powershell
where python
where code
where git
```

Using PATH avoids hardcoding full program locations.

Instead of:

```python
subprocess.Popen([
    r"C:\Program Files\Microsoft VS Code\Code.exe"
])
```

we can use:

```python
subprocess.Popen(["code"])
```

This makes the program cleaner and more portable.

# 5. What is Sound?

Sound is created by vibrations.

When hands clap:

```
Hands collide
      ↓
Air vibrates
      ↓
Microphone detects vibrations
      ↓
Signal becomes digital numbers
```

A computer does not understand a clap directly.

It only receives numerical samples representing the sound wave.

Example:

Silence:
`0, 1, -1, 2, 0`

Talking:
`50, 120, -90, 250`

Clap:
`500, 4000, 15000, 9000`

Large sample values generally represent stronger sound vibrations.

# 6. PyAudio

PyAudio is a Python library used to access audio devices such as:

- microphones
- speakers
- headsets

PyAudio acts as a bridge between Python and the computer's audio system.

```python
import pyaudio
```

Creating a PyAudio object

```python
audio = pyaudio.PyAudio()
```

Explanation:
- `pyaudio` is the module
- `PyAudio` is a class
- `PyAudio()` creates an object
- `audio` stores that object

The audio object manages communication with audio devices.

# 7. Audio Streams

An audio stream is a continuous flow of audio data.

The microphone continuously sends small groups of samples.

```
Microphone
    ↓
Chunk 1
    ↓
Chunk 2
    ↓
Chunk 3
```

This allows audio to be processed in real time.

Instead of recording one full hour and analyzing it later, the program repeatedly:

```
Receives a chunk
      ↓
Processes it
      ↓
Receives the next chunk
```

# 8. Opening the Microphone Stream

Example:

```python
stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    input_device_index=1,
    frames_per_buffer=1024
)
```

Parameter explanation:

- `format=pyaudio.paInt16`

Each audio sample is stored as a signed 16-bit integer.
A signed 16-bit integer can represent positive and negative audio wave values.

- `channels=1`

This selects mono audio.
Mono = one channel
Stereo = two channels
For clap detection, mono is enough.

- `rate=44100`

This is the sample rate.
It means: 44,100 audio samples per second.
The microphone measures the sound wave 44,100 times every second.

- `input=True`

This tells PyAudio to use an input device.
In this project, the input device is the microphone.

- `input_device_index=1`

This explicitly selects microphone device number 1.
The device index was found by listing all PyAudio devices.

- `frames_per_buffer=1024`

The microphone sends audio in chunks of 1,024 samples.
This balances response time, CPU usage, and processing speed.

# 9. Finding the Correct Microphone

PyAudio may select the wrong microphone by default.

The following code lists available devices:

```python
import pyaudio

audio = pyaudio.PyAudio()

for index in range(audio.get_device_count()):
    device = audio.get_device_info_by_index(index)

    print("Index:", index)
    print("Name:", device["name"])
    print("Input channels:", device["maxInputChannels"])
    print("-" * 40)

audio.terminate()
```

The correct microphone for this system was:

```python
DEVICE_INDEX = 1
```

This device produced changing audio values while speaking and clapping.

# 10. Reading Microphone Data

Audio is read using:

```python
data = stream.read(
    1024,
    exception_on_overflow=False
)
```

Explanation:

- `stream.read(1024)`

Reads the next 1,024 audio samples from the microphone.

- `exception_on_overflow=False`

Real-time audio can occasionally arrive faster than the program processes it.
This option prevents the program from crashing due to temporary buffer overflow.

Data type:

The returned value is raw bytes.

```python
print(type(data))
```

Output:

`<class 'bytes'>`

The bytes must be converted into numerical samples before analysis.

# 11. NumPy

NumPy is a Python library used for fast numerical processing.

It is useful for:

- audio
- images
- machine learning
- scientific data
- large arrays

```python
import numpy as np
```

Why NumPy instead of a normal list?

NumPy arrays are:

- faster
- more memory efficient
- suitable for numerical operations
- optimized for processing large amounts of data

Microphone audio contains thousands of samples every second, so NumPy is a good choice.

# 12. Converting Audio Bytes into Numbers

Raw bytes are converted using:

```python
audio_data = np.frombuffer(
    data,
    dtype=np.int16
)
```

Code explanation:

- `np.frombuffer()`

Creates a NumPy array from raw byte data.

- `data`

Contains the raw microphone bytes.

- `dtype=np.int16`

Tells NumPy to interpret the bytes as signed 16-bit integers.
This must match: `format=pyaudio.paInt16`

The PyAudio format and NumPy data type must match.

Result:

The result is a NumPy array:

`[0, -1, 2, 15, -20, 100, ...]`

Each number is one audio sample.

# 13. Why the Program Must Read Continuously

Reading once:

```python
data = stream.read(1024)
```

captures only one small audio chunk.

At a sample rate of 44,100:

`1024 / 44100 ≈ 0.023 seconds`

That is only around 23 milliseconds.

A clap may occur before or after that small recording window.

Therefore, the program uses:

```python
while True:
```

This continuously reads microphone data:

```
Read chunk
    ↓
Process chunk
    ↓
Read next chunk
    ↓
Repeat
```

# 14. RMS Volume

Raw audio contains both positive and negative numbers.

Example:

`-20, 15, -40, 35`

The sign represents the direction of the sound wave.

For loudness, both positive and negative values matter equally.

RMS meaning:

RMS stands for: Root Mean Square

RMS calculates the average energy of the complete audio chunk.
It gives one useful loudness value instead of looking at all 1,024 samples individually.

RMS code:

```python
audio_float = audio_data.astype(np.float32)

rms_volume = np.sqrt(
    np.mean(audio_float ** 2)
)
```

Line-by-line explanation:

Converting to float:

```python
audio_float = audio_data.astype(np.float32)
```

The original audio values use int16.
Squaring an int16 number can exceed its allowed range.
Example: `30000 × 30000 = 900000000` (cannot fit inside int16).
Therefore, the data is converted to float32 before squaring.

Squaring the values:

```python
audio_float ** 2
```

This makes all values positive and emphasizes larger sound values.
Example: `-10` becomes `100`, `20` becomes `400`.

Mean:

```python
np.mean(audio_float ** 2)
```

This calculates the average energy of all samples in the audio chunk.

Square root:

```python
np.sqrt(...)
```

This brings the value back to a scale closer to the original audio samples.

RMS pipeline:

```
Audio samples
      ↓
Convert to float
      ↓
Square every sample
      ↓
Calculate the average
      ↓
Take square root
      ↓
RMS loudness
```

# 15. Measuring Minimum, Maximum and RMS

```python
minimum = np.min(audio_data)
maximum = np.max(audio_data)
```

These functions return the lowest and highest sample values in the current chunk.

Example output:

`Min: -30 | Max: 27 | RMS Volume: 8`

However, maximum values can be affected by one random spike.
RMS is usually more useful for estimating the energy of the complete audio chunk.

# 16. Threshold Detection

A threshold is a decision boundary.

Example:

```python
CLAP_THRESHOLD = 25
```

The condition is:

```python
if rms_volume > CLAP_THRESHOLD:
    print("Loud sound detected")
```

How the threshold was selected:

The threshold was not chosen randomly.
The microphone was tested during:
- silence
- normal speaking
- clapping

For this device: `CLAP_THRESHOLD = 25` worked well.

The best threshold differs between computers because of:
- microphone sensitivity
- microphone gain
- room noise
- audio drivers
- distance from the microphone

This process is called calibration.

# 17. Debouncing

One physical clap may remain loud for several audio chunks.

Without debouncing, one clap may produce multiple detections:

```
Clap detected
Clap detected
Clap detected
Clap detected
```

This happens because the loop runs many times every second.
Debouncing ensures that one physical clap becomes one software event.

Constants:

```python
DEBOUNCE_TIME = 0.25
```

After detecting a clap, the program ignores new clap events for 0.25 seconds.

State variable:

```python
last_clap_time = 0
```

This stores the timestamp of the previous detected clap.

Current timestamp:

```python
current_time = time.time()
```

`time.time()` returns the current Unix timestamp in seconds.

Debounce condition:

```python
current_time - last_clap_time > DEBOUNCE_TIME
```

This calculates how much time passed since the previous clap.

Full condition:

```python
if (
    rms_volume > CLAP_THRESHOLD
    and current_time - last_clap_time > DEBOUNCE_TIME
):
    print("Clap detected")
    last_clap_time = current_time
```

A new clap is accepted only when:
1. The sound is louder than the threshold.
2. Enough time has passed since the previous clap.

# 18. Peak Detection

Threshold detection alone can detect other loud sounds, such as:
- music
- shouting
- door slams
- objects dropping

A clap normally has a sudden increase in volume.
Peak detection checks whether the sound became loud suddenly.

Previous volume:

```python
previous_volume = 0
```

This stores the RMS volume from the previous audio chunk.

Delta:

```python
delta = rms_volume - previous_volume
```

Delta means the difference between the current and previous volume.

Example:
- Previous volume = 5, Current volume = 7 -> Delta = 2 (small change)
- Previous volume = 2, Current volume = 30 -> Delta = 28 (sudden spike)

Peak threshold:

```python
PEAK_THRESHOLD = 10
```

The detector accepts a sound only when its increase is greater than this value.

Improved condition:

```python
if (
    rms_volume > CLAP_THRESHOLD
    and delta > PEAK_THRESHOLD
    and current_time - last_clap_time > DEBOUNCE_TIME
):
```

This asks three questions:
1. Is the sound loud?
2. Did it become loud suddenly?
3. Has enough debounce time passed?

Updating the previous volume:

At the end of every loop:

```python
previous_volume = rms_volume
```

Without this line, every chunk would be compared with zero instead of the previous chunk.

# 19. Clap Gesture Window

The detector was upgraded to classify clap commands inside a five-second window.

Requirements:

- One clap in five seconds: Single-clap command
- Two claps in five seconds: Double-clap command

This makes the interaction easier because the user does not need to clap extremely quickly.

Constants:

```python
WINDOW_DURATION = 5.0
```

The program waits for five seconds after the first clap.

State variables:

```python
clap_count = 0
window_start_time = 0
```

- `clap_count` stores the number of valid claps detected in the current window.
- `window_start_time` stores when the first clap started the window.

# 20. Detecting a Valid Clap

```python
clap_detected = (
    rms_volume > CLAP_THRESHOLD
    and delta > PEAK_THRESHOLD
    and current_time - last_clap_time > DEBOUNCE_TIME
)
```

This stores either `True` or `False`.

# 21. Starting the Five-Second Window

```python
if clap_detected:
    last_clap_time = current_time
    clap_count += 1
```

Each valid clap increases the count.

First clap:

```python
if clap_count == 1:
    window_start_time = current_time
```

The first clap begins the five-second command window.
The timer begins only after the first valid clap.

# 22. Counting Additional Claps

During the active window, every valid clap runs:

```python
clap_count += 1
```

- First clap  → `clap_count = 1`
- Second clap → `clap_count = 2`
- Third clap  → `clap_count = 3`

The current version recognizes one-clap and two-clap commands.

# 23. Checking Whether the Window is Active

```python
window_is_active = clap_count > 0
```

This becomes `True` after at least one clap is detected.

# 24. Finishing the Five-Second Window

```python
if (
    window_is_active
    and current_time - window_start_time >= WINDOW_DURATION
):
```

This condition becomes true when:
1. A clap window is active.
2. Five seconds have passed since the first clap.

The program then interprets the clap count.

```python
if clap_count == 1:
    print("Single clap command detected")

elif clap_count == 2:
    print("Double clap command detected")

else:
    print("No command configured")
```

# 25. Resetting the Gesture State

After interpreting the command:

```python
clap_count = 0
window_start_time = 0
```

This prepares the detector for a new clap sequence.

# 26. Exception Handling

The program listens continuously using an infinite loop. The user stops it using `Ctrl + C` which raises a KeyboardInterrupt.

```python
except KeyboardInterrupt:
    print("Listening stopped")
```

This prevents the program from displaying a large error traceback.

# 27. Cleaning Up the Microphone

The finally block always runs:

```python
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
```

- `stream.stop_stream()`: Stops receiving microphone data.
- `stream.close()`: Closes the audio stream.
- `audio.terminate()`: Releases the PyAudio system resources.

# 28. Complete Clap-Window Code

```python
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

print("Listening for clap commands...")
print("1 clap in 5 seconds  -> Single clap command")
print("2 claps in 5 seconds -> Double clap command")
print("Press Ctrl + C to stop.")

last_clap_time = 0
window_start_time = 0
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
        delta = rms_volume - previous_volume

        clap_detected = (
            rms_volume > CLAP_THRESHOLD
            and delta > PEAK_THRESHOLD
            and current_time - last_clap_time > DEBOUNCE_TIME
        )

        if clap_detected:
            last_clap_time = current_time
            clap_count += 1

            if clap_count == 1:
                window_start_time = current_time
                print(
                    "First clap detected. "
                    "Five-second window started."
                )

            else:
                elapsed = current_time - window_start_time

                print(
                    f"👏 Clap {clap_count} detected "
                    f"after {elapsed:.2f} seconds."
                )

        window_is_active = clap_count > 0

        if (
            window_is_active
            and current_time - window_start_time >= WINDOW_DURATION
        ):
            print(
                f"Window finished. "
                f"Total claps: {clap_count}"
            )

            if clap_count == 1:
                print("Single clap command detected.")

            elif clap_count == 2:
                print("Double clap command detected.")

            else:
                print(
                    f"No command configured for "
                    f"{clap_count} claps."
                )

            clap_count = 0
            window_start_time = 0

            print("Listening for the next command...")

        previous_volume = rms_volume

except KeyboardInterrupt:
    print("Listening stopped.")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()

    print("Microphone closed safely.")
```

# 29. Complete Data Flow

```
Physical clap
      ↓
Microphone detects vibration
      ↓
PyAudio reads raw bytes
      ↓
NumPy converts bytes to int16 samples
      ↓
Samples converted to float32
      ↓
RMS loudness calculated
      ↓
Current RMS compared with threshold
      ↓
Current RMS compared with previous RMS
      ↓
Debounce time checked
      ↓
Valid clap event created
      ↓
Clap counter increases
      ↓
Five-second window ends
      ↓
Command classified
```

# 30. Current Commands

The learning version currently classifies:
- One clap: Single-clap command
- Two claps: Double-clap command
- Three or more claps: No command configured

The project version will connect these commands to actions.
Planned actions:
- One clap: Open VS Code
- Two claps: Open YouTube

# 31. Important Engineering Concepts Learned

- **Calibration**: Threshold values depend on the actual microphone and room.
- **Real-time processing**: Audio is processed continuously in chunks.
- **Signal processing**: Raw samples are processed into RMS loudness.
- **State management**: State variable updates track timestamps, counts, windows, volumes.
- **Debouncing**: Prevents double registration of a single clap event.
- **Peak detection**: Filters slow volume increases to focus on rapid sound spikes.
- **Gesture recognition**: Time windows structure sequences of single events into commands.
- **Resource cleanup**: Safe shutdown release of PyAudio devices.

# 32. Limitations

The current energy-based detector may false trigger on knocks, drops, loud speech.
Possible future improvements:
- Frequency-domain analysis
- Adaptive thresholding
- System tray integration
- Wake-word options

# 33. Next Phase

The next phase is to build a clean production-style project:

```
Clap-Control-PC/
│
├── main.py
├── clap_detector.py
├── actions.py
├── config.py
├── requirements.txt
├── README.md
└── assets/
```
