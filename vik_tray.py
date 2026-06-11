import threading
import json
import time

from pystray import Icon, Menu, MenuItem
from PIL import Image

from voice.voice_module import VoiceModule
from llm.processor import LLMProcessor
from executor.main import process_command


# -------------------------
# LLM логика
# -------------------------

processor = LLMProcessor()

def vik_logic(user_text):

    command = processor.process_command(user_text)

    result = process_command(
        json.dumps(command)
    )

    return str(result)


# -------------------------
# Голосовой поток
# -------------------------

def start_voice():

    voice = VoiceModule()

    voice.start_wake_mode(
        llm_function=vik_logic
    )


# -------------------------
# Трей логика
# -------------------------

def quit_app(icon, item):

    print("Выход...")

    icon.stop()


def create_image():

    image = Image.new(
        "RGB",
        (64, 64),
        color=(0, 120, 255)
    )

    return image


def start_tray():

    icon = Icon(
        "Vik",
        create_image(),
        menu=Menu(
            MenuItem("Выход", quit_app)
        )
    )

    icon.run()


# -------------------------
# MAIN
# -------------------------

if __name__ == "__main__":

    print("🚀 Вик запускается...")

    # голос в фоне
    threading.Thread(
        target=start_voice,
        daemon=True
    ).start()

    time.sleep(1)

    # трей (главный поток)
    start_tray()