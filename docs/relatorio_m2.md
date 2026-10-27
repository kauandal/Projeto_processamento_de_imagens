# Relatório Parcial M2

> Trechos marcados com `[PENDENTE: ...]` dependem de resultados experimentais ou de confirmação da equipe e devem ser preenchidos antes da entrega.

## Identificação

| Item | Informação |
|---|---|
| Projeto | Leitura automática de placas de veículos brasileiros (ALPR) |
| Integrantes | Gustavo Odilon da Costa, João Vitor Loch Martins, Kauan Rocha Dalfovo |
| Repositório | https://github.com/kauandal/Projeto_processamento_de_imagens |
| Commit/tag da entrega | `[PENDENTE]` |
| Vídeo M2 | `[PENDENTE]` |

## 1. Síntese do problema e objetivos atuais

O projeto trata do reconhecimento automático de placas brasileiras (ALPR) em imagens estáticas de câmeras de pedágio do conjunto RodoSol-ALPR. O objetivo é receber uma imagem de veículo, localizar a placa e produzir o texto nela escrito.

Na M2 o foco está em duas etapas: localizar a placa com um detector YOLOv8n ajustado ao dataset e preparar a região recortada com técnicas de processamento de imagens (realce, binarização, correção de inclinação e morfologia), com avaliação quantitativa da localização e comparação controlada de configurações de binarização e morfologia. A leitura com Tesseract é mantida como saída demonstrativa; a segmentação de caracteres e a avaliação completa da leitura ficam para a M3.

Objetivos, escopo e critérios de sucesso detalhados: [proposta.md](proposta.md).

## 2. Resposta ao feedback e evolução desde a M1

A revisão completa da devolutiva está em [revisao_m1_plano_m2.md](../revisao_m1_plano_m2.md). A tabela abaixo registra a ação efetivamente tomada para cada observação.

