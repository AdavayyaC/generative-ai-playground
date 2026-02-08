from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


# load
load_dotenv()

# model definition
model = ChatGroq(
    model="allam-2-7b"
)


# prompt1 for detailed report
prompt1 = PromptTemplate(
    template='Write detailed report about {topic}.',
    input_variables=['topic']
)

prompt2  = PromptTemplate(
    template='extract 5 most important points aof this  {text}.',
    input_variables=['text']
)


parser = StrOutputParser()

# sequential chain 
chain = prompt1 | model | parser  | prompt2 | model | parser


result = chain.invoke({'topic':'AI'})

print(result)
chain.get_graph().print_ascii()