import time
import math
import threading
from collections import defaultdict
from scapy.all import sniff
import tkinter as tk
from tkinter import StringVar, scrolledtext, IntVar
import os
import socket


THRESHOLD = 1000
DETECTION_WINDOW = 60
UPDATE_INTERVAL = 0.01
IP_COUNTER = defaultdict(int)
DETECTED_IPS = {}
packets_detected = 0

def LOCLAL_IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip


def processdapacket(packet):
    global packets_detected
    if packet.haslayer("IP"):
        packets_detected += 1
        src_ip = packet["IP"].src
        IP_COUNTER[src_ip] += 1

def packet_smeller():
    while running:
        try:
            sniff(filter="ip", prn=processdapacket, timeout=DETECTION_WINDOW, store=0)
        except Exception as e:
            output.insert(tk.END, f"Error: {e}\n")

def detect_ddos():
    local_ip = LOCLAL_IP()
    ip_counter_copy = IP_COUNTER.copy()  # dictionary copy
    for ip, count in ip_counter_copy.items():
        if ip == local_ip:
            continue
        if count > THRESHOLD and ip not in DETECTED_IPS:
            DETECTED_IPS[ip] = IntVar(value=0)
            ip_row = detected_frame.grid_size()[1]
            lbl = tk.Label(detected_frame, text=ip)
            lbl.grid(row=ip_row, column=0)
            chk = tk.Checkbutton(detected_frame, text="Block", variable=DETECTED_IPS[ip], command=lambda ip=ip: block_ip(ip))
            chk.grid(row=ip_row, column=1)
    IP_COUNTER.clear()


def block_ip(ip):
    if DETECTED_IPS[ip].get():
        # FIREWALL BLOCK IP
        os.system(f"netsh advfirewall firewall add rule name=\"Block_{ip}\" dir=in action=block remoteip={ip}")
    else:
        # UNBLOCK
        os.system(f"netsh advfirewall firewall delete rule name=\"Block_{ip}\" remoteip={ip}")

def update_gui():
    while running:
        elapsed_time = time.time() - start_time
        time_string.set(f"{elapsed_time:.2f} seconds (PDT)...  Packets smelled: {packets_detected}")
        detect_ddos()
        time.sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    running = True
    start_time = time.time()

    # GUI
    root = tk.Tk()
    root.title("ddos detector")

    time_string = StringVar(root)
    time_label = tk.Label(root, textvariable=time_string)
    time_label.pack(pady=10)

    output = scrolledtext.ScrolledText(root, width=50, height=15)
    output.pack(pady=10)

    detected_frame = tk.Frame(root)
    detected_frame.pack(pady=10)
    tk.Label(detected_frame, text="Detected IP addresses").grid(row=0, column=0)
    tk.Label(detected_frame, text="block toggle").grid(row=0, column=1)

    stop_button = tk.Button(root, text="stop", command=lambda: root.destroy())
    stop_button.pack(pady=10)

    # THREADS
    sniffer_thread = threading.Thread(target=packet_smeller)
    sniffer_thread.start()
    
    gui_update_thread = threading.Thread(target=update_gui)
    gui_update_thread.start()

    root.protocol("WM_DELETE_WINDOW", lambda: exit(0))
    root.mainloop()

    running = False
