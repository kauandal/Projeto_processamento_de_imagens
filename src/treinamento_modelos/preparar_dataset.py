import os
import cv2
import shutil
import random
from pathlib import Path

DATASET_ORIGINAL = Path(r"D:\Faculdade\12 semestre\processamento de imagens\projeto\Dataset_cru\images") 

ROOT_DIR_PROJETO = Path(".") 
DATASET_YOLO = ROOT_DIR_PROJETO / "Data" / "Datasets"

for split in ['train', 'test']:
    os.makedirs(DATASET_YOLO / split / 'images', exist_ok=True)
    os.makedirs(DATASET_YOLO / split / 'labels', exist_ok=True)

def converter_para_yolo(txt_path, img_width, img_height):
    """Lê o txt do RodoSol e converte os corners para o formato YOLO."""
    with open(txt_path, 'r') as f:
        linhas = f.readlines()
        
    corners_str = ""
    for linha in linhas:
        if linha.startswith("corners:"):
            corners_str = linha.replace("corners:", "").strip()
            break
            
    if not corners_str:
        return None

    pontos = []
    for par in corners_str.split():
        x, y = map(int, par.split(','))
        pontos.append((x, y))
        
    x_coords = [p[0] for p in pontos]
    y_coords = [p[1] for p in pontos]
    
    xmin, xmax = min(x_coords), max(x_coords)
    ymin, ymax = min(y_coords), max(y_coords)
    
    centro_x = ((xmin + xmax) / 2) / img_width
    centro_y = ((ymin + ymax) / 2) / img_height
    largura = (xmax - xmin) / img_width
    altura = (ymax - ymin) / img_height
    
    return f"0 {centro_x:.6f} {centro_y:.6f} {largura:.6f} {altura:.6f}"

pastas_origem = ['cars-br', 'cars-me', 'motorcycles-br', 'motorcycles-me']
todos_os_arquivos = []

for pasta in pastas_origem:
    caminho_pasta = DATASET_ORIGINAL / pasta
    if not caminho_pasta.exists():
        continue
        
    for img_path in caminho_pasta.glob("*.jpg"):
        txt_path = img_path.with_suffix('.txt')
        if txt_path.exists():
            todos_os_arquivos.append((img_path, txt_path))

random.shuffle(todos_os_arquivos)

# Split 80/20
split_idx = int(len(todos_os_arquivos) * 0.8)
train_files = todos_os_arquivos[:split_idx]
test_files = todos_os_arquivos[split_idx:]

def processar_lote(lote, tipo_split):
    print(f"Processando {len(lote)} imagens para o conjunto de {tipo_split}...")
    for img_path, txt_path in lote:
        img = cv2.imread(str(img_path))
        h, w = img.shape[:2]
        
        linha_yolo = converter_para_yolo(txt_path, w, h)
        if linha_yolo:
            shutil.copy(img_path, DATASET_YOLO / tipo_split / 'images' / img_path.name)
            label_path = DATASET_YOLO / tipo_split / 'labels' / txt_path.name
            with open(label_path, 'w') as f:
                f.write(linha_yolo + '\n')

processar_lote(train_files, 'train')
processar_lote(test_files, 'test')
print("Dataset convertido e estruturado com sucesso!")