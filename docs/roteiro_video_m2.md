# Roteiro do Vídeo M2

> O vídeo da M2 não foi produzido (decisão D12 em [decisoes.md](decisoes.md)). Este roteiro fica como base para o vídeo da M3.
>
> Tópicos de fala por bloco. Cada apresentador diz o próprio nome ao começar. Indicações entre colchetes são o que deve aparecer na tela.

| Bloco | Conteúdo | Apresentador | Duração |
|---|---|---|---|
| 1 | Evolução desde a M1 | Kauan | 1:00 |
| 2 | Dados | Kauan | 1:00 |
| 3 | Pipeline implementado | João | 1:30 |
| 4 | Execução real | João | 1:30 |
| 5 | Saídas intermediárias | Gustavo | 1:30 |
| 6 | Comparação experimental | Gustavo | 2:00 |
| 7 | Limitações | Gustavo | 0:45 |
| 8 | Plano da M3 | Kauan | 0:45 |

## Bloco 1. Evolução desde a M1 (Kauan)

[README e tabela da seção 2 do relatório]

- Grupo 2: Kauan, João e Gustavo. Projeto: leitura automática de placas brasileiras.
- Entrada: imagem do veículo. Saída: texto da placa.
- Feedback da M1: escopo amplo, sem métricas, pouco código executável.
- Na M2: escopo delimitado a imagens de pedágio com uma placa, métricas de acerto definidas, pipeline executando em Docker.

## Bloco 2. Dados (Kauan)

[dados.md e um arquivo de anotação aberto]

- RodoSol-ALPR, da UFPR: 20 mil imagens de pedágio da ES-060, carros e motos, placas antigas e Mercosul.
- Cada imagem tem anotação com os quatro cantos da placa e o texto. Essa é a referência de avaliação.
- Licença acadêmica, obtida pelo João. O dataset completo fica fora do repositório; uma amostra de 100 imagens está versionada para a execução.
- Detector: 16 mil imagens de treino e 4 mil de teste.

## Bloco 3. Pipeline implementado (João)

[diagrama da seção 4.1 do relatório e filtros.py]

- Localização: YOLOv8n ajustado ao dataset, confiança mínima 0,5.
- No recorte: tons de cinza, CLAHE para realçar contraste, filtro bilateral para reduzir ruído sem borrar bordas.
- Segmentação por limiar adaptativo, correção de inclinação e fechamento morfológico 2x2.
- Leitura com Tesseract em linha única, letras e números.
- Segmentação de caracteres e descritores ficam para a M3.

## Bloco 4. Execução real (João)

[terminal: docker build e docker run do README]

- Tudo em Docker, sem depender da máquina.
- O main.py roda o pipeline nas 50 imagens de teste e depois o experimento 1.
- Mostrar o CSV e as figuras gerados em Data/results.

## Bloco 5. Saídas intermediárias (Gustavo)

[figuras result_img_001101 e result_img_000996]

- Detecção: o retângulo verde marca a placa.
- Recorte: todo o processamento acontece só nele.
- Binarização: caracteres separados do fundo; moldura e faixa da cidade também aparecem.
- Sucesso: img_001101, placa PPR1476 lida corretamente.

## Bloco 6. Comparação experimental (Gustavo)

[exp01.md e tabela de resultados]

- Pergunta: um Otsu simples lê melhor que o pré-processamento completo do pipeline?
- Mesmas 50 imagens de cars-br, mesmo recorte do YOLO, mesmo OCR, mesma referência.
- Otsu: 40% de acerto exato e 74,3% por caractere. Pipeline completo: 12% e 48,3%.
- O adaptativo realça moldura e faixa da cidade, que viram ruído para o OCR.
- Muitos erros são Q lido como O e D lido como 0, letras parecidas em recortes pequenos.
- Falha: img_000996, placa vermelha QRC5076, com polaridade invertida.

## Bloco 7. Limitações (Gustavo)

[seção 7 do relatório]

- Placa vermelha com letra branca não é tratada.
- Moto e Mercosul não foram avaliados no experimento; o OCR lê uma linha só.
- O teste do detector também foi usado como validação, e o IoU não foi calculado.

## Bloco 8. Plano da M3 (Kauan)

[seção 8 do relatório]

- João: divisão oficial do dataset, revisão da binarização, segmentação de caracteres e descritores.
- Gustavo: comparação isolada do limiar, experimento com e sem fechamento, IoU e avaliação por subconjunto.
- Kauan: relatório final, README e vídeo.
- Código e documentação no repositório, link no README. Obrigado.

## Link do vídeo

Não produzido na M2.