| Nº | Orientação recebida | Ação tomada | Arquivo/evidência |
|---:|---|---|---|
| 1 | Escopo do problema amplo | Escopo delimitado a imagens estáticas do RodoSol-ALPR, uma placa por imagem; vídeo e placas de motocicleta em duas linhas no OCR ficaram fora da M2 | [proposta.md, seção 4](proposta.md#4-escopo) |
| 2 | Sem amostra verificável do dataset | Origem, licença, obtenção, formato das anotações e preparação documentados; imagens não versionadas por restrição de licença; IDs usados registrados em `Data/splits/` | [dados.md](dados.md), `Data/splits/` `[PENDENTE: preencher IDs]` |
| 3 | Faltam métricas e critérios de sucesso | Definidos IoU contra os cantos anotados, taxa de localização correta (IoU >= 0,5) e acerto de leitura | [proposta.md, seção 6](proposta.md#6-critérios-de-sucesso), seção 6 deste relatório `[PENDENTE: resultados]` |
| 4 | Relação entre PDI, YOLO e OCR pouco clara | Pipeline descrito etapa por etapa, com entrada, saída e parâmetros de cada uma | Seções 4 e 5 deste relatório |
| 5 | Sem baseline executável | Pipeline executável de ponta a ponta com modelo ajustado e execução em Docker | `src/main.py`, `Dockerfile`, `Models/Deteccao_placa/best.pt` |
| 6 | Repositório com pouco conteúdo executável | Código de preparação de dados, treino, pré-processamento e OCR; dependências e comandos documentados | `src/`, `requirements.txt`, [README.md](../README.md) |
| 7 | Falta proposta técnica separada do README | Criado `docs/proposta.md` | [proposta.md](proposta.md) |
| 8 | Subtotal de 55,00/90 na devolutiva | Grupo apontou soma de 56,25/90 e solicitou esclarecimento | `[PENDENTE: registrar resposta do professor]` |
| 9 | Vídeo pendente com 10/10 pontos | Grupo solicitou confirmação da pontuação | `[PENDENTE: registrar resposta do professor]` |

Diferença em relação ao plano da M2: a revisão da M1 previa localizar a placa por segmentação clássica (limiarização, bordas e morfologia). O grupo manteve o detector YOLO, já previsto na proposta da M1, para a localização, e aplicou as técnicas de segmentação e morfologia na região recortada da placa. A justificativa está na decisão D1 de [decisoes.md](decisoes.md). `[PENDENTE: equipe validar a justificativa]`

## 3. Dados e protocolo experimental

### 3.1 Origem e condições de uso

RodoSol-ALPR: 20.000 imagens de câmeras fixas de pedágio da ES-060 (ES), carros e motocicletas, placas nos padrões brasileiro e Mercosul. Acesso mediante termo de licença para uso acadêmico, assinado pelo grupo. Imagens não versionadas. Detalhes em [dados.md](dados.md).

### 3.2 Quantidade usada e critérios de seleção

`[PENDENTE: quantidade efetiva no treino e no teste do detector; quantidade e critério do subconjunto usado nos experimentos de pré-processamento]`

### 3.3 Características e condições de aquisição

`[PENDENTE: resolução, período do dia, variação de iluminação, conforme documentação oficial e inspeção das imagens]`

### 3.4 Casos típicos e difíceis

| ID da imagem | Subconjunto | Situação |
|---|---|---|
| `[PENDENTE]` | | Caso típico |
| `[PENDENTE]` | | Placa inclinada |
| `[PENDENTE]` | | Baixo contraste ou iluminação desigual |
| `[PENDENTE]` | | Motocicleta, placa em duas linhas |

### 3.5 Referência de avaliação

As referências são as anotações do próprio RodoSol-ALPR, produzidas pelos autores do dataset: os quatro cantos da placa (referência de localização) e o texto da placa (referência de leitura). O grupo não produziu anotações próprias e não revisou a qualidade das anotações; essa é uma limitação da avaliação.

### 3.6 Divisão entre ajuste e avaliação

Detector: divisão aleatória 80/20 em `train` e `test`, sem semente. `[PENDENTE: João confirmar qual conjunto foi usado como validação no treino]`

Pré-processamento (método sem treino): parâmetros escolhidos em `Data/splits/ajuste_ids.txt` e avaliação final em `Data/splits/avaliacao_ids.txt`, sem interseção entre as listas. `[PENDENTE: preencher as listas]`

## 4. Pipeline implementado

### 4.1 Visão geral

```
imagem do veículo
  -> YOLOv8n ajustado (localização da placa)
  -> recorte da caixa delimitadora
  -> tons de cinza -> CLAHE -> filtro bilateral
  -> limiar adaptativo gaussiano (binarização)
  -> correção de inclinação
  -> fechamento morfológico 2x2 -> inversão
  -> Tesseract (linha única, A-Z e 0-9)
  -> texto da placa + figura em Data/results/
```

Ponto de entrada: `src/main.py`, executado diretamente ou pelo `Dockerfile`.

### 4.2 Etapas implementadas

| Etapa | Arquivo | Entrada | Saída | Parâmetros | Status |
|---|---|---|---|---|---|
| Preparação do dataset | `src/treinamento_modelos/preparar_dataset.py` | Imagens e anotações originais | Pastas `train`/`test` no formato YOLO | Divisão 80/20 | Implementado |
| Treino do detector | `src/treinamento_modelos/treinamento.py` | `data.yaml`, pesos `yolov8n.pt` | `best.pt` | 100 épocas, imgsz 640, batch 32, patience 10, GPU | Implementado |
| Localização | `src/main.py` | Imagem BGR | Caixa (xmin, ymin, xmax, ymax) | conf 0,5; primeira caixa | Implementado |
| Recorte | `src/main.py` | Imagem e caixa | Recorte da placa | | Implementado |
| Realce de contraste | `src/pre_processamento/filtros.py` (`aplicar_clahe`) | Placa em cinza | Placa realçada | clipLimit 2,0; tileGridSize 8x8 | Implementado |
| Suavização | `filtros.py` (`preprocessar_para_ocr`) | Placa realçada | Placa suavizada | Bilateral d 11, sigmaColor 17, sigmaSpace 17 | Implementado |
| Binarização | `filtros.py` | Placa suavizada | Máscara binária invertida | Adaptativo gaussiano, bloco 19, C 9 | Implementado |
| Correção de inclinação | `filtros.py` (`corrigir_inclinacao`) | Máscara binária | Máscara rotacionada | Ângulo de `minAreaRect` | Implementado, ver ressalva na seção 5.2 |
| Morfologia | `filtros.py` | Máscara alinhada | Máscara após fechamento | Elemento retangular 2x2 | Implementado |
| Leitura | `src/ocr/leitura.py` | Placa preparada | Texto A-Z/0-9 | Tesseract `--psm 7`, whitelist | Implementado (demonstrativo) |
| Saída visual | `src/main.py` | Etapas anteriores | `Data/results/resultado_final.jpg` | | Implementado |
| Avaliação de localização (IoU) | `src/avaliacao/metricas.py` | Caixa prevista e cantos anotados | IoU por imagem | | `[PENDENTE]` |
| Experimentos de binarização e morfologia | `src/experimentos/` | Recortes de referência | Tabelas de indicadores | | `[PENDENTE]` |

### 4.3 Etapas pendentes

| Etapa | Arquivo previsto | Função |
|---|---|---|
| Segmentação de caracteres | `src/regioes/componentes.py` | Rotular componentes conectados na placa binarizada |
| Descrição das regiões | `src/regioes/descritores.py` | Calcular atributos de forma e filtrar componentes que não são caracteres |
| Retificação por perspectiva | `src/retificacao/perspectiva.py` | Corrigir perspectiva a partir de 4 cantos |
| Pipeline integrado com avaliação | `src/pipeline.py` | Processar uma lista de IDs e gravar CSV de resultados |

## 5. Fundamentação das técnicas e parâmetros

### 5.1 Segmentação

Localização da placa (YOLOv8n). A função de separar a região da placa do restante da imagem, que na proposta da M1 seria feita por segmentação clássica, é realizada por um detector de objetos. O YOLOv8n é a menor variante da família YOLOv8; foi ajustado a partir de pesos pré-treinados no COCO, que não possui a classe placa, usando as caixas derivadas dos cantos anotados do RodoSol-ALPR. A saída é uma caixa delimitadora retangular, que equivale a uma segmentação da placa por região retangular. O limiar de confiança 0,5 descarta detecções fracas. `[PENDENTE: equipe justificar a escolha da variante n e do limiar 0,5]`

Realce com CLAHE. A equalização adaptativa de histograma com limite de contraste opera em blocos (8x8) e limita a amplificação (clipLimit 2,0), realçando caracteres em placas escuras ou com iluminação desigual sem amplificar excessivamente o ruído.

Filtro bilateral. Suaviza o ruído preservando bordas, pois pondera os vizinhos pela distância espacial e pela diferença de intensidade. Isso mantém a borda entre caractere e fundo, que é o que a binarização precisa separar.

Limiar adaptativo gaussiano. Cada pixel é comparado com a média ponderada gaussiana de uma vizinhança 19x19, menos a constante C = 9. Isso tolera variação de iluminação ao longo da placa, ao contrário de um limiar global. Com `THRESH_BINARY_INV`, os caracteres (escuros) viram primeiro plano branco. O experimento 1 compara essa escolha com o limiar global de Otsu. `[PENDENTE: confirmar experimento]`

### 5.2 Morfologia

Fechamento 2x2. Dilatação seguida de erosão com elemento retangular 2x2. Fecha pequenas falhas e interrupções nos traços dos caracteres após a binarização, sem alterar de forma relevante a espessura dos traços. O experimento 2 avalia o efeito de remover essa etapa. `[PENDENTE: confirmar experimento]`

Correção de inclinação. Estima o ângulo do menor retângulo rotacionado que contém todos os pixels brancos da máscara e rotaciona a imagem para alinhá-la. Ressalvas identificadas na revisão do código: as coordenadas vêm de `np.where` na ordem (linha, coluna), e a regra `angle < -45` corresponde à convenção de ângulo do OpenCV anterior à versão 4.5.1. O ângulo também pode ser dominado pela moldura da placa ou por ruído. `[PENDENTE: verificar o comportamento em imagens inclinadas e corrigir se necessário]`

Inversão final. O Tesseract tem melhor desempenho com texto escuro sobre fundo claro, por isso a máscara é invertida antes da leitura.

### 5.3 Análise de regiões e componentes

Planejado para a M3. A placa binarizada será rotulada em componentes conectados (vizinhança 8). Cada componente candidato a caractere será filtrado pelos descritores da seção 5.4. A contagem esperada é de 7 caracteres por placa, o que permite medir o erro de contagem contra o texto anotado.

### 5.4 Representação e descrição

Planejado para a M3, aplicado a cada componente conectado:

| Atributo | Unidade | Forma de cálculo |
|---|---|---|
| Área | pixels | Número de pixels do componente |
| Altura relativa | adimensional | Altura da caixa do componente dividida pela altura da placa |
| Razão de aspecto | adimensional | Largura da caixa do componente dividida pela altura |
| Extensão (retangularidade) | adimensional | Área do componente dividida pela área da sua caixa delimitadora |
| Solidez | adimensional | Área do componente dividida pela área do seu fecho convexo |

Leitura com Tesseract. Modo `--psm 7` (uma linha de texto) e lista de caracteres permitidos A-Z e 0-9, seguidos de limpeza por expressão regular. Esse modo não atende placas de motocicleta, que têm duas linhas.

## 6. Experimentos e resultados

### 6.1 Experimento 1

`[PENDENTE: resumo e link para experimentos/exp01.md]`

### 6.2 Experimento 2

`[PENDENTE: resumo e link para experimentos/exp02.md]`

### 6.3 Tabela consolidada

| Experimento | Configuração | Imagens | Indicador | Resultado |
|---|---|---|---|---|

### 6.4 Análise

`[PENDENTE]`

## 7. Falhas, limitações e riscos

Riscos conhecidos antes dos experimentos estão listados em [proposta.md, seção 9](proposta.md#9-riscos).

`[PENDENTE: falhas observadas nos experimentos, com IDs das imagens e figuras]`

## 8. Plano de conclusão para a M3

Responsáveis sugeridos com base na divisão de papéis da revisão da M1 (Gustavo: segmentação e morfologia; Kauan: métricas e experimentos; João: dados, descritores e documentação). `[PENDENTE: equipe confirmar responsáveis e prazos]`

| Tarefa | Responsável | Prazo | Evidência esperada |
|---|---|---|---|
| Adotar a divisão oficial do RodoSol-ALPR e retreinar o detector com validação separada | João | `[PENDENTE]` | `data.yaml`, IDs em `Data/splits/`, `results.csv` do treino |
| Avaliar a localização no conjunto de teste completo | Kauan | `[PENDENTE]` | CSV com IoU por imagem, IoU médio e taxa de localização por subconjunto |
| Corrigir a correção de inclinação ou substituir por retificação de perspectiva | Gustavo | `[PENDENTE]` | Comparação antes/depois em placas inclinadas |
| Segmentar caracteres por componentes conectados | Gustavo | `[PENDENTE]` | Imagens rotuladas e erro de contagem contra 7 caracteres |
| Extrair descritores e filtrar componentes | João | `[PENDENTE]` | Tabela de descritores e taxa de componentes corretos |
| Tratar placas de motocicleta em duas linhas | Kauan | `[PENDENTE]` | Acerto de leitura separado por subconjunto |
| Avaliar a leitura (acerto exato e por caractere) | Kauan | `[PENDENTE]` | CSV de leitura por imagem |
| Relatório final e vídeo da M3 | Todos | `[PENDENTE]` | `docs/relatorio_m3.md`, link no README |

## 9. Contribuições dos integrantes

`[PENDENTE: equipe preencher, ver docs/contribuicoes.md]`

| Integrante | Contribuições | Evidências |
|---|---|---|

## 10. Referências

1. LAROCA, R. et al. On the Cross-dataset Generalization in License Plate Recognition. In: VISAPP, 2022. (Artigo de apresentação do RodoSol-ALPR.) `[PENDENTE: conferir a referência completa no repositório do dataset]`
2. RodoSol-ALPR Dataset. https://github.com/raysonlaroca/rodosol-alpr-dataset
3. JOCHER, G.; CHAURASIA, A.; QIU, J. Ultralytics YOLOv8. 2023. https://github.com/ultralytics/ultralytics (licença AGPL-3.0)
4. SMITH, R. An Overview of the Tesseract OCR Engine. In: ICDAR, 2007.
5. ZUIDERVELD, K. Contrast Limited Adaptive Histogram Equalization. In: Graphics Gems IV, 1994.
6. TOMASI, C.; MANDUCHI, R. Bilateral Filtering for Gray and Color Images. In: ICCV, 1998.
7. GONZALEZ, R. C.; WOODS, R. E. Digital Image Processing. 4. ed. Pearson, 2018.
8. OpenCV Documentation. https://docs.opencv.org/

## 11. Declaração de uso de IA generativa

`[PENDENTE: ver docs/uso_ia.md]`
