# IR-GPT (Incident Response GPT) — Starter Kit

A free, open‑source starter that helps you build an AI‑assisted Incident Response companion using **Ollama + LangChain + Streamlit**.

## What you get
- 🧠 **System prompt** and **chain design** for IR workflows (triage → analysis → containment → recovery → post‑incident).
- 📚 **RAG** over your local playbooks and procedures (add Markdown/PDF/TXT to `data/playbooks/`).
- 🧪 **Evaluation checklist** and sample scenarios to test your assistant.
- 💻 **Streamlit UI** for a simple web app demo.

## Quick Start (Local, $0)
1) Install prerequisites:
```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: download Ollama from the official site and run the installer
```

2) Pull a small, free LLM (choose one):
```bash
ollama pull phi3:mini
# or
ollama pull mistral
# or
ollama pull llama3:8b
```

3) Create a Python venv and install deps:
```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

4) Add your IR docs:
- Put Markdown/TXT/PDF playbooks into `data/playbooks/`.
- Put sample logs into `data/logs/` (JSONL or TXT).

5) Run the app:
```bash
streamlit run app/app.py
```

---

## Folder Structure
```
ir-gpt-starter/
├─ app/
│  ├─ app.py                # Streamlit UI
│  ├─ pipeline.py           # RAG + Orchestration
│  ├─ prompts/
│  │  ├─ system_ir.md       # System prompt
│  │  └─ style_guardrails.md
├─ data/
│  ├─ playbooks/            # Put your IR playbooks, runbooks, policies here
│  ├─ logs/                 # Put .jsonl / .txt logs here (sample included)
│  └─ examples/             # Prebuilt scenarios
├─ notebooks/               # Optional experimentation
├─ requirements.txt
└─ README.md
```

## Evaluation (fast)
Use `data/examples/scenario_phishing.json` to simulate an alert. In the UI:
- Paste a suspicious email/log line, click **Analyze**.
- The app will retrieve relevant playbook snippets + recommend steps.

Score yourself on:
- **Relevance** (right playbooks pulled?)
- **Actionability** (clear next steps?)
- **Safety** (no risky/irreversible guidance)
- **Traceability** (citations to sources)

## Notes
- This kit is intentionally lightweight. Improve it by adding better embeddings, tools, and more granular chains.
- Keep sensitive data off this machine. Treat logs as synthetic or sanitized.
- You can deploy the Streamlit app on Streamlit Community Cloud for free.
