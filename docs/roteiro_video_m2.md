# Roteiro do Vídeo M2

> Duração alvo: cerca de 10 minutos. Todos os integrantes devem aparecer ou falar de forma identificável. Apresentadores sugeridos pela divisão de papéis da M1. `[PENDENTE: equipe confirmar]`

| Bloco | Conteúdo | Apresentador | Duração |
|---|---|---|---|
| 1 | Evolução desde a M1 | Kauan | 1:00 |
| 2 | Dados | João | 1:00 |
| 3 | Pipeline implementado | Gustavo | 1:30 |
| 4 | Execução real | João | 1:30 |
| 5 | Saídas intermediárias | Gustavo | 1:30 |
| 6 | Comparação experimental | Kauan | 2:00 |
| 7 | Limitações | Gustavo | 0:45 |
| 8 | Plano da M3 | Kauan | 0:45 |

## Bloco 1. Evolução desde a M1

- Problema e objetivo em uma frase.
- Principais pontos do feedback e o que foi feito (escopo delimitado, métricas, código executável, documentação em `docs/`).
- Mostrar a tabela da seção 2 do relatório.

## Bloco 2. Dados

- RodoSol-ALPR: origem, quantidade, subconjuntos, licença.
- Por que as imagens não estão no repositório e como obtê-las.
- Formato da anotação: 4 cantos e texto da placa, usados como referência.
- Divisão usada e quantidade efetiva. `[PENDENTE: números]`

## Bloco 3. Pipeline implementado

- Diagrama da seção 4.1 do relatório.
- Função de cada etapa e principais parâmetros.
- O que está implementado e o que fica para a M3.

## Bloco 4. Execução real

- Gravar a tela executando `docker build` e `docker run` a partir do README.
- Mostrar a saída no console e o arquivo gerado em `Data/results/`.

## Bloco 5. Saídas intermediárias

- Mostrar a detecção, o recorte, a placa após CLAHE, a binarização, o fechamento e a imagem final para o OCR.
- Explicar o que cada etapa mudou na imagem. `[PENDENTE: figuras em docs/figuras/]`

## Bloco 6. Comparação experimental

- Pergunta técnica, configurações comparadas, imagens usadas e o que ficou constante.
- Tabela com o indicador quantitativo.
- Um caso de sucesso e um caso de falha, com o ID da imagem. `[PENDENTE: resultados]`

## Bloco 7. Limitações

- Motocicletas com placa em duas linhas, correção de inclinação, uma placa por imagem, divisão dos dados.

## Bloco 8. Plano da M3

- Tarefas, responsáveis e evidências esperadas (seção 8 do relatório).

## Link do vídeo

`[PENDENTE: link do YouTube, não listado]`
