from langchain_ollama import OllamaLLM
model = OllamaLLM(model="llama3")
result = model.invoke(input = "What is the date of today?")
print(result)

