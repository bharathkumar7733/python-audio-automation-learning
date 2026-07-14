# python-audio-automation-learning

Step-by-step learning repository covering Python modules, OS automation, PyAudio, NumPy audio processing, RMS volume, clap detection, debouncing, peak detection, and clap gesture recognition.

## Folder Structure
```
python-audio-automation-learning/
│
├── lesson_01_modules.py
├── lesson_02_subprocess.py
├── lesson_03_pyaudio.py
├── lesson_04_numpy.py
├── lesson_05_debouncing.py
├── lesson_06_peak_detection.py
├── lesson_07_clap_window.py
├── lesson_debug_microphones.py
├── NOTES.md
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Install PyAudio and NumPy:
   ```bash
   pip install -r requirements.txt
   ```
2. List and debug microphone devices to find the correct index:
   ```bash
   python lesson_debug_microphones.py
   ```
3. Run any lesson file to see incremental logic:
   ```bash
   python lesson_07_clap_window.py
   ```
