import paramiko
import os
from colorama import Fore, Style

def ssh_download():
    ssh_ip = input(Fore.CYAN + "Enter SSH IP: " + Style.RESET_ALL)
    ssh_port = input(Fore.CYAN + "Enter SSH Port (default: 22): " + Style.RESET_ALL) or "22"
    username = input(Fore.CYAN + "Enter SSH username: " + Style.RESET_ALL)
    password = input(Fore.CYAN + "Enter SSH password: " + Style.RESET_ALL)
    remote_path = input(Fore.CYAN + "Enter remote file path to download: " + Style.RESET_ALL)
    local_path = input(Fore.CYAN + "Enter local path to save the file (use ./ for current dir): " + Style.RESET_ALL)

    filename = os.path.basename(remote_path)

    if local_path.endswith("/") or local_path == "./":
        local_path = os.path.join(local_path, filename)

    try:
        print(Fore.YELLOW + f"[+] Connecting to {ssh_ip}:{ssh_port}..." + Style.RESET_ALL)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(ssh_ip, port=int(ssh_port), username=username, password=password, timeout=5)
        sftp = ssh.open_sftp()

        print(Fore.YELLOW + f"[+] Downloading {remote_path} to {local_path}..." + Style.RESET_ALL)
        sftp.get(remote_path, local_path)
        sftp.close()
        ssh.close()

        print(Fore.GREEN + f"[+] Download complete! Saved as {local_path}" + Style.RESET_ALL)
    except paramiko.AuthenticationException:
        print(Fore.RED + "[!] Authentication failed. Check your username/password." + Style.RESET_ALL)
    except paramiko.SSHException:
        print(Fore.RED + "[!] SSH connection failed. Check the IP and port." + Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED + f"[!] Remote file not found: {remote_path}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}" + Style.RESET_ALL)

def ssh_upload():
    ssh_ip = input(Fore.CYAN + "Enter SSH IP: " + Style.RESET_ALL)
    ssh_port = input(Fore.CYAN + "Enter SSH Port (default: 22): " + Style.RESET_ALL) or "22"
    username = input(Fore.CYAN + "Enter SSH username: " + Style.RESET_ALL)
    password = input(Fore.CYAN + "Enter SSH password: " + Style.RESET_ALL)
    local_path = input(Fore.CYAN + "Enter local file path to upload: " + Style.RESET_ALL)
    remote_path = input(Fore.CYAN + "Enter remote path to save the file (use ./ for home directory): " + Style.RESET_ALL)

    if not os.path.exists(local_path):
        print(Fore.RED + f"[!] Error: File {local_path} not found!" + Style.RESET_ALL)
        return

    filename = os.path.basename(local_path)

    if remote_path.endswith("/") or remote_path == "./":
        remote_path = os.path.join(remote_path, filename)

    try:
        print(Fore.YELLOW + f"[+] Connecting to {ssh_ip}:{ssh_port}..." + Style.RESET_ALL)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(ssh_ip, port=int(ssh_port), username=username, password=password, timeout=5)
        sftp = ssh.open_sftp()

        print(Fore.YELLOW + f"[+] Uploading {local_path} to {remote_path}..." + Style.RESET_ALL)
        sftp.put(local_path, remote_path)
        sftp.close()
        ssh.close()

        print(Fore.GREEN + f"[+] Upload complete! File saved as {remote_path}" + Style.RESET_ALL)
    except paramiko.AuthenticationException:
        print(Fore.RED + "[!] Authentication failed. Check your username/password." + Style.RESET_ALL)
    except paramiko.SSHException:
        print(Fore.RED + "[!] SSH connection failed. Check the IP and port." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}" + Style.RESET_ALL)
