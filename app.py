import streamlit as st
import json
import re
from pipeline import analyze
from summarizer import summarize_logs

# ---------- Layout configuration ----------
st.set_page_config(
    page_title="IR-GPT",
    page_icon="🛡️",
    layout="wide",  # makes it full-width for a dashboard feel
    initial_sidebar_state="expanded"
)

# ---------- Header ----------
st.markdown(
    """
    <div style="text-align:center; padding:10px 0;">
        <h1>🛡️ IR-GPT — Incident Response Assistant</h1>
        <p style="color:gray; font-size:16px;">
        Analyze alerts, logs, or incidents using <b>NIST SP 800-61</b> and <b>NIST CSF</b> guidance.<br>
        Paste raw logs, describe your scenario, and indicate if containment is approved.
        </p>
        <hr style="border:0.5px solid #ddd;">
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- Layout: two columns for better spacing ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔹 Optional: Paste Raw Logs for Summarization")
    log_input = st.text_area(
        "Raw Logs",
        height=180,
        placeholder="Paste logs (failed logins, VPN attempts, MFA events, etc.)"
    )
    if log_input.strip():
        log_summary = summarize_logs(log_input)
        st.info(f"Summary: {log_summary}")
    else:
        log_summary = ""

with col2:
    st.subheader("🔹 Incident Scenario")
    query = st.text_area(
        "Alert / Scenario",
        height=180,
        placeholder="Example: Users report multiple failed logins followed by one success..."
    )

# ---------- Approval + Button ----------
st.markdown("---")
center = st.columns([1, 2, 1])[1]
with center:
    approval = st.checkbox("✅ I have approval to take containment actions", value=False)
    submit = st.button("🚀 Analyze Incident", use_container_width=True)
st.markdown("---")

# ---------- Helper: extract JSON cleanly ----------
def extract_json_block(text: str):
    m = re.search(
        r"###RESPONSE_JSON###\s*```json\s*(\{.*?\})\s*```\s*###END_RESPONSE_JSON###",
        text, re.DOTALL | re.IGNORECASE
    )
    if not m:
        m = re.search(r"(\{(?:[^{}]|\{[^{}]*\})*\})\s*$", text.strip(), re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None

# ---------- Run analysis ----------
if submit and query.strip():
    with st.spinner("Analyzing with IR-GPT..."):
        try:
            combined_query = f"{log_summary}\n\n{query}" if log_summary else query
            if not approval:
                combined_query = (
                    "NOTE: containment not approved. "
                    "Provide recommendations limited to detection, verification, and analysis.\n\n"
                    + combined_query
                )

            result = analyze(query=combined_query)
            full_text = result.get("response", "")

            # ----- Narrative section -----
            narrative = re.split(r"###RESPONSE_JSON###", full_text, maxsplit=1, flags=re.IGNORECASE)[0]
            st.subheader("🧭 Proposed Guidance")
            st.write(narrative.strip() or "No narrative provided.")

            # ----- Parsed JSON section -----
            parsed = extract_json_block(full_text)
            if parsed:
                st.subheader("🧩 Structured Fields")
                st.json(parsed)

                ticket_text = parsed.get("notes_for_ticket", "").strip()
                if ticket_text:
                    st.subheader("🗒️ Notes for Ticket")
                    st.code(ticket_text, language="markdown")
                    st.download_button(
                        label="Download ticket summary",
                        data=ticket_text,
                        file_name="ir_ticket_summary.txt",
                        mime="text/plain"
                    )
            else:
                st.info("No structured JSON block detected; narrative shown above.")

            # ----- Sources -----
            sources = result.get("retrieved_sources") or result.get("sources") or []
            if sources:
                st.subheader("📚 Retrieved Sources")
                for s in sources:
                    st.code(s, language="text")

            snippets = result.get("context_snippets") or []
            if snippets:
                st.subheader("🔍 Context Snippets")
                for i, snip in enumerate(snippets, 1):
                    st.code(f"[{i}] {snip}", language="markdown")

        except Exception as e:
            st.error(f"Error: {e}")

else:
    st.info("Enter a scenario and click **Analyze Incident** to begin.")
