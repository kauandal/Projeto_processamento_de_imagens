# Roteiro do Vídeo M2

> Duração alvo: cerca de 10 minutos. Ritmo de referência: cerca de 140 palavras por minuto. Indicações entre colchetes, como `[MOSTRAR: ...]`, são o que deve aparecer na tela e não devem ser lidas. Trechos `[PENDENTE: ...]` dependem dos resultados dos experimentos.

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

## Bloco 1. Evolução desde a M1 (Kauan, 1:00)

`[MOSTRAR: README no GitHub, depois a tabela da seção 2 do relatório]`

Olá, somos o grupo 2 de Processamento de Imagens: eu sou o Kauan, e comigo estão o João e o Gustavo. Nosso projeto é a leitura automática de placas de veículos brasileiros, o chamado ALPR. A ideia é receber a imagem de um veículo, encontrar a placa e informar o texto escrito nela.

Na M1 recebemos três críticas principais: o escopo estava amplo demais, não havia métricas de sucesso e o repositório quase não tinha código executável. Nesta etapa respondemos a cada uma delas. Delimitamos o escopo para imagens estáticas de câmeras de pedágio, com uma placa por imagem. Definimos como indicadores o IoU da localização e o acerto da leitura. E agora temos um pipeline que executa de ponta a ponta, dentro de um container Docker.

Toda a resposta ao feedback, item por item, está nesta tabela do relatório, com o arquivo que comprova cada ação. Agora o João vai apresentar os dados.

## Bloco 2. Dados (João, 1:00)

`[MOSTRAR: repositório oficial do RodoSol-ALPR e depois um arquivo de anotação .txt aberto no editor]`

Usamos o RodoSol-ALPR, um conjunto de dados brasileiro da UFPR, com 20 mil imagens capturadas por câmeras fixas em praças de pedágio da rodovia ES-060, no Espírito Santo. Ele tem carros e motocicletas, com placas no padrão antigo e no padrão Mercosul.

Cada imagem vem com um arquivo de anotação. Ele traz os quatro cantos da placa em pixels e o texto da placa. Esses dois campos são a nossa referência: os cantos servem para medir a localização e o texto serve para medir a leitura.

O acesso ao dataset exige um termo de licença para uso acadêmico, que eu assinei em nome do grupo. Por isso as imagens não estão no repositório; documentamos como obtê-las e preparar os dados no arquivo dados.md.

Para o treino, dividimos as imagens em 80% para treino e 20% para teste, o que resultou em `[PENDENTE: confirmar, esperado 16.000]` imagens de treino e 4.000 de teste. Agora o Gustavo explica o pipeline.

## Bloco 3. Pipeline implementado (Gustavo, 1:30)

`[MOSTRAR: diagrama da seção 4.1 do relatório e depois o arquivo filtros.py]`

O pipeline tem duas partes: localizar a placa e preparar a placa para a leitura.

Para localizar, usamos o YOLOv8n, a menor versão do detector YOLO. Partimos de pesos pré-treinados e fizemos o ajuste com as caixas das placas do RodoSol. O modelo devolve um retângulo em volta da placa, e só aceitamos detecções com confiança acima de 0,5. Esse retângulo faz o papel da segmentação da placa em relação ao resto da imagem.

Depois recortamos a placa e aplicamos as técnicas de processamento de imagens. Primeiro convertemos para tons de cinza e aplicamos o CLAHE, uma equalização de histograma por blocos que realça os caracteres quando a iluminação é desigual. Em seguida usamos o filtro bilateral, que reduz o ruído mas preserva as bordas entre caractere e fundo.

A segmentação é feita por limiar adaptativo gaussiano: cada pixel é comparado com a média da sua vizinhança de 19 por 19 pixels. Isso funciona melhor que um limiar único quando uma parte da placa está mais clara que a outra. Depois corrigimos a inclinação e aplicamos um fechamento morfológico com elemento 2 por 2, que fecha pequenas falhas nos traços dos caracteres. Por fim, a placa vai para o Tesseract, configurado para ler uma linha com letras e números.

A segmentação dos caracteres individuais e os descritores de forma ficam para a M3. O João vai mostrar a execução.

## Bloco 4. Execução real (João, 1:30)

`[MOSTRAR: gravação de tela, terminal aberto na raiz do projeto]`

Para garantir que qualquer pessoa consiga executar o projeto, colocamos tudo em Docker. A imagem já instala o Python, o Tesseract e as bibliotecas nas versões que usamos.

`[EXECUTAR: docker build -t alpr-projeto .]`

O primeiro passo é construir a imagem com o docker build. Esse comando está no README, na seção de instalação.

`[EXECUTAR: docker run da seção Execução do README]`

Agora executamos o container. Como as imagens do dataset não podem ir para o repositório, elas não entram na imagem Docker: montamos a pasta do dataset e a pasta de resultados como volumes.

`[MOSTRAR: mensagens do console aparecendo]`

