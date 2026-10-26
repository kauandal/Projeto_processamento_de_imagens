# Instale o tesseract no sistema operacional e depois: pip install pytesseract
import pytesseract
import re

# Ajuste o caminho do executável caso esteja no Windows
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extrair_texto(imagem_processada):
    
    configuracao = '--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    
    texto_extraido = pytesseract.image_to_string(imagem_processada, config=configuracao)
    
    texto_limpo = re.sub(r'[^A-Z0-9]', '', texto_extraido.upper())
    
    return texto_limpo