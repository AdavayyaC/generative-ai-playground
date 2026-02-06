from langchain_groq import ChatGroq
from pydantic import BaseModel,Field
from dotenv import load_dotenv
from typing import Literal, TypedDict, Annotated, Optional



load_dotenv()

model = ChatGroq(
    model="llama-3.1-8b-instant"
)


# schema

class Review(BaseModel):
    key_themes: list[str] = Field(description="write down all the key discussed in the review")
    
    summary: str = Field(description="A brief summary of the review")
    
    sentiment: Literal['pos', 'nge', 'neu'] = Field(description="return sentiment of the review either negative, positive, neutral")
    
    pros: Optional[list[str]] = Field(default=None, description="write down all the pros inside the list")
    
    cons: Optional[list[str]] = Field(default=None, description="write down all the cons inside the list")
    
    
structuredModel = model.with_structured_output(
    Review,
    method="json_mode"
)

result = structuredModel.invoke(
    """
Respond ONLY in valid JSON.

The JSON must match this structure exactly:
- key_themes: list of strings or null
- summary: string
- sentiment: "positive" | "negative" | "neutral"
- pros: list of strings or null
- cons: list of strings or null

Review:
I recently upgraded to the Samsung Galaxy S24 Ultra...
"""
)




print(result)
print(result.summary)
print(result.sentiment)