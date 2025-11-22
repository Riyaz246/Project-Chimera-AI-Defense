# Project Chimera: AI-Driven Defense Against Polymorphic L7 Attacks

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Focus](https://img.shields.io/badge/Focus-AI%20SecOps-blueviolet)

## 🔍 Executive Summary
Traditional firewalls rely on static signatures (IP reputation or fixed User-Agents) to block Denial of Service (DoS) attacks. Sophisticated attackers bypass this by rotating User-Agents and timing (Polymorphic Attacks). 

**Project Chimera** is a Proof-of-Concept (PoC) detection engine that utilizes a **Local Large Language Model (Llama 3 via Ollama)** to perform real-time behavioral analysis on HTTP traffic. Instead of matching strings, the AI analyzes the *entropy* and *context* of header data to identify adversarial intent.

## 🛠️ Technical Architecture
The lab simulates a "Red Team vs. Blue Team" scenario using a hybrid environment:

* **Attacker (Kali Linux):** A custom multi-threaded Python script (`smart_attacker.py`) that generates L7 HTTP floods with randomized User-Agents and jitter to mimic human behavior.
* **Victim (Windows Host):** A Python-based HTTP server logging all incoming requests.
* **Sentinel (AI Engine):** An asynchronous detection loop (`ai_sentinel.py`) that:
    1.  Ingests logs in real-time.
    2.  Batches requests for context.
    3.  Queries a local **Llama 3** model to grade the traffic for "Malicious" intent.

## 📸 Proof of Detection (Evidence)

### 1. The Attack Pattern (Polymorphic Behavior)
*Observed Traffic: Single source IP (172.18.41.40) initiating requests as "iPhone", "Linux Desktop", and "Windows Chrome" within milliseconds.*
![Logs Screenshot](Screenshot%202025-11-22%20121006.png)

### 2. Real-Time AI Detection
*The Sentinel correctly identifies the anomaly, flagging the high variance of User-Agents from a single source as a "Polymorphic Scan" with HIGH confidence.*
![Detection Screenshot](Screenshot%202025-11-22%20120650.png)

### 3. **The Engine Behind the Detection:**
*The system uses a custom detection loop running in Python, interfacing directly with the local LLM via API.*
![Logic Screenshot](Screenshot%202025-11-22%20121107.png)

## 💻 Key Features (Code Logic)

### 1. The AI "Sentinel" Prompt
Unlike standard regex or static signatures, the system uses **Prompt Engineering** to teach the AI security concepts. This allows it to detect "intent" rather than just matching strings.

```python
prompt = """
Act as a Cyber Threat Analyst. Review these server logs.
DETECTION RULES:
1. Normal users usually stick to ONE User-Agent.
2. If you see the SAME IP using MANY different User-Agents rapidly, it is a "Polymorphic Scan".
OUTPUT format (JSON only): { "verdict": "MALICIOUS", "confidence": "HIGH", ... }
"""
```

### 2. The Polymorphic Engine
The attack script is designed to bypass basic firewall rate limits (WAF) by mimicking legitimate browser headers and randomizing requests:

```python
# Rotates identity for every request to evade signature detection
ua = random.choice(USER_AGENTS)
headers = {'User-Agent': ua}
# Adds Jitter (Random Delay) to evade timing analysis
time.sleep(random.uniform(0.1, 0.5))
```

## 🚀 How to Replicate This Lab

### Prerequisites:
* **Windows 10/11 with Ollama installed ('ollama run llama3').**
* **Kali Linux VM ('Bridged Adapter').**
* **Python 3.x.**

### Steps:
1. Start the Victim: Run `python victim_server.py` on Windows.
2. Start the Sentinel: Run `python ai_sentinel.py` on Windows.
3. Launch Attack: Run `python3 smart_attacker.py` on Kali.
4. Observe: Watch the AI flag the attack in the console.

## 🧠 Skills Demonstrated
* **Detection Engineering: Moving beyond static rules to behavioral analysis.**
* **GenAI for SecOps: Integrating Local LLMs into the OODA loop.**
* **Threat Emulation: Writing custom Python tools to simulate Layer 7 evasion techniques.**
