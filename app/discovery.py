import subprocess
import re
import sqlite3
from tqdm import tqdm

from app.db import DB

def discover_devices():
    print("Scanning network with nmap...")
    proc = subprocess.Popen(["nmap", "-sn", "192.168.0.0/24"], stdout=subprocess.PIPE)
    out, _ = proc.communicate()

    ips = re.findall(r"Nmap scan report for (.+)", out.decode())
    with sqlite3.connect(DB) as conn:
        for ip in tqdm(ips, desc="Saving hosts"):
            conn.execute("INSERT OR IGNORE INTO devices (ip_address, hostname) VALUES (?, ?)", (ip, ip))
    print(f"Discovered {len(ips)} devices.")
