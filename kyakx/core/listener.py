import os
import subprocess
from colorama import Fore, Style

def start_listener(port):
    try:
        print(Fore.YELLOW + f"[+] Starting Netcat listener on port {port}..." + Style.RESET_ALL)
        subprocess.call(["nc", "-lnvp", str(port)])
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Listener stopped by user." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\n[!] Error starting listener: {e}" + Style.RESET_ALL)
