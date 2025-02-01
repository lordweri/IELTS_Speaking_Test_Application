from language_tool_python import LanguageTool
import google.generativeai as gai
import regex as re


gai.configure(api_key="AIzaSyA8kpqELwgcmJY4530KtfYzeAWXf5dDIMk")
gemini_llm = gai.GenerativeModel("gemini-1.5-flash")

def analyse_response(transcription,question):  # Changed function name
    """Use Gemini to analyze the response as an IELTS examiner."""

    prompt = f"""
    You are an IELTS Speaking examiner. Evaluate the candidate's response from the question:
    
    Question: {question}

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

def extract_band_score(feedback):
    """Extracts the band score from the AI feedback safely."""
    match = re.search(r"Band Score: Band (\d+(\.\d+)?)", feedback)  # Match number (e.g., "7", "7.5")
    if match:
        return float(match.group(1))  # Extracted band score as float
    else:
        print("Warning: Could not extract band score from feedback:", feedback)
        return None  # Handle missing scores gracefully

def analyze_response_function(qa_list):
    if len(qa_list) != 14:
        return "Invalid input. Expected 7 Q&A pairs (14 items in the list)."

    part1 = qa_list[:6]  # First 3 Q&A pairs (Part 1)
    part2 = qa_list[6:8]  # Fourth Q&A pair (Part 2)
    part3 = qa_list[8:]  # Last 3 Q&A pairs (Part 3)

    def evaluate_single(question, answer):
        prompt = f"""
        You are an IELTS Speaking examiner. Evaluate the candidate's response:
        
        Question: {question}
        Candidate Response: {answer}

        Provide concise feedback:

        Examiner Feedback:
        Band Score: (Provide a likely band score, e.g., Band 7.0).
        Strengths: (Mention fluency, vocabulary, grammar).
        Areas for Improvement: (Point out weaknesses).
        """

        try:
            response = gemini_llm.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "Error analyzing response."

    # Analyze responses
    part1_feedback, part1_scores = [], []
    for i in range(0, 6, 2):
        feedback = evaluate_single(part1[i], part1[i+1])
        score = extract_band_score(feedback)
        if score is not None:
            part1_scores.append(score)
        part1_feedback.append(feedback)
    part1_avg_score = sum(part1_scores) / len(part1_scores) * 0.15 if part1_scores else 0

    part2_feedback = evaluate_single(part2[0], part2[1])
    part2_score = extract_band_score(part2_feedback)
    part2_score_weighted = part2_score * 0.50 if part2_score else 0

    part3_feedback, part3_scores = [], []
    for i in range(0, 6, 2):
        feedback = evaluate_single(part3[i], part3[i+1])
        score = extract_band_score(feedback)
        if score is not None:
            part3_scores.append(score)
        part3_feedback.append(feedback)
    part3_avg_score = sum(part3_scores) / len(part3_scores) * 0.35 if part3_scores else 0

    overall_score = part1_avg_score + part2_score_weighted + part3_avg_score

    # Create the final feedback report
    feedback_report = f"""
    <h3><u>Part 1 Feedback:</u></h3>
    <p>{part1_feedback[0]}</p>
    <p>{part1_feedback[1]}</p>
    <p>{part1_feedback[2]}</p>

    <h3><u>Part 2 Feedback:</u></h3>
    <p>{part2_feedback}</p>

    <h3><u>Part 3 Feedback:</u></h3>
    <p>{part3_feedback[0]}</p>
    <p>{part3_feedback[1]}</p>
    <p>{part3_feedback[2]}</p>

    <h2><b>Overall Band Score: Band {overall_score:.1f}</b></h2>
    """

    return feedback_report


