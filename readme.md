# Self-RAG — Self-Reflective Retrieval-Augmented Generation

A Python implementation of the **Self-RAG** framework using **LangGraph**, where an LLM dynamically retrieves, generates, and critiques its own outputs through a stateful graph-based pipeline.

---

## What is Self-RAG?

Traditional RAG pipelines blindly retrieve documents and pass them to an LLM — regardless of whether those documents are actually relevant. **Self-RAG** takes a smarter approach: it grades the retrieved documents, evaluates the generated answer, and can rewrite the query and retry if the result isn't good enough.

This implementation uses **LangGraph** to model the full Self-RAG loop as a directed graph with conditional edges, making the decision flow transparent and easy to extend.

---

## How It Works

The system runs a query through the following stateful pipeline:

```
User Question
      │
      ▼
 [Retrieve] ──→ Fetch relevant documents from ChromaDB vector store
      │
      ▼
 [Grade Documents] ──→ Filter out irrelevant docs using an LLM grader
      │
      ├── Relevant docs found ──→ [Generate] ──→ [Grade Generation]
      │                                                  │
      │                                    ┌────────────┴────────────┐
      │                                    ▼                         ▼
      │                             Supported &               Not supported /
      │                             answers question ──→ ✅   off-topic ──→ 🔄
      │
      └── No relevant docs ──→ [Rewrite Query] ──→ loop back to Retrieve
                                     (up to recursion limit)
```

**Key decision nodes:**

- **Document Grader** — Scores each retrieved document for relevance to the question.
- **Answer Grader** — Checks if the generated answer is grounded in the retrieved documents (no hallucinations).
- **Question Grader** — Checks if the generation actually addresses the user's question.
- **Query Rewriter** — Rewrites the question to improve retrieval if initial results are poor.

---

## Project Structure

```
Self-RAG/
├── main.py              # Entry point — runs two demo scenarios
├── requirements.txt     # Python dependencies
└── src/
    └── graph.py         # LangGraph graph definition (nodes, edges, state)
```

---

## Demo Scenarios

Running `main.py` demonstrates two cases:

| Scenario | Query | Expected Behavior |
|---|---|---|
| 1 | *"How to improve relationships"* | Finds relevant docs → generates a grounded answer |
| 2 | *"How to cook a bagel?"* | No relevant docs found → rewrites query repeatedly → gracefully stops at recursion limit |

---