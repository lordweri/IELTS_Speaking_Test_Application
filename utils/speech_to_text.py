import whisper

def speech_to_text(audio_file, model):
    """Transcribe the audio file using the Whisper model."""
    result = model.transcribe(audio_file)
    return result['text']