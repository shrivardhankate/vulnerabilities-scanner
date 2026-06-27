from concurrent.futures import ThreadPoolExecutor
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
def scan_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    result = sock.connect_ex((target_ip, port))
    
    if result == 0:
        open_ports.append(port)
    
    sock.close()
    
with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port, range (1, 66000))
    
end_time = time.time()

open_ports.sort()

print("\nOpen ports found:")

for port in open_ports:
    print(f"Port {port}")
print(f"\n Total open ports: {len(open_ports)}")
print(f"Scanning completed in {end_time - start_time:.2f} seconds.")