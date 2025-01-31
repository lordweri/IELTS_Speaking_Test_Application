import whisper
from utils.audio_recorder import AudioRecorder
from utils.speech_to_text import speech_to_text
from utils.scoring import analyze_response

def test_recording_and_transcription():
    # Step 1: Initialize Whisper model
    print("Loading Whisper model...")
    model = whisper.load_model("base")

    # Step 2: Record audio
    print("Starting audio recording...")
    recorder = AudioRecorder(filename="test_recording.wav")
    recorder.start_recording()

    # Let the user know when to stop recording
    input("Press Enter to stop recording...")
    recorder.stop_recording()
    print("Recording saved to 'test_recording.wav'")

    # Step 3: Transcribe the recorded audio
    print("Transcribing audio...")
    transcription = speech_to_text("test_recording.wav", model)
    print("Transcription:")
    print(transcription)
    print(analyze_response(transcription))

    # Step 4: Clean up
    recorder.close()

if __name__ == "__main__":
    test_recording_and_transcription()