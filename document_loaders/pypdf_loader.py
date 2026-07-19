import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# 2. Setup Groq LLM
model = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

prompt = PromptTemplate(
    template='Write the intent of the following page - \n {bookpage}',
    input_variables=['bookpage']
)


parser = StrOutputParser()

# load ther pdf
loader = PyPDFLoader('book.pdf')
docs = loader.load()

# print(len(docs))

# print(docs[1].page_content)

chain = prompt | model | parser 


result = chain.invoke({"bookpage":docs[3].page_content})

print(result)
