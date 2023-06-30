
from scapy.all import sniff
from scapy.layers.inet import IP, TCP
from threading import Thread
import time
import os
class Verification:
    def __init__(self, path):
        self.suspicious = False
        self.path = path
        self.check()
        if not self.suspicious:
            print("No virus detected")
        else:
            print("Virus detected")
    def check(self):
        # Get all the files in the documents folder
        path = os.path.abspath("../../tests-files")
        files = os.listdir(path)
        # Get the size and content of each file
        files_content = []
        for file in files:
            object = {
                "size": os.stat(path + "\\" + file).st_size,
                "content": open(path + "\\" + file, "rb").read(),
                "name": file,
                "path": os.path.abspath(path + "\\" + file)
            }
            files_content.append(object)



        # Create a thread to analyze the network traffic
        analyze_thread = Thread(target=self.analyze_network_traffic, daemon=True)
        analyze_thread.start()

        # Get the executable file that we want to run to test if it's a virus
        exectutable = os.path.abspath(self.path)
        # Run the executable
        daemon = Thread(target=os.system, args=(exectutable,), daemon=True)
        daemon.start()
        time.sleep(30)

        # Stop the network traffic analysis
        analyze_thread.join()

        # Test if the files have changed
        for file in files_content:
            # Check if the file have been deleted
            if not os.path.exists(file["path"]):
                print(f"File {file['name']} have been deleted")
                self.suspicious = True
                return
            else:
                # Check if the file size have changed
                if os.stat(file["path"]).st_size != file["size"]:
                    print(f"File {file['name']} have been modified")
                    self.suspicious = True
                    return
                # Check if the file content have changed
                elif open(file["path"], "rb").read() != file["content"]:
                    print(f"File {file['name']} have been modified")
                    self.suspicious = True
                    return
        return


    def analyze_network_traffic(self):
        # Sniff network traffic for a certain duration
        packets = sniff(timeout=25)

        # Analyze the captured packets
        for packet in packets:
            if TCP in packet:
                # Perform your analysis based on TCP packets
                # You can access packet fields and perform various checks here
                # Example: Check if the packet is a SYN flood attack
                if packet[TCP].flags == 'S':
                    print("SYN flood attack detected!")

            if IP in packet:
                source_ip = packet[IP].src
                destination_ip = packet[IP].dst

                # Perform verifications based on source and destination IP addresses
                # Example: Check if the packet is coming from or going to a suspicious IP
                suspicious_ips = ["192.168.0.1", "10.0.0.2"]
                if source_ip in suspicious_ips or destination_ip in suspicious_ips:
                    print(f"Suspicious network traffic detected with IP: {source_ip} -> {destination_ip}")
                    self.suspicious = True

                # Perform additional verifications or analysis as needed
                # Example: Check for specific protocols or ports being used
                if packet.haslayer(TCP):
                    source_port = packet[TCP].sport
                    destination_port = packet[TCP].dport

                    # Example: Check if traffic is being sent to a known malicious port
                    malicious_ports = [8080, 4444, 9999]
                    if destination_port in malicious_ports:
                        print(
                            f"Malicious port traffic detected: {source_ip}:{source_port} -> {destination_ip}:{destination_port}")
                        self.suspicious = True
