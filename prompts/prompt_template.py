from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Initialize model
model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1
)

# Streamlit UI
st.header("📄 Research Paper Summarizer")

paper_input = st.selectbox(
    "Select research paper name",
    [
        "Select...",
        "Attention Is All You Need",
        "BERT: Pre-training of Deep Bidirectional Transformers"
    ]
)

style_input = st.selectbox(
    "Select explanation style",
    [
        "Beginner-friendly",
        "Technical-heavy",
        "Core-oriented",
        "Mathematical"
    ]
)

length_input = st.selectbox(
    "Select explanation length",
    [
        "Short (1–2 paragraphs)",
        "Medium (3–5 paragraphs)",
        "Long (detailed explanation)"
    ]
)

user_prompt = st.text_input("Enter your specific question or focus")

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

# Button action
if st.button("Summarize"):
    if paper_input == "Select...":
        st.warning("Please select a research paper.")
    else:
        formatted_prompt = template.format(
            paper=paper_input,
            style=style_input,
            length=length_input,
            question=user_prompt
        )

        result = model.invoke(formatted_prompt)
        st.subheader("📌 Summary")
        st.write(result.content)
