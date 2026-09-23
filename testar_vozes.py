import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

print("LISTA DE VOZES INSTALADAS")
for index, voice in enumerate(voices):
    print(f"\n[{index}] Nome da Voz: {voice.name}")
    print(f"    ID: {voice.id}")
    
    # Configura a voz atual e testa
    engine.setProperty('voice', voice.id)
    engine.setProperty('rate', 180) 
    
    texto_teste = f"Olá, eu sou a voz número {index}."
    print("    Falando...")
    engine.say(texto_teste)
    engine.runAndWait()

print("\nTeste concluído. Qual número você preferiu?")