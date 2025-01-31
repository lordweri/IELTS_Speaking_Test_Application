import google.generativeai as genai
import random
genai.configure(api_key="AIzaSyA8kpqELwgcmJY4530KtfYzeAWXf5dDIMk")  
model = genai.GenerativeModel("gemini-1.5-flash")
def generate_part1_question():
    """Generates a list of three Part 1 questions for the IELTS Speaking test."""
    
    prompt = """
    You are an IELTS Speaking examiner. 
    Generate three Part 1 questions: the first about the candidate’s personal background,
    the second about their origin or hometown, and the third about their job, studies, or self-description. 
    For Part 2, create one cue card topic requiring a 1-2 minute response, with bullet points guiding the candidate on what to include. 
    For Part 3, generate three follow-up questions diving deeper into an abstract or broader topic related to the Part 2 cue card.
    Return only the list of seven questions without any additional text or formatting.
    No stars please just pure text
    """

    # Generate response using Gemini AI
    questions = model.generate_content(prompt)

    # Return the generated questions in a list format
    if questions:
        return [q.strip() for q in questions.text.split('\n') if q.strip()]
    else:
        return ["Error generating questions"]


def practice_questions():
    '''Generate a practice question for the IELTS Speaking test with randomized categories.'''

    # Randomly select a category (1, 2, or 3)
    category = random.choice([1, 2, 3])

    if category == 1:
        prompt = "Generate an introductory IELTS Speaking question. Example topics: personal background, hobbies, daily routine. Return only the question."
    elif category == 2:
        prompt = "Generate a general topic IELTS Speaking question that encourages extended answers. Example topics: technology, travel, education. Return only the question."
    else:
        prompt = "Generate an simple abstract concept IELTS Speaking question. Example topics: happiness, culture, love. Return only the question."

    # Generate the question using Gemini
    response = model.generate_content(prompt)

    return response.text.strip() if response else "Error generating question"
    question = model.generate_content(prompt)
