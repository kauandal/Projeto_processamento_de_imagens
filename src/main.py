import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO
from src.pre_processamento.filtros import preprocessar_para_ocr
from src.ocr.leitura import extrair_texto

caminho_modelo = 'Models/Deteccao_placa/yolov8_rodosol/weights/best.pt'
modelo_yolo = YOLO(caminho_modelo)

caminho_imagem = 'Data/Datasets/test/images/img_010001.jpg'
img_original = cv2.imread(caminho_imagem)
img_rgb = cv2.cvtColor(img_original, cv2.COLOR_BGR2RGB)

resultados = modelo_yolo.predict(img_original, conf=0.5)

if len(resultados[0].boxes) > 0:
    box = resultados[0].boxes[0]
    xmin, ymin, xmax, ymax = map(int, box.xyxy[0])
    
    placa_recortada = img_original[ymin:ymax, xmin:xmax]
    
    placa_pronta = preprocessar_para_ocr(placa_recortada)
    
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
    plt.show()
    
    print(f"Placa detectada: {texto_placa}")
else:
    print("Nenhuma placa detectada na imagem.")