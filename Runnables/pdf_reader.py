from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
# load document

loader = TextLoader('sample.txt')
documents = loader.load()

# split the text into smaller chunks
