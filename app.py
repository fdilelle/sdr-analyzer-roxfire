import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io

st.set_page_config(page_title="AI SDR Lead Analyzer", layout="centered")

# ---------------------------
# STYLE
# ---------------------------

st.markdown("""
<style>

body {
    font-size:18px;
}

h1 {
    font-size:40px !important;
}

h2 {
    font-size:28px !important;
}

h3 {
    font-size:24px !important;
}

textarea {
    font-size:16px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# SESSION STATE
# ---------------------------

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "email_text" not in st.session_state:
    st.session_state.email_text = ""

# ---------------------------
# HEADER
# ---------------------------

st.title("🚀 AI SDR Lead Analyzer")
st.write("Website Audit + Outreach Campaign Generator")
st.caption("Built by Fernando A. Di Lelle")

# ---------------------------
# STEP 1
# ---------------------------

st.header("Step 1 — Analyze Website")

url = st.text_input("Paste company website URL")

analyze = st.button("Analyze Website")

# ---------------------------
# WEBSITE ANALYSIS
# ---------------------------

def analyze_website(url):

    score = 50
    notes = []

    try:
        r = requests.get(url, timeout=8)
        soup = BeautifulSoup(r.text, "html.parser")
        html = r.text.lower()

        if "form" in html:
            score += 15
            notes.append("Lead Capture: Yes")
        else:
            notes.append("Lead Capture: No")

        if "chat" in html:
            score += 10
            notes.append("Live Chat: Yes")
        else:
            notes.append("Live Chat: No")

        if "facebook" in html or "instagram" in html:
            score += 10
            notes.append("Meta Ads / Social: Detected")

        if "gtag" in html or "googleads" in html:
            score += 10
            notes.append("Google Ads Tracking: Detected")

        title = soup.title.string if soup.title else "Company"

    except:
        title = "Company"
        notes.append("Website could not be fully analyzed")

    score = min(score,100)

    return score, notes, title


# ---------------------------
# RUN ANALYSIS
# ---------------------------

if analyze and url:

    score, notes, title = analyze_website(url)

    st.session_state.analysis_done = True
    st.session_state.score = score
    st.session_state.notes = notes
    st.session_state.company = title


    email_template = f"""Subject: 2-3 More Roofing Leads for {title}

Hi there,

I recently reviewed your website and noticed there may be opportunities to increase inbound leads.

Many roofing companies today are generating consistent bookings using targeted Google Ads and optimized landing pages.

Based on what I saw, there are a few quick improvements that could increase conversions significantly.

Would you be open to a quick 10-minute call so I can show you what I found?

Best,
"""

    st.session_state.email_text = email_template


# ---------------------------
# STEP 2 RESULTS
# ---------------------------

if st.session_state.analysis_done:

    st.success("Analysis completed")

    st.header("Step 2 — Lead Conversion Score")

    st.metric("Lead Conversion Score", f"{st.session_state.score}/100")

    st.subheader("Marketing Audit")

    for n in st.session_state.notes:
        st.write("•", n)


# ---------------------------
# STEP 3 EMAIL EDITOR
# ---------------------------

if st.session_state.analysis_done:

    st.header("Step 3 — Edit Outreach Email")

    st.write("You can customize the email before generating the campaign")

    email_text = st.text_area(
        "Edit email text",
        value=st.session_state.email_text,
        height=220,
        key="email_editor"
    )

    st.session_state.email_text = email_text


# ---------------------------
# STEP 4 LEAD LIST
# ---------------------------

if st.session_state.analysis_done:

    st.header("Step 4 — Upload Lead List")

    st.write("Upload CSV or Excel with columns: Company, Email, Name")

    file = st.file_uploader("Upload Lead File", type=["csv","xlsx"])


    if file:

        if file.name.endswith("csv"):
            df = pd.read_csv(file)

        else:
            df = pd.read_excel(file)

        st.write("Preview of uploaded leads:")
        st.dataframe(df.head())


        df["Email Body"] = st.session_state.email_text

        csv = df.to_csv(index=False)

        st.download_button(
            "Download Personalized Email Campaign",
            csv,
            "outreach_campaign.csv",
            "text/csv"
        )


# ---------------------------
# RESET BUTTON
# ---------------------------

if st.session_state.analysis_done:

    if st.button("Analyze Another Company"):

        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()