O sistema carrega o modelo treinado, lê a imagem, faz a detecção e depois o OCR. No final ele imprime a placa detectada, que neste caso foi `[PENDENTE: texto lido]`. A placa anotada no dataset é PPC5431.

`[MOSTRAR: abrir Data/results/resultado_final.jpg]`

E aqui está o arquivo gerado na pasta de resultados, com as três etapas lado a lado. O Gustavo vai explicar o que cada uma mostra.

## Bloco 5. Saídas intermediárias (Gustavo, 1:30)

`[MOSTRAR: figuras de docs/figuras, uma etapa por vez. Ajustar a fala ao que as figuras realmente mostram]`

Nesta primeira imagem vemos a detecção do YOLO: o retângulo verde marca onde o modelo encontrou a placa. Comparando com a imagem original, dá para ver que o detector ignora o resto do veículo e o fundo.

Aqui está o recorte da placa. É sobre ele que todo o processamento seguinte acontece, o que reduz bastante a quantidade de informação irrelevante.

Depois do CLAHE, o contraste entre os caracteres e o fundo aumenta, principalmente nas regiões mais escuras da placa. Nesta outra imagem está o resultado do limiar adaptativo: os caracteres viram regiões brancas sobre fundo preto. Vejam que a moldura da placa e algumas manchas também aparecem; é isso que a etapa de componentes vai filtrar na M3.

Após o fechamento morfológico, as pequenas falhas dentro dos traços são preenchidas, e os caracteres ficam mais contínuos. A última imagem é a versão invertida, com texto escuro sobre fundo claro, que é o formato em que o Tesseract funciona melhor.

Agora vamos para um caso difícil. `[MOSTRAR: imagem de caso difícil]` Nesta placa `[PENDENTE: descrever o caso, por exemplo inclinação ou baixo contraste]`, e o resultado foi `[PENDENTE]`. O Kauan apresenta a comparação experimental.

## Bloco 6. Comparação experimental (Kauan, 2:00)

`[MOSTRAR: docs/experimentos/exp01.md e a tabela de resultados]`

A pergunta do nosso experimento foi: o limiar adaptativo melhora a binarização da placa em relação a um limiar global de Otsu?

Comparamos as duas configurações nas mesmas `[PENDENTE: quantidade]` imagens, listadas pelo ID no arquivo avaliacao_ids.txt. Todo o resto ficou constante: o mesmo realce com CLAHE, o mesmo filtro bilateral, a mesma morfologia e o mesmo OCR. A única coisa que mudou foi o método de limiarização.

Para isolar o efeito da binarização, os recortes da placa foram feitos a partir dos cantos anotados, e não da detecção do YOLO. Assim, um erro do detector não interfere no resultado.

O indicador foi o acerto da leitura contra o texto anotado no dataset, medido de duas formas: placas lidas exatamente certas e acerto por caractere.

`[MOSTRAR: tabela]`

O limiar adaptativo obteve `[PENDENTE: resultado]` e o Otsu obteve `[PENDENTE: resultado]`. `[PENDENTE: interpretação, por exemplo em quais tipos de imagem a diferença apareceu]`

`[MOSTRAR: caso de sucesso]` Este é um caso de sucesso: na imagem `[PENDENTE: ID]`, `[PENDENTE: o que funcionou e por quê]`.

`[MOSTRAR: caso de falha]` E este é um caso de falha: na imagem `[PENDENTE: ID]`, `[PENDENTE: o que falhou e por quê]`.

Essa falha mostra que `[PENDENTE: o que a falha ensina e qual decisão ela motiva para a M3]`. O Gustavo fala agora das limitações.

## Bloco 7. Limitações (Gustavo, 0:45)

`[MOSTRAR: seção 7 do relatório ou a tabela de riscos da proposta]`

O pipeline ainda tem limitações claras. As placas de motocicleta têm duas linhas, e o Tesseract está configurado para ler uma linha só, então elas tendem a falhar. A correção de inclinação usa todos os pixels brancos da placa e pode ser enganada pela moldura ou por ruído. O sistema também considera só uma placa por imagem.

Por fim, a divisão entre treino e teste foi aleatória e sem um conjunto de validação separado, o que pode deixar os resultados do detector otimistas. O Kauan apresenta o que vamos fazer na M3.

## Bloco 8. Plano da M3 (Kauan, 0:45)

`[MOSTRAR: tabela da seção 8 do relatório]`

Para a M3, o João vai adotar a divisão oficial do RodoSol e retreinar o detector com validação separada. Eu fico com a avaliação da localização pelo IoU em todo o conjunto de teste e com a avaliação da leitura. O Gustavo vai implementar a segmentação dos caracteres por componentes conectados e corrigir o alinhamento da placa, e o João vai extrair os descritores de forma para filtrar o que não é caractere.

Cada tarefa tem a evidência esperada registrada no relatório. Todo o código e a documentação estão no repositório, com o link no README. Obrigado.

## Link do vídeo

`[PENDENTE: link do YouTube, não listado]`
