#encoding: utf-8
import sys, os, argparse, threading, json, subprocess
from queue import Queue

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

try:
    import requests
except ImportError:
    print(f"{bcolors.FAIL}requests not found. Installing...{bcolors.ENDC}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests


def clear():
    # Clears the terminal screen depending on OS
    os.system('cls' if os.name == 'nt' else 'clear')

def request_thread(url, path, error, i, total_lines, success_event, lock, log_file, proxies, headers):
    # Executes a single HTTP request and logs result based on response content
    full_url = url + path.strip()
    try:
        r = requests.get(full_url, timeout=10, proxies=proxies, headers=headers)
        if error in r.text:
            with lock:
                print(f"{bcolors.FAIL}[{r.status_code}] {full_url} {bcolors.BOLD + bcolors.ENDC}({i+1}/{total_lines})", end='\x1b[1K\r')
        else:
            with lock:
                print(f"{bcolors.OKGREEN}[PAYLOAD SUCCESS] {full_url}{bcolors.ENDC}")
            success_event.set()
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[SUCCESS] {full_url} ({r.status_code})\n")
    except requests.exceptions.ProxyError as e:
        with lock:
            print(f"{bcolors.FAIL}[PROXY ERROR] Could not connect to proxy: {e}{bcolors.ENDC}")
        sys.exit(1)
    except requests.RequestException as e:
        with lock:
            print(f"{bcolors.WARNING}[REQUEST FAILED] {full_url} - {e}{bcolors.ENDC}")

def run_threads(wordlist_lines, error, url, thread_num, proxies, headers):
    # Manages threading and task queue to perform concurrent requests
    total_lines = len(wordlist_lines)
    success_event = threading.Event()
    log_file = "found_payloads.log"
    lock = threading.Lock()

    queue = Queue()
    for line in wordlist_lines:
        queue.put(line)

    def worker():
        while not queue.empty() and not success_event.is_set():
            i = total_lines - queue.qsize()
            path = queue.get()
            request_thread(url, path, error, i, total_lines, success_event, lock, log_file, proxies, headers)
            queue.task_done()

    threads = []
    for _ in range(thread_num):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)

    queue.join()

    if success_event.is_set():
        sys.exit(0)

def load_wordlist(option):
    # Loads a wordlist file based on user-selected preset or custom filename
    if option.lower() == 's':
        path = "list_normal.txt"
    elif option.lower() == 'b':
        path = "list_bigger.txt"
    elif option.lower() == 'c':
        path = input("Choose the list: ")
    else:
        print("Not a valid option")
        sys.exit(1)

    if not os.path.isfile(path):
        print(f"{bcolors.FAIL}[ERROR] Wordlist not found: {path}{bcolors.ENDC}")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.readlines()

def msgload(url, wordlist_option, error, thread_num, proxy_str, headers_str):
    # Displays UI and prepares proxy/header data before triggering the main scan logic
    clear()
    print("""
 __  ___ __      __               __               
|  .'  _|__.----|  |--.-----.----|  |--.-----.----.
|  |   _|  |  __|     |  -__|  __|    <|  -__|   _|
|__|__| |__|____|__|__|_____|____|__|__|_____|__|                                            
    """)
    print(f"{bcolors.OKGREEN}Made by horizon.sh and zk{bcolors.ENDC}")
    print("\n[!] legal disclaimer: Usage of LFIchecker for attacking targets without prior mutual consent is illegal. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.")
    print("\n==========================")
    print(f"{bcolors.OKGREEN}URL:{bcolors.ENDC} {url}")
    print(f"{bcolors.OKGREEN}WORDLIST:{bcolors.ENDC} {wordlist_option}")
    print(f"{bcolors.OKGREEN}ERROR STR:{bcolors.ENDC} {error}")
    print(f"{bcolors.OKGREEN}THREADS:{bcolors.ENDC} {thread_num}")
    print(f"{bcolors.OKGREEN}PROXIES:{bcolors.ENDC} {proxy_str or 'None'}")
    print(f"{bcolors.OKGREEN}HEADERS:{bcolors.ENDC} {headers_str or 'None'}")
    print("==========================\n")

    proxies = json.loads(proxy_str) if proxy_str else None
    headers = json.loads(headers_str) if headers_str else None

    wordlist_lines = load_wordlist(wordlist_option)
    run_threads(wordlist_lines, error, url, thread_num, proxies, headers)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LFI checker')
    parser.add_argument('-u', '--url', help='URL to check', required=True)
    parser.add_argument('-w', '--wordlist', help='Wordlist to use (S, B, or C)', required=True)
    parser.add_argument('-e', '--error', help='Error to look for', required=True)
    parser.add_argument('-t', '--threads', help='Number of threads. Default: 2', default=2, type=int)
    parser.add_argument('--proxy', help='Proxy dictionary as JSON string. Example: "{\"http\": \"http://127.0.0.1:8080\"}"')
    parser.add_argument('--headers', help='Headers dictionary as JSON string. Example: "{\"User-Agent\": \"CustomAgent\"}"')
    args = parser.parse_args()
    try:
        msgload(args.url, args.wordlist, args.error, args.threads, args.proxy, args.headers)
    except KeyboardInterrupt:
        print(f'{bcolors.WARNING}\n[QUIT] You quit this session.{bcolors.ENDC}')
    except Exception as e:
        print(f'{bcolors.FAIL}\n[ERROR] An error has occurred {bcolors.ENDC}\n\n{e}')
