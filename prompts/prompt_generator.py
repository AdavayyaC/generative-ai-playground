from langchain_core.prompts import PromptTemplate

# template
# Prompt Template
template = PromptTemplate(
    input_variables=["paper", "style", "length", "question"],
    template="""
You are an expert research assistant.

Research Paper: {paper}
Explanation Style: {style}
Explanation Length: {length}

User Question / Focus:
{question}

Provide a clear, well-structured explanation accordingly.
"""
)

template.save('template.json')