import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import os
import queue

print("Carregando motor de transcrição (Faster-Whisper)...")
model = WhisperModel("base", device="cpu", compute_type="int8")

def capturar_voz():
    fs = 16000
    q = queue.Queue()

    def callback(indata, frames, time, status):
        """Pega os pedaços de áudio em tempo real."""
        q.put(indata.copy())

    print("\n[ Microfone aberto. Pode falar... (Paro de ouvir quando você fizer silêncio) ]")
    
    gravacao = []
    silencio_limite = 0.02  # Sensibilidade do volume (aumente se o ambiente for muito barulhento)
    frames_silencio = 0
    max_silencio = int(fs * 1.5)  # 1.5 segundos de silêncio para cortar a gravação
    falou_algo = False

    # Abre o microfone indefinidamente até a lógica quebrar o loop
    with sd.InputStream(samplerate=fs, channels=1, callback=callback):
        while True:
            dados = q.get()
            gravacao.append(dados)
            
            # Calcula o volume do pedaço atual de áudio
            volume = np.max(np.abs(dados))
            
            if volume > silencio_limite:
                falou_algo = True
                frames_silencio = 0 # Zera o contador de silêncio porque você está falando
            elif falou_algo:
                frames_silencio += len(dados)
                
            # Se você já falou e fez uma pausa de 1.5s, encerra a captura
            if falou_algo and frames_silencio > max_silencio:
                break

    print("Traduzindo sua fala...")
    audio_completo = np.concatenate(gravacao)
    
    caminho_temp = "temp_audio.wav"
    write(caminho_temp, fs, (audio_completo * 32767).astype(np.int16)) 
        
    segments, _ = model.transcribe(caminho_temp, language="pt")
    texto_final = "".join([s.text for s in segments])
    
    if os.path.exists(caminho_temp):
        try:
            os.remove(caminho_temp)
        except: pass
        
    return texto_final.strip()