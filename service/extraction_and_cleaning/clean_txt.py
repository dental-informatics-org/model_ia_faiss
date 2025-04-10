import re

def limpar_texto(texto, converter_minusculas=True):
    # Remover caracteres de controle invisíveis
    texto = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', texto)

    # Remover espaços extras (sem remover quebras de linha duplas)
    texto = re.sub(r'[ \t]+', ' ', texto)

    # Remover quebras de linha extras
    texto = re.sub(r'\r\n|\n\r', '\n', texto)
    texto = re.sub(r'\r+', '\n', texto)
    texto = re.sub(r'\n+', '\n', texto)
    texto = re.sub(r'\n\s*\n', '\n\n', texto)

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

    # Substituir quebras de linha por espaço, apenas se a linha anterior não termina com ponto final
    #texto = re.sub(r'(?<!\.)\n(?=\S)', ' ', texto)

    # Remover linhas com apenas números ou pontuação
    texto = re.sub(r'^\s*(\d+[\s\.,]*)+$', '', texto, flags=re.MULTILINE)

    # Remover linhas com menos de 4 palavras (ignora múltiplos espaços)
    texto = re.sub(r'^(?:\s*\S+){1,3}\s*$', '', texto, flags=re.MULTILINE)

    # Reduzir quebras de linha múltiplas para uma só dupla
    texto = re.sub(r'\n{2,}', '\n\n', texto)

    # Remover linhas completamente vazias
    texto = re.sub(r'^\s*$', '', texto, flags=re.MULTILINE)

    # Converter para minúsculas (opcional)
    if converter_minusculas:
        texto = texto.lower()

    return texto.strip()
