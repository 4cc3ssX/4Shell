import socket
import sys
 
def Main():
        host = '127.0.0.1'
        port = 5000
         
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
                s.connect((host,port))
        except ConnectionRefusedError:
                print("[\033[033m ERROR \033[00m] Cannot connect to shell. \n\t[\033[033m Err \033[00m: Connection refused! ]")
                sys.exit()
        print("[\033[032m OK \033[00m]Shell has been connected with %s" % host)
        try:
                shell = input("%s~$\033[033m" % host)
                
                while shell != 'q':
                        s.send(shell.encode())

                        data = s.recv(4096).decode()
                        print('\t')
                        print ('\033[00m\033[030m'+data+'\033[00m')
                        shell = input("\033[00m%s~$\033[033m" % host)
        except KeyboardInterrupt:
                print("\n\033[00m[\033[033m ERROR \033[00m] Exiting the shell. \n\t[\033[033m Err \033[00m: Keyboard Interrupt! ]")
                sys.exit()
        s.close()
 
if __name__ == '__main__':
    Main()