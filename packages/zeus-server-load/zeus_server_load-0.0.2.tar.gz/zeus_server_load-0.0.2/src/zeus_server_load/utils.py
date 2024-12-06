import logging
import threading
import time
from datetime import datetime
from colorama import init, Fore, Style
import os


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        filename='server.log',
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s'
    )


def log_info(message):
    """Log informational messages."""
    logging.info(message)


def log_error(message):
    """Log error messages."""
    logging.error(message)


def log_success(message):
    """Log success messages."""
    logging.info(message)


def display_menu(server):
    """Display the menu-driven interface."""
    init(autoreset=True)
    start_time = datetime.now()
    while True:
        uptime = datetime.now() - start_time
        print(f"\n{Fore.CYAN}Zeus Server Load - Uptime: {str(uptime).split('.')[0]}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Select an option:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. Add HWID{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. Tail Logs{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. Exit{Style.RESET_ALL}")
        choice = input(f"{Fore.GREEN}Enter your choice: {Style.RESET_ALL}")
        if choice == '1':
            hwid = input("Enter HWID to add: ")
            if server.hwid_manager.add_hwid(hwid):
                print(f"{Fore.GREEN}HWID '{hwid}' added successfully.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}HWID '{hwid}' is already in the whitelist.{Style.RESET_ALL}")
        elif choice == '2':
            tail_logs()
        elif choice == '3':
            print("Exiting...")
            server.shutdown()
            break
        else:
            print("Invalid choice. Please try again.")


def tail_logs():
    """Tail the server logs."""
    log_file = 'server.log'
    if not os.path.exists(log_file):
        print("Log file does not exist.")
        return
    print(f"Tailing logs from {log_file}. Press Ctrl+C to exit.")
    try:
        with open(log_file, 'r') as f:
            # Move to the end of the file
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                print(line, end='')
    except KeyboardInterrupt:
        print("\nExiting log tail.")
