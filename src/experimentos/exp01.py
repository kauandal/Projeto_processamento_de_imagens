import cv2
import re
import random
import csv
import pytesseract
import matplotlib.pyplot as plt
from pathlib import Path
from ultralytics import YOLO

# Resolução dinâmica que funciona tanto rodando solto no src/ quanto dentro de src/experimentos/
dir_atual = Path(__file__).resolve().parent
RAIZ_PROJETO = dir_atual.parent.parent if dir_atual.name == 'experimentos' else dir_atual.parent

CAMINHO_YOLO = RAIZ_PROJETO / 'Models' / 'Deteccao_placa' / 'best.pt'
PASTA_DATASET_ORIGINAL = RAIZ_PROJETO / 'Data' / 'imagens_testes' / 'dataset_original'
PASTA_SAIDA_CSV = RAIZ_PROJETO / 'Data' / 'results' / 'exp01'
PASTA_FIGURAS = RAIZ_PROJETO / 'docs' / 'figuras'

PASTA_SAIDA_CSV.mkdir(parents=True, exist_ok=True)
PASTA_FIGURAS.mkdir(parents=True, exist_ok=True)

def extrair_texto_ocr(imagem_bin):
    config = '--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    texto = pytesseract.image_to_string(imagem_bin, config=config)
    return re.sub(r'[^A-Z0-9]', '', texto.upper())

def processar_otsu(img_gray):
    _, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh

def processar_adaptativo(img_gray):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray_contrast = clahe.apply(img_gray)
    blur = cv2.bilateralFilter(gray_contrast, d=11, sigmaColor=17, sigmaSpace=17)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 9)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    return cv2.bitwise_not(cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel))

def salvar_comparacao(recorte, otsu, txt_otsu, adapt, txt_adapt, txt_real, img_nome, filename):
    fig, ax = plt.subplots(1, 3, figsize=(12, 4))
    ax[0].imshow(cv2.cvtColor(recorte, cv2.COLOR_BGR2RGB))
    ax[0].set_title(f'Original\nReal: {txt_real}')
    ax[0].axis('off')
    
    ax[1].imshow(otsu, cmap='gray')
    ax[1].set_title(f'Otsu\nLido: {txt_otsu}')
    ax[1].axis('off')
    
    ax[2].imshow(adapt, cmap='gray')
    ax[2].set_title(f'Adaptativo\nLido: {txt_adapt}')
    ax[2].axis('off')
    
    plt.tight_layout()
    plt.savefig(str(PASTA_FIGURAS / f"{img_nome}_{filename}"))
    plt.close()

def rodar_experimento(qnt_imagens=50):
    if not CAMINHO_YOLO.exists() or not PASTA_DATASET_ORIGINAL.exists():
        print(f"[ERRO] Caminhos nao encontrados no exp01.\nYOLO: {CAMINHO_YOLO}\nDataset: {PASTA_DATASET_ORIGINAL}")
        return

    modelo_yolo = YOLO(str(CAMINHO_YOLO))
    imagens = list(PASTA_DATASET_ORIGINAL.glob("*.jpg"))
    random.shuffle(imagens)
    
    acertos_otsu = 0
    acertos_adaptativo = 0
    analisadas = 0
    
    print(f"\n[EXP01] Iniciando experimento controlado com {qnt_imagens} imagens...")
    
    csv_path = PASTA_SAIDA_CSV / 'resultados_exp01.csv'
    
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Imagem', 'Real (Ground Truth)', 'Lido Otsu', 'Lido Adaptativo', 'Acerto Otsu', 'Acerto Adaptativo'])
        
        for img_path in imagens[:qnt_imagens]:
            txt_path = img_path.with_suffix('.txt')
            if not txt_path.exists(): continue
                
            texto_real = ""
            with open(txt_path, 'r') as f:
                for linha in f:
                    if linha.startswith("plate:"):
                        texto_real = linha.split(":")[1].strip().upper()
            
            if not texto_real: continue

            img = cv2.imread(str(img_path))
            resultados = modelo_yolo.predict(img, conf=0.5, verbose=False)
            
            if len(resultados[0].boxes) > 0:
                box = resultados[0].boxes[0]
                xmin, ymin, xmax, ymax = map(int, box.xyxy[0])
                placa_recortada = img[ymin:ymax, xmin:xmax]
                gray = cv2.cvtColor(placa_recortada, cv2.COLOR_BGR2GRAY)
                
                img_otsu = processar_otsu(gray)
                img_adapt = processar_adaptativo(gray)
                
                texto_otsu = extrair_texto_ocr(img_otsu)
                texto_adapt = extrair_texto_ocr(img_adapt)
                
                acertou_otsu = (texto_otsu == texto_real)
                acertou_adapt = (texto_adapt == texto_real)
                
                if acertou_otsu: acertos_otsu += 1
                if acertou_adapt: acertos_adaptativo += 1
                analisadas += 1
                
                writer.writerow([img_path.name, texto_real, texto_otsu, texto_adapt, acertou_otsu, acertou_adapt])
                
                if acertou_adapt and not acertou_otsu:
                    salvar_comparacao(placa_recortada, img_otsu, texto_otsu, img_adapt, texto_adapt, texto_real, img_path.name, "sucesso_adaptativo.jpg")
                elif not acertou_adapt and not acertou_otsu:
                    salvar_comparacao(placa_recortada, img_otsu, texto_otsu, img_adapt, texto_adapt, texto_real, img_path.name, "falha_geral.jpg")

    # Resumo no terminal
    print("\n" + "="*40)
    print("RESULTADOS QUANTITATIVOS DO EXPERIMENTO 1")
    print(f"Total analisadas com sucesso no recorte YOLO: {analisadas}")
    if analisadas > 0:
        print(f"Acertos OCR com Otsu Global: {acertos_otsu} ({(acertos_otsu/analisadas)*100:.1f}%)")
        print(f"Acertos OCR com Adaptativo: {acertos_adaptativo} ({(acertos_adaptativo/analisadas)*100:.1f}%)")
    print("="*40)
    print(f"[EXP01] Analise concluida. Resultados detalhados salvos em: {csv_path}")

if __name__ == "__main__":
    rodar_experimento(50)