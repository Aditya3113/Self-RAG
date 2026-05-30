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

## Getting Started

### Prerequisites

- Python 3.9+
- An OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/Aditya3113/Self-RAG.git
cd Self-RAG

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory and add your API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Run

```bash
python main.py
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `langgraph` | Stateful graph orchestration for the RAG loop |
| `langchain` | Core LLM chains and document abstractions |
| `langchain-openai` | OpenAI LLM and embeddings integration |
| `langchain_community` | Community loaders and retrievers |
| `langchainhub` | Pull prompts from LangChain Hub |
| `chromadb` | Local vector store for document retrieval |
| `langchain-text-splitters` | Chunk documents for embedding |
| `beautifulsoup4` | Web document loading/parsing |
| `tiktoken` | Token counting for OpenAI models |
| `python-dotenv` | Load environment variables from `.env` |

---

## Key Concepts

**Self-RAG** (Asai et al., 2023) introduces *reflection tokens* that allow a model to decide when to retrieve, assess document relevance, and verify that its generated answer is factually grounded. This implementation approximates that framework using LLM-based graders at each decision point instead of fine-tuned reflection tokens.

The `recursion_limit` parameter in `main.py` controls how many times the graph can loop before halting — useful for preventing infinite rewrite cycles when no relevant documents exist.

---

## References

- [Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection](https://arxiv.org/abs/2310.11511) — Asai et al., 2023
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Self-RAG Tutorial](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_self_rag/)