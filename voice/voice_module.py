import os, wave, time, threading
import numpy as np
import sounddevice as sd
import keyboard
import pygame
from gtts import gTTS
from faster_whisper import WhisperModel

class VoiceModule:
    def __init__(self, model_size="tiny", wav_path="C:\\Jarvis_Voice\\output.wav"):
        self.sample_rate = 16000
        self.channels = 1
        self.audio_format = np.int16
        self.wav_path = wav_path
        self.is_recording = False
        self.audio_buffer = []
        self.model = None
        self.llm_callback = None
        threading.Thread(target=self._init_whisper, args=(model_size,), daemon=True).start()

    def _init_whisper(self, model_size):
        print(f"⏳ [Voice] Загрузка модели Whisper ({model_size})...")
        self.model = WhisperModel(model_size, device="cpu", compute_type="float32")
        print("🤖 [Voice] Голосовой модуль полностью готов к работе!")

    def speak(self, text):
        if not text: return
        tts = gTTS(text=text, lang="ru")
        temp_path = "C:\\Jarvis_Voice\\temp_voice.mp3"
        tts.save(temp_path)
        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy(): time.sleep(0.1)
        pygame.mixer.music.unload()
        pygame.mixer.quit()
        try:
            if os.path.exists(temp_path): os.remove(temp_path)
        except: pass

    def _record_loop(self):
        self.audio_buffer = []
        with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, dtype=self.audio_format) as stream:
            while self.is_recording:
                data, overflow = stream.read(1024)
                self.audio_buffer.append(data)

    def _transcribe_audio(self):
        if not os.path.exists(self.wav_path) or self.model is None: return ""
        segments, info = self.model.transcribe(self.wav_path, language="ru", beam_size=1)
        return "".join([segment.text for segment in segments]).strip()

    def _toggle_recording(self, e):
        if e.event_type != keyboard.KEY_DOWN: return
        if not self.is_recording:
            if self.model is None: print("⏳ Модель ИИ еще загружается, подождите..."); return
            self.is_recording = True
            print("\n🎤 [Голос] Запись пошла... Говорите. (Нажмите ПРОБЕЛ для окончания)")
            threading.Thread(target=self._record_loop, daemon=True).start()
        else:
            self.is_recording = False
            print("🛑 [Голос] Запись остановлена. Распознавание...")
            if self.audio_buffer:
                audio_data = np.concatenate(self.audio_buffer, axis=0)
                with wave.open(self.wav_path, "wb") as wf:
                    wf.setnchannels(self.channels)
                    wf.setsampwidth(2)
                    wf.setframerate(self.sample_rate)
                    wf.writeframes(audio_data.tobytes())
                user_text = self._transcribe_audio()
                print(f"📝 [Голос] Распознано: « {user_text} »")
                if self.llm_callback and user_text:
                    threading.Thread(target=self._run_callback, args=(user_text,), daemon=True).start()
                elif not user_text:
                    self.speak("Я не расслышал команду, сэр.")
            else: print("❌ Ошибка записи звука.")

    def _run_callback(self, text):
        bot_answer = self.llm_callback(text)
        print(f"🔊 [Джарвис]: {bot_answer}")
        self.speak(bot_answer)

    def start_listening(self, llm_function):
        self.llm_callback = llm_function
        keyboard.hook_key("space", self._toggle_recording)
        keyboard.wait()
