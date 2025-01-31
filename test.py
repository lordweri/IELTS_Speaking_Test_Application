from utils.question_generator import generate_part1_question, generate_part2_question, generate_part3_question, practice_questions

# Test Part 1 question generation
print("Testing Part 1 Question Generation:")
part1_question = generate_part1_question()
print("Input: N/A (no input required for Part 1)")
print("Output:", part1_question)
print("="*50)

# Test Part 2 question generation
print("Testing Part 2 Question Generation:")
part2_question = generate_part2_question()
print("Input: N/A (no input required for Part 2)")
print("Output:", part2_question)
print("="*50)

# Test Part 3 question generation with a previous response
previous_response = "I enjoy traveling because it broadens my perspective."
print("Testing Part 3 Question Generation with Previous Response:")
print("Input: Previous Response:", previous_response)
part3_question = generate_part3_question(previous_response)
print("Output:", part3_question)
print("="*50)

# Test random practice question generation
print("Testing Practice Question Generation:")
practice_question = practice_questions()
print("Input: N/A (random practice question)")
print("Output:", practice_question)
print("="*50)
