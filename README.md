# 🛡️ IR-GPT: AI-Driven Incident Response Assistant

AI-driven Incident Response assistant built using **Retrieval-Augmented Generation (RAG)**, **NIST SP 800-61**, and **NIST CSF** mapping.  
Generates the best possible recommended actions aligned with cybersecurity frameworks.

---

## ⚙️ Setup Instructions

# 1️⃣ Clone the repository
git clone https://github.com/ad15401/IR--GPT.git
cd IR--GPT

# 2️⃣ Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Pull a model using Ollama
ollama pull mistral
# (Optionally, you can use other models like phi3:mini or llama3:8b)

# 5️⃣ Set the model environment variable
export IRGPT_MODEL="mistral"

# 6️⃣ Launch the app
cd app
streamlit run app.py

# When Streamlit starts, open the URL shown in your terminal
# Typically: http://localhost:8501

🧩 Tech Stack
- Python
- Streamlit
- ChromaDB (Vector Database)
- SentenceTransformers
- Ollama (Local LLMs)
- NIST SP 800-61 & NIST CSF

🧠 Architecture Overview
1. Retrieves relevant content from NIST-based playbooks via ChromaDB
2. Embeds text using SentenceTransformers
3. Feeds context + scenario into a local Ollama LLM
4. Produces structured recommendations (JSON) and analyst narrative

🧠 Example Use Case
Scenario:
"Multiple failed logins followed by one success; file permissions modified on host."

IR-GPT retrieves guidance from NIST-aligned playbooks and provides:
- Analysis of event patterns
- Recommended containment and response actions
- Structured JSON fields for incident tracking systems

🧰 Governance & Framework Mapping
- NIST SP 800-61: Detection, Analysis, Containment, Recovery phases
- NIST CSF: Identify, Protect, Detect, Respond, Recover
- Designed for GRC analysts, SOC teams, and IR consultants

👤 Author
Anirudh Diwakar
Security+ Certified | M.S. Cybersecurity Risk Management | Indiana University
LinkedIn: https://www.linkedin.com/in/anirudhdiwakar15/
Email: anirudhdiwakar15@gmail.com

🖼️ Demo
# Screenshot for reference:
<img width="1901" height="963" alt="image" src="https://github.com/user-attachments/assets/0a7caaa6-d104-419c-a8bf-1d37eea950b3" />

⭐ Contribute
# Pull requests and feedback are welcome!
# If this project helps you, consider starring ⭐ the repository.


