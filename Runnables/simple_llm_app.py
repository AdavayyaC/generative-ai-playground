from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()

# llm define
llm = ChatGroq(
    model='llama-3.1-8b-instant'
)

# prompt template
prompt = PromptTemplate(
    template='Suggest a catchy blog title about {topic}.',
    input_variables=['topic']
)

# take input
topic = input("Enter topic name: ")

# format the prompt 
formatted_prompt = prompt.format(topic=topic)

# call llm (invoke)
blog_title = llm.invoke(formatted_prompt)

# print anser
print("Geerated Blog Title :",blog_title.content)

