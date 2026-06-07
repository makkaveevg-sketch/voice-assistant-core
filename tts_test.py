import os
import time
from gtts import gTTS
import pygame

def speak(text):
    tts = gTTS(text=text, lang='ru')
    tts.save("temp_voice.mp3")
    
    pygame.mixer.init()
    pygame.mixer.music.load("temp_voice.mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
        
    pygame.mixer.music.unload()
    pygame.mixer.quit()
    
    if os.path.exists("temp_voice.mp3"):
        os.remove("temp_voice.mp3")

if __name__ == "__main__":
    print("📢 Джарвис генерирует голос...")
    speak("Привет, Денис! Я готов к работе.")
    print("✅ Воспроизведение завершено.")
