import os
from colorama import Fore, Style
import readline
import atexit

# Maximum number of commands to store in history
MAX_HISTORY = 100
HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".kyakx_history")

def setup_command_history():
    """Set up command history for readline."""
    # Make sure readline is available
    try:
        readline
    except NameError:
        print(Fore.YELLOW + "[!] Readline not available. Command history disabled." + Style.RESET_ALL)
        return
    
    # Set up history file
    try:
        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'w') as f:
                pass
        
        readline.read_history_file(HISTORY_FILE)
        readline.set_history_length(MAX_HISTORY)
        atexit.register(readline.write_history_file, HISTORY_FILE)
        
        print(Fore.GREEN + "[+] Command history enabled" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.YELLOW + f"[!] Failed to set up command history: {e}" + Style.RESET_ALL)

def show_history():
    """Display command history to user."""
    try:
        history_length = readline.get_current_history_length()
        
        if history_length == 0:
            print(Fore.YELLOW + "[!] No command history available." + Style.RESET_ALL)
            return
        
        print(Fore.CYAN + "\n=== Command History ===" + Style.RESET_ALL)
        
        for i in range(1, history_length + 1):
            cmd = readline.get_history_item(i)
            if cmd:
                print(f"{i}: {cmd}")
        
        print(Fore.CYAN + "======================" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[!] Error displaying history: {e}" + Style.RESET_ALL)