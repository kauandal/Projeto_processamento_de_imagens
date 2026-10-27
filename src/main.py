import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO
from pre_processamento.filtros import preprocessar_para_ocr
from ocr.leitura import extrair_texto
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parent.parent

caminho_modelo = RAIZ_PROJETO / 'Models' / 'Deteccao_placa' / 'best.pt'
caminho_imagem = RAIZ_PROJETO / 'Data' / 'Datasets' / 'test' / 'images' / 'img_000002.jpg'
caminho_resultado = RAIZ_PROJETO / 'Data' / 'results' / 'resultado_final.jpg'

# Garante que a pasta de resultados exista
caminho_resultado.parent.mkdir(parents=True, exist_ok=True)

print("[SISTEMA] Iniciando carregamento do modelo e leitura da imagem...")
modelo_yolo = YOLO(str(caminho_modelo))
img_original = cv2.imread(str(caminho_imagem))

if img_original is None:
    raise FileNotFoundError(f"Imagem não encontrada em: {caminho_imagem}")

img_rgb = cv2.cvtColor(img_original, cv2.COLOR_BGR2RGB)

print("[SISTEMA] Realizando inferencia na imagem...")
resultados = modelo_yolo.predict(img_original, conf=0.5, verbose=False)

if len(resultados[0].boxes) > 0:
    box = resultados[0].boxes[0]
    xmin, ymin, xmax, ymax = map(int, box.xyxy[0])
    
    placa_recortada = img_original[ymin:ymax, xmin:xmax]
    
    placa_pronta = preprocessar_para_ocr(placa_recortada)
    
    print("[SISTEMA] Extraindo texto via OCR...")
    texto_placa = extrair_texto(placa_pronta)
    
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    
    img_bbox = img_rgb.copy()
    cv2.rectangle(img_bbox, (xmin, ymin), (xmax, ymax), (0, 255, 0), 3)
    ax[0].imshow(img_bbox)
    ax[0].set_title('1. Detecção YOLO')
    ax[0].axis('off')
    
    ax[1].imshow(cv2.cvtColor(placa_recortada, cv2.COLOR_BGR2RGB))
    ax[1].set_title('2. Recorte')
    ax[1].axis('off')
    
    ax[2].imshow(placa_pronta, cmap='gray')
    ax[2].set_title(f'3. OCR: {texto_placa}')
    ax[2].axis('off')
    
    plt.tight_layout()
    plt.savefig(str(caminho_resultado))
    
    print("----------------------------------------")
    print(f"RESULTADO FINAL - PLACA DETECTADA: {texto_placa}")
    print(f"Imagem de analise salva em: {caminho_resultado}")
    print("----------------------------------------")
else:
    print("Nenhuma placa detectada na imagem.")