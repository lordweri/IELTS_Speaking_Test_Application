# Weri Masao
# Date: 2021-09-30
# Description: A simple audio recorder class that uses PyAudio to record audio from the microphone.

import pyaudio
import wave
import threading

class AudioRecorder:
    def __init__(self, filename="audio.wav"):
        self.filename = filename
        self.channels = 1
        self.rate = 16000
        self.frames_per_buffer = 1024
        self.format = pyaudio.paInt16
        self.frames = []
        self.recording = False
        self.stream = None
        self.p = pyaudio.PyAudio()

    def start_recording(self):
        """Start recording indefinitely."""
        if self.recording:
            print("Already recording...")
            return

        self.recording = True
        self.frames = []

        self.stream = self.p.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.frames_per_buffer)
        print("Recording started...")

        def record():
            while self.recording:
                data = self.stream.read(self.frames_per_buffer)
                self.frames.append(data)

        self.thread = threading.Thread(target=record)
        self.thread.start()

    def stop_recording(self):
        """Stop recording and save the audio file."""
        if not self.recording:
            print("Not currently recording.")
            return

        self.recording = False
        self.thread.join()  # Wait for recording to finish
        self.stream.stop_stream()
        self.stream.close()

        # Save to file
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

        print(f"Recording saved to {self.filename}")
        return self.filename

    def close(self):
        """Terminate PyAudio instance."""
        self.p.terminate()
