# Registro de Decisões

> Datas e responsáveis tirados do histórico do git quando disponíveis. Trechos marcados com `[PENDENTE: ...]` precisam de confirmação da equipe.

| Nº | Data | Decisão | Alternativas consideradas | Justificativa | Responsável |
|---:|---|---|---|---|---|
| D1 | 26/10/2026 | Localizar a placa com YOLOv8n ajustado ao RodoSol-ALPR, e não por segmentação clássica | Limiarização, bordas, morfologia e filtragem de contornos na imagem inteira (previsto na revisão da M1) | YOLO já era a proposta da M1; o dataset tem anotações suficientes para ajuste; a variação de fundo e veículo dificulta regras fixas na imagem inteira. As técnicas de segmentação e morfologia passam a atuar na região recortada `[PENDENTE: equipe validar]` | João |
| D2 | 26/10/2026 | Aplicar o pré-processamento apenas ao recorte da placa, depois da detecção | Pré-processar a imagem inteira antes da detecção (proposta da M1) | O detector trabalha com a imagem colorida original; binarizar antes eliminaria informação usada por ele `[PENDENTE: equipe validar]` | João |
| D3 | 26/10/2026 | Usar Tesseract para a leitura na M2 | Treinar reconhecedor próprio; outras bibliotecas de OCR | Disponível sem treino; permite demonstrar o fluxo completo; a avaliação da leitura fica para a M3 `[PENDENTE: equipe validar]` | João |
| D4 | 26/10/2026 | Converter os 4 cantos anotados em caixa alinhada aos eixos para treinar o YOLO | Treinar modelo de caixa orientada ou de pontos-chave | Formato padrão de detecção do Ultralytics; os 4 cantos continuam disponíveis para avaliação e retificação | João |
| D5 | 27/10/2026 | Executar o pipeline em Docker (Python 3.11, Tesseract, ultralytics 8.3.163) | Instalação manual em cada máquina | Elimina diferenças de ambiente, incluindo a instalação do Tesseract no Windows | João |
| D6 | 27/10/2026 | Não versionar imagens do dataset; versionar apenas IDs, código e resultados | Publicar uma amostra de imagens | Termo de licença do RodoSol-ALPR restringe a redistribuição | Kauan |
| D7 | 27/10/2026 | Versionar o modelo treinado `Models/Deteccao_placa/best.pt` (19 MB) | Hospedar fora do repositório e documentar o download | Permite executar o pipeline sem GPU e sem retreinar `[PENDENTE: confirmar se o termo de licença permite publicar o modelo]` | João |
| D8 | 27/10/2026 | Avaliar o pré-processamento com recortes obtidos dos cantos anotados | Avaliar com recortes do YOLO | Isola o efeito da binarização e da morfologia dos erros do detector `[PENDENTE: equipe validar]` | Kauan |
| D9 | `[PENDENTE]` | Divisão dos dados para treino e avaliação | Divisão aleatória 80/20 atual; divisão oficial do dataset | `[PENDENTE: equipe decidir; recomendação: divisão oficial, com IDs registrados]` | `[PENDENTE]` |
