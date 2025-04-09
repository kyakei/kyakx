import os
from colorama import Fore, Style
from kyakx.core.dependency_checker import check_dependency, install_dependency
from kyakx.core.main_menu import main_menu

def web_menu():
    """Menu for web exploitation and recon."""
    print("\n1. Nmap Scan (Fast Service Detection)")
    print("2. Feroxbuster Scan (Directory Bruteforce)")
    print("3. Go Back\n")

    choice = input(Fore.CYAN + "Select an option: " + Style.RESET_ALL)

    if choice == "1":
        nmap_scan()
    elif choice == "2":
        feroxbuster_scan()
    elif choice == "3":
        main_menu()
    else:
        print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)
        web_menu()

def nmap_scan():
    ip = input(Fore.CYAN + "Enter target IP: " + Style.RESET_ALL)

    if not check_dependency("nmap"):
        install_dependency("nmap")

    print(Fore.YELLOW + f"\n[+] Running Nmap scan on {ip}..." + Style.RESET_ALL)
    os.system(f"nmap -sC -sV -p- --min-rate 10000 {ip}")

    input(Fore.CYAN + "\nPress Enter to return to menu..." + Style.RESET_ALL)
    web_menu()

def feroxbuster_scan():
    url = input(Fore.CYAN + "Enter target URL: " + Style.RESET_ALL)

    if not check_dependency("feroxbuster"):
        install_dependency("feroxbuster")

    print(Fore.YELLOW + f"\n[+] Running Feroxbuster on {url}..." + Style.RESET_ALL)
    os.system(f"feroxbuster -u {url} -t 70 --scan-dir-listings")

    input(Fore.CYAN + "\nPress Enter to return to menu..." + Style.RESET_ALL)
    web_menu()