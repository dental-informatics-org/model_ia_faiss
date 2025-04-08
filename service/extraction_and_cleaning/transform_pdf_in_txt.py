import fitz 

def extrair_texto_pdf(file_location: str) -> str:
    text = ""
    try:
        print(file_location)
        documento = fitz.open(file_location)
        for pagina in documento:
            text += pagina.get_text()
        documento.close()
        return text
    except Exception as e:
        print(f"Erro ao processar {file_location}: {e}")
        return ""