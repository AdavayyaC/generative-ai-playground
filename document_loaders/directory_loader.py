from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
 

loader = DirectoryLoader(
    path='books',
    glob='*.pdf',
    loader_cls=PyPDFLoader
)

docs = loader.lazy_load()

try:
    first_doc = next(docs)
    print(first_doc.page_content)
    print(first_doc.metadata)
except StopIteration:
    print("No documents found")

for document in docs:
    print(document.metadata)