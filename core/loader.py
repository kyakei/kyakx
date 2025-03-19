import sys
import time
from colorama import Fore, Style, init

init(autoreset=True)

def loading_animation():
    animation = ["|", "/", "-", "\\"]
    for _ in range(10):
        for char in animation:
            sys.stdout.write(f"\r{Fore.CYAN}[{char}] Initializing tool...")
            sys.stdout.flush()
            time.sleep(0.1)
    print("\r" + " " * 30)

if __name__ == "__main__":
    loading_animation()
