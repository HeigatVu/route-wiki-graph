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
