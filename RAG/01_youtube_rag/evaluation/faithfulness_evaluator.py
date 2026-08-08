from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


def evaluate_faithfulness(context, answer):

    prompt = f"""
You are a strict RAG faithfulness evaluator.

Your ONLY job is to check whether the claims in the RAG Answer
are supported by the Retrieved Context.

Do NOT use:
- your own knowledge
- outside information
- the Ground Truth
- assumptions
- common knowledge

Retrieved Context:
------------------
{context}
------------------

RAG Answer:
------------------
{answer}
------------------

Evaluate the answer using these rules:

1. Break the RAG Answer into its important factual claims.
2. Check every claim against the Retrieved Context.
3. A claim is supported ONLY if the Retrieved Context directly
   supports it.
4. If the answer adds information that is not present in the
   Retrieved Context, treat that claim as unsupported.
5. Do not give credit just because a claim may be factually true
   in the real world.
6. If an answer says "the context does not explain..." that is
   supported only if the context actually fails to explain it.

Scoring:

1.0 = All important claims are supported.
0.8 = Most claims are supported, with minor unsupported details.
0.5 = Some important claims are supported and some are unsupported.
0.2 = Most important claims are unsupported.
0.0 = The answer is not supported by the retrieved context.

Return EXACTLY:

Score: <number>

Supported Claims:
- <claim>
- <claim>

Unsupported Claims:
- <claim>
- <claim>

Reason:
<short explanation>
"""

    response = llm.invoke(prompt)

    return response.content