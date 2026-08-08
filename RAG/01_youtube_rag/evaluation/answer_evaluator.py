from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


def evaluate_answer(question, ground_truth, answer):

    prompt = f"""
You are evaluating a RAG system.

Question:
{question}

Ground Truth:
{ground_truth}

RAG Answer:
{answer}

Evaluate how well the RAG Answer matches the Ground Truth.

Give a score from 0 to 1:

1.0 = Completely correct
0.8 = Mostly correct
0.5 = Partially correct
0.2 = Mostly incorrect
0.0 = Completely incorrect

Return exactly this format:

Score: <number>
Reason: <short explanation>
"""

    response = llm.invoke(prompt)

    return response.content