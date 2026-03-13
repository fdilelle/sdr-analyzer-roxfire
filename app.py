import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="AI SDR Lead Analyzer", layout="centered")

# -----------------------------
# STYLE
# -----------------------------

st.markdown("""
<style>

h1 {font-size:38px}
h2 {font-size:28px}
p, label {font-size:18px}

textarea {font-size:16px}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE INIT
# -----------------------------

defaults = {
    "analysis_done": False,
    "score": None,
    "notes": [],
    "company": "",
    "email_text": "",
    "email_editor": "",
}

for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------
# HEADER
# -----------------------------

st.title("🚀 AI SDR Lead Analyzer")

st.write("Website Audit + AI Outreach Generator")

# -----------------------------
# STEP 1
# -----------------------------

st.header("Step 1 — Analyze Website")

url = st.text_input("Website URL")

if st.button("Analyze Website"):

    try:

        r = requests.get(url, timeout=10)
        html = r.text.lower()

        soup = BeautifulSoup(r.text, "html.parser")

        score = 50
        notes = []

        if "form" in html:
            score += 15
            notes.append("Lead capture form detected")
        else:
            notes.append("No lead capture form detected")

        if "chat" in html:
            score += 10
            notes.append("Live chat detected")

        if "facebook" in html or "instagram" in html:
            score += 10
            notes.append("Social marketing detected")

        if "gtag" in html or "googleads" in html:
            score += 10
            notes.append("Google Ads tracking detected")

        score = min(score,100)

        company = soup.title.string if soup.title else "Company"

        st.session_state.analysis_done = True
        st.session_state.score = score
        st.session_state.notes = notes
        st.session_state.company = company

        if st.session_state.email_text == "":
            template = f"""Subject: Quick idea for {company}

Hi {{name}},

I was reviewing your website and noticed a few opportunities to increase inbound leads.

Many companies like yours are generating consistent bookings using optimized landing pages and targeted Google Ads campaigns.

Would you be open to a quick 10-minute call so I can show you what I found?

Best regards,
"""

            st.session_state.email_text = template
            st.session_state.email_editor = template

    except:
        st.error("Could not analyze website")

# -----------------------------
# STEP 2
# -----------------------------

if st.session_state.analysis_done:

    st.header("Step 2 — Marketing Score")

    st.metric("Lead Conversion Score", f"{st.session_state.score}/100")

    for n in st.session_state.notes:
        st.write("•", n)

# -----------------------------
# STEP 3
# -----------------------------

if st.session_state.analysis_done:

    st.header("Step 3 — Edit Outreach Email")

    def update_email():
        st.session_state.email_text = st.session_state.email_editor

    st.text_area(
        "Edit your email",
        key="email_editor",
        height=220,
        on_change=update_email
    )

# -----------------------------
# STEP 4
# -----------------------------

if st.session_state.analysis_done:

    st.header("Step 4 — Upload Lead List")

    file = st.file_uploader("Upload CSV or Excel (columns: Name, Email, Company)")

    if file:

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.subheader("Lead Preview")

        st.dataframe(df.head())

        emails = []

        for _,row in df.iterrows():

            body = st.session_state.email_text.replace("{name}",str(row["Name"]))

            emails.append(body)

        df["Generated Email"] = emails

        st.subheader("Campaign Preview")

        st.dataframe(df.head())

        csv = df.to_csv(index=False)

        st.download_button(
            "Download Campaign File",
            csv,
            "campaign.csv",
            "text/csv"
        )

# -----------------------------
# RESET
# -----------------------------

if st.session_state.analysis_done:

    if st.button("Start New Analysis"):

        for k in list(st.session_state.keys()):
            del st.session_state[k]

        st.rerun()