from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Load environment variables
load_dotenv()

# Initialize model
model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1
)

# Chat history (context memory)
chat_history = [
    SystemMessage(content="You are a helpful assistant.")
]

# Infinite chat loop
while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "q", "quit"]:
        print("Buggie AI: Goodbye 👋")
        break

    # Add user message
    chat_history.append(HumanMessage(content=user_input))

    
    result = model.invoke(chat_history)

    # Adding  AI response to history
    chat_history.append(AIMessage(content=result.content))

    # Print AI response
    print("Buggie AI:", result.content)

# Optional: inspect chat history
print(chat_history)
