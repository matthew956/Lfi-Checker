import requests

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

print(f"""{bcolors.FAIL}
███████╗██╗░░░░░██╗  ░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗███████╗██████╗░
██╔════╝██║░░░░░██║  ██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝██╔════╝██╔══██╗
█████╗░░██║░░░░░██║  ██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░█████╗░░██████╔╝
██╔══╝░░██║░░░░░██║  ██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
██║░░░░░███████╗██║  ╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗███████╗██║░░██║
╚═╝░░░░░╚══════╝╚═╝  ░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝{bcolors.ENDC}""")

print(f"""{bcolors.OKCYAN}Made by horizon.sh{bcolors.ENDC}
==================================================================================\n""")

url = input("[-] Select the URL must be like this (https://example.com/index.php?page=): ")
wordlist = input("[-] Select S for a smaller list or B for a bigger list: ")

if wordlist.lower() == 's':
    fli_list = open("list_normal.txt", "r+")
elif wordlist.lower() == 'b':
    fli_list = open("list_bigger.txt", "r+")
else:
    print("Not a valid option")

for list in fli_list.readlines():
    url_list = url + list
    r = requests.get(url_list)
    print(r.text)
    
except KeyboardInterrupt:
	print('\033[1;31m \nGoodbye :(')
except Exception as e:
	print('\033[1;31m \nError')
