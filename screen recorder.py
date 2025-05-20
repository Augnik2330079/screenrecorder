import sounddevice as sd
import soundfile as sf
import threading
import queue
from tkinter import *
from tkinter import filedialog
import numpy as np

q = queue.Queue()
recording = False
audio_data = []

def record_audio():
    global recording, audio_data
    recording = True
    audio_data = []
    def callback(indata, frames, time, status):
        if recording:
            audio_data.append(indata.copy())
        else:
            raise sd.CallbackStop()
    with sd.InputStream(samplerate=44100, channels=2, callback=callback):
        while recording:
            sd.sleep(100)

def start_recording():
    threading.Thread(target=record_audio).start()
    record_btn.config(state=DISABLED)
    stop_btn.config(state=NORMAL)
    save_btn.config(state=DISABLED)
    status_label.config(text="Recording...")

def stop_recording():
    global recording
    recording = False
    record_btn.config(state=NORMAL)
    stop_btn.config(state=DISABLED)
    save_btn.config(state=NORMAL)
    status_label.config(text="Recording stopped. Ready to save.")

def save_audio():
    if audio_data:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav")],
            title="Save as"
        )
        if file_path:
            arr = np.concatenate(audio_data, axis=0)
            sf.write(file_path, arr, 44100)
            status_label.config(text=f"Saved as {file_path}")
        else:
            status_label.config(text="Save cancelled.")
    else:
        status_label.config(text="No recording to save.")

voice_rec = Tk()
voice_rec.geometry("320x220")
voice_rec.title("Voice Recorder")

record_btn = Button(voice_rec, text="Start Recording", command=start_recording)
record_btn.pack(pady=5)

stop_btn = Button(voice_rec, text="Stop Recording", command=stop_recording, state=DISABLED)
stop_btn.pack(pady=5)

save_btn = Button(voice_rec, text="Save", command=save_audio, state=DISABLED)
save_btn.pack(pady=5)

status_label = Label(voice_rec, text="")
status_label.pack(pady=5)

voice_rec.mainloop()
