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

Launch the app

cd app
streamlit run app.py
Open the local link shown in the terminal (usually http://localhost:8501).

