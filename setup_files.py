import json
import os

arquivos_json = [
    "memory/episodic/events.json",
    "memory/semantic/preferences.json",
    "memory/procedural/rules.json",
    "app/personality/slang.json"
]

for caminho in arquivos_json:
    # Garante que a pasta existe antes de criar o arquivo
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    
    # Cria o arquivo com um colchete vazio [] para ser um JSON válido
    if not os.path.exists(caminho):
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump([], f)
        print(f"Arquivo criado: {caminho}")

print("\nArquivos de memória prontos para uso!")