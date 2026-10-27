# Projeto Disciplina Processamento de Imagens
## Leitura automatica de placas de carro
#### Alunos: Gustavo Odilon da Costa, João Vitor Loch Martins, Kauan Rocha Dalfovo

### Links

| Item | Link |
|---|---|
| Vídeo M1 | https://youtu.be/FeMPxT-Z_Ko |
| Vídeo M2 | |
| Proposta revisada | [docs/proposta.md](docs/proposta.md) |
| Relatório M2 | [docs/relatorio_m2.md](docs/relatorio_m2.md) |
| Revisão da M1 | [revisao_m1_plano_m2.md](revisao_m1_plano_m2.md) |
| Dados | [docs/dados.md](docs/dados.md) |
| Experimentos | [docs/experimentos](docs/experimentos) |
| Decisões | [docs/decisoes.md](docs/decisoes.md) |
| Contribuições | [docs/contribuicoes.md](docs/contribuicoes.md) |
| Uso de IA | [docs/uso_ia.md](docs/uso_ia.md) |

### Contexto e Problema Investigado
Com o aumento do fluxo de veículos nas vias e nas entradas e saídas de estabelecimentos, o monitoramento desse fluxo vem se tornando cada vez mais importante, tanto por questões de segurança, como para fiscalizar rodovias e identificar carros que cometem infrações de transito, quanto para facilitar processos de empresas, como a cobrança de estacionamento ou controle de acesso a condominios. O monitoramento via cameras nesse contexto supre uma grande lacuna, porém a dependencia de pessoas para monitorar esses casos abre precedentes para falhas e erros humanos. Para tirar essa responsabilidade do olho humano uma alternativa é o ALPR (Automatic Licence Plate Recognition) uma ferramenta que automaticamente detecta uma placa de um veículo e lê seu conteúdo.

### Objetivo Geral
Desenvolver um sistema o qual ao ser fornecido uma imagem detectará as placas de veículos presentes e informará o texto escrito nelas.

### Objetivos da M2
1. Localizar a placa com um detector YOLOv8n ajustado ao RodoSol-ALPR e medir a localização contra os cantos anotados (IoU).
2. Preparar a região da placa com realce, suavização, binarização, correção de inclinação e morfologia, gerando saídas intermediárias.
3. Comparar de forma controlada configurações de binarização e de morfologia.
4. Planejar para a M3 a segmentação de caracteres por componentes conectados e a avaliação da leitura.

Detalhes em [docs/proposta.md](docs/proposta.md).

### Entradas e Saídas

| Item | Descrição |
|---|---|
| Entrada | Imagem colorida de um veículo (JPEG do RodoSol-ALPR) |
| Saídas intermediárias | Caixa da placa, recorte, placa binarizada e após morfologia |
| Saída final | Texto da placa no console e figura `Data/results/resultado_final.jpg` com as etapas |

### Estágio Atual

| Etapa | Status |
|---|---|
| Preparação do dataset no formato YOLO | Implementado |
| Treino do detector YOLOv8n | Implementado, modelo em `Models/Deteccao_placa/best.pt` |
| Localização e recorte da placa | Implementado |
| Pré-processamento da placa (CLAHE, bilateral, limiar adaptativo, inclinação, fechamento) | Implementado |
| Leitura com Tesseract | Implementado, uso demonstrativo |
| Execução em Docker | Implementado |
| Avaliação de localização (IoU) | `[PENDENTE]` |
| Experimentos de binarização e morfologia | `[PENDENTE]` |
| Segmentação de caracteres e descritores | Planejado para a M3 |
| Avaliação da leitura | Planejado para a M3 |

### Resumo da Solução Proposta
O usuário fornece uma imagem de veículo. O detector YOLOv8n ajustado localiza a placa, a região é recortada e passa por realce de contraste (CLAHE), filtro bilateral, limiar adaptativo, correção de inclinação e fechamento morfológico. A placa preparada é lida pelo Tesseract. O pipeline completo está descrito na seção 4 de [docs/relatorio_m2.md](docs/relatorio_m2.md). A versão da M1, que previa pré-processar a imagem inteira antes da detecção, está preservada no histórico do repositório.

### Tecnologias usadas
Python 3.11 (imagem Docker), OpenCV para o processamento de imagens, NumPy, Matplotlib para as figuras, Ultralytics 8.3.163 (YOLOv8n) para a detecção e Tesseract com pytesseract para a leitura. O ambiente é executado em Docker. Versões das bibliotecas em [requirements.txt](requirements.txt). `[PENDENTE: fixar as versões das demais bibliotecas]`

### Conjunto de dados
O conjunto de dados usados para o treinamento do modelo de IA e a validação dos resultados do sistema será o RodoSol-ALPR, um dataset brasileiro coletado pela UFPR em paradas de pedágio ao longo da ES-060 no Espirito Santo. O Dataset conta com 20.000 imagens de carros e motocicletas com anotações dos quatro cantos da placa, se a placa é no padrão Brasileiro ou Mercosul, e a combinação de letras e numeros escrita na placa. O Dataset já foi obtido através do contato do aluno João Vitor Loch Martins com os pesquisadores do Dataset e foi assinado um "license-agreement" para o uso academico dos dados. 

Link do github do dataset: https://github.com/raysonlaroca/rodosol-alpr-dataset

### Estrutura do Projeto

```
|   README.md
|   requirements.txt
|   revisao_m1_plano_m2.md
|
+---Data
|   +---Datasets          (não versionado)
|   +---splits
|   \---results
|       +---exp01
|       +---exp02
|       \---pipeline
+---docs
|   +---experimentos
|   \---figuras
+---Models
|   +---Deteccao_placa
|   +---Leitura_placa
|   \---Pre_treinado
+---notebooks
\---src
    |   main.py
    |   pipeline.py
    |
    +---avaliacao
    +---deteccao
    +---experimentos
    +---ocr
    +---pre_processamento
    +---regioes
    +---retificacao
    +---segmentacao
    +---treinamento_modelos
    \---utils
```

### Instalação
Rode o seguinte comando no terminal (PowerShell ou bash) na raiz do projeto:

```bash
docker build -t alpr-projeto .
```

### Execução
O dataset não é copiado para a imagem Docker. Ele deve estar em `Data/Datasets` e é montado como volume na execução, junto com a pasta de resultados.

Execute o seguinte comando na raiz do projeto:

```bash
docker run --rm --name execucao-alpr -v "${PWD}/Data/Datasets:/app/Data/Datasets" -v "${PWD}/Data/results:/app/Data/results" alpr-projeto
```

### Exemplo Mínimo
Pré-requisito: dataset preparado em `Data/Datasets` conforme [docs/dados.md](docs/dados.md).

| Item | Valor |
|---|---|
| Entrada | `Data/Datasets/test/images/img_000002.jpg` (definida em `src/main.py`) |
| Comando | `docker run` da seção Execução |
| Saída no console | `RESULTADO FINAL - PLACA DETECTADA: <texto>` |
| Saída em arquivo | `Data/results/resultado_final.jpg` com detecção, recorte e placa processada |
| Texto esperado | `PPC5431` (campo `plate` da anotação original; carro, placa no padrão brasileiro antigo) |

### Resultados
`[PENDENTE: resumo dos indicadores e link para a seção 6 de docs/relatorio_m2.md]`
