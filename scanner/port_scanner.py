import socket
import time

target = input("Enter the target IP address or hostname: ")

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Error: Unable to resolve hostname or IP address.")
    exit()

print(f"Target: {target}...")
print(f"IP Address:{target_ip}...")
print("Scanning ports...")

start_time = time.time()

open_ports = []
for port in range(1, 135):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    
    result = sock.connect_ex((target_ip, port))
    
    if result == 0:
        print(f"[OPEN] Port {port}")
        open_ports.append(port)
        
    sock.close()
end_time = time.time()
print(f"\n Open ports: {len(open_ports)}")
print(f"Scanning completed in {end_time - start_time:.2f} seconds.")