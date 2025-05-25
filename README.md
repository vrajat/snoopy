# Snoopy

Snoopy is a lightweight, dockerized CLI tool to scan your LAN and capture traffic from selected devices. Built with:

- Typer for CLI UX
- Pyshark for packet capture
- tqdm for progress bars
- uv for fast dependency installation
- SQLite for embedded DB

## 🔧 Install (Local)

```bash
uv pip install -r requirements.txt
python app/cli.py --help
```

## 🐳 Docker

```bash
docker build -t snoopy .
docker run --cap-add=NET_ADMIN --net=host -v $PWD:/data snoopy discover
```

## 🧪 Example Usage

```bash
python app/cli.py discover
python app/cli.py capture --ip 192.168.0.118 --interface eth0 --count 200
python app/cli.py summary
```

Database: `network_devices.db`
