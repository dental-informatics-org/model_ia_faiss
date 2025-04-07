from transformers import LongformerTokenizer

# Carregar o tokenizer do Longformer
tokenizer = LongformerTokenizer.from_pretrained('allenai/longformer-base-4096')

# Função para processar os parágrafos e transformar em tokens
def process_paragraphs(text):
    # Dividir o texto em parágrafos
    paragraphs = text.split('\n')
    
    # Lista para armazenar os tokens separados por parágrafo
    tokenized_paragraphs = []
    
    # Para cada parágrafo, tokenizamos
    for paragraph in paragraphs:
        tokens = tokenizer.encode(paragraph, truncation=False)
        tokenized_paragraphs.append(tokens)
    
    return tokenized_paragraphs

# Função para agrupar os tokens em "capítulos" sem ultrapassar o limite de tokens
def group_tokens_into_chapters(tokenized_paragraphs, max_tokens=2048):
    chapters = []
    current_chapter = []
    current_tokens_count = 0
    
    # Agrupar parágrafos em capítulos
    for tokens in tokenized_paragraphs:
        tokens_count = len(tokens)
        
        # Se adicionar esse parágrafo exceder o limite de tokens, salva o capítulo atual
        if current_tokens_count + tokens_count > max_tokens:
            chapters.append(current_chapter)
            current_chapter = [tokens]
            current_tokens_count = tokens_count
        else:
            current_chapter.append(tokens)
            current_tokens_count += tokens_count
    
    # Adicionar o último capítulo
    if current_chapter:
        chapters.append(current_chapter)
    
    return chapters

# Função para decodificar os tokens de volta ao texto
def decode_tokens(tokenized_paragraphs):
    decoded_paragraphs = []
    for paragraph_tokens in tokenized_paragraphs:
        decoded_paragraph = tokenizer.decode(paragraph_tokens, skip_special_tokens=True)
        decoded_paragraphs.append(decoded_paragraph)
    return decoded_paragraphs