#!/bin/bash
# install_termux.sh

echo "📱 Installing NIGHTMARE DDoS Ripper on Termux..."

# Update and upgrade
pkg update && pkg upgrade -y

# Install Python and basic tools
pkg install -y python python-pip git curl wget

# Install core dependencies
pip install --upgrade pip
pip install requests aiohttp psutil cryptography fake-useragent

# Install platform-specific dependencies
pip install colorama blessed tqdm rich

# Install optional dependencies (if needed)
pip install dnspython pysocks cloudscraper

echo "✅ Installation complete on Termux!"
echo "🚀 Run: python3 nightmare_universal.py"
