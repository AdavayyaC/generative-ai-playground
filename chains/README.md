# LangChain LCEL Implementation Patterns

This repository contains reference implementations of LangChain Expression Language (LCEL). The objective is to demonstrate how to architect LLM workflows using functional composition instead of imperative code. These patterns are model-agnostic and focus on the flow of data through prompts, models, and output parsers.

---

## Technical Overview
LCEL utilizes the pipe operator (`|`) to instantiate a `Runnable` sequence. This approach provides built-in support for streaming, async operations, and observability.

### 1. Basic Chain (`simple_chain.py`)
This represents the atomic unit of any LangChain application. It follows a strictly linear execution path.


* **Logic Flow:** Input Dictionary -> `PromptTemplate` -> `BaseChatModel` -> `StrOutputParser`.
* **Engineering Goal:** To establish a baseline for connectivity between the application and the LLM provider.
* **Visualization:** The `.get_graph().print_ascii()` method is used here to verify the directed acyclic graph (DAG) structure.

### 2. Sequential Chain (`sequential_chain.py`)
A multi-stage pipeline where the output of a preceding component serves as the input for the subsequent component.

* **Logic Flow:** `Chain(A) | Chain(B)`.
* **Engineering Goal:** To handle complex tasks that require multiple reasoning steps or "Chain of Thought" processing where the context must be refined over iterations.
* **Example Implementation:** Generating a technical report and then piping that full text into an extraction prompt to identify key metrics.

### 3. Parallel Chain (`parallel_chain.py`)
Utilizes `RunnableParallel` to execute multiple independent operations concurrently.

* **Logic Flow:** Input -> `{Task_A, Task_B}` -> Merging Node -> Final Output.
* **Engineering Goal:** Reducing latency. By running independent tasks (e.g., summary generation and quiz generation) in parallel, the total execution time is limited by the slowest branch rather than the sum of all branches.
* **Final Aggregation:** A final prompt is used to synthesize the parallel outputs into a single cohesive document.

### 4. Conditional Chain (`conditional_chain.py`)
Implements logic-based routing within the chain architecture.

* **Logic Flow:** `Classifier -> RunnableBranch(Condition_1, Condition_2, Default)`.
* **Engineering Goal:** To implement a "Router" pattern. This ensures that the system handles different types of input data with specialized sub-chains, improving accuracy and reducing token waste.
* **Schema Enforcement:** Uses `PydanticOutputParser` to ensure the classifier returns a structured object (JSON), allowing the branching logic to evaluate attributes programmatically.

---
## System Visualization
For all included scripts, the execution graph can be inspected using the following method to ensure the architecture matches the design:
```python
chain.get_graph().print_ascii()