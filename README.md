# 🛡️ IR-GPT: AI-Driven Incident Response Assistant

AI-driven Incident Response assistant built using RAG, NIST SP 800-61, and NIST CSF mapping. Generates best possible recommended actions.

---

## 🚀 Features
- Local RAG pipeline (Python + Streamlit + ChromaDB + Ollama)
- Offline models (Phi-3, Mistral, Llama3)
- NIST SP 800-61 and CSF alignment
- Structured JSON output for audit and governance

## 🧩 Setup
1. Install dependencies  
   ```bash
   pip install -r requirements.txt
  2. Run Ollama and pull the model  
   ```bash
   ollama pull mistral
   export IRGPT_MODEL="mistral"
💡 You can replace “mistral” with other local models like “phi3:mini” or “llama3:8b”.
3. Launch the app  
   ```bash
   cd app
   streamlit run app.py
Once it starts, open the local URL shown in the terminal — usually http://localhost:8501

📄 Documentation

For deeper understanding:

Engineer’s Guide (PDF)

Portfolio Report (PDF)

🧠 Architecture Overview

IR-GPT uses a Retrieval-Augmented Generation (RAG) design:

Retrieves relevant context from your NIST-based playbooks using ChromaDB

Embeds text via SentenceTransformers

Passes context + user input into a local Ollama LLM

Produces structured recommendations (JSON) and narrative analysis

🧩 Tech Stack

Python, Streamlit, ChromaDB, Ollama

SentenceTransformers for semantic search

NIST SP 800-61 and NIST CSF for mapping response phases

👤 Author

Anirudh Diwakar
Security+ Certified | M.S. Cybersecurity Risk Management | Indiana University
https://www.linkedin.com/in/anirudhdiwakar15/
