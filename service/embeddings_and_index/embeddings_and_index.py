from redis import Redis
import torch.multiprocessing as mp
import os
import torch
from transformers import AutoTokenizer, AutoModel
import faiss
import numpy as np
import pickle

redis_conn = Redis(host="localhost", port=6379)

# 🔹 Configuração única do start method (antes de qualquer importação que use multiprocessing)
try:
    mp.set_start_method('spawn', force=True)
except RuntimeError:
    pass

# Definição do dispositivo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Caminhos dos arquivos
INDICE_PATH = "data/index/faiss_index"
ID_PARA_TEXTO_PATH = "data/index/id_para_texto.pkl"
dimension = 768  # Dimensão dos embeddings
os.makedirs(os.path.dirname(INDICE_PATH), exist_ok=True)

# Inicializa dicionário
global id_para_texto
id_para_texto = {}

# 🔹 Inicializa os modelos no início do script (para evitar re-inicializações em subprocessos)
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
model = AutoModel.from_pretrained('sentence-transformers/paraphrase-multilingual-mpnet-base-v2').to(device)

def gerar_embeddings(texto):
    """Gera embeddings para um texto dado."""
    tokens = tokenizer(texto, return_tensors='pt', truncation=True, padding=True)
    tokens = {k: v.to(device) for k, v in tokens.items()}
    
    with torch.no_grad():
        output = model(**tokens)

    token_embeddings = output.last_hidden_state
    attention_mask = tokens["attention_mask"].unsqueeze(-1).expand(token_embeddings.shape).float()
    emb = (token_embeddings * attention_mask).sum(dim=1) / attention_mask.sum(dim=1)
    emb = emb.cpu().numpy().astype(np.float32)

    faiss.normalize_L2(emb)  # Normalizar embeddings antes de retornar
    return emb

def carregar_id_para_texto():
    """Carrega o dicionário ID -> Texto do disco."""
    global id_para_texto
    if os.path.exists(ID_PARA_TEXTO_PATH):
        with open(ID_PARA_TEXTO_PATH, "rb") as f:
            id_para_texto = pickle.load(f)
        print(f"Carregado id_para_texto com {len(id_para_texto)} itens.")
    else:
        id_para_texto = {}

def salvar_id_para_texto():
    """Salva o dicionário ID -> Texto no disco."""
    with open(ID_PARA_TEXTO_PATH, "wb") as f:
        pickle.dump(id_para_texto, f)

def carregar_indice():
    """Carrega ou cria um índice FAISS."""
    if os.path.exists(INDICE_PATH):
        index = faiss.read_index(INDICE_PATH)
        if index.d != dimension:
            raise ValueError(f"Dimensão do índice ({index.d}) não corresponde ao esperado ({dimension})")
        return index
    else:
        print(f"⚠️ ERRO: O arquivo {INDICE_PATH} não existe. Um novo índice será criado.")
        quantizer = faiss.IndexFlatIP(dimension)
        index = faiss.IndexIVFFlat(quantizer, dimension, 100, faiss.METRIC_INNER_PRODUCT)
        return index

def indexar_textos(linhas):
    """Indexa uma lista de textos no FAISS."""
    global id_para_texto, index

    embeddings = [gerar_embeddings(linha) for linha in linhas]
    embeddings = np.vstack(embeddings)  # Empilha os arrays
    faiss.normalize_L2(embeddings)  # 🔹 Normaliza antes de adicionar

    if embeddings.shape[1] != dimension:
        raise ValueError(f"Dimensão dos embeddings ({embeddings.shape[1]}) não corresponde ao esperado ({dimension})")

    # 🔹 Se o índice não foi treinado, treine antes de adicionar os embeddings
    if not index.is_trained:
        print("⚠️ Índice FAISS ainda não treinado. Treinando agora...")
        index.train(embeddings)
        print("✅ Treinamento concluído.")

    index.add(embeddings)  # Adiciona os embeddings ao índice

    # 🔹 Salvar ID -> texto
    novo_id = len(id_para_texto)
    for i, linha in enumerate(linhas):
        id_para_texto[novo_id + i] = linha
    
    salvar_id_para_texto()
    faiss.write_index(index, INDICE_PATH)
    print(f"✅ Índice FAISS salvo em {INDICE_PATH}")

    # 🔹 Forçar recarregamento do índice
    index = carregar_indice()
    print("🔄 Índice FAISS recarregado com sucesso.")

def buscar_textos(consulta, top_k=5):
    """Busca textos similares a uma consulta."""
    global index, id_para_texto

    if redis_conn.get("recarregar_indice") == b"true":
        index = carregar_indice()
        carregar_id_para_texto()
        redis_conn.set("recarregar_indice", "false")

    embedding = gerar_embeddings(consulta)
    faiss.normalize_L2(embedding)
    distancias, indices = index.search(embedding, top_k)
    
    resultados = []
    for i, idx in enumerate(indices[0]):
        if idx in id_para_texto:
            resultados.append({
                "texto": id_para_texto[idx],
                "distancia": float(distancias[0][i])
            })
    return resultados

# 🔹 Carregar os dados ao iniciar
index = carregar_indice()
carregar_id_para_texto()
print("✅ Sistema pronto para buscas!")
