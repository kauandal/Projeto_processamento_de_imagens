# Instalar antes: pip install ultralytics
from ultralytics import YOLO

def treinar_modelo():
    model = YOLO('yolov8n.pt') 

    # Inicia o fine-tunning
    results = model.train(
        data='Data/Datasets/data.yaml', 
        epochs=100,             # 100 épocas geralmente é suficiente
        imgsz=640,
        batch=32,       
        device=0,       
        workers=2,              
        project='Models/Deteccao_placa', # Onde salvar o modelo treinado
        name='yolov8_rodosol', # Nome da pasta de resultados
        patience=10            # Early Stopping se não melhorar após 10 épocas
    )

if __name__ == '__main__':
    treinar_modelo()