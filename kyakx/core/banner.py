import time
import sys
import random
from colorama import Fore, Style, init
from kyakx.core.version import get_version_info

init(autoreset=True)

def animated_banner():
    banner_text = "SUKA NOW OWNS YOU ♥"
    
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    
    for char in banner_text:
        color = random.choice(colors)
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(0.08)  # Slightly faster animation
    
    print(Style.RESET_ALL)  # Reset color
    print(Fore.CYAN + get_version_info() + Style.RESET_ALL)

def funky_loading():
    loading_text = "LOADING KyakX..."
    for char in loading_text:
        sys.stdout.write(Fore.YELLOW + char)
        sys.stdout.flush()
        time.sleep(0.03)  # Faster loading
    time.sleep(0.3)
    print("\n")
    animated_banner()
    time.sleep(0.5)  # Shorter delay

if __name__ == "__main__":
    funky_loading()
