from scapy.all import *

output_file = open("tcp_log.txt", "a")

def log_tcp(packet):
    # Check if the packet has a TCP layer
    if packet.haslayer(TCP):
        # Check if the packet is going to or from the specified IP address
        if packet[IP].src == ip_address or packet[IP].dst == ip_address:
            # Log the packet information to the output file
            log_str = "Timestamp: " + str(packet.time) + " | Source IP: " + packet[IP].src + " | Destination IP: " + packet[IP].dst + " | Source Port: " + str(packet[TCP].sport) + " | Destination Port: " + str(packet[TCP].dport) + " | Flags: " + str(packet[TCP].flags)
            print(log_str)
            output_file.write(log_str + "\n")

# Ask the user for the IP address to monitor
ip_address = input("Enter the IP address to monitor: ")

# Start sniffing packets on your network interface
sniff(filter="tcp", prn=log_tcp)
output_file.close()
