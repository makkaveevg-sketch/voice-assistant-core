import os
import subprocess
import webbrowser
import config

def open_app(app_name):
    path = config.APPS.get(app_name.lower())
    if path:
        subprocess.Popen(path, shell=True)
        return f"Запускаю {app_name}"
    return f"Приложение {app_name} не настроено в config.py"

def close_app(app_name):
    # Команда taskkill принудительно закрывает процесс по имени
    # /F - принудительно, /IM - имя образа (exe файла)
    # Мы берем имя из конфига (например, 'notepad.exe')
    path = config.APPS.get(app_name.lower())
    if path:
        exe_name = path.split('\\')[-1].split(' ')[0] # вытаскиваем только имя файла .exe
        os.system(f"taskkill /f /im {exe_name}")
        return f"Закрываю {app_name}"
    return "Не удалось определить имя процесса для закрытия"

def open_url(url):
    webbrowser.open(url)
    return f"Открываю сайт: {url}"

def shutdown_pc():
    # /s - выключение, /t 1 - через 1 секунду
    os.system("shutdown /s /t 1")
    return "Выключаю компьютер..."

def restart_pc():
    # /r - перезагрузка
    os.system("shutdown /r /t 1")
    return "Перезагружаю компьютер..."