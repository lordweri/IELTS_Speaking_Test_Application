from flask import Flask, request, jsonify, render_template
import whisper
import urllib3
from utils.audio_recorder import AudioRecorder
from utils.speech_to_text import speech_to_text
from utils.scoring import analyze_response
import warnings
warnings.filterwarnings("ignore", category=urllib3.exceptions.NotOpenSSLWarning)


app = Flask(__name__)   
recorder = AudioRecorder()
#Load Whisper Model
whisper_model = whisper.load_model("base")
@app.route('/')

def index():
    return render_template('index.html')

@app.route('/start-recording', methods=['POST'])
def start_recording():
    recorder.start_recording()
    return jsonify({"status": "recording started"})

@app.route('/stop-recording', methods=['POST'])
def stop_recording():
    audio_file = recorder.stop_recording()
    return jsonify({"status": "recording stopped", "audio_file": audio_file})

@app.route('/time-recording', methods=['POST'])
def time_recording():
    audio_file = recorder.record_audio()
    return jsonify({"status": "recording stopped", "audio_file": audio_file})

@app.route('/process-audio', methods=['POST'])
def process_audio():
    audio_file = request.json['audio_file']
    transcription = speech_to_text(audio_file, whisper_model)
    evaluation = analyze_response(transcription)

    return jsonify({"evaluation": evaluation, "transcription": transcription})

if __name__ == '__main__':
    app.run(debug=True)