import spacy
from language_tool_python import LanguageTool

# Load the language model
nlp = spacy.load("en_core_web_sm")

# Initialize the language tool for grammar checks
tool = LanguageTool('en-US')

def score_response(response):
    """Score the response based on grammar and spelling."""
    # Tokenize the response
    doc = nlp(response)
    word_count = len([token.text for token in doc if token.is_alpha])
    sentence_count = len([sent for sent in doc.sents])  

    fluency_score = (word_count / sentence_count)

    matches = tool.check(response)
    grammar_score = len(matches)

    lexical_score = len(set([token.text.lower() for token in doc if token.is_alpha])) / word_count
    overall_score = fluency_score - grammar_score + lexical_score
    return {"fluency_score": fluency_score, "grammar_score": grammar_score, "lexical_score": lexical_score, "overall_score": overall_score}