import requests
import pyfiglet
import os
from colorama import init, Fore, Style
from rich.console import Console
from rich.panel import Panel
import sys

console = Console()

# Initialize Colorama for colored output
init(autoreset=True)

def is_connected():
    """Checks internet connectivity by pinging a reliable server."""
    try:
        requests.get("http://httpbin.org/ip", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

def display_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = pyfiglet.figlet_format("Proxy Check")
    print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
    panel_text = (
        "[bold green]🛡️  Proxy Scanner Tool v1.0[/bold green]\n"
        "[blue]This tool checks whether a given proxy (SOCKS4, SOCKS5, HTTP, or HTTPS) is working and identifies its type.[/blue]\n"
        "[magenta]Developed by Kunal Dharme[/magenta]"
    )
    console.print(Panel.fit(panel_text, border_style="bright_blue"))

def check_proxy(proxy):
    """Checks if the given proxy is SOCKS4, SOCKS5, HTTP, or HTTPS."""
    try:
        ip, port = proxy.split(":")
        port = int(port)
    except ValueError:
        print(Fore.RED + f"[X] Invalid proxy format: {proxy} (Expected format: IP:PORT)")
        return

    # Check SOCKS4
    try:
        proxies = {
            "http": f"socks4://{proxy}",
            "https": f"socks4://{proxy}"
        }
        requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
        print(Fore.MAGENTA + f"[✓] {proxy} is a SOCKS4 proxy")
        return
    except:
        pass

    # Check SOCKS5
    try:
        proxies = {
            "http": f"socks5://{proxy}",
            "https": f"socks5://{proxy}"
        }
        requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
        print(Fore.GREEN + f"[✓] {proxy} is a SOCKS5 proxy")
        return
    except:
        pass

    # Check HTTP and HTTPS
    try:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
        print(Fore.BLUE + f"[✓] {proxy} is an HTTP proxy")
        try:
            requests.get("https://httpbin.org/ip", proxies=proxies, timeout=5)
            print(Fore.CYAN + f"[✓] {proxy} also supports HTTPS")
        except:
            print(Fore.YELLOW + f"[!] {proxy} does NOT support HTTPS")
        return
    except:
        print(Fore.RED + f"[X] {proxy} is NOT a working proxy")

def main():
    try:
        display_banner()
        print(Fore.BLUE + "🛜  Please make sure your internet connection is active...\n")

        if not is_connected():
            print(Fore.RED + "[X] No internet connection detected! Please turn on the internet and try again.")
            return

        while True:
            print(Fore.CYAN + "\n[ Proxy Checker Menu ]")
            print(Fore.YELLOW + "1. Enter a single proxy (IP:PORT)")
            print(Fore.YELLOW + "2. Provide a file containing multiple proxies")
            print(Fore.LIGHTRED_EX + "3. Exit")
            choice = input(Fore.CYAN + "\n[?] Select an option (1, 2, or 3): ").strip()

            if choice == "1":
                proxy = input(Fore.CYAN + "[?] Enter the proxy (IP:PORT): ").strip()
                check_proxy(proxy)

            elif choice == "2":
                filename = input(Fore.CYAN + "[?] Enter the proxy list filename (e.g., proxies.txt): ").strip()
                try:
                    with open(filename, "r") as file:
                        proxies = [line.strip() for line in file if line.strip()]
                except FileNotFoundError:
                    print(Fore.RED + f"[X] File '{filename}' not found!")
                    continue

                print(Fore.YELLOW + f"[!] Checking {len(proxies)} proxies...\n")
                for proxy in proxies:
                    check_proxy(proxy)

            elif choice == "3":
                print(Fore.GREEN + "[✓] Exiting program. Goodbye!")
                break

            else:
                print(Fore.RED + "[X] Invalid option! Please try again.")
                continue

            cont = input(Fore.CYAN + "\n[?] Do you want to check more proxies? (yes/no): ").strip().lower()
            if cont not in ["y", "yes"]:
                print(Fore.GREEN + "[✓] Exiting program. Goodbye!")
                break

    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Interrupted by user. Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
