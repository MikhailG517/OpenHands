#!/usr/bin/env python3
"""
Скрипт развертывания OpenHands Canvas на VPS 82.25.56.194
Домен: https://ai.iotrus.ru
"""
import paramiko
import os
from pathlib import Path

# Настройки подключения
SERVER_HOST = "82.25.56.194"
SERVER_USER = "root"
SSH_KEY_PATH = "E:/AI/ServerPC/.secrets/ssh_VPS_clean"
DEPLOY_DIR = "/opt/openhands_canvas"
LOCAL_DIR = "E:/AI/ServerPC/openhands_official/deploy"

def connect_ssh():
    """Подключение к серверу через SSH"""
    print(f"📡 Подключение к {SERVER_HOST}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Загружаем ключ
    key = paramiko.Ed25519Key.from_private_key_file(SSH_KEY_PATH)
    ssh.connect(SERVER_HOST, username=SERVER_USER, pkey=key)
    print("✅ Подключено к серверу")
    return ssh

def run_ssh_command(ssh, command, description=""):
    """Выполнение команды на сервере"""
    if description:
        print(f"🔧 {description}")
    stdin, stdout, stderr = ssh.exec_command(command)
    exit_code = stdout.channel.recv_exit_status()
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    if output:
        print(output)
    if error and exit_code != 0:
        print(f"⚠️ Ошибка: {error}")
    
    return exit_code, output, error

def upload_file_sftp(ssh, local_path, remote_path):
    """Загрузка файла через SFTP"""
    sftp = ssh.open_sftp()
    try:
        sftp.put(local_path, remote_path)
        print(f"✅ Загружен: {remote_path}")
    finally:
        sftp.close()

def main():
    print("🚀 Начало развертывания OpenHands Canvas на ai.iotrus.ru")
    print("=" * 70)
    
    ssh = connect_ssh()
    
    try:
        # Шаг 1: Создание директории
        run_ssh_command(ssh, f"mkdir -p {DEPLOY_DIR}", "Создание директории развертывания")
        
        # Шаг 2: Загрузка docker-compose.yml
        print("\n📤 Загрузка конфигурационных файлов...")
        upload_file_sftp(ssh, 
                        f"{LOCAL_DIR}/docker-compose.yml", 
                        f"{DEPLOY_DIR}/docker-compose.yml")
        
        # Шаг 3: Загрузка nginx конфигурации для системного nginx
        upload_file_sftp(ssh, 
                        f"{LOCAL_DIR}/ai.iotrus.ru.conf", 
                        "/etc/nginx/sites-available/ai.iotrus.ru.conf")
        
        # Шаг 3.1: Создание симлинка для активации конфига
        run_ssh_command(ssh, 
                       "ln -sf /etc/nginx/sites-available/ai.iotrus.ru.conf /etc/nginx/sites-enabled/ai.iotrus.ru.conf",
                       "Активация nginx конфигурации")
        
        # Шаг 3.2: Проверка конфигурации nginx
        run_ssh_command(ssh, "nginx -t", "Проверка конфигурации nginx")
        
        # Шаг 4: Остановка старых контейнеров
        print("\n🛑 Остановка старых контейнеров...")
        run_ssh_command(ssh, f"cd {DEPLOY_DIR} && docker compose down || true")
        
        # Шаг 5: Загрузка образов
        print("\n📦 Загрузка Docker образов...")
        run_ssh_command(ssh, 
                       f"cd {DEPLOY_DIR} && docker compose pull", 
                       "Загрузка ghcr.io/all-hands-ai/openhands:0.9")
        
        # Шаг 6: Запуск контейнеров
        print("\n🚀 Запуск контейнеров...")
        run_ssh_command(ssh, 
                       f"cd {DEPLOY_DIR} && docker compose up -d",
                       "Запуск OpenHands Canvas")
        
        # Шаг 6.1: Перезагрузка nginx для применения конфига
        run_ssh_command(ssh, "systemctl reload nginx", "Перезагрузка nginx")
        
        # Шаг 7: Ожидание готовности
        print("\n⏳ Ожидание готовности сервисов...")
        import time
        time.sleep(10)
        
        # Шаг 8: Проверка статуса
        print("\n📊 Проверка статуса контейнеров...")
        run_ssh_command(ssh, f"cd {DEPLOY_DIR} && docker compose ps")
        
        # Шаг 9: Проверка логов
        print("\n📋 Последние логи OpenHands:")
        run_ssh_command(ssh, f"cd {DEPLOY_DIR} && docker compose logs --tail=20 openhands")
        
        # Шаг 10: Проверка доступности
        print("\n🔍 Проверка доступности...")
        exit_code, output, _ = run_ssh_command(ssh, 
                                               "curl -s http://localhost:3000/alive || echo 'Health check failed'")
        
        print("\n🔍 Проверка через домен...")
        run_ssh_command(ssh, "curl -Ik https://ai.iotrus.ru/ | head -5 || echo 'Domain check failed'")
        
        print("\n" + "=" * 70)
        print("✅ РАЗВЕРТЫВАНИЕ ЗАВЕРШЕНО")
        print("=" * 70)
        print("\n🌐 OpenHands Canvas доступен по адресам:")
        print("   • https://ai.iotrus.ru (основной)")
        print("   • http://82.25.56.194:3000 (прямой доступ)")
        print("\n📊 Мониторинг:")
        print(f"   docker compose -f {DEPLOY_DIR}/docker-compose.yml ps")
        print(f"   docker compose -f {DEPLOY_DIR}/docker-compose.yml logs -f openhands")
        print("\n🔄 Управление:")
        print(f"   cd {DEPLOY_DIR}")
        print("   docker compose restart")
        print("   docker compose down")
        print("   docker compose up -d")
        
    except Exception as e:
        print(f"\n❌ Ошибка развертывания: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("\n🔌 Подключение к серверу закрыто")

if __name__ == "__main__":
    main()
