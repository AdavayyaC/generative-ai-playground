from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Create chat prompt template
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful customer support agent"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{query}")
])

# Load chat history correctly
chat_history = []

with open("chat_history.txt", "r") as f:
    for line in f:
        chat_history.append(HumanMessage(content=line.strip()))

# Create prompt
prompt = chat_template.invoke({
    "chat_history": chat_history,
    "query": "Where is my refund?"
})

print(prompt)
