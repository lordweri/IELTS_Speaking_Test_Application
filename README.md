Markdown

# IELTS Speaking Test Application

**IF YOU HAVE CLONED THE REPOSITORY RUN THIS COMMAND BEFORE RUNNING THE APPLICATION PLEASE**

**pip uninstall torch torchvision torchaudio**

**pip cache purge**

**pip install torch torchvision torchaudio**


This project is a web application designed to simulate the IELTS Speaking test, providing users with practice questions, recording functionality, automated speech-to-text conversion, and AI-powered evaluation and feedback.

## Table of Contents

- [Requirements](#requirements)
- [Frameworks and Libraries](#frameworks-and-libraries)
- [API Integrations](#api-integrations)
- [Project Structure](#project-structure)
- [Running the Application](#running-the-application)
- [LLM Integration and Scoring System](#llm-integration-and-scoring-system)
- [Challenges and Solutions](#challenges-and-solutions)
- [Future Improvements](#future-improvements)

## Requirements

- Python 3.x
- Flask
- Whisper
- Google Generative AI API
- `language_tool_python`
- `urllib3`
- `webbrowser`
- `regex`
- `jspdf` (for PDF download)

## Frameworks and Libraries

IELTS_SPEAKING_TEST_APPLICATION/
├──.vscode/
│   └── settings.json
├── static/
│   ├── script.js
│   └── style.css
├── templates/
│   └── index.html
├── utils/
│   ├── audio_recorder.py
│   ├── question_generator.py
│   ├── scoring.py
│   └── speech_to_text.py
├── venv/ 
├──.gitattributes
├── app.py
├── audio.wav
├── Dockerfile
├── README.md
└── requirements.txt

- **Flask:** Web framework for creating the application's backend and routing.
- **Whisper:** OpenAI's speech recognition model for converting audio to text.
- **Google Generative AI (Gemini):** Large Language Model used for generating questions and providing feedback.
- **`language_tool_python`:**  Library for grammar and style checking (not currently used but intended for future improvements).
- **`urllib3`:** HTTP client library (used for handling warnings).
- **`webbrowser`:** Python module to open a URL in the browser.
- **`regex`:** Regular expression library for extracting information from text.
- **`jspdf`:** JavaScript library for generating PDFs (used in the frontend).

## API Integrations

- **Google Generative AI API (Gemini):** Used for:
    - Generating IELTS speaking questions (Part 1, 2, and 3).
    - Analyzing user responses and providing feedback based on IELTS criteria.
- **Whisper API (Local Model):** Used for transcribing recorded audio into text.

## Project Structure

## Running the Application

1. **Clone the repository:** (If applicable)
2. **Install dependencies:** `pip install -r requirements.txt` (Create `requirements.txt` with all the necessary libraries)
3. **Set up API Keys:**
    - Obtain a Google Generative AI API key and set it as an environment variable or directly in the `scoring.py` and `question_generator.py` files (Not recommended for production).
4. **Run the Flask app:** `python app.py`
5. The application will automatically open in your web browser at `http://127.0.0.1:5000`.

## LLM Integration and Scoring System

- **Question Generation:** The `question_generator.py` script uses the Gemini API to generate IELTS-style questions for all parts of the speaking test.  It constructs prompts for Gemini to act as an IELTS examiner and produce relevant questions.
- **Speech-to-Text:** The `speech_to_text.py` script uses the Whisper model to transcribe user recordings into text.
- **Response Evaluation:** The `scoring.py` script uses the Gemini API to analyze the transcribed responses. It sends a prompt to Gemini that includes the question and the user's answer, instructing Gemini to provide feedback in the style of an IELTS examiner, including strengths, weaknesses, pronunciation tips, vocabulary suggestions, and a band score.  The `analyze_response_function` provides a more detailed analysis for the full test, weighting the scores for each section. The `extract_band_score` function extracts the numerical band score from the Gemini feedback.
- **Feedback Display:** The frontend (`script.js`) displays the evaluation returned by the backend in the designated HTML elements.

## Challenges and Solutions

- **Gemini API Errors:** Implemented `try...except` blocks in `scoring.py` and `question_generator.py` to handle potential errors during API calls and provide informative error messages.
- **Band Score Extraction:** Used regular expressions in the `extract_band_score` function to reliably extract the band score from the Gemini feedback, even if the format varies slightly.
- **Asynchronous Operations:** Used `async/await` in `script.js` to handle asynchronous operations like recording, transcription, and evaluation, preventing the UI from blocking.
- **Data Handling:** Ensured proper data flow between frontend and backend using JSON for requests and responses.
- **Audio Recording:** Implemented a robust audio recording mechanism using the `AudioRecorder` utility class.
- **Duplicate Code:** The utility functions (`speech_to_text.py`, `scoring.py`, `question_generator.py`) are duplicated between the main directory and the `utils` directory. This should be refactored to avoid redundancy and improve maintainability.  The `utils` directory should be the single source of truth for these functions.

## Future Improvements

- **Grammar and Spell Checking:** Integrate `language_tool_python` for more precise grammar and spelling error detection.
- **Improved UI/UX:** Enhance the user interface for a better user experience.
- **More Detailed Feedback:** Refine the Gemini prompts to get more specific and actionable feedback.
- **User Authentication:** Implement user authentication to store and track progress.
- **Database Integration:** Store user data, evaluations, and progress in a database.
- **Refactoring:** Remove duplicate code and improve the overall structure of the project.
- **Unit Testing:** Add unit tests to ensure the reliability of the code.
- **Deployment:** Deploy the application to a web server to make it accessible online.
