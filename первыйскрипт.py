import wave
import numpy as np
import sounddevice as sd

SAMPLE_RATE = 16000  
DURATION = 5  
CHANNELS = 1  
AUDIO_FORMAT = np.int16  

def record_audio(filename="output.wav"):
    print("🎤 Запись пошла... Говорите!")
    
    audio_data = sd.rec(
        int(DURATION * SAMPLE_RATE), 
        samplerate=SAMPLE_RATE, 
        channels=CHANNELS, 
        dtype=AUDIO_FORMAT
    )
    
    sd.wait()  
    print("✅ Запись завершена. Сохраняем в файл...")

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())
        
    print(f"💾 Файл успешно сохранен как: {filename}")

if __name__ == "__main__":
    record_audio()
