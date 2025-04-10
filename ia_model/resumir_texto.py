import os
import json
import subprocess
from time import time
import requests
from transformers import AutoTokenizer

RAW_DIR = 'data/json/raw'
CLEAN_DIR = 'data/json/clean'
MODEL = 'gemma-3-12b-it'
TOKEN_LIMIT = 4000
API_URL='http://127.0.0.1:1234/v1/chat/completions'

os.makedirs(CLEAN_DIR, exist_ok=True)

PROMPT_INICIAL = (
"Você é um assistente que limpa, organiza e extrai conhecimento útil de textos médicos e odontológicos.\n"
"Seu trabalho é:\n"
"- Remover autores, datas, referências bibliográficas e títulos de artigos.\n"
"- Eliminar duplicações e repetições de frases.\n"
"- Ignorar sumários, listas de artigos, nomes de revistas, números de páginas e citações.\n"
"- Focar apenas em explicações claras e organizadas por tema (ex: cicatrização, implantes, etc).\n"
"- Não numerar os parágrafos nem dividir em múltiplas linhas ou itens de listas.\n"
"- Organize a resposta de forma contínua, sem quebra de linhas ou listas, em um único bloco de texto.\n"
"- Caso não tenha informações relevantes, responda apenas com um ponto.\n\n"
"Texto:\n"
)

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf")

def dividir_em_blocos(paragrafos, token_limit):
    blocos = []
    bloco_atual = ""
    for p in paragrafos:
        teste_bloco = bloco_atual + "\n\n" + p
        if len(tokenizer.encode(teste_bloco)) < token_limit:
            bloco_atual = teste_bloco
        else:
            blocos.append(bloco_atual.strip())
            bloco_atual = p
    if bloco_atual:
        blocos.append(bloco_atual.strip())
    return blocos

def limpar_resposta(resposta):
    linhas = resposta.split('\n')
    parágrafos_limpos = []
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
        linha = linha.lstrip("0123456789. )-")  # Remove numeração
        linha = linha.strip()
        if linha:
            parágrafos_limpos.append(linha)
    return parágrafos_limpos

def processar_bloco(texto):
    headers = {
            "Content-Type": "application/json"
        }
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": PROMPT_INICIAL}, {"role": "user", "content": texto}],
        "temperature": 0.7,
        "max_tokens": 1500
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(f"Erro ao chamar a API do LMStudio: {response.text}")
    
    resposta = response.json()
    texto_resposta = resposta['choices'][0]['message']['content'].strip()
    return limpar_resposta(texto_resposta)

def process_file(filename):
    caminho_entrada = os.path.join(RAW_DIR, filename)
    caminho_saida = os.path.join(CLEAN_DIR, filename)

    try:
        with open(caminho_entrada, 'r') as f:
            data = json.load(f)

        if not isinstance(data, list) or not data:
            print(f"[AVISO] Nenhum texto encontrado em {filename}")
            return

        blocos = dividir_em_blocos(data, TOKEN_LIMIT)
        print(f"[INFO] {filename}: {len(blocos)} blocos para processar")

        resultados = []
        tempos = []

        for i, bloco in enumerate(blocos):
            print(f"  - Processando bloco {i+1}/{len(blocos)}...")
            inicio = time()
            try:
                resultado = processar_bloco(bloco)
                resultados.extend(resultado)
            except Exception as e:
                print(f"[ERRO] no bloco {i+1}: {e}")
            duracao = round(time() - inicio, 2)
            tempos.append(duracao)
            print(f"    Tempo do bloco {i+1}: {duracao}s")

        with open(caminho_saida, 'w') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)

        print(f"[OK] Finalizado: {filename}")
        print(f"Tempo médio por bloco: {round(sum(tempos)/len(tempos), 2)}s")
        print(f"Tempo total: {round(sum(tempos), 2)}s\n")

    except Exception as e:
        print(f"[ERRO] Falha ao processar {filename}: {e}")

def process_all():
    start = time()
    arquivos = [f for f in os.listdir(RAW_DIR) if f.endswith('.json')]
    for arquivo in arquivos:
        process_file(arquivo)
    print(f"Tempo total de todos os arquivos: {round(time() - start, 2)}s")

if __name__ == '__main__':
    process_all()