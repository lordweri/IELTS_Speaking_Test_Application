from language_tool_python import LanguageTool
import google.generativeai as gai


gai.configure(api_key="AIzaSyA8kpqELwgcmJY4530KtfYzeAWXf5dDIMk")
gemini_llm = gai.GenerativeModel("gemini-1.5-flash")

def analyze_response(transcription,question):  # Changed function name
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

def analyze_response_function(qa_list):
    """
    Analyze a list of questions and answers in the format [q, a, q, a, q, a, q, a, q, a, q, a, q, a].
    Provide feedback and an overall IELTS score based on the given weighting.
    """
    if len(qa_list) != 14:  # Ensure the list has exactly 7 Q&A pairs
        return "Invalid input. Expected 7 Q&A pairs (14 items in the list)."

    # Split the list into Part 1, Part 2, and Part 3
    part1 = qa_list[:6]  # First 3 Q&A pairs (Part 1)
    part2 = qa_list[6:8]  # Fourth Q&A pair (Part 2)
    part3 = qa_list[8:]  # Last 3 Q&A pairs (Part 3)

    # Function to evaluate a single Q&A pair
    def evaluate_single(question, answer):
        prompt = f"""
        You are an IELTS Speaking examiner. Evaluate the candidate's response from the question:
        
        Question: {question}

        Candidate Response: {answer}

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
            response = gemini_llm.generate_content(prompt)  # Call Gemini API
            return response.text.strip()  # Access the text content
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "Error analyzing response."  # Handle errors gracefully

    # Evaluate Part 1 (15% weight)
    part1_feedback = []
    part1_scores = []
    for i in range(0, 6, 2):  # Iterate over Q&A pairs
        question = part1[i]
        answer = part1[i + 1]
        feedback = evaluate_single(question, answer)
        part1_feedback.append(feedback)
        # Extract band score from feedback (e.g., "Band Score: Band 7")
        band_score = float(feedback.split("Band Score: Band ")[1].split(".")[0])
        part1_scores.append(band_score)
    part1_avg_score = sum(part1_scores) / len(part1_scores) * 0.15  # Apply 15% weight

    # Evaluate Part 2 (50% weight)
    part2_question = part2[0]
    part2_answer = part2[1]
    part2_feedback = evaluate_single(part2_question, part2_answer)
    part2_score = float(part2_feedback.split("Band Score: Band ")[1].split(".")[0]) * 0.50  # Apply 50% weight

    # Evaluate Part 3 (35% weight)
    part3_feedback = []
    part3_scores = []
    for i in range(0, 6, 2):  # Iterate over Q&A pairs
        question = part3[i]
        answer = part3[i + 1]
        feedback = evaluate_single(question, answer)
        part3_feedback.append(feedback)
        # Extract band score from feedback
        band_score = float(feedback.split("Band Score: Band ")[1].split(".")[0])
        part3_scores.append(band_score)
    part3_avg_score = sum(part3_scores) / len(part3_scores) * 0.35  # Apply 35% weight

    # Calculate overall score
    overall_score = part1_avg_score + part2_score + part3_avg_score

    # Generate general overview
    general_overview = f"""
    Overall Band Score: Band {overall_score:.1f}

    General Overview:
    - Part 1 (15% weight): Average Band {sum(part1_scores) / len(part1_scores):.1f}
    - Part 2 (50% weight): Band {part2_score / 0.50:.1f}
    - Part 3 (35% weight): Average Band {sum(part3_scores) / len(part3_scores):.1f}

    Strengths:
    - The candidate demonstrates [insert strengths from feedback].

    Areas for Improvement:
    - The candidate should focus on [insert areas for improvement from feedback].
    """

    # Combine feedback
    feedback_report = f"""
    Part 1 Feedback:
    {part1_feedback[0]}
    {part1_feedback[1]}
    {part1_feedback[2]}

    Part 2 Feedback:
    {part2_feedback}

    Part 3 Feedback:
    {part3_feedback[0]}
    {part3_feedback[1]}
    {part3_feedback[2]}

    {general_overview}
    """

    return feedback_report



