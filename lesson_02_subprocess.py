# Lesson 2: Processes & Subprocesses
# A process is a running program instance. A subprocess is started by another process.
import subprocess

# subprocess.Popen runs a program as a separate background process.
# We pass the command and arguments as a list of strings.
subprocess.Popen(["notepad"])

# Key concepts:
# - "notepad" is searched in the system PATH directories.
# - Popen doesn't block the Python program execution (non-blocking).
