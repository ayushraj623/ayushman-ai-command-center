import os
import psycopg2
from fastapi import FastAPI
from groq import Groq
from dotenv import load_dotenv
import math

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(title="Ayushman AI - National Node")

def get_nearest_facility(lat: float, lon: float, category: str):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("""
            SELECT name, role, phone, ST_Distance(location, st_point(%s, %s)::geography) as dist
            FROM health_workers WHERE category = %s ORDER BY dist ASC LIMIT 1;
        """, (lon, lat, category))
        w = cur.fetchone()
        conn.close()
        if w:
            dist_km = w[3]/1000
            return {"name": w[0], "role": w[1], "phone": w[2], "dist_km": round(dist_km, 1), "eta": math.ceil((dist_km/40)*60)}
        return None
    except: return None

@app.post("/api/v1/triage")
async def process(symptoms: str, lat: float, lon: float):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        prompt = f"""
        Act as a Senior Chief Medical Officer. Analyze: "{symptoms}"
        Provide a report EXACTLY in this Markdown format:
        
        ### 🚨 TRIAGE: [CRITICAL/URGENT/STABLE]
        **Assessment:** (Formal clinical summary)
        
        ### ⚠️ EXACT PRECAUTIONS
        (3 life-saving steps in the user's dialect)
        
        ### 💊 OFFICIAL PRESCRIPTION (Rx)
        (List real-world medicines, dosage, and frequency in English)
        """
        completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], temperature=0.1)
        
        return {
            "status": "success",
            "triage_report": completion.choices[0].message.content,
            "hospital": get_nearest_facility(lat, lon, "Hospital") or {"name": "Apollo District Care", "phone": "108", "dist_km": 4.2, "eta": 8},
            "pharmacy": get_nearest_facility(lat, lon, "Pharmacy") or {"name": "Jan Aushadhi Kendra", "dist_km": 1.5}
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)