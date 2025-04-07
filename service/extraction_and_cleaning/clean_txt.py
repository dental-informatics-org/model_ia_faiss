import re

def limpar_texto(texto, converter_minusculas=True):
    # Remover caracteres de controle invisíveis
    texto = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', texto)

    # Remover espaços extras (sem remover quebras de linha duplas)
    texto = re.sub(r'[ \t]+', ' ', texto)

    # Remover quebras de linha extras
    texto = re.sub(r'\r\n|\n\r', '\n', texto)  # Unificar \r\n e \n\r para \n
    texto = re.sub(r'\r+', '\n', texto)  # Substituir \r por \n
    texto = re.sub(r'\n+', '\n', texto)  # Reduzir múltiplas quebras de linha para uma única
    texto = re.sub(r'\n\s*\n', '\n\n', texto)  # Garantir que parágrafos sejam mantidos

    # Remover hifenização causada por quebras de linha
    texto = re.sub(r'(\S)-\n(\S)', r'\1\2', texto)

    # Remover quebras de linha dentro de parágrafos
    texto = re.sub(r'(?<=\S) \n(?=\S)', ' ', texto)

    # Remover espaços extras no início e no final de cada linha
    texto = re.sub(r'^\s+', '', texto, flags=re.MULTILINE)
    texto = re.sub(r'\s+$', '', texto, flags=re.MULTILINE)

    # Normalizar tabulações
    texto = re.sub(r'\s*\t\s*', '\t', texto)

    # Remover espaços extras no final das linhas
    texto = re.sub(r'\s+\n', '\n', texto)

    # Remover caracteres especiais, mantendo letras, números, espaços, ponto, vírgula e quebras de linha
    texto = re.sub(r'[^a-zA-Z0-9.,\n ]', '', texto)

    # Converter para minúsculas (opcional)
    if converter_minusculas:
        texto = texto.lower()

    return texto.strip()
