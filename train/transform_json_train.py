import json
import requests
import re

# Configuração do servidor LM Studio
LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"  # A API local do LM Studio
MODEL_NAME = "qwen2.5-coder-14b-instruct"  # Modelo que você está usando

# Função para enviar a requisição para o LM Studio
def limpar_texto_com_lmstudio(texto):
    """ Envia o texto para o LM Studio e recebe o texto otimizado """
    
    # Primeiro, vamos adicionar um pré-processamento para limpar os títulos e nomes de autores
    texto = re.sub(r"([a-zA-Z]+ [a-zA-Z]+(?: [a-zA-Z]+){0,2})\s*-\s*(mestre|doutor|professor|dr|médico|engenheiro|etc.)", "", texto)
    texto = re.sub(r"\b(\d{4})\b", "", texto)  # Remove números isolados (anos, por exemplo)

    prompt = f"""Você é um agente especializado na limpeza e otimização de textos extraídos de documentos acadêmicos. Sua tarefa é realizar as seguintes ações:

1. Remover títulos acadêmicos, referências bibliográficas, referencias, números de páginas, capítulos e qualquer conteúdo relacionado a figuras ou imagens, mas SEM PERDER o contexto informativo relevante do texto.
   
2. Corrigir palavras incompletas ou aquelas que foram corrigidas automaticamente de forma incorreta.

3. Remover ou manter números, dependendo do contexto. Não é necessário escrever números por extenso, a menos que faça sentido dentro do contexto do texto.

4. Manter apenas o conteúdo relevante para a compreensão do tema abordado, eliminando seções irrelevantes, como sumários ou seções sem valor informativo.

5. Remover todos os caracteres especiais (como hifens, aspas, barras, parênteses) sem alterar o significado do texto.

6. Deixar o texto em letras minúsculas, sem perda de contexto.

7. Remover espaços em branco extras, mantendo apenas um espaço entre as palavras.

8. Corrigir erros de digitação e gramática, mantendo a fluência do texto.

9. Garantir que o texto final seja coeso e coerente, com uma estrutura lógica e fluida.

11. Remover informações irrelevantes ou redundantes, como "este artigo discute" ou "neste estudo".

12. Remover informações que não são necessárias para a compreensão do texto, como "o autor afirma que" ou "segundo o estudo".

13. Remover informações que não são relevantes para o tema principal do texto, como "o autor menciona" ou "o estudo mostra".

Formato de saída: Apenas o texto limpo, sem explicações adicionais. Não é necessário gerar lista de ações ou justificativas.

Texto:

    {texto}
    """

    # Corpo da requisição para o LM Studio
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "Você é um agente especializado na limpeza e otimização de textos extraídos de documentos."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    # Enviando a requisição
    response = requests.post(LM_STUDIO_URL, json=payload)
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        response_data = response.json()
        # Retornando o texto limpo
        return response_data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    else:
        print(f"Erro na requisição: {response.status_code}")
        return ""

# Carregar o JSON original
with open("train/pymupdf_output.json", "r", encoding="utf-8") as f:
    original_data = json.load(f)

# Transformar os dados
transformed_data = {
    "training_params": {
        "epochs": 30,
        "batch_size": 16,
        "learning_rate": 5e-5
    },
    "data": []
}

# Obter o número total de textos
total_textos = sum(len(sublist) for sublist in original_data)

# Iterar pelos elementos do JSON e gerar as respostas
processed_texts = 0
for sublist in original_data:
    for text in sublist:
        texto_limpo = limpar_texto_com_lmstudio(text)
        print(f"Texto limpo: {texto_limpo[:100]}")

        # Atualizar o progresso
        processed_texts += 1
        progress = (processed_texts / total_textos) * 100
        print(f"Progresso: {progress:.2f}%")
        
        transformed_data["data"].append({"input_text": text, "target_text": texto_limpo})

# Salvar o novo JSON com o texto limpo
with open("train/train_longformer.json", "w", encoding="utf-8") as f:
    json.dump(transformed_data, f, indent=2, ensure_ascii=False)

print("Arquivo train_longformer.json criado com sucesso!")
