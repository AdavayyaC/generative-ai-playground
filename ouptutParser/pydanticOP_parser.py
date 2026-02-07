from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

# model definition
model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1,
)


# pydantic object 
class Person(BaseModel):
    name: str = Field(description="Name of the person")
    age: int = Field(lt=10, description="Age of the person (must be < 10)")
    city: str = Field(description="City the person belongs to")


# parser 
parser = PydanticOutputParser(pydantic_object=Person)

# tempalte prompt
template = PromptTemplate(
    template=(
        "Generate a fictional {place} child.\n"
        "Respond with ONLY valid JSON.\n"
        "{format_instruction}"
    ),
    input_variables=["place"],
    partial_variables={
        "format_instruction": parser.get_format_instructions()
    },
)

# # prmpt
# prompt = template.invoke({"place": "Indian"})

# # result 
# result = model.invoke(prompt)
# print(result)
# parsed_result = parser.parse(result.content)
# print(parsed_result)


# now chain

chain = template | model | parser
final_result = chain.invoke({'place':'nepal'})
print(final_result)