import socket
import sys
import os
 
def Main():
        host = '127.0.0.1'
        port = 4723
         
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
                s.connect((host,port))
        except ConnectionRefusedError:
                print("[\033[033m ERROR \033[00m] Cannot connect to shell. \n\t[\033[033m Err \033[00m: Connection refused! ]")
                sys.exit()
        print("[\033[032m OK \033[00m] Shell has been connected with %s" % host)
        try:
            s.send("whoami".encode())
            user = s.recv(1024).decode()
            if user == "root":
                    print("[ \033[031mROOT\033[00m ] Shell is connected as root!")
                    euid = 0
            else:
                    euid = 1
            prompt(euid,host)
            while not shell:
                prompt(euid,host)
            while shell != 'exit':
                s.send(shell.encode())
                data = s.recv(4096).decode()
                if not data: break
                print ('\033[00m\033[032m%s\033[00m' % (data))
                prompt(euid,host)
        except KeyboardInterrupt:
                print("\n\033[00m[\033[033m ERROR \033[00m] Exiting the shell. \n\t[\033[033m Err \033[00m: Keyboard Interrupt! ]")
                sys.exit()
        s.close()
def prompt(euid, host):
    global shell
    shell = input("\033[00m%s~%s \033[033m" % (host, "#" if euid==0 else "$"))
if __name__ == '__main__':
    Main()
