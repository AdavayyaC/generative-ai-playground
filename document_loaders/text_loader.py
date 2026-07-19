import os
from langchain_community.document_loaders import TextLoader
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()


# 2. Setup Groq LLM
model = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

prompt = PromptTemplate(
    template='Write a summary for following poem - \n {poem}',
    input_variables=['poem']
)

parser = StrOutputParser()

loader = TextLoader('cricket.txt',encoding='utf-8')

docs = loader.load()

# print("type : ", type(docs))

# print(docs[0])

# print(docs[0].metadata)

# chain form
chain =  prompt | model | parser

result = chain.invoke({'poem':docs[0].page_content})
print(result)