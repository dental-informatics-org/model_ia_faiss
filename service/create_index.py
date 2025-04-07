import os
import pickle
import faiss
import numpy as np

# Caminhos dos arquivos
INDICE_PATH = "data/index/faiss_index"
ID_PARA_TEXTO_PATH = "data/index/id_para_texto.pkl"
DIMENSION = 768  # Dimensão dos embeddings
N_CLUSTERS = 100  # Número de clusters para o índice IVFFlat

def verificar_e_criar_indices():
    """ Verifica se os arquivos FAISS e id_para_texto existem. Se não existirem, cria novos. """
    os.makedirs(os.path.dirname(INDICE_PATH), exist_ok=True)

    if not os.path.exists(INDICE_PATH):
        print("⚠️ Índice FAISS não encontrado. Criando um novo...")
        quantizer = faiss.IndexFlatIP(DIMENSION)
        index = faiss.IndexIVFFlat(quantizer, DIMENSION, N_CLUSTERS, faiss.METRIC_INNER_PRODUCT)
        index.train(np.random.randn(N_CLUSTERS, DIMENSION).astype('float32'))  # Treina com dados aleatórios
        faiss.write_index(index, INDICE_PATH)
        print(f"✅ Índice FAISS criado e salvo em {INDICE_PATH}")

    if not os.path.exists(ID_PARA_TEXTO_PATH):
        print("⚠️ Arquivo id_para_texto.pkl não encontrado. Criando um novo...")
        with open(ID_PARA_TEXTO_PATH, "wb") as f:
            pickle.dump({}, f)
        print(f"✅ Arquivo id_para_texto.pkl criado e salvo em {ID_PARA_TEXTO_PATH}")
