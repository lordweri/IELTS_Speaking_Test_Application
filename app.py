from flask import Flask, request, jsonify, render_template
import whisper
import urllib3
from utils.audio_recorder import AudioRecorder
from utils.speech_to_text import speech_to_text
from utils.scoring import analyze_response, analyze_response_function
from utils.question_generator import generate_part1_question, practice_questions
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

@app.route('/process-audio', methods=['POST'])
def process_audio():
    audio_file = request.json['audio_file']
    transcription = speech_to_text(audio_file, whisper_model)
    return jsonify({"transcription": transcription})

@app.route('/practice-question', methods=['GET'])
def practice_question():
    question = practice_questions()
    return jsonify({"question": question})

@app.route('/part-question', methods=['GET'])
def part1_question():
    questions = generate_part1_question()
    return jsonify({"questions": questions})


@app.route('/evaluate-response', methods=['POST'])
def evaluate_response():
    """Evaluate the response based on the given question."""
    data = request.json
    question = data.get('question')
    transcription = data.get('transcription')

    if not question or not transcription:
        return jsonify({"error": "Both question and transcription are required"}), 400

    evaluation = analyze_response(transcription, question)
    evaluation = evaluation.replace("\n", "<br>")

    return jsonify({"evaluation": evaluation})

@app.route('/analyze-response', methods=['POST'])
def analyze_response():
    try:
        # Get the conversations list from the request
        conversations = request.json.get('conversations')
        if not conversations or len(conversations) % 2 != 0:
            return jsonify({"error": "Invalid conversations format. Expected a list of Q&A pairs."}), 400

        # Call the analyze_response function (assuming it's defined elsewhere)
        feedback = analyze_response_function(conversations)  # Replace with your actual function
        return jsonify({"feedback": feedback})
    except Exception as e:
        print(f"Error analyzing response: {e}")
        return jsonify({"error": "An error occurred while analyzing the response."}), 500
    

if __name__ == '__main__':
    app.run(debug=True)