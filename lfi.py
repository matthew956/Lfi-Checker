#encoding: utf-8
import requests, sys, os, argparse, threading

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def request_thread(lista, error, i, total_lines, success_event):
    r = requests.get(lista)
    if error in str(r.text):
        print(bcolors.FAIL + f"\r[{r.status_code}] {lista} {bcolors.BOLD + bcolors.ENDC}({i+1}/{total_lines})", end='\x1b[1K\r')
    else:
        print(bcolors.OKGREEN + f"[PAYLOAD SUCCESS] " + lista + bcolors.ENDC)
        success_event.set()  # signal that a payload success has been found

def loops(lfi_list, error, url, thread_num):
    total_lines = sum(1 for _ in lfi_list)  # count total lines in the file
    lfi_list.seek(0)  # reset file pointer to the beginning

    success_event = threading.Event()  # create a shared event

    threads = []
    for i, lista in enumerate(lfi_list):
        lista = url + lista.rstrip('\n')
        t = threading.Thread(target=request_thread, args=(lista, error, i, total_lines, success_event))
        threads.append(t)
        t.start()

        # Limit the number of threads to the specified thread_num
        while len(threads) >= thread_num:
            for t in threads:
                if not t.is_alive():
                    threads.remove(t)
                    break

        if success_event.is_set():  # check if a payload success has been found
            break

    # wait for all threads to finish
    for t in threads:
        t.join()

    if success_event.is_set():  # if a payload success was found, exit the program
        sys.exit(0)

def selec(wordlist, error, url, thread_num):
    if wordlist.lower() == 's':
        lfi_list = open("list_normal.txt", "r+")
    elif wordlist.lower() == 'b':
        lfi_list = open("list_bigger.txt", "r+")
    elif wordlist.lower() == 'c':
        choose_list = input("Choose the list: ")
        lfi_list = open(f"{choose_list}", "r+")
    else:
        print("Not a valid option")
        return

    loops(lfi_list, error, url, thread_num)

def msgload(url, wordlist, error, thread_num):
    clear()
    print("""
 __  ___ __      __               __               
|  .'  _|__.----|  |--.-----.----|  |--.-----.----.
|  |   _|  |  __|     |  -__|  __|    <|  -__|   _|
|__|__| |__|____|__|__|_____|____|__|__|_____|__|                                           
    """)
    print(f"{bcolors.OKGREEN}Made by horizon.sh{bcolors.ENDC}")
    print("\n[!] legal disclaimer: Usage of LFIchecker for attacking targets without prior mutual consent is illegal. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.")
    print("\n==========================")
    print(f"{bcolors.OKGREEN}URL:{bcolors.ENDC} {url}")
    print(f"{bcolors.OKGREEN}WORDLIST:{bcolors.ENDC} {wordlist}")
    print(f"{bcolors.OKGREEN}ERROR STR:{bcolors.ENDC} {error}")
    print(f"{bcolors.OKGREEN}THREADS:{bcolors.ENDC} {thread_num}")
    print("==========================")
    print("\n")
    selec(wordlist, error, url, thread_num)

def clear():
    os.system('clear|cls')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LFI checker')
    parser.add_argument('-u', '--url', help='URL to check', required=True)
    parser.add_argument('-w', '--wordlist', help='Wordlist to use (S, B, or C)', required=True)
    parser.add_argument('-e', '--error', help='Error to look for', required=True)
    parser.add_argument('-t', '--threads', help='Number of threads. Default: 2', required=False, default=2, type=int)
    args = parser.parse_args()
    try:
        msgload(args.url, args.wordlist, args.error, args.threads)
    except (KeyboardInterrupt):
        print(f'{bcolors.WARNING} \n[QUIT] You quit this session {bcolors.ENDC}')
    except (Exception) as e:
        print(f'{bcolors.FAIL} \n[ERROR] An error has occured {bcolors.ENDC} \n\n {e}')
