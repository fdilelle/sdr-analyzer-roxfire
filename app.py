import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

st.set_page_config(page_title="AI SDR Lead Analyzer", page_icon="🚀")

st.title("AI SDR Lead Analyzer")
st.markdown("Website Audit + Outreach Generator")
st.caption("Built by Fernando A. Di Lelle")

# ================= SIDEBAR =================

with st.sidebar:

    st.header("Your Information")

    name = st.text_input("Name", "Fernando A. Di Lelle")
    email = st.text_input("Email", "fdilelle@gmail.com")
    phone = st.text_input("Phone", "+54 911 6926 0805")
    linkedin = st.text_input("LinkedIn", "linkedin.com/in/fdilelle-consultant")

    st.header("Outreach Settings")

    industry = st.selectbox(
        "Industry",
        ["Roofing","HVAC","Med Spa","Cleaning Services","Other"]
    )

    outreach_style = st.selectbox(
        "Outreach Style",
        ["Bold","Professional","Friendly"]
    )

# ================= WEBSITE INPUT =================

url = st.text_input(
    "Paste company website",
    placeholder="https://www.example.com"
)

if st.button("Analyze Website") and url:

    try:

        headers = {"User-Agent":"Mozilla/5.0"}
        response = requests.get(url,headers=headers,timeout=15)

        soup = BeautifulSoup(response.text,"html.parser")

        title = soup.title.string.strip() if soup.title else "Company"
        text = soup.get_text().lower()

        # ===== Detection =====

        lead_keywords = ["quote","estimate","book","schedule"]
        chat_keywords = ["livechat","tawk","intercom","drift"]
        ads_keywords = ["gtag","google ads","facebook pixel","fbq"]

        has_lead = any(k in text for k in lead_keywords)
        has_chat = any(k in text for k in chat_keywords)
        has_ads = any(k in text for k in ads_keywords)

        meta = soup.find("meta",attrs={"name":"description"})
        h1 = soup.find("h1")

        has_meta = meta is not None
        has_h1 = h1 is not None

        # ===== Score =====

        score = 100

        if not has_lead: score -= 30
        if not has_chat: score -= 20
        if not has_meta: score -= 15
        if not has_ads: score -= 10
        if not has_h1: score -= 5

        st.success("Analysis completed")

        st.metric("Lead Conversion Score",f"{score}/100")

        # ================= AUDIT =================

        st.subheader("Marketing Audit")

        audit = f"""
Lead Capture: {"Yes" if has_lead else "No"}
Live Chat: {"Yes" if has_chat else "No"}
Meta Description: {"Yes" if has_meta else "No"}
H1 Tag: {"Yes" if has_h1 else "No"}
Ads Tracking: {"Detected" if has_ads else "Not detected"}

Overall Conversion Score: {score}/100
"""

        st.text_area("Audit Summary",audit,height=200)

        # ================= EMAIL GENERATION =================

        st.subheader("Generated Outreach Email")

        if outreach_style == "Bold":

            cta="Reply YES and I will send two available times for a quick 15-minute strategy call."

        elif outreach_style=="Professional":

            cta="Would you be open to a short strategy conversation next week?"

        else:

            cta="Would you be open to a quick chat about generating more booked jobs?"

        subject=f"2-3x More {industry} Leads for {title}?"

        email_template=f"""
Subject: {subject}

Hi {{name}},

I recently reviewed your website and noticed there may be opportunities to increase inbound leads.

Many companies in the {industry.lower()} industry are generating more bookings using targeted Google Ads and optimized landing pages.

{cta}

Best regards,
{name}
{email}
{phone}
{linkedin}
"""

        edited_email = st.text_area(
            "Edit the email before generating the campaign",
            email_template,
            height=300
        )

        # ================= LEAD LIST =================

        st.subheader("Upload Lead List")

        uploaded_file = st.file_uploader(
            "Upload Excel or CSV file with columns: Company, Email, Name",
            type=["csv","xlsx"]
        )

        if uploaded_file:

            if uploaded_file.name.endswith(".csv"):

                df = pd.read_csv(uploaded_file)

            else:

                df = pd.read_excel(uploaded_file)

            st.write("Preview of uploaded leads")

            st.dataframe(df)

            if st.button("Generate Outreach Campaign"):

                emails=[]

                for _,row in df.iterrows():

                    message = edited_email.replace("{name}",str(row["Name"]))

                    emails.append(message)

                df["Personalized Email"] = emails

                st.success("Campaign generated")

                st.dataframe(df)

                csv = df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    "Download Campaign CSV",
                    csv,
                    file_name="outreach_campaign.csv",
                    mime="text/csv"
                )

    except Exception as e:

        st.error(f"Error analyzing site: {e}")

else:

    st.info("Paste a website URL to start the analysis")

st.caption("AI SDR Prospecting Tool")
