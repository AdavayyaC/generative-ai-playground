import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain, create_history_aware_retriever

from src.prompts.rag_prompt import history_aware_prompt, qa_prompt

load_dotenv()

def create_rag_chain(retriever):

    llm = ChatGroq(
        model="qwen/qwen3.6-27b",
        temperature=0
    )

    # 1. Create a history-aware retriever
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, history_aware_prompt
    )

    # 2. Create the QA chain
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    # 3. Create the final retrieval chain
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return rag_chain