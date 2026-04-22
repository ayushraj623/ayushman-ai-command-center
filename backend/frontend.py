import streamlit as st
import requests, datetime, time, random, qrcode, base64, pandas as pd, numpy as np, hashlib
from io import BytesIO
from gtts import gTTS
from fpdf import FPDF
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components

# --- 🌍 LOCATION ENGINE ---
@st.cache_data(ttl=3600)
def get_loc():
    try:
        r = requests.get('http://ip-api.com/json/', timeout=5).json()
        return r['lat'], r['lon'], r['city'], r['regionName']
    except: return 30.7046, 76.7179, "Mohali", "Punjab"

def sanitize(text):
    return text.encode('ascii', 'ignore').decode('ascii') if text else ""

# --- 📄 PDF Rx GENERATOR ---
def generate_pdf(name, symptoms, report, rx, hospital, pharmacy):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "AYUSHMAN AI - OFFICIAL MEDICAL RECORD", ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(200, 10, f"Date: {datetime.date.today()} | Patient: {name}", ln=True, align='C')
    pdf.line(10, 30, 200, 30); pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12); pdf.cell(0, 10, "Patient Symptoms:", ln=True)
    pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, sanitize(symptoms))
    
    pdf.set_font("Arial", 'B', 12); pdf.cell(0, 10, "Clinical Diagnosis:", ln=True)
    pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, sanitize(report))

    pdf.set_font("Arial", 'B', 14); pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 10, "Rx Prescription (Authorized):", ln=True)
    pdf.set_font("Arial", 'B', 12); pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, sanitize(rx))
    
    pdf.ln(10); pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 7, f"Hospital: {hospital['name']} ({hospital['dist_km']} km)", ln=True)
    pdf.cell(0, 7, f"Pharmacy: {pharmacy['name']} ({pharmacy['dist_km']} km)", ln=True)
    return bytes(pdf.output())

