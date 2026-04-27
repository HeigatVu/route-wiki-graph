# Multi-Vault Knowledge Router

A specialized routing system designed to manage and navigate across multiple, independent knowledge vaults. Using natural language queries, it directs you to the most relevant vault and provides suggested queries for deeper exploration.

## Architecture

The system operates on a "Hub and Spoke" model:

1.  **The Router (Hub):** This repository. It maintains a central registry (`ATLAS.md`) of all available knowledge.
2.  **The Vaults (Spokes):** Independent wiki repositories located in the `vaults/` directory.

### Dependency: Vault Schema
For the router to index a vault, it **must** follow the schema defined in the [wiki-llm-graph-knowledge](https://github.com/HeigatVu/wiki-llm-graph-knowledge) repository.

The router specifically looks for:
- `30_wiki/overview.md`: A high-level summary of the vault's content.
- `WIKI_STATUS.md`: Automatically generated statistics and last-action timestamps.

## Setup

### Prerequisites
- [uv](https://github.com/astral-sh/uv) installed.
- Access to an LLM (Ollama running `llama3.2` or a Gemini API key).

### Installation

1.  **Clone this repository:**
    ```bash
    git clone <this-repo-url>
    cd Obsidian-llm-wiki
    ```

2.  **Configure Environment:**
    ```bash
    cp .env.example .env
    # Edit .env with your LOCAL_MODEL or GEMINI_API_KEY
    ```

3.  **Add Your Vaults:**
    Clone or move your knowledge vaults into the `vaults/` directory.
    ```bash
    # Example
    git clone git@github.com:HeigatVu/wiki-llm-graph-knowledge.git vaults/my-vault
    ```

4.  **Initialize the Atlas:**
    The router uses a central index to route questions efficiently.
    ```bash
    python update_atlas.py
    ```

## Usage

### Routing a Question
To find which vault contains the answer to your question:
```bash
python route.py "Your question here"
```

### Deep Query
Once the router identifies the correct vault (e.g., `vaults/alzheimer`), navigate there and use its local tools:
```bash
cd vaults/alzheimer
uv run main.py query "Your detailed question"
```

