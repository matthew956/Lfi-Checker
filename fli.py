import requests
import argparse

parser = argparse.ArgumentParser(description='Checks for FLI vulnerabilities', epilog='Made by horizon.sh')
parser.add_argument('-u', '--url', type=str, required=True, help='Checks for url')
parser.add_argument('-s', '--show', action='store_true', help='Show all urls, failed and not failed.')
args = parser.parse_args()

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

url = str(args.url)
fli_list = open("list.txt", "r+")

print(f"""{bcolors.FAIL}
███████╗██╗░░░░░██╗  ░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗███████╗██████╗░
██╔════╝██║░░░░░██║  ██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝██╔════╝██╔══██╗
█████╗░░██║░░░░░██║  ██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░█████╗░░██████╔╝
██╔══╝░░██║░░░░░██║  ██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
██║░░░░░███████╗██║  ╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗███████╗██║░░██║
╚═╝░░░░░╚══════╝╚═╝  ░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝{bcolors.ENDC}""")

print(f"""{bcolors.OKCYAN}Made by horizon.sh{bcolors.ENDC}
==================================================================================\n""")

for list in fli_list.readlines():
    url_list = url + list
    r = requests.get(url_list)
    print(r.text)
    #if r.text == 200:
      #print(str(url_list))
      






    #if args.show == True:
        #if r.status_code == 200:
            #print("Success! " + url_list)
        #else:
            #print("Failed! " + url_list)
    #else:
        #if r.status_code == 200:
            #print("Success! " + url_list)