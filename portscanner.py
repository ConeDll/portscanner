import socket
import colorama
from colorama import Fore
import threading
import os
from optparse import OptionParser
import json

parser = OptionParser()
parser.add_option("-t", "--target", dest="target", help="target")
(options, args) = parser.parse_args()

if not options.target:
    print("Error: Target IP address not provided.")
    parser.print_help()
    exit()

try:
    with open("settings.json", "r") as check:
        settings = json.load(check)
except FileNotFoundError:
    settings = {
        "port": 1024,
        "show-closed-ports": False,
        "save": False
    }
    with open("settings.json", "w") as check:
        json.dump(settings, check, indent=4)

os.system('cls' if os.name == 'nt' else 'clear')

portaraligi = settings["port"]
save = settings["save"]
showclosed = settings["show-closed-ports"]
gosterme = showclosed

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
    except Exception as e:
        if gosterme:
            print(Fore.RED + f"{port} -> CLOSED")
    finally:
        s.close()

def main():
    target = options.target
    print(f"{Fore.CYAN}--------------------Starting Scan---------------------------")
    start_port = 1
    end_port = portaraligi
    threads = []
    
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(target, port))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(f"{Fore.CYAN}[+]Completed")

    if save:
        with open(f"{target}_scan.txt", "w") as kaydet:
            kaydet.write(str(saveports))

if __name__ == "__main__":
    main()
