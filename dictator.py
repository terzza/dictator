#!/usr/bin/env python

import _thread
import pyaudio
import wave
import whisper
import sounddevice # TODO importing this silences the verbose stderr from PyAudio. Would be good to find a better solution


class Dictator:

    WHISPER_MODELS = ["tiny", "base", "small", "medium", "large", "turbo"]
    AUDIO_FORMAT = pyaudio.paInt16
    CHANNELS = 1
    FRAME_RATE = 44100
    CHUNK_SIZE = FRAME_RATE // 4
    TEMP_WAV_FILENAME = "temp_audio.wav"
    LINE_SPACING = "\n"

    def __init__(self, verbose_instructions=True):
        print("Initialising...") if verbose_instructions else ""
        self.MODEL_NAME = self.WHISPER_MODELS[1]
        self.DEVICE = "cpu"
        # self.DEVICE = "cuda"
        self.READY_PROMPT = "Ready to Record? [Y/n]" if verbose_instructions else ">"
        self.RECORDING_PROMPT = ">>> RECORDING " if verbose_instructions else ""

        self.py_audio = pyaudio.PyAudio()
        self.whisper_model = whisper.load_model(self.MODEL_NAME, device=self.DEVICE)

    def get_user_input(self, user_input_messages):
        user_input_messages.append(input(self.RECORDING_PROMPT))

    def open_stream(self):
        self.stream = self.py_audio.open(
            format=self.AUDIO_FORMAT,
            channels=self.CHANNELS,
            rate=self.FRAME_RATE,
            input=True,
            frames_per_buffer=self.CHUNK_SIZE
        )

    def close_stream(self):
        self.stream.stop_stream()
        self.stream.close()

    def start_recording(self):
        self.open_stream()
        frames = []

        user_input = []
        _thread.start_new_thread(self.get_user_input, (user_input,))

        while True:
            frames.append(self.stream.read(self.CHUNK_SIZE))
            if user_input:
                break
            print(".", end="", flush=True)

        self.close_stream()
        self.save_audio(frames)

    def save_audio(self, frames):
        wav_output = wave.open(self.TEMP_WAV_FILENAME, 'wb')
        wav_output.setnchannels(self.CHANNELS)
        wav_output.setsampwidth(self.py_audio.get_sample_size(self.AUDIO_FORMAT))
        wav_output.setframerate(self.FRAME_RATE)
        wav_output.writeframes(b''.join(frames))
        wav_output.close()

    def close(self):
        self.py_audio.terminate()

    def transcribe(self):
        audio = whisper.load_audio(self.TEMP_WAV_FILENAME)
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(
            audio,
            n_mels=self.whisper_model.dims.n_mels
        ).to(self.whisper_model.device)

        options = whisper.DecodingOptions()
        result = whisper.decode(self.whisper_model, mel, options)

        return result.text

    def detect_language(self, mel):
        if self.whisper_model:
            _, probs = self.whisper_model.detect_language(mel)
            print(f"Detected language: {max(probs, key=probs.get)}")

    def start_cli(self):
        running = True
        while running:
            print(self.READY_PROMPT, end="", flush=True)
            user_input = input("")

            if user_input not in ["Y", "y", ""]:
                break

            self.start_recording()
            print(f"{self.LINE_SPACING}{self.transcribe().strip()}{self.LINE_SPACING}")


if __name__ == "__main__":
    dictator = Dictator()
    dictator.start_cli()
