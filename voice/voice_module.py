import os
import wave
import time
import threading

import numpy as np
import sounddevice as sd
import pygame

import asyncio
import edge_tts
from faster_whisper import WhisperModel


class VoiceModule:

    def __init__(
        self,
        model_size="tiny",
        wav_path="C:\\Jarvis_Voice\\output.wav"
    ):

        self.sample_rate = 16000
        self.channels = 1
        self.audio_format = np.int16

        self.wav_path = wav_path

        self.model = None
        self.llm_callback = None

        threading.Thread(
            target=self._init_whisper,
            args=(model_size,),
            daemon=True
        ).start()

    def _init_whisper(self, model_size):

        print(f"⏳ [Voice] Загрузка модели Whisper ({model_size})...")

        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="float32"
        )

        print("🤖 [Voice] Голосовой модуль готов!")

    def speak(self, text):

        if not text:
            return

        temp_path = "temp_voice.mp3"

        async def generate_voice():

            communicate = edge_tts.Communicate(
                text=text,
                voice="ru-RU-DmitryNeural"
            )

            await communicate.save(temp_path)

        asyncio.run(generate_voice())

        pygame.mixer.init()

        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()
        pygame.mixer.quit()

        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except:
            pass
    def _transcribe_audio(self):

        if not os.path.exists(self.wav_path):
            return ""

        if self.model is None:
            return ""

        segments, info = self.model.transcribe(
            self.wav_path,
            language="ru",
            beam_size=1
        )

        text = "".join(
            segment.text
            for segment in segments
        )

        return text.strip()

    def listen_once(self, seconds=3):

        print(f"🎤 Слушаю {seconds} сек...")

        audio_data = sd.rec(
            int(seconds * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.audio_format
        )

        sd.wait()

        with wave.open(self.wav_path, "wb") as wf:

            wf.setnchannels(self.channels)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)

            wf.writeframes(
                audio_data.tobytes()
            )

        text = self._transcribe_audio()

        return text

    def _run_callback(self, text):

        try:

            result = self.llm_callback(text)

            print(f"🔊 [Вик]: {result}")

            self.speak(str(result))

        except Exception as e:

            print("Ошибка callback:", e)

    def start_wake_mode(self, llm_function):

        self.llm_callback = llm_function

        wake_words = [
            "вик",
            "эй вик",
            "vik",
            "vick"
        ]

        print("🎤 Режим ожидания активирован")

        while True:

            try:

                if self.model is None:

                    time.sleep(1)

                    continue

                text = self.listen_once(2)

                if not text:
                    continue

                print("👂 Услышано:", text)

                text_lower = text.lower()

                activated = any(
                    word in text_lower
                    for word in wake_words
                )

                if not activated:
                    continue

                print("🔥 Активация")

                self.speak("Слушаю")

                command = self.listen_once(5)

                if not command:
                    continue

                print("📝 Команда:", command)

                threading.Thread(
                    target=self._run_callback,
                    args=(command,),
                    daemon=True
                ).start()

            except Exception as e:

                print("Ошибка:", e)

                time.sleep(1)