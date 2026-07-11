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
        service = serv_name(port)
        banner = grab_banner(port)
        parsed_banner = parse_banner(service, banner)
        open_ports.append((port, service, parsed_banner))
    sock.close()
    
def serv_name(port):
    try:
        return socket.getservbyport(port).upper()
    except OSError:
        return "Unknown"
    
def grab_banner(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((target_ip, port))
        if port == 80:
            request = (
                "GET / HTTP/1.1\r\n"
                f"Host: {target}\r\n"
                "Connection: close\r\n\r\n"
            )
            sock.send(request.encode())
        banner = sock.recv(1024).decode(errors="ignore")
        return banner.strip()
    except Exception:
        return "No banner available"
    finally:
        sock.close()
        
def parse_banner(service, banner):
    if banner == "No banner available":
        return banner
    
    if service == "SSH":
        return banner.splitlines()[0] 
    
    elif service == "HTTP":
        header = banner.split("\r\n")[0]
        
        for line in banner.split("\r\n"):
            if line.lower().startswith("server:"):
                return line.split(":", 1)[1].strip()
            
        return "Server header not found"
    
    else:
        return banner

with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port, range (1, 4000))
    
end_time = time.time()

open_ports.sort()
if open_ports:
    print("\nOpen ports found:")

    for port, service, banner in open_ports:
        print(f"[OPEN] Port {port:<5} Service: {service} Banner: {banner}")
    print(f"\nTotal open ports: {len(open_ports)}")
    print(f"Scanning completed in {end_time - start_time:.2f} seconds.")
else:
    print("\nNo open ports found.")
    print(f"Scanning completed in {end_time - start_time:.2f} seconds.")