from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1,
    max_tokens=50
)



result = model.invoke("write a poem")
print(result.content)


# ----------------------------------------------------------
#  documentation of above code 
# Temperature controls randomness in the model’s output. It affects how creative or deterministic the response are.
#  1. low val (0.0 -0.3 ) deterministic val
#  1. low val (0.0 -0.3 ) deterministic val