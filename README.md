# Generative AI Playground

A hands-on learning repository for exploring Generative AI concepts with LangChain, prompt engineering, document loaders, vector stores, and LLM integrations.


![Python](https://img.shields.io/badge/Python-3.8+-blue) ![LangChain](https://img.shields.io/badge/LangChain-Latest-green) ![License](https://img.shields.io/badge/License-MIT-yellow)


## What this project covers

This repository includes practical examples for:

- Prompt templates and chat history
- Simple and sequential LLM chains
- Document loaders for text, PDF, and web content
- Output parsing with JSON and Pydantic
- Vector stores such as Chroma and FAISS
- LangChain integrations with Groq, Google, Hugging Face, OpenAI, and Anthropic
- Basic structured output and retrieval-based workflows

## Project structure

- [chains](chains) - examples of chain orchestration patterns
- [document_loaders](document_loaders) - text, PDF, and web-based loaders
- [prompts](prompts) - prompt templates and prompt utilities
- [Runnables](Runnables) - runnable chain examples
- [Vector-stores](Vector-stores) - vector database demos
- [structured-output](structured-output) - structured output examples
- [langchain-models](langchain-models) - model provider examples
- [VisionModels](VisionModels) - vision model experiments

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/AdavayyaC/generative-ai-playground.git
cd generative-ai-playground
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root and add your API keys, for example:

```env
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
ANTHROPIC_API_KEY=your_anthropic_key
```

## Notes

This repository is intended for experimentation and learning. Some examples may require API keys and internet access depending on the model provider and loader used.

## Final note

If the AI starts acting like it knows everything, remember: it’s still just a very confident autocomplete with a PhD in vibes.

