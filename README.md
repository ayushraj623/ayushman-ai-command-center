# 🇮🇳 Ayushman AI: Rural Health Command Center

Ayushman AI is a full-stack, autonomous triage and logistics command center designed to bridge the healthcare gap in rural India. By leveraging state-of-the-art LLMs, spatial routing, and the Ayushman Bharat Digital Mission (ABDM) framework, this system provides zero-latency emergency medical response.

## 🚀 Key Features

* **Biometric ABHA Integration:** Simulated facial scan to instantly verify ABHA ID and ₹5 Lakh PMJAY coverage.
* **Bhashini Multi-Lingual Triage:** Multi-dialect voice support (Hindi/English/Punjabi) for zero-literacy accessibility.
* **AI Clinical Officer:** Llama 3.3 powered triage reports, precautions, and ICD-10 diagnostic codes via Groq.
* **Live SOS Logistics:** Real-time proximity tracking for the nearest hospital and pharmacy.
* **Ambulance Live Tracking:** Animated GPS progress bar showing the ambulance's approach in kilometers.
* **Secure Rx Generation:** Downloadable PDF prescription with an anti-fraud QR hash for pharmacists.


## 🛠️ Technology Stack

* **Frontend:** Streamlit
* **Backend:** FastAPI, Python 3.10+
* **AI Engine:** Llama 3.3 70B (Groq API)
* **Logistics:** PostGIS / Spatial Routing Logic
* **PDF Engine:** FPDF2

## ⚙️ How to Run
1. Start Backend: `python main.py`
2. Start Frontend: `streamlit run frontend.py`

## 👨‍💻 Author
**Ayush Raj**
Aspiring Engineer | CGC University Mohali 

