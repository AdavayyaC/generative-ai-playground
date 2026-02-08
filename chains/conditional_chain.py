from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda
from pydantic import BaseModel, Field
from typing import Literal

# Load env
load_dotenv()

# Model
model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# ---------------- Pydantic Schema ----------------
class Feedback(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(
        description="Sentiment of the feedback"
    )

parser = StrOutputParser()
parser2 = PydanticOutputParser(pydantic_object=Feedback)

# ---------------- Classifier Prompt ----------------
prompt1 = PromptTemplate(
    template="""
            You must classify the sentiment of the feedback.
            Return ONLY valid JSON.
            Do NOT explain.
            Feedback:
            {feedback}
            {format_instructions}
            """,
    input_variables=["feedback"],
    partial_variables={
        "format_instructions": parser2.get_format_instructions()
    }
)

classifier_chain = prompt1 | model | parser2

# ---------------- Response Prompts ----------------
prompt_positive = PromptTemplate(
    template="Write an appropriate response to this positive feedback:\n{feedback}",
    input_variables=["feedback"],
)

prompt_negative = PromptTemplate(
    template="Write an appropriate response to this negative feedback:\n{feedback}",
    input_variables=["feedback"],
)

pos_chain = prompt_positive | model | parser
neg_chain = prompt_negative | model | parser

# ---------------- Branching ----------------
branch_chain = RunnableBranch(
    (lambda x: x.sentiment == "positive", pos_chain),
    (lambda x: x.sentiment == "negative", neg_chain),
    RunnableLambda(lambda _: "Could not determine sentiment")
)

# ---------------- Final Chain ----------------
chain = classifier_chain | branch_chain

# ---------------- Run ----------------
result = chain.invoke({
    "feedback": "The product quality is consistently degrading"
})

print(result)
chain.get_graph().print_ascii()