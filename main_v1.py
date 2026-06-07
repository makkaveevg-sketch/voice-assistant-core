import os
import wave
import time
import threading
import numpy as np
import sounddevice as sd
import keyboard
from gtts import gTTS
import pygame

SAMPLE_RATE = 16000  
CHANNELS = 1  
AUDIO_FORMAT = np.int16  

is_recording = False
audio_buffer = []

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

def record_loop():
    global is_recording, audio_buffer
    audio_buffer = []
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype=AUDIO_FORMAT) as stream:
        while is_recording:
            data, overflow = stream.read(1024)
            audio_buffer.append(data)

def toggle_recording(e):
    global is_recording, audio_buffer
    if e.event_type == keyboard.KEY_DOWN:
        if not is_recording:
            is_recording = True
            print("\n🎤 Запись пошла... Говорите! Нажмите ПРОБЕЛ еще раз для остановки.")
            threading.Thread(target=record_loop, daemon=True).start()
        else:
            is_recording = False
            print("🛑 Запись остановлена. Сохраняем файл...")
            
            if audio_buffer:
                audio_data = np.concatenate(audio_buffer, axis=0)
                with wave.open("output.wav", 'wb') as wf:
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(2)  
                    wf.setframerate(SAMPLE_RATE)
                    wf.writeframes(audio_data.tobytes())
                
                print("💾 Файл успешно сохранен как: output.wav")
                speak("Запись успешно сохранена")
            else:
                print("❌ Данные звука не получены.")

if __name__ == "__main__":
    print("🤖 Джарвис запущен и готов к работе.")
    print("Нажми ПРОБЕЛ, чтобы начать запись команды.")
    
    keyboard.hook_key('space', toggle_recording)
    keyboard.wait()
  