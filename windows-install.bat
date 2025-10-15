@echo off
REM install_windows.bat

echo 🖥️ Installing NIGHTMARE DDoS Ripper on Windows...

python -m pip install --upgrade pip

REM Core dependencies
pip install requests aiohttp psutil cryptography fake-useragent

REM Windows-specific dependencies
pip install colorama pywin32 windows-curses

REM Performance dependencies
pip install uvloop orjson ujson

REM Optional dependencies
pip install dnspython pysocks cloudscraper scapy

echo ✅ Installation complete on Windows!
echo 🚀 Run: python nightmare_universal.py
