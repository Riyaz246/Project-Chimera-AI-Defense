# ai_sentinel.py
# Role: The Blue Team Defense Engine
# OS: Windows
import time
import requests
import json
import os

# Configuration
LOG_FILE = "access_logs.txt"
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "llama3"  # Make sure you ran 'ollama pull llama3'

def analyze_batch(log_lines):
    print(f"\n[?] Analyzing batch of {len(log_lines)} requests...")
    
    # Prompt Engineering: Teaching the AI how to hunt
    prompt = f"""
    Act as a Cyber Threat Analyst. Review these server logs.
    
    LOGS:
    {log_lines}
    
    DETECTION RULES:
    1. Normal users usually stick to ONE User-Agent.
    2. If you see the SAME IP using MANY different User-Agents rapidly, it is a "Polymorphic Scan".
    
    OUTPUT format (JSON only):
    {{ "verdict": "MALICIOUS" or "BENIGN", "confidence": "HIGH" or "LOW", "explanation": "Short reason" }}
    """
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    
    try:
        # Query the Local LLM
        response = requests.post(OLLAMA_API, json=payload)
        result = response.json()['response']
        parsed = json.loads(result)
        
        # Alert Logic
        if parsed['verdict'] == "MALICIOUS":
            print(f"🚨 [ALERT] THREAT DETECTED!")
            print(f"    Reason: {parsed['explanation']}")
            print(f"    Confidence: {parsed['confidence']}")
        else:
            print(f"✅ [SAFE] Traffic looks normal.")
            
    except Exception as e:
        print(f"[!] AI Error: {e}")

def follow_logs():
    print(f"[*] AI Sentinel Active. Watching {LOG_FILE}...")
    
    if not os.path.exists(LOG_FILE):
        print(f"[!] Error: {LOG_FILE} not found. Start victim_server.py first!")
        return

    f = open(LOG_FILE, "r")
    f.seek(0, 2) # Skip to end of file (Real-time mode)
    
    batch = []
    
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.5)
            continue
            
        batch.append(line.strip())
        
        # Batch Size: Send to AI every 8-10 requests
        if len(batch) >= 8:
            analyze_batch("\n".join(batch))
            batch = []

if __name__ == "__main__":
    follow_logs()
