# Registro de Decisões

> Datas e responsáveis tirados do histórico do git.

| Nº | Data | Decisão | Alternativas consideradas | Justificativa | Responsável |
|---:|---|---|---|---|---|
| D1 | 26/10/2026 | Localizar a placa com YOLOv8n ajustado ao RodoSol-ALPR, e não por segmentação clássica | Limiarização, bordas, morfologia e filtragem de contornos na imagem inteira (previsto na revisão da M1) | YOLO já era a proposta da M1; o dataset tem anotações suficientes para ajuste; a variação de fundo e veículo dificulta regras fixas na imagem inteira. As técnicas de segmentação e morfologia passam a atuar na região recortada | João |
| D2 | 26/10/2026 | Aplicar o pré-processamento apenas ao recorte da placa, depois da detecção | Pré-processar a imagem inteira antes da detecção (proposta da M1) | O detector trabalha com a imagem colorida original; binarizar antes eliminaria informação usada por ele | João |
| D3 | 26/10/2026 | Usar Tesseract para a leitura na M2 | Treinar reconhecedor próprio; outras bibliotecas de OCR | Disponível sem treino; permite demonstrar o fluxo completo; a avaliação detalhada da leitura fica para a M3 | João |
| D4 | 26/10/2026 | Converter os 4 cantos anotados em caixa alinhada aos eixos para treinar o YOLO | Treinar modelo de caixa orientada ou de pontos-chave | Formato padrão de detecção do Ultralytics; os 4 cantos continuam disponíveis para avaliação e retificação | João |
| D5 | 27/10/2026 | Executar o pipeline em Docker (Python 3.11, Tesseract, ultralytics 8.3.163) | Instalação manual em cada máquina | Elimina diferenças de ambiente, incluindo a instalação do Tesseract no Windows | João |
| D6 | 27/10/2026 | Versionar uma amostra de 100 imagens em `Data/imagens_testes/`, sem versionar o dataset completo | Não versionar nenhuma imagem e exigir o dataset montado como volume | Permite executar o pipeline e o experimento a partir do repositório, sem o dataset completo de 20.000 imagens | João |
| D7 | 27/10/2026 | Versionar o modelo treinado `Models/Deteccao_placa/best.pt` (19 MB) | Hospedar fora do repositório e documentar o download | Permite executar o pipeline sem GPU e sem retreinar | João |
| D8 | 27/10/2026 | Avaliar o pré-processamento com os recortes do YOLO | Recortar pelos cantos anotados | Avalia o pipeline nas condições reais de uso; o mesmo recorte é usado nas duas configurações, o que mantém a comparação controlada | João, Gustavo |
| D9 | 26/10/2026 | Divisão aleatória 80/20 para treino e validação do detector | Divisão oficial do dataset com validação separada | Divisão usada no treino disponível; a adoção da divisão oficial está no plano da M3 | João |
| D10 | 27/10/2026 | Comparar um Otsu simples com o pré-processamento completo do pipeline no experimento 1 | Trocar só o tipo de limiar mantendo o restante | Verifica se a cadeia completa atual se justifica frente a um método mais simples; a comparação isolada fica para a M3 | João, Gustavo |
| D11 | 27/10/2026 | Revisar o limiar adaptativo do pipeline na M3 | Manter a configuração atual | No experimento 1, o Otsu simples teve 40% de acerto exato contra 12% do pipeline completo | Equipe |
| D12 | 27/10/2026 | Não produzir o vídeo da M2 | Gravar vídeo curto ou completo | O tempo disponível até a entrega foi priorizado para a implementação, o experimento e a documentação; o roteiro preparado em `docs/roteiro_video_m2.md` fica como base para o vídeo da M3 | Equipe |
