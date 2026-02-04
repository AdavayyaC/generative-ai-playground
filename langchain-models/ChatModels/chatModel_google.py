from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    
    max_tokens=50
)



result = model.invoke("write a poem")
print(result.content)
