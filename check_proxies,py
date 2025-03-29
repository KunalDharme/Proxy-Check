import requests
import socks
import socket
import pyfiglet
from colorama import init, Fore, Style

banner = pyfiglet.figlet_format("Proxy Check")
print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
print(Fore.RED + "[!] This tool checks whether a given proxy (SOCKS4, SOCKS5, HTTP, or HTTPS) is working and identifies its type." + Style.RESET_ALL)


# Initialize Colorama for colored output
init(autoreset=True)

def check_proxy(proxy):
    """Checks if the given proxy is SOCKS4, SOCKS5, HTTP, or HTTPS."""
    try:
        ip, port = proxy.split(":")
        port = int(port)  # Ensure port is an integer
    except ValueError:
        print(Fore.RED + f"[X] Invalid proxy format: {proxy} (Expected format: IP:PORT)")
        return

    # Check for SOCKS4
    socks.set_default_proxy(socks.SOCKS4, ip, port)
    socket.socket = socks.socksocket
    try:
        requests.get("http://httpbin.org/ip", timeout=5)
        print(Fore.MAGENTA + f"[✓] {proxy} is a SOCKS4 proxy")
        return
    except (requests.RequestException, socket.error):
        pass  # Move to next check

    # Check for SOCKS5
    socks.set_default_proxy(socks.SOCKS5, ip, port)
    socket.socket = socks.socksocket
    try:
        requests.get("http://httpbin.org/ip", timeout=5)
        print(Fore.GREEN + f"[✓] {proxy} is a SOCKS5 proxy")
        return
    except (requests.RequestException, socket.error):
        pass  # Move to next check

    # Check for HTTP Proxy
    http_proxy = f"http://{proxy}"
    proxies_dict = {"http": http_proxy, "https": http_proxy}
    try:
        requests.get("http://httpbin.org/ip", proxies=proxies_dict, timeout=5)
        print(Fore.BLUE + f"[✓] {proxy} is an HTTP proxy")

        # Check if it supports HTTPS
        try:
            requests.get("https://www.google.com", proxies=proxies_dict, timeout=5)
            print(Fore.CYAN + f"[✓] {proxy} also supports HTTPS")
        except (requests.RequestException, socket.error):
            print(Fore.YELLOW + f"[!] {proxy} does NOT support HTTPS")

        return
    except (requests.RequestException, socket.error):
        print(Fore.RED + f"[X] {proxy} is NOT a working proxy")

# Menu for input selection
print(Fore.CYAN + "\n[ Proxy Checker Menu ]")
print(Fore.YELLOW + "1. Enter a single proxy (IP:PORT)")
print(Fore.YELLOW + "2. Provide a file containing multiple proxies")
choice = input(Fore.CYAN + "\n[?] Select an option (1 or 2): ").strip()

# Option 1: Enter a single proxy manually
if choice == "1":
    proxy = input(Fore.CYAN + "[?] Enter the proxy (IP:PORT): ").strip()
    check_proxy(proxy)

# Option 2: Provide a file with multiple proxies
elif choice == "2":
    filename = input(Fore.CYAN + "[?] Enter the proxy list filename (e.g., proxies.txt): ").strip()

    try:
        with open(filename, "r") as file:
            proxies = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + f"[X] File '{filename}' not found!")
        exit()

    print(Fore.YELLOW + f"[!] Checking {len(proxies)} proxies...\n")

    for proxy in proxies:
        check_proxy(proxy)

else:
    print(Fore.RED + "[X] Invalid option! Please restart the script.")
