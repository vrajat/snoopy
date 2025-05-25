import typer
import sqlite3
from tabulate import tabulate
from app.discovery import discover_devices
from app.capture import capture_traffic
from app.db import init_db, DB

app = typer.Typer()

@app.command()
def discover():
    """Scan and store live devices on the LAN."""
    init_db()
    discover_devices()

@app.command()
def capture(ip: str, interface: str = "eth0", count: int = 100):
    """Capture traffic to/from a specific IP."""
    init_db()
    capture_traffic(ip, interface, count)

@app.command()
def summary():
    """Print traffic summary."""
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*), SUM(length) FROM traffic_log")
        total_packets, total_bytes = cursor.fetchone()
        cursor.execute("SELECT src_ip, COUNT(*) as cnt FROM traffic_log GROUP BY src_ip ORDER BY cnt DESC LIMIT 5")
        top_senders = cursor.fetchall()

        print(f"📦 Total Packets: {total_packets or 0}")
        print(f"📈 Total Bytes: {total_bytes or 0}")
        print("\nTop Talkers:")
        print(tabulate(top_senders, headers=["Source IP", "Packet Count"]))

if __name__ == "__main__":
    app()
