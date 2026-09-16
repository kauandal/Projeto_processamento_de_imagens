# Revisão da M1 e Plano de Ação para a M2

## Parte A — Identificação da equipe e dos materiais conferidos

| Item | Informação |
|---|---|
| Identificação do grupo | Grupo 2 |
| Integrantes | Gustavo O. da Costa; Kauan Rocha Dalfovo; João Vitor Loch |
| Repositório avaliado | https://github.com/kauandal/Projeto_processamento_de_imagens |
| Commit da entrega M1 | `2eeb068d6648da98d8df5f0b3ac31cbc7a65e896` |
| Documento de feedback | Devolutiva da M1 — Grupo 2 |
| Data da conferência | 15/09/2026 |
| Nota da devolutiva | 66,25/100 |
| Nota registrada no diário | 6,7/10 |

## Parte B — Resposta ao feedback

| Nº | Síntese da observação | Classificação | Evidência ou justificativa | Ação |
|---:|---|---|---|---|
| 1 | Escopo do problema ainda está amplo. | Concordamos | A proposta inclui pré-processamento, detecção, retificação e OCR. | Priorizar localização e retificação da placa. |
| 2 | Não há amostra verificável do dataset no repositório. | Concordamos | O dataset é descrito, mas não há amostra ou instrução reprodutível na entrega avaliada. | Documentar obtenção e preparação dos dados respeitando a licença. |
| 3 | Faltam métricas e critérios formais de sucesso. | Concordamos | Entrada e saída estão definidas, mas sem métricas quantitativas. | Utilizar IoU e taxa de localização correta. |
| 4 | O pipeline não define claramente a relação entre PDI, YOLO e OCR. | Concordamos | As técnicas são citadas, porém sem protocolo de comparação bem definido. | Detalhar o pipeline e separar as etapas. |
| 5 | Não há baseline executável nem resultados quantitativos. | Concordamos | A entrega M1 não apresenta teste funcional documentado. | Implementar baseline e registrar resultados. |
| 6 | O repositório possui estrutura, mas pouco conteúdo executável. | Concordamos | O notebook e as pastas estavam praticamente vazios. | Adicionar implementação inicial e instruções de execução. |
| 7 | Falta uma proposta técnica detalhada separada do README. | Concordamos | A documentação está concentrada no README. | Criar `docs/proposta.md`. |
| 8 | O subtotal informado foi 55,00/90. | Discordamos | A soma dos critérios sem o vídeo resulta em 56,25/90. | Solicitar esclarecimento sobre o subtotal. |
| 9 | O vídeo aparece como pendente, apesar de constarem 10/10 pontos. | Concordamos parcialmente | A devolutiva informa que o conteúdo ainda dependia de conferência. | Confirmar se os 10 pontos são definitivos. |

### Síntese da posição do grupo

O grupo concorda com as principais observações técnicas da avaliação e utilizará essas críticas para delimitar melhor o projeto e implementar um baseline executável na M2. A principal divergência identificada está no subtotal informado na devolutiva, pois a soma dos critérios sem o vídeo resulta em 56,25/90. A crítica de maior impacto técnico é a necessidade de definir claramente o pipeline e priorizar inicialmente a localização e retificação das placas.

## Parte C — Conferência das pontuações

| Critério | Valor máximo | Nível | Pontuação registrada | Pontuação recalculada | Diferença |
|---|---:|---|---:|---:|---:|
| Problema | 15 | Adequado | 11,25 | 11,25 | 0,00 |
| Imagens e dados | 10 | Adequado | 7,50 | 7,50 | 0,00 |
| Objetivos e sucesso | 10 | Adequado | 7,50 | 7,50 | 0,00 |
| Pipeline | 15 | Parcial | 7,50 | 7,50 | 0,00 |
| Viabilidade | 15 | Parcial | 7,50 | 7,50 | 0,00 |
| Repositório | 10 | Parcial | 5,00 | 5,00 | 0,00 |
| Markdown | 10 | Parcial | 5,00 | 5,00 | 0,00 |
| Vídeo | 10 | Pendente | 10,00 | 10,00 | 0,00 |
| Histórico | 5 | Adequado | 5,00 | 5,00 | 0,00 |
| **Total** | **100** |  | **66,25** | **66,25** | **0,00** |

### Resultado da conferência aritmética

- [ ] A soma está correta e coincide com todos os valores da devolutiva.
- [x] Foi identificada uma possível divergência na soma.
- [ ] Não foi possível reproduzir a soma.

**Memória de cálculo:**

`11,25 + 7,50 + 7,50 + 7,50 + 7,50 + 5,00 + 5,00 + 10,00 + 5,00 = 66,25`

Sem o vídeo:

`66,25 - 10,00 = 56,25`

A devolutiva informa subtotal de 55,00/90, portanto há uma diferença de 1,25 ponto nesse subtotal.

## Parte D — Conferência da nota registrada no diário

| Verificação | Valor |
|---|---:|
| Nota recalculada | 6,625/10 |
| Nota da devolutiva | 6,625/10 |
| Nota no diário | 6,7/10 |
| Diferença | +0,075 |

- [ ] A nota registrada no diário está correta.
- [x] A nota registrada no diário parece diferente da conversão direta da devolutiva.
- [ ] O grupo ainda não conseguiu confirmar o registro.

A conversão direta de 66,25/100 é 6,625/10. Como o diário registra 6,7, o grupo solicita esclarecimento sobre o arredondamento utilizado.

