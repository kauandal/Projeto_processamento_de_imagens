# Dados

> Trechos marcados com `[PENDENTE: ...]` dependem de confirmação da equipe ou da documentação oficial do dataset.

## 1. Origem do conjunto

O projeto usa o RodoSol-ALPR, conjunto brasileiro de imagens de veículos capturadas por câmeras fixas em praças de pedágio da rodovia ES-060, no Espírito Santo, disponibilizado por pesquisadores da UFPR.

- Repositório oficial: https://github.com/raysonlaroca/rodosol-alpr-dataset
- Total: 20.000 imagens.
- Subconjuntos usados pelo código (`src/treinamento_modelos/preparar_dataset.py`): `cars-br`, `cars-me`, `motorcycles-br`, `motorcycles-me` (carros e motocicletas, placas no padrão brasileiro antigo e Mercosul).
- Resolução: 1280x720 pixels na imagem `img_000002.jpg`, verificada pela conversão da anotação para o formato YOLO (seção 5).
- `[PENDENTE: confirmar na documentação oficial a quantidade por subconjunto, se todas as imagens têm a mesma resolução e se o subconjunto de carros inclui ônibus e caminhões]`

## 2. Licença e condições de uso

O acesso ao RodoSol-ALPR é concedido mediante solicitação aos autores e assinatura de um termo de licença para uso acadêmico. O integrante João Vitor Loch Martins solicitou o acesso e assinou o termo em nome do grupo.

Por essa condição, nenhuma imagem do dataset é versionada neste repositório. O `.gitignore` exclui `Data/Datasets/*` e o `.dockerignore` impede que as imagens entrem na imagem Docker.

`[PENDENTE: confirmar no termo de licença se é permitido publicar o modelo treinado Models/Deteccao_placa/best.pt e figuras com recortes de placas]`

## 3. Procedimento de obtenção

1. Acessar o repositório oficial do RodoSol-ALPR e seguir as instruções de solicitação de acesso.
2. Assinar e enviar o termo de licença aos autores.
3. Baixar e extrair o arquivo recebido. A pasta extraída contém `images/` com os quatro subconjuntos.

## 4. Preparação local

O script `src/treinamento_modelos/preparar_dataset.py` lê as imagens e anotações originais, converte os cantos da placa para o formato YOLO e copia o resultado para `Data/Datasets/train` e `Data/Datasets/test`.

Antes de executar, ajustar a variável `DATASET_ORIGINAL` no início do script para o caminho da pasta `images/` extraída. `[PENDENTE: substituir o caminho absoluto por argumento de linha de comando]`

```bash
python src/treinamento_modelos/preparar_dataset.py
```

Estrutura gerada:

```
Data/Datasets/
    train/images/   train/labels/
    test/images/    test/labels/
```

O arquivo `Data/Datasets/data.yaml`, usado pelo treinamento, não é gerado pelo script. No treino realizado, ele apontou a pasta `test` tanto para validação quanto para teste (ver seção 8). `[PENDENTE: João versionar o data.yaml usado no treino]`

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

| Arquivo | Finalidade | Quantidade |
|---|---|---|
| Data/splits/ajuste_ids.txt | Imagens usadas para escolher parâmetros do pré-processamento | `[PENDENTE]` |
| Data/splits/avaliacao_ids.txt | Imagens reservadas para a avaliação final, não usadas no ajuste | `[PENDENTE]` |

Treino do detector (situação atual): divisão aleatória 80/20 entre `train` e `test` sobre todas as imagens com anotação encontradas nos quatro subconjuntos. A pasta `test` tem 4.000 imagens. `[PENDENTE: João confirmar a quantidade em train; pela proporção 80/20, o esperado é 16.000]`

## 7. Critérios de seleção

`[PENDENTE: equipe definir]` Recomendação: subconjunto de avaliação estratificado pelos quatro subconjuntos, incluindo casos típicos e casos difíceis identificados por ID (placa inclinada, baixo contraste, iluminação desigual, placa suja ou parcialmente oculta, motocicleta com placa em duas linhas).

## 8. Prevenção de vazamento entre divisões

Situação atual:

- A divisão é feita com `random.shuffle` sem semente; não é possível reproduzi-la.
- Não existe conjunto de validação separado. As 4.000 imagens de `test` foram usadas como validação durante o treino, inclusive para a parada antecipada (`patience=10`) e para a escolha do `best.pt`, e também como teste. Por isso, as métricas do detector nesse conjunto são métricas de validação e tendem a ser otimistas; não devem ser apresentadas como desempenho em teste independente.

Ação planejada: adotar a divisão oficial do RodoSol-ALPR (treino, validação e teste), registrar os IDs em `Data/splits/` e ajustar os parâmetros do pré-processamento apenas com imagens de treino ou validação. `[PENDENTE: confirmar na documentação oficial o arquivo e as proporções da divisão]`

## 9. Restrições e limitações

- Câmeras fixas de pedágio: enquadramento e escala da placa pouco variados; os resultados não se generalizam diretamente para câmeras móveis ou de rua.
- Uma placa por imagem na grande maioria dos casos.
- As anotações foram produzidas pelos autores do dataset, não pelo grupo; o grupo não revisou a qualidade dos cantos anotados.
- Restrição de licença impede publicar amostras das imagens.
