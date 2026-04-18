import os
import sys
from pathlib import Path

import ollama

ROOT = Path(__file__).parent
ATLAS_FILE = ROOT / "ATLAS.md"

# Load .env from root
env_path = ROOT / ".env"

if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip().strip("'\"")

def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def call_local_llm(prompt: str) -> str:
    """Try Ollama first."""
    model = os.getenv("LOCAL_MODEL", "llama3.2")
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False
    }).encode("utf-8")

    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        result = json.loads(response.read().decode("utf-8"))
        return result["response"]

def call_gemini_llm(prompt: str) -> str:
    """Fallback to Gemini if Ollama is not running."""
    try:
        import google.generativeai as genai
    except ImportError:
        print("Error: pip install google-generativeai")
        sys.exit(1)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set")
        sys.exit(1)

    genai.configure(api_key=api_key)
    model_name = os.getenv("LLM_MODEL", "gemini-2.0-flash")
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

def call_llm(prompt: str) -> str:
    """Use local LLM, fall back to Gemini if unavailable."""
    use_local = os.getenv("USE_LOCAL_LLM", "true").lower() == "true"

    if use_local:
        try:
            return call_local_llm(prompt)
        except Exception as e:
            print(f"  [warn] Ollama unavailable ({e}), falling back to Gemini...")
            return call_gemini_llm(prompt)
    else:
        return call_gemini_llm(prompt)

def route(question: str):
    atlas = read_file(ATLAS_FILE)
    if not atlas:
        print("ATLAS.md not found. Run: python update_atlas.py first")
        sys.exit(1)

    prompt = f"""You are a knowledge navigator for a personal wiki system.
The user has multiple knowledge vaults. Your job is ONLY to guide 
them to the right vault — do NOT answer the question yourself.

Here is the registry of all available vaults:
{atlas}

User question: "{question}"

Respond in this exact format:

## Where to go
- **Primary vault:** <vault_name> — <one sentence why>
- **Secondary vault (if relevant):** <vault_name> — <one sentence why>

## What to search for once inside
- <specific concept or keyword 1>
- <specific concept or keyword 2>
- <specific concept or keyword 3>

## Suggested query to run locally
`query: <refined version of the question suited for that vault>`

Keep your response short and direct. 
Do not answer the question itself.
"""

    print("\n" + "=" * 50)
    print(f"Question: {question}")
    print("=" * 50)
    result = call_llm(prompt)
    print(result)
    print("=" * 50 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python route.py "your question here"')
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    route(question)