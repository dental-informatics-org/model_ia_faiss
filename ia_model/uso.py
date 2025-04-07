import torch
from transformers import LongformerTokenizer, LongformerForSequenceClassification


# Carregar o modelo e tokenizer
tokenizer = LongformerTokenizer.from_pretrained('allenai/longformer-base-4096')
model = LongformerForSequenceClassification.from_pretrained('allenai/longformer-base-4096')


# Função de previsão
def predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=2048)
    
    # Enviar para GPU, se disponível
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = outputs.logits.argmax(dim=-1)
    
    return predictions.item()
