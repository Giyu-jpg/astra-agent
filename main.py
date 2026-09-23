import os
import sys
import requests
import json
import string
import io

# Força o terminal a aceitar caracteres UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    from app.brain.ouvinte import capturar_voz
    from app.brain.voz import falar
except ImportError:
    print("Erro: Módulos de voz não encontrados.")
    sys.exit()

URL_OLLAMA = "http://localhost:11434/api/generate"
MODELO = "llama3.2" 
CAMINHO_FATOS = "memory/semantic/facts.json"

def aprender_fato(fato):
    """Salva uma informação permanentemente no cérebro da IA."""
    os.makedirs(os.path.dirname(CAMINHO_FATOS), exist_ok=True)
    
    try:
        with open(CAMINHO_FATOS, 'r', encoding='utf-8') as f:
            fatos = json.load(f)
    except:
        fatos = []
        
    fatos.append(fato)
    with open(CAMINHO_FATOS, 'w', encoding='utf-8') as f:
        json.dump(fatos, f, indent=4, ensure_ascii=False)
        
def carregar_fatos():
    """Lê tudo o que a IA já aprendeu sobre você."""
    if not os.path.exists(CAMINHO_FATOS): return ""
    try:
        with open(CAMINHO_FATOS, 'r', encoding='utf-8') as f:
            fatos = json.load(f)
            return "\n- ".join(fatos)
    except: return ""

def carregar_personalidade():
    """Lê o slang.json para o tom de voz e gírias."""
    caminho = "app/personality/slang.json"
    if not os.path.exists(caminho): return ""
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            tom = dados.get("tom", "natural")
            regras = "\n- ".join(dados.get("regras", []))
            return f"Tom: {tom}\nRegras:\n- {regras}"
    except: return ""

def perguntar_ia(prompt_usuario):
    """Envia o comando com a personalidade e os fatos aprendidos."""
    personalidade = carregar_personalidade()
    fatos_aprendidos = carregar_fatos()
    
    # O Cérebro agora recebe quem você é, mas sem o peso das conversas antigas
    prompt_final = (
        "Você é um assistente pessoal de Teste . Responda SEMPRE em português brasileiro.\n"
        f"DIRETRIZES DE PERSONALIDADE:\n{personalidade}\n\n"
        f"O QUE VOCÊ JÁ APRENDEU SOBRE O APRENDIZADO De HOJE?:\n- {fatos_aprendidos}\n\n"
        f"Teste: {prompt_usuario}\nIA:"
    )
    
    payload = {
        "model": MODELO,
        "prompt": prompt_final,
        "stream": False,
        "options": {"num_thread": 6, "num_ctx": 1024}
    }
    try:
        response = requests.post(URL_OLLAMA, json=payload, timeout=120)
        return response.json().get('response', 'Sem resposta.')
    except Exception as e:
        return f"Erro: {e}"

def limpar_texto(texto):
    return texto.lower().translate(str.maketrans('', '', string.punctuation)).strip()

if __name__ == "__main__":
    print(f"Pessoal AI integrada: MODO APRENDIZADO")
    
    try:
        while True:
            comando_bruto = capturar_voz()
            if not comando_bruto or len(comando_bruto) < 2: continue

            comando = limpar_texto(comando_bruto)
            print(f"Usuario: {comando_bruto}")
            
            # GATILHOS DE COMANDO
            
            # 1. Comando de saída
            if any(p in comando for p in ['sair', 'tchau', 'encerrar']):
                falar("Sistemas encerrados. Falou.")
                break
                
            # 2. Comando de Aprendizado 
            elif comando.startswith("aprenda que") or comando.startswith("grave que"):
                # Pega só a informação depois do "aprenda que"
                fato_novo = comando_bruto.lower().replace("aprenda que", "").replace("grave que", "").strip()
                aprender_fato(fato_novo)
                resposta = "Massa! Já gravei essa informação no meu banco de dados."
                print(f"IA > {resposta}")
                falar(resposta)
                continue 
            # 3. Conversa Normal
            print("IA pensando...", end="\r")
            resposta_texto = perguntar_ia(comando_bruto)
            print(f"IA > {resposta_texto}")
            falar(resposta_texto)
            
    except KeyboardInterrupt:
        print("\nSaindo...")