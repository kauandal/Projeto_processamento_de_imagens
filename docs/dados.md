# Dados

## 1. Origem do conjunto

O projeto usa o RodoSol-ALPR, conjunto brasileiro de imagens de veículos capturadas por câmeras fixas em praças de pedágio da rodovia ES-060, no Espírito Santo, disponibilizado por pesquisadores da UFPR.

- Repositório oficial: https://github.com/raysonlaroca/rodosol-alpr-dataset
- Total: 20.000 imagens.
- Subconjuntos usados pelo código (`src/treinamento_modelos/preparar_dataset.py`): `cars-br`, `cars-me`, `motorcycles-br`, `motorcycles-me` (carros e motocicletas, placas no padrão brasileiro antigo e Mercosul).
- Resolução: 1280x720 pixels na imagem `img_000002.jpg`, verificada pela conversão da anotação para o formato YOLO (seção 5).

## 2. Licença e condições de uso

O acesso ao RodoSol-ALPR é concedido mediante solicitação aos autores e assinatura de um termo de licença para uso acadêmico. O integrante João Vitor Loch Martins solicitou o acesso e assinou o termo em nome do grupo.

O dataset completo não é versionado: o `.gitignore` exclui `Data/Datasets/*`. Para que o pipeline e o experimento executem sem o dataset completo, o grupo versionou uma amostra de 100 imagens em `Data/imagens_testes/` (seção 6), com uso restrito à finalidade acadêmica desta disciplina. Quem quiser reproduzir o treino ou usar o conjunto completo deve solicitar o acesso aos autores (seção 3).

## 3. Procedimento de obtenção

1. Acessar o repositório oficial do RodoSol-ALPR e seguir as instruções de solicitação de acesso.
2. Assinar e enviar o termo de licença aos autores.
3. Baixar e extrair o arquivo recebido. A pasta extraída contém `images/` com os quatro subconjuntos.

## 4. Preparação local

O script `src/treinamento_modelos/preparar_dataset.py` lê as imagens e anotações originais, converte os cantos da placa para o formato YOLO e copia o resultado para `Data/Datasets/train` e `Data/Datasets/test`. Antes de executar, ajustar a variável `DATASET_ORIGINAL` no início do script para o caminho da pasta `images/` extraída.

```bash
python src/treinamento_modelos/preparar_dataset.py
```

Estrutura gerada:

```
Data/Datasets/
    train/images/   train/labels/
    test/images/    test/labels/
```

O `data.yaml` usado no treino está versionado em `Data/imagens_testes/yolo/data.yaml`. Ele aponta `train/images` para treino e `test/images` para validação.

A amostra versionada em `Data/imagens_testes/` foi gerada por `separar_amostras.py`, na raiz do projeto, a partir do dataset original e da pasta `test`. O script usa caminhos absolutos da máquina de quem o executou e deve ser ajustado antes de nova execução.

## 5. Formato das anotações

Cada imagem `img_XXXXXX.jpg` tem um arquivo `img_XXXXXX.txt` com campos no formato `chave: valor`. Exemplo real (`img_000002.txt`):

```
type: car
plate: PPC5431
layout: Brazilian
corners: 560,383 679,382 680,423 561,422
```

| Campo | Conteúdo | Uso no projeto |
|---|---|---|
| `type` | Tipo de veículo (`car` no exemplo) | Estratificação dos resultados |
| `plate` | Texto da placa, 7 caracteres | Referência para avaliar a leitura |
| `layout` | Padrão da placa (`Brazilian` no exemplo; Mercosul nos subconjuntos `-me`) | Estratificação dos resultados |
| `corners` | Quatro pontos `x,y` em pixels; no exemplo, na ordem superior esquerdo, superior direito, inferior direito, inferior esquerdo | Referência de localização (IoU) e, na M3, retificação |

Conversão para o YOLO: a caixa delimitadora é o menor retângulo alinhado aos eixos que contém os quatro cantos; centro, largura e altura são normalizados pela largura e altura da imagem; classe única `0` (placa). Os rótulos convertidos ficam em `Data/Datasets/<split>/labels/` e não contêm o texto da placa.

Verificação da conversão com `img_000002`: os cantos dão x de 560 a 680 e y de 382 a 423. O rótulo YOLO gerado é `0 0.484375 0.559028 0.093750 0.056944`, que corresponde a centro (620; 402,5), largura 120 e altura 41 pixels numa imagem de 1280x720, ou seja, a conversão está correta para esse caso.

## 6. Subconjuntos usados

| Conjunto | Local | Finalidade | Quantidade |
|---|---|---|---|
| Treino do detector | `Data/Datasets/train` (não versionado) | Fine-tuning do YOLOv8n | 16.000 (80% de 20.000) |
| Validação e teste do detector | `Data/Datasets/test` (não versionado) | Validação durante o treino | 4.000 |
| Amostra do experimento 1 | `Data/imagens_testes/dataset_original`, IDs em `Data/splits/avaliacao_ids.txt` | Avaliação da leitura contra o campo `plate` | 50 imagens de `cars-br`, com anotação original |
| Amostra do pipeline | `Data/imagens_testes/yolo` | Execução demonstrativa do pipeline | 50 imagens de `test`, com rótulo YOLO |

Nenhum parâmetro do pré-processamento foi ajustado com as imagens do experimento 1: os valores vieram do código do pipeline. Por isso `Data/splits/ajuste_ids.txt` está vazio.

## 7. Critérios de seleção

As duas amostras foram sorteadas aleatoriamente por `separar_amostras.py`, sem semente, e ficaram fixas a partir do sorteio: os IDs estão registrados em `Data/splits/avaliacao_ids.txt` e as imagens, em `Data/imagens_testes/`. A amostra do experimento 1 contém apenas `cars-br`, subconjunto de placas de uma linha, compatível com o modo de leitura do OCR. Placas Mercosul e de motocicleta ficaram fora do experimento e estão previstas para a M3.

## 8. Prevenção de vazamento entre divisões

- A divisão do detector foi feita com `random.shuffle` sem semente e não é reproduzível.
- Não existe conjunto de validação separado. As 4.000 imagens de `test` foram usadas como validação durante o treino, inclusive para a parada antecipada (`patience=10`) e para a escolha do `best.pt`. As métricas do detector nesse conjunto são, portanto, métricas de validação e tendem a ser otimistas.
- A amostra do experimento 1 foi sorteada do dataset original sem verificar se as imagens estavam no treino do detector. Isso pode favorecer a qualidade do recorte, mas afeta igualmente as duas configurações comparadas.

Ação planejada para a M3: adotar a divisão oficial do RodoSol-ALPR, com treino, validação e teste separados, e registrar os IDs em `Data/splits/`.

## 9. Restrições e limitações

- Câmeras fixas de pedágio: enquadramento e escala da placa pouco variados; os resultados não se generalizam diretamente para câmeras móveis ou de rua.
- Uma placa por imagem na grande maioria dos casos.
- As anotações foram produzidas pelos autores do dataset, não pelo grupo; o grupo não revisou a qualidade dos cantos anotados.
- A amostra do experimento tem 50 imagens de um único subconjunto, o que limita a generalização dos resultados.