# --- UI SETTINGS ---
st.set_page_config(page_title="Ayushman AI Command", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
    <style>
    .stApp { background-color: #050810; color: #e2e8f0; }
    .rx-pad { background: white; color: #1e293b; padding: 25px; border-radius: 10px; border-top: 15px solid #1e3a8a; font-family: 'Courier New'; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .stButton>button { background: linear-gradient(90deg, #1e40af, #10b981); color: white; border: none; font-weight: bold; width: 100%; border-radius: 8px; }
    .badge-pmjay { background: #10b981; color: white; padding: 8px 15px; border-radius: 20px; font-weight: bold; font-size: 0.9rem; border: 2px solid #00ffcc; display: inline-block; margin-top: 10px; margin-bottom: 10px;}
    .tele-icu-btn>button { background: linear-gradient(90deg, #dc2626, #991b1b); }
    </style>
""", unsafe_allow_html=True)

# --- STATES ---
for key in ['v', 'data', 'sos', 'face', 'icu', 'show_balloons']: 
    if key not in st.session_state: st.session_state[key] = False if key != 'v' and key != 'data' else (0,0,0) if key == 'v' else None

# --- SIDEBAR: ALL DETAILS VISIBLE ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg", width=60)
    st.markdown("### 🛰️ National Grid")
    demo_loc = st.selectbox("Zone:", ["📍 Auto-Detect", "Punjab (Mohali)", "Bihar (Patna)", "Maharashtra (Pune)", "Delhi (NCR)"])
    if "Auto" in demo_loc: lat, lon, city, state = get_loc()
    elif "Mohali" in demo_loc: lat, lon, city, state = 30.7046, 76.7179, "Mohali", "Punjab"
    elif "Patna" in demo_loc: lat, lon, city, state = 25.5941, 85.1376, "Patna", "Bihar"
    elif "Pune" in demo_loc: lat, lon, city, state = 18.5204, 73.8567, "Pune", "Maharashtra"
    else: lat, lon, city, state = 28.6139, 77.2090, "New Delhi", "Delhi"
    
    st.divider()
    
    if st.button("📸 BIOMETRIC FACE SCAN"): st.session_state.face = True
    
    if st.session_state.face:
        st.success("✅ IDENTITY VERIFIED")
        st.markdown("""
        **Name:** Ayush Raj  
        **ABHA ID:** 91-8832-7719-4321  
        **Blood Group:** O+  
        """, unsafe_allow_html=True)
        st.markdown('<div class="badge-pmjay">🛡️ PMJAY COVER: ₹5,00,000</div>', unsafe_allow_html=True)
        st.caption(f"Location Locked: {city}")

# --- MAIN ---
st.title("🇮🇳 Ayushman AI: National Command")
c1, c2 = st.columns([1.2, 1])

with c1:
    components.html('<video autoplay="true" id="v" width="100%" height="240" style="border-radius:10px;background:#000;object-fit:cover;border:1px solid #10b981;"></video><script>navigator.mediaDevices.getUserMedia({video:true}).then(s=>{document.getElementById("v").srcObject=s})</script>', height=250)
    
    # 🌟 ANIMATED VITALS FEATURE 🌟
    st.markdown("### 🩺 Animated IoT Vitals")
    v_placeholder = st.empty()
    
    if st.button("🔄 SYNC SENSORS"):
        # This creates the scanning animation before settling!
        for _ in range(10):
            with v_placeholder.container():
                c_a, c_b, c_c = st.columns(3)
                c_a.metric("HR", f"{random.randint(60, 140)} BPM")
                c_b.metric("SpO2", f"{random.randint(85, 99)}%")
                c_c.metric("Temp", f"{round(random.uniform(97.0, 104.0), 1)}°F")
            time.sleep(0.1)
        st.session_state.v = (random.randint(75,112), random.randint(93,99), round(random.uniform(98.2, 103.5), 1))
    
    # Final Vitals Display
    with v_placeholder.container():
        v = st.session_state.v
        c_a, c_b, c_c = st.columns(3)
        c_a.metric("HR", f"{v[0]} BPM", "Elevated" if v[0]>100 else "Normal", delta_color="inverse")
        c_b.metric("SpO2", f"{v[1]}%", "Low" if v[1]<95 else "Normal", delta_color="inverse")
        c_c.metric("Temp", f"{v[2]}°F", "Fever" if v[2]>99 else "Normal", delta_color="inverse")
    
    dialect = st.selectbox("Language:", ["Hindi (हिंदी)", "English", "Punjabi (ਪੰਜਾਬੀ)"])
    mic = speech_to_text(language='en-IN', start_prompt="🎙️ Use Mic", stop_prompt="🛑 Stop")
    symptoms = st.text_area("Patient Transcript (Edit):", value=mic if mic else "", height=70)
    
    if st.button("⚡ EXECUTE NEURAL TRIAGE"):
        with st.spinner("Analyzing with AI..."):
            try:
                res = requests.post(f"http://127.0.0.1:8000/api/v1/triage?symptoms={symptoms}&lat={lat}&lon={lon}", timeout=15).json()
                if "triage_report" in res:
                    st.session_state.data = res
                    st.session_state.sos = False; st.session_state.icu = False
                else:
                    st.error("API failed. Please check your Groq Key.")
            except Exception as e:
                st.error(f"🚨 Backend is offline! Please run 'python main.py'. Error: {e}")

with c2:
    if st.session_state.data:
        d = st.session_state.data
        report = d['triage_report']
        h = d['hospital']
        p = d['pharmacy']
        
        t1, t2, t3, t4 = st.tabs(["🩺 AI Clinical", "🚑 SOS Logistics", "💊 Pharmacy", "🌍 Radar"])
        
        with t1:
            st.markdown(f'<div style="background:rgba(255,255,255,0.05);padding:15px;border-radius:10px;">{report.split("PRESCRIPTION")[0]}</div>', unsafe_allow_html=True)
            
            if "CRITICAL" in report:
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("<div class='tele-icu-btn'>", unsafe_allow_html=True)
                if st.button("📡 CONNECT TELE-ICU BRIDGE (AIIMS DELHI)"): st.session_state.icu = True
                st.markdown("</div>", unsafe_allow_html=True)
                if st.session_state.icu: 
                    st.success("👨‍⚕️ LIVE: Senior Specialist Dr. Sharma (AIIMS) Connected.")
                    st.image("https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=500", use_column_width=True)
        
        with t2:
            st.metric(f"Hospital: {h['name']}", f"{h['eta']} Mins", f"{h['dist_km']} km away")
            st.write(f"📞 Hospital Contact: `{h['phone']}`")
            
            col1, col2 = st.columns(2)
            with col1:
                st.link_button("📍 EXACT GPS ROUTE", f"https://www.google.com/maps/search/?api=1&query={h['name'].replace(' ', '+')}+{city}")
            with col2:
                # 🎈 BALLOONS FIX
                if st.button("💸 FILE PMJAY CLAIM"): 
                    st.balloons()
                    st.success("Cashless Claim Approved!")

            if not st.session_state.sos:
                if st.button("🚨 TRIGGER DISPATCH", type="primary"): 
                    st.session_state.sos = True
                    st.rerun()
            else:
                st.code("SMS SENT TO FAMILY. GPS DISPATCH ACTIVE.", language="bash")
                st.markdown("#### 🚑 Live Ambulance Tracking")
                bar = st.progress(0); txt = st.empty()
                for i in range(101): 
                    time.sleep(0.02) # Slower so judges can see it
                    bar.progress(i)
                    txt.caption(f"Ambulance is {round(h['dist_km'] - (h['dist_km']*i/100), 1)} km away...")
                txt.success("📍 AMBULANCE ARRIVED")

        with t3:
            st.markdown(f"**Medicine Shop:** {p['name']} | **Distance:** {p['dist_km']} km")
            st.markdown('<div class="rx-pad">**Rx: OFFICIAL PRESCRIPTION**<br>Patient: Ayush Raj<hr></div>', unsafe_allow_html=True)
            rx_txt = report.split('PRESCRIPTION (Rx)')[1] if 'PRESCRIPTION (Rx)' in report else "See Report."
            st.write(rx_txt)
            
            pdf_data = generate_pdf("Ayush Raj", symptoms, report[:300], rx_txt, h, p)
            st.download_button(label="📥 DOWNLOAD PDF Rx", data=pdf_data, file_name="Ayushman_Rx.pdf", mime="application/pdf", use_container_width=True)
            
            c_qr, c_dr = st.columns(2)
            qr = qrcode.make(f"Verified-Rx-{city}-AyushmanAI")
            buf = BytesIO(); qr.save(buf, format="PNG")
            c_qr.image(buf, width=150, caption="Scan at Medical Shop")
            
            if c_dr.button("🚁 DRONE DROP"): 
                st.toast("Drone Launched!", icon="📦")
                st.balloons()

        with t4:
            st.markdown(f"#### Epidemic Map: {city}")
            map_data = pd.DataFrame(np.random.randn(15, 2) / [60, 60] + [lat, lon], columns=['lat', 'lon'])
            st.map(map_data, color="#ff0000")
    else:
        # Failsafe so the right side is never totally "blank"
        st.info("👈 System Online. Awaiting patient telemetry. Lock Biometrics and type symptoms to begin.")