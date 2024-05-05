import socket
import colorama
from colorama import Fore
import threading
import os
from optparse import OptionParser
import json
parser = OptionParser()
parser.add_option("-t","--target",dest="target",help="target")
(options,args) = parser.parse_args()
try:
    with open("settings.json", "r") as check:
        testoku = json.load(check)
except FileNotFoundError:
    testoku = {
        "port": 1024,
        "show-closed-ports": False,
        "save":False
    }
    with open("settings.json", "w") as check:
        json.dump(testoku, check, indent=4)
if os.name == 'posix':
    os.system('clear')
elif os.name == 'nt':
    os.system('cls')
with open("settings.json","r") as file:
    options = json.load(file)
    portaraligi = options["port"]
    save = options["save"]
    showclosed = options["show-closed-ports"]
    if showclosed == False:
        gosterme = True
    elif showclosed == True:
        gosterme = False
colorama.init()
saveports = []
def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        s.connect((target, port))
        service = socket.getservbyport(port)
        print(Fore.GREEN + f"{port} -> OPEN ({service})")
        saveports.append(port)
    except:
        if gosterme == False:
            print(Fore.RED + f"{port} -> CLOSED")
        elif gosterme == True:
            pass
    finally:
        s.close()
def main():
    target = options.target
    print(f"{Fore.CYAN}--------------------Starting Scan---------------------------")
    start_port = 1
    end_port = portaraligi
    threads = []
    
    for port in range(start_port, end_port+1):
        thread = threading.Thread(target=scan_port, args=(target, port))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print(f"{Fore.CYAN}[+]Completed")
    if save == True:
        with open(f"{target}_scan.txt","w") as kaydet:
            kaydet.write(str(saveports))
if __name__ == "__main__":
    main()
