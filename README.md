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

📄 Documentation
docs/
├── IR-GPT_Engineers_Guide.pdf
└── IR-GPT_Portfolio_Report.pdf

👤 Author
Adiwakar
Security+ Certified | M.S. Cybersecurity Risk Management | Indiana University
LinkedIn: https://linkedin.com/in/adiwakar
Email: adiwakar@example.com (optional)

🖼️ Demo
# Add a screenshot of your Streamlit interface for better visibility:
![IR-GPT Demo](docs/IR-GPT-Demo.png)

⭐ Contribute
# Pull requests and feedback are welcome!
# If this project helps you, consider starring ⭐ the repository.


