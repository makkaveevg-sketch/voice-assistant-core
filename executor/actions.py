import os
import subprocess
import webbrowser
from executor import config

def open_app(app_name, as_admin=False):
    path = config.APPS.get(app_name.lower())
    if path:
        try:
            # Если в пути есть пробел и это не системная команда, 
            # используем shell=True через subprocess для сложных путей с аргументами
            if "--" in path or "/" in path:
                operation = "runas" if as_admin else None
                # Для сложных путей с аргументами лучше подходит subprocess
                subprocess.Popen(path, shell=True)
                return f"Вик: Запускаю {app_name} с аргументами"
            else:
                # Для обычных путей и .bat оставляем надежный startfile
                operation = "runas" if as_admin else "open"
                os.startfile(path, operation)
                return f"Вик: {app_name} запущен"
        except Exception as e:
            return f"Ошибка запуска: {e}"
    return "Приложение не найдено"



def close_app(app_name):
    path = config.APPS.get(app_name.lower())
    if path:

        if "discord" in app_name.lower():
            exe_name = "Discord.exe"
        else:
            full_name = os.path.basename(path)
            exe_name = full_name.split(' ')[0] 
        
        os.system(f"taskkill /f /im {exe_name}")
        return f"Попытка закрыть {exe_name} выполнена"
    return "Не удалось найти приложение в конфиге"

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