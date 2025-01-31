from language_tool_python import LanguageTool
import google.generativeai as gai


gai.configure(api_key="AIzaSyA8kpqELwgcmJY4530KtfYzeAWXf5dDIMk")
gemini_llm = gai.GenerativeModel("gemini-1.5-flash")

def analyze_response(transcription):  # Changed function name
    """Use Gemini to analyze the response as an IELTS examiner."""

    prompt = f"""
    You are an IELTS Speaking examiner. Evaluate the candidate's response:

    Candidate Response: {transcription}

    Provide concise feedback in this format:

    Examiner Feedback:
    Band Score: (Provide a likely band score, e.g., Band 7-8).
    Strengths: (Mention fluency, vocabulary, and grammatical strengths).
    Areas for Improvement: (Point out areas that could be improved).

    Pronunciation Tips:
    Stress: (Highlight key words with correct stress).
    Sounds: (Identify difficult sounds to improve).
    Intonation: (Suggest improvements).

    Vocabulary Tips:
    Synonyms: (Suggest alternatives for commonly used words).
    Collocations: (Recommend natural word pairings).
    """

    try:
        response = gemini_llm.generate_content(prompt) # Call Gemini API
        return response.text.strip() # Access the text content
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Error analyzing response."  # Handle errors gracefully