## Parte E — Diagnóstico da situação atual

| Componente | Situação atual | Evidência existente | Lacuna identificada |
|---|---|---|---|
| Definição e delimitação do problema | Adequado | Problema ALPR definido no README. | Reduzir o escopo inicial. |
| Objetivo e saída esperada | Adequado | Entrada e saída descritas. | Definir métricas. |
| Conjunto inicial de imagens | Parcial | Dataset RodoSol-ALPR definido. | Falta procedimento reprodutível. |
| Pipeline proposto | Parcial | Etapas gerais descritas. | Melhorar justificativas e sequência. |
| Evidência de viabilidade | Parcial | Dataset disponível. | Falta baseline executável. |
| Fundamentação e referências | Parcial | Dataset e tecnologias citados. | Faltam justificativas técnicas. |
| Organização do repositório | Parcial | Estrutura criada. | Pouco conteúdo executável. |
| Relatório técnico | Ausente | Conteúdo concentrado no README. | Criar documentação técnica. |
| Página parcial do projeto | Ausente | Não identificada na M1. | Criar página parcial. |
| Registro de decisões e limitações | Parcial | Algumas decisões no README. | Registrar riscos e limitações. |

## Parte F — Plano de ação para a M2

### Ajustes herdados da M1

| Prioridade | Problema | Ação | Responsável | Prazo | Evidência |
|---|---|---|---|---|---|
| Essencial | Escopo amplo | Priorizar localização e retificação | Todos | Semana 1 | Escopo atualizado |
| Essencial | Falta de baseline | Implementar versão funcional inicial | Gustavo / Kauan | Semana 2 | Código executável |
| Essencial | Falta de protocolo | Definir subconjunto fixo, métricas e parâmetros | Kauan | Semana 1 | Protocolo documentado |
| Importante | Pipeline pouco definido | Documentar etapas e função de cada técnica | Gustavo | Semana 1 | `docs/proposta.md` |
| Importante | Dataset pouco reprodutível | Documentar obtenção e preparação | João | Semana 1 | README atualizado |
| Importante | Falta de métricas | Implementar IoU e taxa de localização | Kauan | Semana 2 | Tabela/CSV de resultados |

### Novos desenvolvimentos da M2

| Entrega ou resultado | Tarefa concreta | Responsável principal | Colaboradores | Prazo | Evidência esperada | Dependências ou riscos |
|---|---|---|---|---|---|---|
| Implementação inicial | Criar pipeline executável | Kauan | Gustavo e João | Semana 2 | Execução registrada | Ambiente e dataset |
| Segmentação | Testar limiarização e/ou bordas | Gustavo | Kauan | Semana 2 | Máscaras e parâmetros | Iluminação |
| Morfologia matemática | Aplicar operações morfológicas | Gustavo | Kauan | Semana 2 | Comparação antes/depois | Escolha do kernel |
| Extração de características | Extrair área, proporção e rectangularidade | João | Gustavo | Semana 3 | Tabela/CSV | Variação das imagens |
| Experimentos | Comparar configurações | Kauan | Todos | Semana 3 | Tabela comparativa | Ajuste excessivo |
| Casos difíceis | Testar imagens com baixa iluminação, inclinação e oclusão | João | Todos | Semana 3 | Resultados e análise | Diversidade dos casos |
| Relatório técnico parcial | Atualizar métodos e resultados | João | Todos | Entrega M2 | Documento atualizado | Atraso na documentação |
| Página parcial | Mostrar pipeline e resultados | Kauan | Todos | Entrega M2 | Página atualizada | Dependência dos resultados |
| Organização e reprodutibilidade | Atualizar README, dependências e comandos | Gustavo | Todos | Entrega M2 | Instruções atualizadas | Diferenças de ambiente |

### Protocolo experimental mínimo

| Elemento | Definição do grupo |
|---|---|
| Pergunta do experimento | Qual configuração do pipeline localiza placas com maior consistência? |
| Imagens ou amostra utilizadas | Subconjunto fixo do RodoSol-ALPR |
| Método principal | Segmentação e detecção de regiões candidatas com PDI |
| Configurações comparadas | Limiarização/bordas, kernels e operações morfológicas |
| Resultado esperado | Localizar a região correspondente à placa |
| Métrica | IoU e taxa de localização correta |
| Registro dos resultados | CSV/tabela com imagem, parâmetros e resultado |
| Limitações previstas | Iluminação, inclinação, perspectiva, ruído e oclusões |

### Distribuição das responsabilidades

| Integrante | Responsabilidades principais | Artefatos | Validação |
|---|---|---|---|
| Gustavo O. da Costa | Segmentação e morfologia | Código das etapas de PDI | Revisão pelo grupo |
| Kauan Rocha Dalfovo | Baseline, métricas e experimentos | Pipeline e resultados | Testes no subconjunto fixo |
| João Vitor Loch | Dataset, características e documentação | Dados, descritores e relatório | Revisão pelo grupo |

## Parte G — Compromisso da equipe

> Declaramos que revisamos a devolutiva da M1, conferimos as pontuações e a nota registrada no diário, identificamos as correções necessárias e definimos um plano de ação para a M2. As discordâncias apresentadas neste documento estão acompanhadas de evidências localizáveis na entrega avaliada. Os integrantes conhecem as tarefas, os prazos e os resultados esperados para a próxima etapa.

**Integrantes:**

- Gustavo O. da Costa
- Kauan Rocha Dalfovo
- João Vitor Loch

**Data:** 15/09/2026
