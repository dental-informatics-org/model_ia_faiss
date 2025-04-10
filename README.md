# model_ia_faiss

# Indexação de Livros com Faiss

Este projeto visa a indexação de livros em formato PDF utilizando o Faiss para criação de embeddings. Através de uma API FastAPI, o projeto processa arquivos PDF e cria um índice para buscas eficientes. Ele também possui workers para rodar em segundo plano e uma infraestrutura em Docker com Redis e MongoDB.

## Descrição

O objetivo do projeto é criar um sistema eficiente de indexação de livros, que transforma dados extraídos de arquivos PDF em formatos que podem ser pesquisados rapidamente. Utilizando o Faiss, o sistema gera **embeddings** dos textos extraídos dos PDFs, criando índices que permitem buscas rápidas e precisas.

### O que é um índice?

Um **índice** é uma estrutura de dados que facilita a busca rápida de informações. Em vez de procurar por uma palavra ou frase em todos os documentos, o índice permite que você encontre rapidamente onde as informações relevantes estão localizadas, com base em embeddings e outras técnicas de indexação.

### O que são embeddings?

**Embeddings** são representações vetoriais de palavras ou trechos de texto em um espaço contínuo, permitindo que o sistema capture semelhanças semânticas entre diferentes partes do texto. Embeddings são amplamente utilizados em tarefas de processamento de linguagem natural (NLP), como busca e análise de texto.

## Funcionalidades

- **Processamento de PDFs**: O sistema aceita arquivos PDF, extrai o texto e cria embeddings para indexação.
- **Indexação com Faiss**: Utiliza Faiss para armazenar e buscar os embeddings de maneira eficiente.
- **API FastAPI**: A API permite que os usuários interajam com o sistema, enviando PDFs e realizando buscas nos índices.
- **Worker para Processamento em Segundo Plano**: O projeto usa Redis e RQ para gerenciar tarefas assíncronas, como a criação do índice e a busca.
- **Suporte a CUDA**: O sistema é configurado para usar CUDA para aceleração de processamento, mas também funciona sem CUDA, usando a CPU.

## Requisitos

- Python 3.9 ou superior
- Docker e Docker Compose
- CUDA (opcional, mas recomendado para aceleração)

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/misereitor/model_ia_faiss.git
cd model_ia_faiss
```

2. Configure o ambiente:

- **Usando Docker**: O projeto já possui a configuração necessária para rodar o MongoDB, Redis e o backend da API utilizando Docker.

```bash
docker-compose up -d
```

3. Instale as dependências:

```bash
pip install -r requeriments.txt
```

4. Rode a API:

```bash
python main.py
```

5. Rode o Worker (em outro terminal):

```bash
python start_worker.py
```

## Estrutura do Projeto

- **main.py**: Arquivo principal da aplicação FastAPI. Inclui rotas para processamento de arquivos, buscas e tarefas em segundo plano.
- **start_worker.py**: Script para iniciar o worker que processa tarefas em segundo plano usando Redis e RQ.
- **Dockerfile**: Configuração do Docker para rodar a aplicação com CUDA e as dependências necessárias.
- **docker-compose.yml**: Define os serviços do Docker, como MongoDB e Redis, para rodar o sistema.
- **requeriments.txt**: Lista de dependências do projeto.
- **routers**: Contém os módulos responsáveis pelas rotas de processamento de arquivos, busca de índices e gerenciamento de tarefas.
- **db**: Módulo que contém a configuração do MongoDB e outras funções relacionadas à persistência de dados.
- **service**: Contém a lógica de criação de índices e processamento de embeddings.

## Como Funciona

1. O usuário envia um arquivo PDF via API.
2. O sistema extrai o texto do PDF e cria embeddings a partir dos dados extraídos.
3. Os embeddings são armazenados em um índice Faiss para buscas rápidas.
4. O sistema permite realizar buscas nos dados indexados, retornando os resultados com base na semelhança semântica.
5. O worker processa as tarefas em segundo plano, como a criação do índice e a atualização dos dados.

## Configuração de CUDA

Se você possui uma GPU com suporte a CUDA, o Faiss será capaz de utilizar a aceleração de hardware para criar e pesquisar embeddings de forma muito mais rápida. Isso é especialmente útil para grandes volumes de dados, como livros inteiros, onde a aceleração de hardware pode reduzir significativamente o tempo de processamento.

- **Com CUDA**: O Faiss utilizará automaticamente a GPU para criar os embeddings e realizar buscas, proporcionando desempenho muito mais rápido.
- **Sem CUDA**: Se você não possui uma GPU compatível com CUDA, o Faiss funcionará utilizando a CPU. Embora isso ainda permita o funcionamento do sistema, o desempenho pode ser mais lento, especialmente em grandes conjuntos de dados.

**Nota:** Para garantir que o Faiss use a GPU, certifique-se de ter o `faiss-gpu` instalado. Caso contrário, o sistema usará a versão CPU (`faiss-cpu`).

## Tarefas em Segundo Plano

O sistema usa o Redis e o RQ para gerenciar tarefas em segundo plano. Isso permite que o processamento de arquivos e a criação de índices sejam feitos de maneira assíncrona, sem bloquear a execução da API.

### Comandos para Rodar o Worker

Em um terminal separado, execute o seguinte comando para iniciar o worker:

```bash
python start_worker.py
```

Isso irá iniciar o worker que irá processar as tarefas em segundo plano.

## Contribuindo

1. Faça um fork do repositório.
2. Crie uma branch para sua modificação (`git checkout -b feature/nome-da-sua-feature`).
3. Faça suas modificações.
4. Commit suas alterações (`git commit -m 'Adiciona nova feature'`).
5. Envie sua branch para o repositório remoto (`git push origin feature/nome-da-sua-feature`).
6. Abra um Pull Request.

## Future Updates

- Configurar um LLM para otimizar o livro. (Atualmente, estou usando a API do LMStudio, que é a mais performática para esse caso. O script correspondente pode ser encontrado em `ia_model/resumir_texto.py`.)

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```

Esse `README.md` cobre a descrição do projeto, suas funcionalidades, instalação, configuração e execução, além de fornecer detalhes sobre os conceitos de **índice** e **embeddings**. Você pode personalizar conforme necessário para melhor adequar-se às necessidades do seu projeto.
```


We have already created a CR for Portal C1382851.

We need the below details to update the CR.

Implementation Plan – Details about the deployment like what are all the JIRA IDs that are going live
Backout Plan – If something goes wrong, what is the plan for rollback.
PR details – Any PR link, Merged from QA to Prod.
Qtest Results – Qtest results link which will have the test case results.



Along with other items, I would like you to cover below points as well :

Check if you have required accesses for the deployment
Show Luis what code you will be deploying, how coder merge etc. will be done
What is required from Jira story perspective qtest and tagging etc.
How to smoke test in PROD?
How to make sure the deployment is successful
