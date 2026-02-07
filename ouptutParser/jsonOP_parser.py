from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1,
   
)

parser = JsonOutputParser()


template = PromptTemplate(
    template="write the facts about {topic} \n {format_instruction}",
    input_variables=['topic'],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)

# prompt = template.format()

# result = model.invoke(prompt)
# print(result)

# finalResult = parser.parse(result.content)

# print('-'*30,'\n')
# print(type(finalResult))
# print( finalResult)

#  we can use the chain also for this above code
chain = template | model | parser 

chainResult = chain.invoke({'topic':'cricket'})

print(chainResult)