import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="AI SDR Analyzer", layout="centered")

# --------------------------
# SESSION STATE INIT
# --------------------------

defaults = {
    "step": 1,
    "analysis_done": False,
    "score": None,
    "notes": [],
    "company": "",
    "email_text": ""
}

for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --------------------------
# HEADER
# --------------------------

st.title("AI SDR Lead Analyzer")
st.write("Website Audit + Outreach Generator")

# --------------------------
# STEP NAVIGATION
# --------------------------

st.sidebar.title("Workflow")

if st.sidebar.button("1 Analyze Website"):
    st.session_state.step = 1

if st.sidebar.button("2 Marketing Audit"):
    st.session_state.step = 2

if st.sidebar.button("3 Edit Email"):
    st.session_state.step = 3

if st.sidebar.button("4 Upload Leads"):
    st.session_state.step = 4

step = st.session_state.step

# --------------------------
# STEP 1 ANALYZE
# --------------------------

if step == 1:

    st.header("Step 1 — Analyze Website")

    url = st.text_input("Website URL")

    if st.button("Analyze"):

        try:

            r = requests.get(url, timeout=10)
            html = r.text.lower()

            soup = BeautifulSoup(r.text, "html.parser")

            score = 50
            notes = []

            if "form" in html:
                score += 15
                notes.append("Lead capture form detected")

            if "chat" in html:
                score += 10
                notes.append("Live chat detected")

            if "facebook" in html or "instagram" in html:
                score += 10
                notes.append("Social media detected")

            if "gtag" in html or "googleads" in html:
                score += 10
                notes.append("Google Ads tracking detected")

            score = min(score,100)

            company = soup.title.string if soup.title else "Company"

            st.session_state.score = score
            st.session_state.notes = notes
            st.session_state.company = company
            st.session_state.analysis_done = True

            if st.session_state.email_text == "":

                st.session_state.email_text = f"""Subject: Quick idea for {company}

Hi {{name}},

I reviewed your website and noticed a few opportunities to increase inbound leads.

Many companies today are generating more leads using optimized landing pages and targeted Google Ads campaigns.

Would you be open to a quick 10-minute call so I can show you what I found?

Best regards,
"""

            st.success("Analysis complete")

        except:
            st.error("Could not analyze website")

# --------------------------
# STEP 2 AUDIT
# --------------------------

if step == 2:

    st.header("Step 2 — Marketing Audit")

    if not st.session_state.analysis_done:
        st.warning("Run the website analysis first")

    else:

        st.metric("Lead Conversion Score", f"{st.session_state.score}/100")

        for n in st.session_state.notes:
            st.write("•", n)

# --------------------------
# STEP 3 EMAIL EDITOR
# --------------------------

if step == 3:

    st.header("Step 3 — Edit Outreach Email")

    if not st.session_state.analysis_done:
        st.warning("Run the analysis first")

    else:

        st.session_state.email_text = st.text_area(
            "Edit email template",
            value=st.session_state.email_text,
            height=250
        )

# --------------------------
# STEP 4 LEADS
# --------------------------

if step == 4:

    st.header("Step 4 — Upload Lead List")

    if not st.session_state.analysis_done:
        st.warning("Run the analysis first")

    else:

        file = st.file_uploader("Upload CSV or Excel (Name, Email, Company)")

        if file:

            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)

            st.subheader("Lead Preview")

            st.dataframe(df.head())

            emails = []

            for _,row in df.iterrows():

                body = st.session_state.email_text.replace(
                    "{name}",
                    str(row["Name"])
                )

                emails.append(body)

            df["Generated Email"] = emails

            st.subheader("Campaign Preview")

            st.dataframe(df.head())

            csv = df.to_csv(index=False)

            st.download_button(
                "Download Campaign CSV",
                csv,
                "campaign.csv",
                "text/csv"
            )

# --------------------------
# RESET
# --------------------------

st.sidebar.write("---")

if st.sidebar.button("Reset App"):

    for k in list(st.session_state.keys()):
        del st.session_state[k]

    st.rerun()