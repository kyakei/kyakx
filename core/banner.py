import time
import sys
from colorama import Fore, Style, init

init(autoreset=True)

def animated_banner():
    """Animated effect for 'SUKA NOW OWNS YOU ♥'"""
    banner_text = "SUKA NOW OWNS YOU ♥"
    for char in banner_text:
        sys.stdout.write(Fore.RED + char)
        sys.stdout.flush()
        time.sleep(0.1)  # Adjust speed of animation
    print(Style.RESET_ALL)  # Reset color

def funky_loading():
    """Funky loading animation before displaying the banner."""
    loading_text = "LOADING KyakX..."
    for char in loading_text:
        sys.stdout.write(Fore.YELLOW + char)
        sys.stdout.flush()
        time.sleep(0.05)
    time.sleep(0.5)
    print("\n")
    animated_banner()
    time.sleep(1)

if __name__ == "__main__":
    funky_loading()
