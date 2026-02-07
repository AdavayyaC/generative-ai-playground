
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1,
   
)


#--------------------------
# using inbuilt strOutputParser 

# 1st prompt -> detailed prompt
print("-------------detailed answer-------------------------->\n")
template1 = PromptTemplate(
    template="write a detailed report on {topic}",
    input_variables=['topic']
)


# 2st prompt -> summary  prompt
template2 = PromptTemplate(
    template="write a sumary  of 6 to 8 line for   following text \n. {text}",
    input_variables=['text']
)


prompt1 = template1.invoke({'topic':'cricket'})

result = model.invoke(prompt1)
print(result.content)
print("-------------summary -------------------------->\n")


prompt2 = template2.invoke({'text':result.content})

summary = model.invoke(prompt2)
print(summary.content)

#--------------------------
# # using inbuilt strOutputParser 

# parser = StrOutputParser()

# chain = template1 | model | parser | template2 | model | parser

# chainResult = chain.invoke({'topic':'black hole'})

# print(chainResult)