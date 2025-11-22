# victim_server.py
# Role: The Target System
# OS: Windows
import http.server
import socketserver
import logging

# Configuration
PORT = 8080
LOG_FILE = "access_logs.txt"

# Setup logging: Writes to file AND prints to console
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(message)s')

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # 1. Capture the Attacker's IP
        client_ip = self.client_address[0]
        
        # 2. Capture the User-Agent (The "Disguise")
        user_agent = self.headers.get('User-Agent', 'Unknown')
        request_line = args[0]
        
        # 3. Format the log entry for the AI
        log_entry = f"IP: {client_ip} | UA: {user_agent} | REQ: {request_line}"
        
        logging.info(log_entry)
        print(f"[+] {log_entry}")

# Prevent "Address already in use" errors
socketserver.TCPServer.allow_reuse_address = True

print(f"[*] Victim Server running on Port {PORT}. Logging to {LOG_FILE}...")
print("[*] Press Ctrl+C to stop.")

try:
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n[!] Server stopped.")
