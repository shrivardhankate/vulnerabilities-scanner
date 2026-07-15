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

vulnerability_db = {
    "Dropbear": {
        "2020.80": {
            "cve": "CVE-2020-36254",
            "severity": "High",
            "cvss": 8.8,
            "description": "Example vulnerability for learning.",
            "recommendation": "Upgrade to the latest patched version."
        }
    }
}

def scan_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    result = sock.connect_ex((target_ip, port))
    if result == 0:
        service = serv_name(port)
        banner = grab_banner(port)
        parsed_banner = parse_banner(service, banner)
        software, version = extract_version(service, parsed_banner)
        vulnerability = lookup_vulnerability(software, version)
        open_ports.append({
            "port": port,
            "service": service,
            "banner": parsed_banner,
            "software": software,
            "version": version,
            "vulnerability": vulnerability
        })
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
        header = banner.split("\r\n\r\n")[0]
        
        for line in header.split("\r\n"):
            if line.lower().startswith("server:"):
                return line.split(":", 1)[1].strip()
            
        return "Server header not found"
    
    else:
        return banner

def extract_version(service, banner):
    if banner == "No banner available":
        return "Unknown", "Unknown"
    if service == "SSH":
        version_line = banner.split("-")[-1]
        parts = version_line.split("_")
        if len(parts) >= 2:
            software = parts[0].capitalize()
            version = parts[1]
        else:
            software = "Unknown"
            version = "Unknown"
    else:
        software = "Unknown"
        version = "Unknown"

    return software, version

def lookup_vulnerability(software, version):
    
    software_data = vulnerability_db.get(software)
    
    if software_data is None:
        return None
    
    version_data = software_data.get(version)
    if version_data is None:
        return version_data
    
    return version_data

with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port, range (1, 4000))
    
end_time = time.time()

open_ports.sort(key=lambda x: x["port"])
if open_ports:
    print("\nOpen ports found:")

    for port_info in open_ports:
        vuln = port_info['vulnerability']
        print(
    f"\n[OPEN] Port {port_info['port']}\n"
    f"Service : {port_info['service']}\n"
    f"Banner  : {port_info['banner']}\n"
    f"Software: {port_info['software']}\n"
    f"Version : {port_info['version']}\n"
    f"Vulnerability: {vuln['cve'] if port_info['vulnerability'] else 'None'}"
    f"\nCVSS Score: {vuln['cvss'] if port_info['vulnerability'] else 'N/A'}"
    f"\nSeverity: {vuln['severity'] if port_info['vulnerability'] else 'N/A'}"
    f"\nDescription: {vuln['description'] if port_info['vulnerability'] else 'N/A'}"
    f"\nRecommendation: {vuln['recommendation'] if port_info['vulnerability'] else 'N/A'}"
    )
    print(f"\nTotal open ports: {len(open_ports)}")
    print(f"Scanning completed in {end_time - start_time:.2f} seconds.")
else:
    print("\nNo open ports found.")
    print(f"Scanning completed in {end_time - start_time:.2f} seconds.")
    