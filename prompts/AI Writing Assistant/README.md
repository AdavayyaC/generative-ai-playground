# AI Writing Assistant

A prompt-engineered Streamlit capstone. It uses three explicit stages:

1. **Brief extractor** turns a rough description into a validated JSON brief.
2. **Content generator** writes a blog, email, report, or social post using the brief.
3. **Quality checker** scores clarity, audience fit, brief coverage, and voice consistency.

The system prompt includes three few-shot examples. No fine-tuning, RAG, or document retrieval is used.

## Run

From this directory:

```powershell
pip install -r requirements.txt
streamlit run app.py
```

Add the Groq API key to the repository `.env` file:

```env
GROQ_API_KEY=your_groq_key
```

The assistant always uses Groq's `openai/gpt-oss-120b` model. Temperature and
length remain adjustable in the sidebar.

The generated JSON can be downloaded from the results panel.