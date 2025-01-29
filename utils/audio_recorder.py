import pyaudio
import wave

def record_audio(filename="audio/response.wav", duration=5):
    # Set up the audio stream
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1,
                        rate=44100, input=True,
                        frames_per_buffer=1024)
    frames = []

    # Record audio for the specified duration
    for i in range(0, int(44100 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    # Stop recording and save the audio file
    stream.stop_stream()
    stream.close()
    audio.terminate()
    wf = wave.open(filename, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b"".join(frames))
    wf.close()
    return filename