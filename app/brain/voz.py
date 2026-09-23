import edge_tts
import asyncio
import os
from playsound import playsound

def falar(texto):
    """Gera voz neural e toca usando o playsound, contornando o erro do pygame."""
    voz_escolhida = "pt-BR-AntonioNeural" 
    arquivo_temp = "fala_temp.mp3"
    
    # 1. Gera o áudio neural
    async def gerar_audio():
        comunicacao = edge_tts.Communicate(texto, voz_escolhida, rate="+5%")
        await comunicacao.save(arquivo_temp)
        
    asyncio.run(gerar_audio())
    
    # 2. Toca o áudio
    playsound(arquivo_temp)
    
    # 3. Limpa o arquivo
    if os.path.exists(arquivo_temp):
        try:
            os.remove(arquivo_temp)
        except OSError:
            pass # Ignora se o Windows segurar o arquivo temporariamente

if __name__ == "__main__":
    print("Testando a voz neural com Playsound...")
    falar("Olá! Sistema de áudio alternativo ativado com sucesso.")