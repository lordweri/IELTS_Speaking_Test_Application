from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
Answer the question below.

here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def handle_conversation():
    context = ""
    while True:
        question = input("Enter a question: ")
        if question.lower() == "exit":
            break

        result = chain.invoke({"context": context, "question": question})
        print("Bot: ",result)
        context += f"\nUser: {question}\nAI: {result}"

if __name__ == "__main__":
    handle_conversation()