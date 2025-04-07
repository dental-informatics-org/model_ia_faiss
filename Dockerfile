FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app
COPY requeriments.txt .
RUN pip3 install --no-cache-dir -r requeriments.txt

COPY . .

ENV PYTHONPATH=/app
ENV CUDA_VISIBLE_DEVICES=0

# Executar o script de entrada
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
