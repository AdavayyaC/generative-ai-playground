from langchain_groq import ChatGroq
from pydantic import BaseModel,Field
from dotenv import load_dotenv
from typing import Literal, TypedDict, Annotated, Optional



load_dotenv()

model = ChatGroq(
    model="llama-3.1-8b-instant"
)


# schema
json_schema = {
     "title": "Review",
  "type": "object",
  "properties": {
    "key_themes": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Write down all the key themes discussed in the review in a list"
    },
    "summary": {
      "type": "string",
      "description": "A brief summary of the review"
    },
    "sentiment": {
      "type": "string",
      "enum": ["pos", "neg"],
      "description": "Return sentiment of the review either negative, positive or neutral"
    },
    "pros": {
      "type": ["array", "null"],
      "items": {
        "type": "string"
      },
      "description": "Write down all the pros inside a list"
    },
    "cons": {
      "type": ["array", "null"],
      "items": {
        "type": "string"
      },
      "description": "Write down all the cons inside a list"
    },
    "name": {
      "type": ["string", "null"],
      "description": "Write the name of the reviewer"
    }
  },
  "required": ["key_themes", "summary", "sentiment"]
}
    
structuredModel = model.with_structured_output(
    json_schema,
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
