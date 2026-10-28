import cv2
import csv
import matplotlib.pyplot as plt
from ultralytics import YOLO
from pre_processamento.filtros import preprocessar_para_ocr
from ocr.leitura import extrair_texto
from pathlib import Path

try:
    from experimentos.exp01 import rodar_experimento
except ModuleNotFoundError:
    from exp01 import rodar_experimento

RAIZ_PROJETO = Path(__file__).resolve().parent.parent

caminho_modelo = RAIZ_PROJETO / 'Models' / 'Deteccao_placa' / 'best.pt'
pasta_imagens_yolo = RAIZ_PROJETO / 'Data' / 'imagens_testes' / 'yolo' / 'images'
pasta_resultados_pipeline = RAIZ_PROJETO / 'Data' / 'results' / 'pipeline'

pasta_resultados_pipeline.mkdir(parents=True, exist_ok=True)

print("[SISTEMA] Iniciando carregamento do modelo...")
if not caminho_modelo.exists():
    raise FileNotFoundError(f"Modelo não encontrado em: {caminho_modelo}")

modelo_yolo = YOLO(str(caminho_modelo))

imagens_teste = list(pasta_imagens_yolo.glob('*.jpg'))
print(f"[SISTEMA] Iniciando pipeline principal em {len(imagens_teste)} imagens...")

csv_pipeline_path = pasta_resultados_pipeline / 'resultados_pipeline.csv'

with open(csv_pipeline_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Imagem', 'Texto Detectado', 'Placa Localizada'])

    for img_path in imagens_teste:
        img_original = cv2.imread(str(img_path))
        if img_original is None:
            continue

        img_rgb = cv2.cvtColor(img_original, cv2.COLOR_BGR2RGB)
        resultados = modelo_yolo.predict(img_original, conf=0.5, verbose=False)

        if len(resultados[0].boxes) > 0:
            box = resultados[0].boxes[0]
            xmin, ymin, xmax, ymax = map(int, box.xyxy[0])
            
            placa_recortada = img_original[ymin:ymax, xmin:xmax]
            placa_pronta = preprocessar_para_ocr(placa_recortada)
            texto_placa = extrair_texto(placa_pronta)
            
            writer.writerow([img_path.name, texto_placa, True])
            
            # Montagem e salvamento da imagem com os 3 passos
            fig, ax = plt.subplots(1, 3, figsize=(15, 5))
            img_bbox = img_rgb.copy()
            cv2.rectangle(img_bbox, (xmin, ymin), (xmax, ymax), (0, 255, 0), 3)
            
            ax[0].imshow(img_bbox)
            ax[0].set_title('1. Deteccao YOLO')
            ax[0].axis('off')
            
            ax[1].imshow(cv2.cvtColor(placa_recortada, cv2.COLOR_BGR2RGB))
            ax[1].set_title('2. Recorte')
            ax[1].axis('off')
            
            ax[2].imshow(placa_pronta, cmap='gray')
            ax[2].set_title(f'3. OCR: {texto_placa}')
            ax[2].axis('off')
            
            plt.tight_layout()
            caminho_salvamento_img = pasta_resultados_pipeline / f"result_{img_path.name}"
            plt.savefig(str(caminho_salvamento_img))
            plt.close()
        else:
            writer.writerow([img_path.name, "NENHUMA PLACA", False])

print("[SISTEMA] Pipeline principal finalizado.")
print(f"[SISTEMA] Imagens salvas e CSV gerado em: {pasta_resultados_pipeline}")
print("-" * 50)

print("[SISTEMA] Iniciando execucao do Experimento 01...")
rodar_experimento(50)
print("[SISTEMA] Processo completo finalizado com sucesso.")