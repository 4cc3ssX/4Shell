import socket
import sys
import os
from colorama import Fore,Back

def Main():
        host = '127.0.0.1'
        port = 4723
         
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
                s.connect((host,port))
        except ConnectionRefusedError:
                resp(1,"Connection refused!")
                sys.exit()
        resp(0,"Shell has been connected with %s" % host)
        try:
            s.send("whoami".encode())
            user = s.recv(1024).decode().strip()
            if user == "root":
                    print(f"[ {Fore.RED}ROOT{Fore.RESET} ] Shell is connected as root!")
                    euid = 0
            else:
                    print(f"[ {Fore.BLUE}USER{Fore.RESET} ] Shell is connect as user!")
                    euid = 1
            prompt(user,euid,host,s)
            while shell != 'exit':
                s.send(shell.encode())
                data = s.recv(4096).decode().strip()
                if data:
                    print(f'{Fore.RESET}{Fore.GREEN}{data}{Fore.RESET}')
                prompt(user,euid,host,s)
        except KeyboardInterrupt:
                resp(1,"Keyboard Interrupt!")
                sys.exit(0)
        s.close()
def resp(typo,message):
    if typo == 1:
        print(f"{Fore.RESET}[ {Fore.RED}ERROR{Fore.RESET} ] Exiting the shell. \n\t[\033[033m Err \033[00m: {message} ]")
    elif typo == 0:
        print(f"{Fore.RESET}[ {Fore.GREEN}OK{Fore.RESET} ] {message}")
def prompt(user,euid, host, s):
    global shell
    s.send("pwd".encode())
    pwd = s.recv(1024).decode().strip()
    shell = input("\033[00m%s@%s~%s%s " % (Fore.RED+user+Fore.RESET,Fore.YELLOW+host+Fore.RESET, Fore.CYAN+pwd+Fore.RESET, "#" if euid==0 else "$"))
    while not shell:
        prompt(user,euid,host,pwd)
if __name__ == '__main__':
    Main()
