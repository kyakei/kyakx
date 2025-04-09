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
        elif tool == "metasploit-framework" or tool == "msfvenom":
            print(Fore.YELLOW + "[*] Installing Metasploit Framework... This may take a while." + Style.RESET_ALL)
            print(Fore.YELLOW + "[*] For Debian/Ubuntu: Installing from apt repositories" + Style.RESET_ALL)
            install_cmd = "sudo apt install metasploit-framework -y || " + \
                          "sudo curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && " + \
                          "sudo chmod 755 msfinstall && " + \
                          "sudo ./msfinstall && " + \
                          "sudo rm msfinstall"
        else:
            install_cmd = f"sudo apt install {tool} -y || sudo yum install {tool} -y || sudo pacman -S {tool} --noconfirm"

    elif os_type == "macos":
        install_cmd = f"brew install {tool}"

    elif os_type == "windows":
        print(Fore.RED + f"[!] Windows detected. Please install {tool} manually from the official website." + Style.RESET_ALL)
        return

    if install_cmd:
        print(Fore.YELLOW + f"[*] Running: {install_cmd}" + Style.RESET_ALL)
        exit_code = os.system(install_cmd)
        
        if exit_code == 0:
            print(Fore.GREEN + f"[+] {tool} installation completed successfully!" + Style.RESET_ALL)
            return True
        else:
            print(Fore.RED + f"[!] {tool} installation failed with exit code {exit_code}." + Style.RESET_ALL)
            print(Fore.YELLOW + f"[*] Please try installing {tool} manually." + Style.RESET_ALL)
            return False
