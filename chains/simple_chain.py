from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

prompt = PromptTemplate(
    template="generate 5 intersting facts about {topic}",
    input_variables=['topic']
)

# model defintion
model = ChatGroq(
   model="llama-3.1-8b-instant",
   temperature=0.1
)

# parser
parser = StrOutputParser()

# LangChain Expression Language = LCEL
chain = prompt | model | parser 

result = chain.invoke({'topic':'write a kannada poem for Malikjaan \n '})

print(result)


# now inside chain : it will give you nodes how dereicte 
# chain.get_graph().print_ascii()
