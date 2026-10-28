import shutil
import random
from pathlib import Path

# 1. Definição dos Caminhos Principais
RAIZ_PROJETO = Path(r"D:\Faculdade\12 semestre\processamento de imagens\projeto\Projeto_processamento_de_imagens")
PASTA_CRUA_ORIGEM = Path(r"D:\Faculdade\12 semestre\processamento de imagens\projeto\Dataset_cru\images\cars-br")

# Caminhos de Origem (YOLO)
YOLO_ORIGEM_IMG = RAIZ_PROJETO / 'Data' / 'Datasets' / 'test' / 'images'
YOLO_ORIGEM_LBL = RAIZ_PROJETO / 'Data' / 'Datasets' / 'test' / 'labels'
YOLO_YAML = RAIZ_PROJETO / 'Data' / 'Datasets' / 'data.yaml'

# Caminhos de Destino (Para o Docker)
DESTINO_CRU = RAIZ_PROJETO / 'Data' / 'imagens_testes' / 'dataset_original'
DESTINO_YOLO_IMG = RAIZ_PROJETO / 'Data' / 'imagens_testes' / 'yolo' / 'images'
DESTINO_YOLO_LBL = RAIZ_PROJETO / 'Data' / 'imagens_testes' / 'yolo' / 'labels'

# 2. Criar pastas de destino (cria as subpastas automaticamente se não existirem)
DESTINO_CRU.mkdir(parents=True, exist_ok=True)
DESTINO_YOLO_IMG.mkdir(parents=True, exist_ok=True)
DESTINO_YOLO_LBL.mkdir(parents=True, exist_ok=True)

def separar_amostra(pasta_origem_img, pasta_origem_txt, pasta_destino_img, pasta_destino_txt, quantidade=50):
    # Pega todas as imagens JPG da pasta
    todas_imagens = list(pasta_origem_img.glob('*.jpg'))
    
    # Embaralha e seleciona a quantidade desejada para evitar viés
    random.shuffle(todas_imagens)
    amostra = todas_imagens[:quantidade]
    
    sucessos = 0
    for img_path in amostra:
        txt_path = pasta_origem_txt / (img_path.stem + '.txt')
        
        # Só copia se o arquivo de texto (anotação/label) correspondente existir
        if txt_path.exists():
            shutil.copy(img_path, pasta_destino_img / img_path.name)
            
            # Se a pasta de destino do txt for diferente da img (caso do YOLO), usa a específica
            if pasta_destino_txt:
                shutil.copy(txt_path, pasta_destino_txt / txt_path.name)
            else:
                shutil.copy(txt_path, pasta_destino_img / txt_path.name) # Caso dataset cru
                
            sucessos += 1
            
    return sucessos

print("Separando 50 imagens do Dataset Cru...")
# No dataset cru, as imagens e anotações estão na mesma pasta
qtd_cru = separar_amostra(PASTA_CRUA_ORIGEM, PASTA_CRUA_ORIGEM, DESTINO_CRU, None, 50)
print(f"Sucesso: {qtd_cru} pares (img/txt) copiados para o Dataset Original.")

print("\nSeparando 50 imagens do Dataset YOLO...")
# No dataset YOLO, imagens e labels estão em pastas separadas
qtd_yolo = separar_amostra(YOLO_ORIGEM_IMG, YOLO_ORIGEM_LBL, DESTINO_YOLO_IMG, DESTINO_YOLO_LBL, 50)
print(f"Sucesso: {qtd_yolo} pares copiados para o Dataset YOLO.")

# Copia o data.yaml para a raiz da nova pasta yolo
if YOLO_YAML.exists():
    shutil.copy(YOLO_YAML, RAIZ_PROJETO / 'Data' / 'imagens_testes' / 'yolo' / 'data.yaml')
    print("Arquivo data.yaml copiado com sucesso.")

print("\nConcluído! A sua pasta 'Data/imagens_testes' está pronta para ser usada no Docker.")