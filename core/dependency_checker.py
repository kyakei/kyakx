import os
import shutil
import platform
from colorama import Fore, Style

def check_dependency(tool):
    return shutil.which(tool) is not None

def detect_os():
    os_type = platform.system().lower()
    if "linux" in os_type:
        return "linux"
    elif "darwin" in os_type:
        return "macos"
    elif "windows" in os_type:
        return "windows"
    return None

def install_dependency(tool):
    os_type = detect_os()

    if not os_type:
        print(Fore.RED + "[!] OS detection failed. Please install manually." + Style.RESET_ALL)
        return

    confirm = input(Fore.YELLOW + f"\n[!] {tool} not found. Do you want to install it? (y/n): " + Style.RESET_ALL).lower()
    if confirm != "y":
        print(Fore.RED + f"Skipping {tool} installation." + Style.RESET_ALL)
        return

    print(Fore.CYAN + f"\n[+] Installing {tool} on {os_type}..." + Style.RESET_ALL)

    install_cmd = None

    if os_type == "linux":
        if tool == "nmap":
            install_cmd = "sudo apt install nmap -y || sudo yum install nmap -y || sudo pacman -S nmap --noconfirm"
        elif tool == "feroxbuster":
            install_cmd = "sudo apt install feroxbuster -y || sudo pacman -S feroxbuster --noconfirm"
        elif tool == "netcat" or tool == "nc":
            install_cmd = "sudo apt install netcat -y || sudo yum install nmap-ncat -y || sudo pacman -S openbsd-netcat --noconfirm"
        elif tool == "socat":
            install_cmd = "sudo apt install socat -y || sudo yum install socat -y || sudo pacman -S socat --noconfirm"
        else:
            install_cmd = f"sudo apt install {tool} -y || sudo yum install {tool} -y || sudo pacman -S {tool} --noconfirm"

    elif os_type == "macos":
        install_cmd = f"brew install {tool}"

    elif os_type == "windows":
        print(Fore.RED + f"[!] Windows detected. Please install {tool} manually from the official website." + Style.RESET_ALL)
        return

    if install_cmd:
        os.system(install_cmd)
        print(Fore.GREEN + f"[+] {tool} installation completed!" + Style.RESET_ALL)
