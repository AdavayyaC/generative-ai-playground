from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    provider="hf-inference",   # 🔑 THIS IS THE FIX
    max_new_tokens=50,
    temperature=0
)

result = llm.invoke("What is the capital of Karnataka?")
print(result)
