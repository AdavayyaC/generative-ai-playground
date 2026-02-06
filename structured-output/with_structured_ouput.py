from langchain_groq import ChatGroq
from dotenv import load_dotenv
from typing import Literal, TypedDict, Annotated, Optional



load_dotenv()

model = ChatGroq(
    model="llama-3.1-8b-instant"
)


# schema

class Review(TypedDict):
    key_themes : Annotated[list[str], "write down all the key discussed in the review"]
    summary: Annotated[str, "A brief summary of the review"]
    sentiment:  Annotated[Literal['pos','nge'] ,"return sentiment of the review either negetive,positive, neutral"]
    pros: Annotated[Optional[list[str]], "write down all the pros inside the list"]
    cons: Annotated[Optional[list[str]], "write down all the cons inside the list"]
    
    
structuredModel = model.with_structured_output(
    Review,
    method="json_mode"
)

result = structuredModel.invoke(
    "Respond ONLY in valid JSON.\n\n"
    "Summarize the review and classify sentiment.\n\n"
    "I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it’s an absolute powerhouse! "
    "The Snapdragon 8 Gen 3 processor makes everything lightning fast—whether I’m gaming, multitasking, "
    "or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast "
    "charging is a lifesaver.\n\n"
    "The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it often. "
    "What really blew me away is the 200MP camera—the night mode is stunning, capturing crisp, vibrant images "
    "even in low light. Zooming up to 100x actually works well for distant objects, but anything beyond 30x "
    "loses quality.\n\n"
    "However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung’s One UI "
    "still comes with bloatware—why do I need five different Samsung apps for things Google already provides? "
    "The $1,300 price tag is also a hard pill to swallow.\n\n"
    "Pros:\n"
    "- Insanely powerful processor (great for gaming and productivity)\n"
    "- Stunning 200MP camera with incredible zoom capabilities\n"
    "- Long battery life with fast charging\n"
    "- S-Pen support is unique and useful"
)



print(result)
print(result['summary'])
print(result['sentiment'])