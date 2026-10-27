# Proposta Técnica Revisada

> Convenção deste documento: trechos marcados com `[PENDENTE: ...]` dependem de resultados experimentais ou de confirmação da equipe e devem ser preenchidos antes da entrega.

## 1. Problema

Sistemas de monitoramento de veículos (pedágios, estacionamentos, controle de acesso) dependem de operadores humanos para identificar placas em imagens de câmera, o que gera custo e erro. O problema investigado é o reconhecimento automático de placas brasileiras (ALPR) em imagens estáticas: localizar a placa no quadro e ler sua sequência de caracteres.

Na M2 o problema foi delimitado, conforme o feedback da M1, para imagens de câmeras fixas de pedágio do conjunto RodoSol-ALPR, com placas nos padrões brasileiro antigo e Mercosul, em carros e motocicletas.

## 2. Objetivo geral

Desenvolver um pipeline que receba uma imagem de veículo, localize a placa, prepare a região recortada por processamento de imagens e produza o texto da placa.

## 3. Objetivos específicos

1. Localizar a placa na imagem com um detector YOLOv8 ajustado (fine-tuning) ao RodoSol-ALPR e medir a qualidade da localização contra os cantos anotados.
2. Preparar a região da placa com realce de contraste, suavização, binarização, correção de inclinação e morfologia, gerando saídas intermediárias verificáveis.
3. Comparar de forma controlada configurações de binarização e de morfologia na região da placa.
4. Planejar para a M3 a segmentação dos caracteres por componentes conectados, a descrição das regiões e a avaliação da leitura.

## 4. Escopo

### 4.1 Dentro do escopo da M2

- Imagens estáticas do RodoSol-ALPR (carros e motocicletas, padrões brasileiro e Mercosul).
- Uma placa por imagem (o pipeline atual usa a primeira detecção).
- Localização por YOLOv8n ajustado e pré-processamento da região recortada.
- Leitura preliminar com Tesseract, usada apenas como saída demonstrativa.
- Avaliação quantitativa preliminar da localização e das configurações de binarização/morfologia.

### 4.2 Fora do escopo da M2

- Vídeo e rastreamento entre quadros.
- Múltiplas placas na mesma imagem.
- Placas de motocicleta em duas linhas na etapa de OCR (o modo atual do Tesseract lê uma única linha).
- Treinamento de um reconhecedor de caracteres próprio.
- Imagens de outras fontes ou condições de aquisição (noturnas com infravermelho, câmeras móveis).

## 5. Entradas e saídas

| Item | Descrição |
|---|---|
| Entrada | Imagem colorida de um veículo (JPEG do RodoSol-ALPR). |
| Saída intermediária 1 | Caixa delimitadora da placa (xmin, ymin, xmax, ymax) e confiança do detector. |
| Saída intermediária 2 | Recorte da placa. |
| Saída intermediária 3 | Placa binarizada, alinhada e após morfologia, pronta para o OCR. |
| Saída final | Texto da placa (A-Z, 0-9) e figura com as três etapas em `Data/results/`. |

## 6. Critérios de sucesso

| Critério | Indicador | Meta |
|---|---|---|
| Localização da placa | IoU entre a caixa prevista e a caixa obtida dos 4 cantos anotados | IoU médio `[PENDENTE: meta da equipe]` |
| Taxa de localização correta | Proporção de imagens com IoU >= 0,5 (critério usual em detecção de objetos) | `[PENDENTE: meta da equipe]` |
| Qualidade da binarização | Proporção de placas cuja leitura coincide exatamente com o texto anotado e acerto por caractere | `[PENDENTE: meta da equipe]` |
| Segmentação de caracteres (M3) | Erro de contagem de componentes em relação aos 7 caracteres esperados | `[PENDENTE: meta da equipe]` |

## 7. Pipeline proposto

1. Entrada: leitura da imagem com OpenCV.
2. Localização: YOLOv8n ajustado ao RodoSol-ALPR (`Models/Deteccao_placa/best.pt`), limiar de confiança 0,5.
3. Recorte da região da placa a partir da caixa prevista.
4. Pré-processamento da placa (`src/pre_processamento/filtros.py`): tons de cinza, CLAHE, filtro bilateral, limiar adaptativo gaussiano, correção de inclinação, fechamento morfológico e inversão.
5. Leitura com Tesseract em modo de linha única, com lista de caracteres permitidos (`src/ocr/leitura.py`).
6. Saída: figura com detecção, recorte e placa processada, e texto impresso no console.

Etapas planejadas para a M3: segmentação de caracteres por componentes conectados, filtragem por descritores de forma, retificação da placa por transformação de perspectiva e avaliação sistemática da leitura.

Experimentos propostos para a M2 `[PENDENTE: confirmar escolha da equipe]`:

- Experimento 1: limiar adaptativo gaussiano (configuração atual) contra limiar global de Otsu, aplicados aos mesmos recortes de placa.
- Experimento 2: pré-processamento com e sem o fechamento morfológico 2x2.

Para isolar o efeito do pré-processamento dos erros do detector, os recortes dos experimentos 1 e 2 devem ser obtidos a partir dos cantos anotados, e não da caixa prevista pelo YOLO.

## 8. Mudanças desde a M1

| Item | M1 | M2 | Justificativa | Evidência |
|---|---|---|---|---|
| Escopo | Pré-processamento, detecção, retificação e OCR, com possível extensão a vídeo | Imagens estáticas, uma placa por imagem, foco em localização e preparação da placa | Feedback 1 da M1 (escopo amplo) | Seção 4 deste documento |
| Ordem do pipeline | Pré-processamento da imagem inteira antes da detecção | Detecção primeiro; pré-processamento aplicado só ao recorte da placa | `[PENDENTE: equipe confirmar motivo]` | `src/main.py` |
| Métricas | Não definidas | IoU, taxa de localização correta, acerto de leitura | Feedback 3 da M1 | Seção 6 deste documento |
| Implementação | Pastas vazias | Pipeline executável com YOLO, PDI e OCR, em Docker | Feedbacks 5 e 6 da M1 | `src/`, `Dockerfile` |
| Documentação | Concentrada no README | Proposta, relatório, dados e decisões em `docs/` | Feedback 7 da M1 | `docs/` |
| Tecnologias | Pillow e OpenCV | OpenCV, Ultralytics, Tesseract; Pillow não é usado | Ferramentas efetivamente adotadas no código | `requirements.txt` |

## 9. Riscos

| Risco | Impacto | Mitigação |
|---|---|---|
| Divisão treino/teste aleatória sem semente e sem conjunto de validação separado | Resultados não reproduzíveis e possivelmente otimistas | Adotar a divisão oficial do RodoSol-ALPR e registrar os IDs em `Data/splits/` |
| Placas de motocicleta em duas linhas | Falha sistemática do OCR em modo de linha única | Separar resultados por subconjunto; tratar na M3 |
| Correção de inclinação baseada em `minAreaRect` sobre todos os pixels brancos | Ângulo dominado pela moldura ou por ruído | Avaliar casos inclinados; considerar retificação pelos 4 cantos na M3 |
| Restrição de licença do dataset | Imagens não podem ser publicadas | Versionar apenas IDs, código e resultados agregados |
| Dependência de GPU para treino | Só um integrante consegue treinar | Versionar o modelo treinado e os registros do treino |

## 10. Referências

Ver a seção de referências em [relatorio_m2.md](relatorio_m2.md#10-referências).
