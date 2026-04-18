```text
┌────────────────────────────┐
│       ROUTE WIKI GRAPH       │
└────────────────────────────┘
               │
               ▼
┌────────────────────────────┐
│  Input: user question      │
│ (natural language)         │
└────────────────────────────┘
               │
               ▼
┌────────────────────────────┐
│  Route.py                  │
│                            │
│ 1) Parse question          │
│ 2) Route to...             │
│    - atlas.md (summary)    │
│    - vault/ (specific)     │
│ 3) Call LLM                │
│ 4) Generate response       │
└────────────────────────────┘
               │
               ▼
┌────────────────────────────┐
│  Output:                  │
│ - Direct answer            │
│ - Citations                │
│ - "See also" links         │
└────────────────────────────┘
```

# Background

The Route-Wiki Graph is a tool that allows you to query your Obsidian vault with natural language questions.
I build this to support navigate my notes and answer my questions based on all my knowledge base, which was build by my [wiki-llm-graph-knowledge](https://github.com/HeigatVu/wiki-llm-graph-knowledge)

# How to use it

```bash
uv run route.py "What is the best way to learn quantum computing?"
```

- It will first check its internal "Knowledge Atlas" (atlas.md)
- If the answer is not there, it will search your entire vault for relevant notes
- It uses an LLM (Ollama or Gemini) to understand your question and generate a clear answer
- Citations are automatically included so you know which notes were used