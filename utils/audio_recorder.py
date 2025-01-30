import pyaudio
import wave

def record_audio(filename="audio.wav", duration=10):
    """Record audio and save it to the specified file."""
    p = pyaudio.PyAudio()
    
    # Set parameters
    channels = 1
    rate = 16000
    frames_per_buffer = 1024
    format = pyaudio.paInt16

    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=frames_per_buffer)
    print("Recording...")

    frames = []
    for _ in range(0, int(rate / frames_per_buffer * duration)):
        data = stream.read(frames_per_buffer)
        frames.append(data)

    print("Recording finished!")
    
    # Save the audio to a file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    stream.stop_stream()
    stream.close()
    p.terminate()

    return filename
