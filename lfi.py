#encoding: utf-8
import requests, sys, os

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

def loops(lfi_list, error, url):
	for lista in lfi_list.readlines():
		lista = url + lista.rstrip('\n')
		r = requests.get(lista)
		if error in str(r.text):
			print(bcolors.FAIL + "-] " + lista + " Invalido!" + bcolors.ENDC, end="\r")
		else:
			print(bcolors.OKGREEN + "\n[+] " + lista + " Valido!" + bcolors.ENDC)

def selec(wordlist, error, url):
	if wordlist.lower() == 's':
		lfi_list = open("list_normal.txt", "r+")
	elif wordlist.lower() == 'b':
		lfi_list = open("list_bigger.txt", "r+")
	elif wordlist.lower() == 'c':
		choose_list = input("[-] Choose the list: ")
		lfi_list = open(f"{choose_list}", "r+")
	else:
		print("Not a valid option")
	print("===============================================================================================================")
	clear()
	loops(lfi_list, error, url)

def inputs():
	url = input(f"{bcolors.OKGREEN}[+] Select the URL must be like this (https://example.com/index.php?page=):{bcolors.ENDC} ")
	wordlist = input(f"{bcolors.OKGREEN}[+] Select S for a smaller list or B for a bigger list (or C to choose your own wordlist):{bcolors.ENDC} ")
	error = input(f"{bcolors.OKGREEN}[+] Input the error that you receive:{bcolors.ENDC} ")
	selec(wordlist, error, url)

def msgload():
	clear()
	print(f"""{bcolors.FAIL}
	██╗░░░░░███████╗██╗  ░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗███████╗██████╗░
	██║░░░░░██╔════╝██║  ██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝██╔════╝██╔══██╗
	██║░░░░░█████╗░░██║  ██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░█████╗░░██████╔╝
	██║░░░░░██╔══╝░░██║  ██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
	███████╗██║░░░░░██║  ╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗███████╗██║░░██║
	╚══════╝╚═╝░░░░░╚═╝  ░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝{bcolors.ENDC}""")

	print(f"{bcolors.OKCYAN}Made by horizon.sh{bcolors.ENDC}")
	print("===============================================================================================================")
	inputs()

def clear():
    os.system('cls|clear')

try:
	msgload()
except (KeyboardInterrupt):
	print(f'{bcolors.WARNING} \n[-] You quit this session {bcolors.ENDC}')
except (Exception) as e:
	print(f'{bcolors.FAIL} \n[-] Error {bcolors.ENDC} \n\n {e}')
