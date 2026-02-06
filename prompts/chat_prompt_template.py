from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

# creating dynamic templates
chat_template = ChatPromptTemplate([
    ('system' ,'your are helpful {domain} expert'),
    ('human' , 'explain in simple terms, what is {topic}')
])

prompt = chat_template.invoke({
    'domain' :'cricket',
    'topic' : 'batting'
})

print(prompt)