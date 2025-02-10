#!/usr/bin/env python

from dictator import Dictator
import tkinter as tk
import threading


class DictatorGui(tk.Tk):

    BUTTON_START = "Start"
    BUTTON_STOP = "Stop"
    BUTTON_TRANSCRIBING = "Transcribing..."

    def __init__(self):
        super().__init__()
        self.dictator = Dictator()
        self.recording = False

        self.text_box = tk.Text(self, height=30, width=150)
        self.text_box.pack(fill=tk.X)

        self.log_box = tk.Text(self, height=5)
        self.log_box.pack(fill=tk.X)

        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X)

        self.record_button_text = tk.StringVar()
        self.record_button_text.set(self.BUTTON_START)
        self.record_button = tk.Button(button_frame, textvariable=self.record_button_text, command=self.recording_toggle, height=10)
        self.record_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.copy_button = tk.Button(button_frame, text="Copy", command=self.copy_to_clipboard, height=10)
        self.copy_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def recording_toggle(self):
        if not self.recording:
            self.recording = True
            self.log_box.insert(tk.END, "Recording Started\n")
            threading.Thread(target=self.start_recording, daemon=True).start()
        else:
            self.recording = False
            self.stop_recording()
            self.log_box.insert(tk.END, "Recording Stopped\n")

    def start_recording(self):
        self.record_button_text.set(self.BUTTON_STOP)
        self.dictator.start_recording()

    def stop_recording(self):
        self.dictator.stop_recording()
        threading.Thread(target=self.transcribe, daemon=True).start()

    def transcribe(self):
        self.dictator.recording_is_finished.wait()

        self.record_button_text.set(self.BUTTON_TRANSCRIBING)
        self.record_button.config(state=tk.DISABLED)
        transcription = self.dictator.transcribe()
        print(f"\n>>> TRANSCRIPTION: '{transcription}'")
        self.text_box.insert(tk.END, f"\n{transcription.strip()}\n")

        self.record_button_text.set(self.BUTTON_START)
        self.record_button.config(state=tk.NORMAL)

    def copy_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.text_box.get("1.0", tk.END).strip())


if __name__ == "__main__":
    app = DictatorGui()
    app.mainloop()
