# Dictator
Dictator is a commandline program that allows you to dictate to your computer
and have the text transcription be displayed in the terminal, ready to be copy
and pasted wherever you may need it.

Under the hood Dictator use Whisper, the AI speech recognition model from
OpenAI.



## Requirements
Dictator is tested with:
* Python 3.12
* Ubuntu 22.04.5 LTS
* Nvidia RTX 3060 12GB



## Installation
```
# Clone the repo
git clone git@github.com:terzza/dictator.git

# Enter the repo
cd dictator

# Create a Python virtual environment (presuming you're using Python 3.12)
python3.12 -m venv env

# Activate the virtual environment
source env/bin/activate

# Upgrade pip
pip install -U pip

# Install the dependencies
pip install -r requirements.txt

```



## Running
```
# Enter the repo
cd dictator

# Activate the virtual environment
source env/bin/activate

# Start the program
python dictator.py
```



## Roadmap
* Create GUI wrapper with clipboard copy button
* Check Ubuntu system dependencies in a fresh installation
* Expose configuration options via commandline arguments
* Testing on CPU only and / or GPUs with lower VRAM
* Keep a log file of transcriptions
* Optionally keep a copy of all recordings (might not actually be useful ;-/)
* Investigate PyAudio directly into Whisper without intermediary file
* Find better solution to PyAudio stderr hack with sounddevice
* Words per minute indicator (helpful to see how dictation might be faster that
typing WPM)
* Test sequence that can be run against the test wav file with all models and
devices to give an indication of system speed
