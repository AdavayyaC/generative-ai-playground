from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# load env
load_dotenv()

# model define
llm = ChatGroq(
    model='llama-3.1-8b-instant',
    temperature=0.2
)

# create prompt template
prompt = PromptTemplate(
    template="Suggest a catchy blog title about {topic}",
    input_variables=["topic"]
)

# create # LCEL chain
chain = prompt | llm 

# run the chain with topic
topic = input("Enter Topic")
output = chain.invoke({"topic":topic})

print("\n\n--------Generated Blog title :--------\n\n",output.content)