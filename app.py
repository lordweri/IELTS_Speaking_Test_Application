from flask import Flask, request, jsonify, render_template
import whisper
from utils.audio_recorder import record_audio
from utils.speech_to_text import speech_to_text
from utils.scoring import score_response

app = Flask(__name__)   

#Load Whisper Model
whisper_model = whisper.load_model("base")
@app.route('/')

def index():
    return render_template('index.html')
'''
@app.route('/start-recording', methods=['POST'])
def start_recording():
    audio_file = record_audio()
    return jsonify({"status": "success", "audio_file": "audio.wav"})

@app.route('/process-audio', methods=['POST'])
def process_audio():
    audio_file = request.json['audio_file']
    transcription = speech_to_text(audio_file, whisper_model)
    score = score_response(transcription)
    return jsonify({"transcription": transcription, "score": score})
'''

if __name__ == '__main__':
    app.run(debug=True)