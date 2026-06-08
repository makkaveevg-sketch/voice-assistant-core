import os
import subprocess
import webbrowser
import config

def open_app(app_name, as_admin=False):
    path = config.APPS.get(app_name.lower())
    if path:
        try:
            # Если as_admin=True, используем операцию 'runas' (запрос прав админа)
            # Если False, используем обычное открытие
            operation = 'runas' if as_admin else 'open'
            
            # Получаем папку файла, чтобы батник не "терял" свои ресурсы
            cwd = os.path.dirname(path)
            
            os.startfile(path, operation, cwd=cwd)
            return f"Выполнено: {app_name} запущен (Админ: {as_admin})"
        except Exception as e:
            return f"Ошибка при запуске: {e}"
    return f"Приложение {app_name} не найдено в конфиге"

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