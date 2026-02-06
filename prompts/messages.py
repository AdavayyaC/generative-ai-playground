from langchain_core.messages import  SystemMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize model
model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1
)

messages = [
    SystemMessage(content='You are helpful assistant'),
    HumanMessage(content='tell me about langchain') 
]

result = model.invoke(messages)

context = AIMessage(content=result.content)

messages.append(context)

print(messages)