import json
from torch.optim import AdamW
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import LongformerForSequenceClassification, LongformerTokenizer
import os

# Limpar cache da GPU
torch.cuda.empty_cache()

# Carregar dados
with open('train/train_longformer.json', 'r') as f:
    data = json.load(f)['data']

# Criar mapeamento de rótulos
label_map = {"relevante": 0, "irrelevante": 1}

# Filtrar dados válidos
filtered_data = [item for item in data if item['target_text'] in label_map]
if not filtered_data:
    raise ValueError("Erro: Nenhum dado válido encontrado após filtragem. Verifique os rótulos no JSON.")

# Separar textos e rótulos
train_texts = [item['input_text'] for item in filtered_data]
train_labels = [label_map[item['target_text']] for item in filtered_data]

# Criar dataset personalizado
class TextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=4096):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        label = torch.tensor(self.labels[idx], dtype=torch.long)
        return {"input_ids": encoding['input_ids'].squeeze(0), "attention_mask": encoding['attention_mask'].squeeze(0), "label": label}

# Diretório para salvar checkpoints
checkpoint_dir = "checkpoints"
os.makedirs(checkpoint_dir, exist_ok=True)

# Carregar modelo e tokenizer
tokenizer = LongformerTokenizer.from_pretrained("allenai/longformer-base-4096")
model_path = os.path.join(checkpoint_dir, "longformer_checkpoint")

if os.path.exists(model_path):
    print("Carregando modelo do checkpoint...")
    model = LongformerForSequenceClassification.from_pretrained(model_path)
else:
    model = LongformerForSequenceClassification.from_pretrained("allenai/longformer-base-4096", num_labels=len(label_map))

# Criar dataset e DataLoader
train_dataset = TextDataset(train_texts, train_labels, tokenizer)
train_dataloader = DataLoader(train_dataset, batch_size=11, shuffle=True)

# Configurar otimizador
optimizer = AdamW(model.parameters(), lr=5e-5)
optimizer_path = os.path.join(checkpoint_dir, "optimizer.pt")

if os.path.exists(optimizer_path):
    print("Carregando otimizador do checkpoint...")
    optimizer.load_state_dict(torch.load(optimizer_path))

# Habilitar checkpointing
model.gradient_checkpointing_enable()
model.enable_input_require_grads()

# Configurar dispositivo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Treinamento
num_epochs = 5
scaler = torch.amp.GradScaler('cuda')

for epoch in range(num_epochs):
    print(f"Epoch {epoch+1}/{num_epochs}")
    model.train()
    total_loss = 0
    
    for batch in train_dataloader:
        optimizer.zero_grad()
        inputs = {key: value.to(device) for key, value in batch.items() if key != "label"}
        labels = batch["label"].to(device)
        
        with torch.amp.autocast('cuda'):
            outputs = model(**inputs, labels=labels)
            loss = outputs.loss
        
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        
        total_loss += loss.item()
    
    avg_loss = total_loss / len(train_dataloader)
    print(f"Loss: {avg_loss:.6f}")
    
    # Salvar modelo e otimizador após cada época
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)
    torch.save(optimizer.state_dict(), optimizer_path)
    print(f"Checkpoint salvo para a época {epoch+1}.")
