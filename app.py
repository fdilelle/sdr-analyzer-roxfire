import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from datetime import date

st.set_page_config(page_title="SDR Lead Analyzer - Roxfire", page_icon="🚀", layout="centered")

st.title("🔍 SDR Lead Analyzer")
st.markdown("**Pre-Application Task Generator** – Roxfire Marketing Agency")
st.caption("Fernando A. Di Lelle • 100% reutilizable")

# ================== SIDEBAR ==================
with st.sidebar:
    st.header("Tus datos")
    nombre = st.text_input("Nombre", "Fernando A. Di Lelle")
    email = st.text_input("Email", "fdilelle@gmail.com")
    phone = st.text_input("Teléfono", "+54 911 6926 0805")
    linkedin = st.text_input("LinkedIn", "linkedin.com/in/fdilelle-consultant")
    
    st.header("Configuración")
    industria = st.selectbox("Industria", ["Roofing", "HVAC", "Med Spa", "Cleaning Services", "Other"])
    estilo = st.selectbox("Estilo del Outreach", 
                         ["Bold CTA (Reply YES)", "Professional", "Friendly & Helpful"])
    
    st.markdown("---")
    if st.button("🔄 Reiniciar todo (Nueva empresa)"):
        st.session_state.clear()
        st.rerun()

# ================== MAIN ==================
url = st.text_input("🔗 Pega la URL de la empresa (ej: https://www.texasbestroofingsolutions.com/)", 
                    placeholder="https://www.ejemplo.com")

if st.button("🚀 Analizar Sitio Web", type="primary", use_container_width=True) and url:
    with st.spinner("Analizando el sitio web..."):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            titulo = soup.title.string.strip() if soup.title else "Empresa"
            texto = soup.get_text().lower()
            
            # Detecciones inteligentes
            tiene_quote = any(kw in texto for kw in ['instant quote', 'get quote', 'online quote', 'book online', 
                                                    'schedule now', 'free estimate', 'instant estimate'])
            tiene_ads = any(kw in texto for kw in ['google ads', 'meta ads', 'facebook pixel', 'gtag', 'fbq'])
            
            # Step 2 inteligente
            if not tiene_quote:
                problema = "lack of an instant quote form or online booking tool"
                impacto = "Homeowners must call to schedule, creating friction and causing many to abandon the site."
            else:
                problema = "weak or missing clear call-to-action for lead capture"
                impacto = "The site relies only on basic contact forms."
            
            step2 = f"""Upon reviewing {titulo}’s website, there are no visible signs that they are currently running Google Ads or Meta Ads.

One clear marketing issue I noticed is the {problema}. {impacto}

This is a missed opportunity in the competitive U.S. market. Roxfire Marketing Agency could help them generate 2–3x more qualified leads by running targeted Google Ads and building optimized landing pages with easy online booking."""

            # Step 3 según estilo e industria
            if estilo == "Bold CTA (Reply YES)":
                cta = f"Just reply **YES** and I’ll send you 2 time slots for a quick 15-minute strategy call this week."
            elif estilo == "Professional":
                cta = "Would you have 15 minutes next week for a quick strategy call?"
            else:
                cta = "Are you open to a quick 15-minute chat to see how many more jobs we could book for you?"
            
            asunto = f"2-3x More {industria} Leads Booked for {titulo}?"
            
            outreach = f"""**Subject:** {asunto}

Hi {titulo} Team,

I just reviewed your site — you’re clearly a trusted local expert in {industria.lower()} with strong reviews and great service.  

However, without an instant quote form or online booking option, customers searching urgently are probably going to your competitors.

At Roxfire Marketing Agency we specialize in helping {industria.lower()} companies dominate local search with Google Ads and simple booking pages — delivering 2-3x more qualified leads and booked jobs.

{cta}

Best regards,  
{nombre}  
Sales Development Representative  
Roxfire Marketing Agency  
{email} | {phone}  
{linkedin}"""

            # ================== MOSTRAR RESULTADOS ==================
            st.success("✅ Análisis completado!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Step 1")
                ciudad = st.text_input("City and State (edita si hace falta)", 
                                       value="Burleson, Texas (DFW area)")
                st.code(f"Company name: {titulo}\nWebsite: {url}\nCity and state: {ciudad}")
            
            with col2:
                st.subheader("Step 2")
                st.markdown(step2)
            
            st.subheader("Step 3 – Outreach Message")
            mensaje_final = st.text_area("Edita si querés", outreach, height=320)
            
            # Botones de acción
            colA, colB, colC = st.columns(3)
            with colA:
                st.download_button("📥 Descargar como TXT", 
                                   mensaje_final + "\n\n" + step2, 
                                   file_name=f"Pre-Application_Task_{titulo}.txt")
            with colB:
                if st.button("📋 Copiar Documento Completo"):
                    full_doc = f"""Pre-Application Task – Sales Development Representative (SDR) & Closer
Fernando A. Di Lelle
{email} | {linkedin}
{phone} | Buenos Aires, Argentina
Date: {date.today().strftime('%B %d, %Y')}

### Step 1
Company name: {titulo}
Website link: {url}
City and state: {ciudad}

### Step 2
{step2}

### Step 3
{mensaje_final}"""
                    st.code(full_doc, language=None)
                    st.success("¡Documento completo copiado! Pégalo en Google Docs.")
            
            with colC:
                if st.button("🔄 Nueva Empresa"):
                    st.session_state.clear()
                    st.rerun()

        except Exception as e:
            st.error(f"Error al cargar la página: {e}")

else:
    st.info("Pegá la URL y hacé clic en **Analizar Sitio Web**")

st.caption("Hecho con ❤️ para Fernando • Reutilizable ilimitadamente")
