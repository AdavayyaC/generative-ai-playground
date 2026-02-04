from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7
)

result = llm.invoke("Hi")
print(result.content)


#
# Loads your API key

# Creates a connection to an AI model (Groq’s LLaMA 3.1)

# Sends a question (prompt) to the model

# Prints the model’s answ



# Temperature controls randomness in the model’s output. It affects how creative or deterministic the response are.
#  1. low val (0.0 -0.3 ) deterministic val
#  1. low val (0.0 -0.3 ) deterministic val

