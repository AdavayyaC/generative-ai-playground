# Structured Output with AI using TypedDict, Pydantic, and JSON Schema

This repository was created to understand how **structured output** can be used in AI-based applications using Python.

When working with **Large Language Models (LLMs)**, the model usually returns responses as plain text. While this is fine for chat-based usage, it becomes a problem in real applications where programs expect data in a **fixed and predictable format**.

To solve this issue, this project explores different ways to **define and enforce structure** on AI outputs using:

- TypedDict  
- Pydantic  
- JSON Schema  

All examples are implemented using **LangChain with Groq LLaMA models**.

---

## Why Structured Output Matters in AI

In basic AI usage:

- The model returns free-form text  
- The output format may change anytime  
- Parsing text manually is unreliable  

However, in real-world applications such as:

- Sentiment analysis  
- Review summarization  
- Information extraction  
- API-based AI systems  

we need **clean and consistent JSON output**.

Structured output helps make AI responses:

- Predictable  
- Machine-readable  
- Easier to validate  
- Safer to use in code  

---

## Methods Used in This Project

### 1. TypedDict for Structured Output

`TypedDict` is used to define the **expected structure** of the AI output.

**Key points:**

- Simple and lightweight  
- Improves clarity of expected fields  
- Beginner-friendly  

**AI use case:**

- When you want the LLM to return JSON  
- When strict validation is not required  
- Useful for learning and prototyping  

**Limitation:**

- No runtime validation  
- Incorrect data may still pass through  

---

### 2. Pydantic for Structured Output

Pydantic is used for **runtime validation** of AI outputs.

**Key points:**

- Validates data types  
- Supports optional and required fields  
- Raises errors for invalid output  

**AI use case:**

- Production-level AI applications  
- APIs consuming AI-generated data  
- When incorrect output must be rejected  

This is the **most practical and recommended approach** for real-world projects.

---

### 3. JSON Schema for Structured Output

JSON Schema defines structure using a **standard JSON format**.

**Key points:**

- Language-independent  
- Can be shared across systems  
- Provides strict control over output format  

**AI use case:**

- Large-scale systems  
- Multiple services using the same schema  
- When strict structure enforcement is required  

This approach is more verbose but very flexible.

---

## AI Use Case Implemented

The AI is given a **product review** as input and asked to return structured information such as:

- Summary  
- Sentiment  
- Key themes  
- Pros  
- Cons  

Instead of returning plain text, the AI returns a **JSON object** that follows the defined structure.

This makes it easy to:

- Store results in a database  
- Display data in a user interface  
- Use the output for further processing  

---
 ## Technologies Used

- Python  
- LangChain  
- Groq (LLaMA 3.1)  
- Pydantic  
- python-dotenv  

---
