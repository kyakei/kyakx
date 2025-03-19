import os

def start_listener(port):
    print(f"Starting Netcat on port {port}...")
    os.system(f"nc -lnvp {port}")
