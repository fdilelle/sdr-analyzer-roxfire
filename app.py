import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="AI SDR Lead Analyzer", layout="centered")

# -------------------------------------------------
# STYLE (bigger fonts)
# -------------------------------------------------

st.markdown("""
<style>

h1 {font-size:40px !important;}
h2 {font-size:30px !important;}
h3 {font-size:24px !important;}
p, label, div {font-size:18px !important;}

textarea {font-size:16px !important;}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "score" not in st.session_state:
    st.session_state.score = None

if "notes" not in st.session_state:
    st.session_state.notes = []

if "company" not in st.session_state:
    st.session_state.company = ""

if "email_text" not in st.session_state:
    st.session_state.email_text = ""

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("🚀 AI SDR Lead Analyzer")

st.write("Website Audit + Outreach Campaign Generator")

st.caption("Built by Fernando A. Di Lelle")

# -------------------------------------------------
# STEP 1
# -------------------------------------------------

st.header("Step 1 — Analyze Website")

url = st.text_input("Paste company website URL")

if st.button("Analyze Website"):

    if url == "":
        st.warning("Please enter a website URL")

    else:

        with st.spinner("Analyzing website..."):

            try:

                r = requests.get(url, timeout=10)
                soup = BeautifulSoup(r.text, "html.parser")
                html = r.text.lower()

                score = 50
                notes = []

                if "form" in html:
                    score += 15
                    notes.append("Lead Capture form detected")

                else:
                    notes.append("No lead capture form detected")

                if "chat" in html:
                    score += 10
                    notes.append("Live chat detected")

                else:
                    notes.append("No live chat detected")

                if "facebook" in html or "instagram" in html:
                    score += 10
                    notes.append("Social marketing detected")

                if "gtag" in html or "googleads" in html:
                    score += 10
                    notes.append("Google Ads tracking detected")

                title = soup.title.string if soup.title else "Company"

                score = min(score, 100)

                st.session_state.analysis_done = True
                st.session_state.score = score
                st.session_state.notes = notes
                st.session_state.company = title

                # IMPORTANT: only set template if email is empty

                if st.session_state.email_text == "":

                    st.session_state.email_text = f"""Subject: 2–3 More Leads for {title}

Hi {{name}},

I reviewed your website and noticed a few opportunities to increase inbound leads.

Many companies today are generating consistent bookings using targeted Google Ads and optimized landing pages.

Would you be open to a quick 10-minute call so I can show you what I found?

Best regards,
"""

            except:

                st.error("Website could not be analyzed")

# -------------------------------------------------
# STEP 2
# -------------------------------------------------

if st.session_state.analysis_done:

    st.header("Step 2 — Lead Conversion Score")

    st.metric("Score", f"{st.session_state.score}/100")

    st.subheader("Marketing Audit")

    for n in st.session_state.notes:
        st.write("•", n)

# -------------------------------------------------
# STEP 3
# -------------------------------------------------

if st.session_state.analysis_done:

    st.header("Step 3 — Edit Outreach Email")

    st.info("{name} will be replaced with the lead name from your uploaded file")

    st.session_state.email_text = st.text_area(
        "Edit email",
        value=st.session_state.email_text,
        height=240
    )

# -------------------------------------------------
# STEP 4
# -------------------------------------------------

if st.session_state.analysis_done:

    st.header("Step 4 — Upload Lead List")

    file = st.file_uploader(
        "Upload CSV or Excel (columns: Company, Email, Name)",
        type=["csv", "xlsx"]
    )

    if file:

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)

        else:
            df = pd.read_excel(file)

        st.write("Preview")

        st.dataframe(df.head())

        df["Email Body"] = st.session_state.email_text

        csv = df.to_csv(index=False)

        st.download_button(
            "Download Campaign CSV",
            csv,
            "outreach_campaign.csv",
            "text/csv"
        )

# -------------------------------------------------
# RESET
# -------------------------------------------------

if st.session_state.analysis_done:

    if st.button("Analyze Another Company"):

        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()