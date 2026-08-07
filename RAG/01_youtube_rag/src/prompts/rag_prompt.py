from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""
You are a helpful assistant.

Context:
{context}

Question:
{question}
""",
    input_variables=["context", "question"],
)