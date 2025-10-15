#!/bin/bash
# install_linux.sh

echo "🐧 Installing NIGHTMARE DDoS Ripper on Linux..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3 python3-pip python3-venv git curl wget
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev

# Create virtual environment
python3 -m venv nightmare-env
source nightmare-env/bin/activate

# Install core dependencies
pip install --upgrade pip
pip install requests aiohttp psutil cryptography fake-useragent

# Linux-specific dependencies
pip install python-prctl resource uvloop

# Performance optimization
pip install orjson ujson numpy

# Optional dependencies
pip install dnspython pysocks cloudscraper scapy

echo "✅ Installation complete on Linux!"
echo "🚀 Run: source nightmare-env/bin/activate && python3 nightmare_universal.py"
