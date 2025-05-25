import pyshark
import sqlite3
from datetime import datetime
from tqdm import tqdm

from app.db import DB

def capture_traffic(ip, interface="eth0", count=100):
    print(f"Capturing {count} packets on interface {interface} filtered for host {ip}...")
    capture = pyshark.LiveCapture(interface=interface, display_filter=f"ip.addr == {ip}")

    with sqlite3.connect(DB) as conn:
        for i, packet in enumerate(tqdm(capture.sniff_continuously(packet_count=count))):
            try:
                timestamp = packet.sniff_time.isoformat()
                src_ip = packet.ip.src
                dst_ip = packet.ip.dst
                proto = packet.transport_layer or 'N/A'
                length = int(packet.length)
                info = str(packet.highest_layer)
                conn.execute("""
                    INSERT INTO traffic_log (timestamp, src_ip, dst_ip, protocol, length, info)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (timestamp, src_ip, dst_ip, proto, length, info))
            except Exception as e:
                print(f"Packet parse error: {e}")
