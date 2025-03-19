from core.shell_generator import generate_linux_reverse_shell, generate_windows_reverse_shell
from core.encoding import encode_payload
from core.listener import start_listener
from core.dependency_checker import check_dependency, install_dependency
from core.web_tools import web_menu
from colorama import Fore, Style, init
from core.exploits import exploits_menu

init(autoreset=True)

def main_menu():
    print(Fore.YELLOW + "\n1. Reverse Shell")
    print(Fore.YELLOW + "2. Web Exploitation & Recon")
    print(Fore.YELLOW + "3. Exploits")
    print(Fore.YELLOW + "4. Exit\n")

    choice = input(Fore.CYAN + "Select an option: " + Style.RESET_ALL)

    if choice == "1":
        reverse_shell_menu()
    elif choice == "2":
        web_menu()
    elif choice == "3":
        exploits_menu()
    elif choice == "4":
        exit(0)
    else:
        print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)
        main_menu()

def reverse_shell_menu():
    print("\n1. Linux Reverse Shell")
    print("2. Windows Reverse Shell")
    print("3. Go Back\n")

    shell_choice = input(Fore.CYAN + "Select: " + Style.RESET_ALL)

    if shell_choice == "1":
        linux_shell_menu()
    elif shell_choice == "2":
        windows_shell_menu()
    elif shell_choice == "3":
        main_menu()
    else:
        print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
        reverse_shell_menu()

def linux_shell_menu():
    shell_types = ["Bash", "Python", "Perl", "Ruby", "Netcat", "Socat"]

    print("\nChoose Linux Shell Type:")
    for i, shell in enumerate(shell_types, start=1):
        print(f"{i}. {shell}")

    choice = input(Fore.CYAN + "Select an option: " + Style.RESET_ALL)

    try:
        choice = int(choice)
        if 1 <= choice <= len(shell_types):
            shell_type = shell_types[choice - 1].lower()
            ip = input("Enter IP: ")
            port = input("Enter Port: ")

            payload = generate_linux_reverse_shell(shell_type, ip, port)
            encoded_payload = choose_encoding(payload)

            print("\nGenerated Payload:\n")
            print(encoded_payload)

            start_nc_listener(port)

            main_menu()
        else:
            print(Fore.RED + "Invalid option!" + Style.RESET_ALL)
            linux_shell_menu()
    except ValueError:
        print(Fore.RED + "Enter a valid number!" + Style.RESET_ALL)
        linux_shell_menu()

def windows_shell_menu():
    ip = input("Enter IP: ")
    port = input("Enter Port: ")

    payload = generate_windows_reverse_shell(ip, port)
    encoded_payload = choose_encoding(payload)

    print("\nGenerated Windows Payload:\n")
    print(encoded_payload)

    start_nc_listener(port)

    main_menu()

def choose_encoding(payload):
    """Ask user if they want to encode the payload."""
    print("\nChoose encoding type:")
    print("1. Base64 Encode")
    print("2. URL Encode")
    print("3. Double URL Encode")
    print("4. No Encoding\n")

    encoding_choice = input(Fore.CYAN + "Select encoding type: " + Style.RESET_ALL)

    encoding_map = {
        "1": "base64",
        "2": "url",
        "3": "double_url",
        "4": None
    }

    encoding_type = encoding_map.get(encoding_choice)
    return encode_payload(payload, encoding_type) if encoding_type else payload

def start_nc_listener(port):
    """Check for Netcat, install if missing, then start listener."""
    
    if not check_dependency("nc"):
        print(Fore.RED + "[!] Netcat (nc) not found!" + Style.RESET_ALL)
        install_dependency("nc")
    
    if check_dependency("nc"):
        start_listener_choice = input(Fore.YELLOW + f"\nStart Netcat listener on port {port}? (y/n): " + Style.RESET_ALL)
        if start_listener_choice.lower() == "y":
            start_listener(port)
    else:
        print(Fore.RED + "[!] Netcat installation failed. Cannot start listener." + Style.RESET_ALL)
