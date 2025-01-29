import whisper

def transcribe_audio(audio_file, model):
    """Transcribe the audio file using the Whisper model."""
    result = model.transcribe(audio_file)
    return result['text']