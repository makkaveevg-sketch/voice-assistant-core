import os

def get_path(path):
    return os.path.expandvars(path)


APPS = {
    "discord": get_path(r"%AppData%\Microsoft\Windows\Start Menu\Programs\Discord Inc\Discord.lnk"),
    "yandex": r"C:\Program Files\Yandex\YandexBrowser\Application\browser.exe",
    "vscode": get_path(r"%LocalAppData%\Programs\Microsoft VS Code\Code.exe"),
    "steam": get_path(r"%ProgramFiles(x86)%\Steam\Steam.exe"),
    "zapret": r"C:\Users\Admin\Desktop\ds\general (ALT).bat",
    "zapret9": r"C:\Users\Admin\Desktop\ds\general (ALT9).bat"
}