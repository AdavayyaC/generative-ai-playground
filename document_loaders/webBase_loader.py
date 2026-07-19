import json
import os

from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

urls = [
    "https://python.langchain.com/docs/concepts/text_splitters",
    "https://python.langchain.com/docs/concepts/vectorstores",
]

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)

parser = JsonOutputParser()

prompt = PromptTemplate(
    template="""
You are a senior research analyst.
Analyze the webpage content below and return a polished JSON report.
{format_instructions}

Web content:
{text}
""",
    input_variables=["text"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser

loader = WebBaseLoader(urls)
docs = loader.load()

for doc in docs:
    title = doc.metadata.get("title") or "Web Page"
    content = doc.page_content[:12000]
    result = chain.invoke({"text": content})

    print(f"\n=== {title} ===")
    print(json.dumps(result, indent=2))
    print("-" * 80)
