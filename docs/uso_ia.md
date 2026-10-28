# Declaração de Uso de IA Generativa

## Síntese

O código do projeto foi desenvolvido pelos integrantes do grupo. Isso inclui a preparação do dataset, o treinamento do detector, o pré-processamento da placa, a leitura por OCR, o pipeline principal e a configuração do Docker.

A IA generativa foi usada como ferramenta de apoio em duas frentes: organização da estrutura do repositório e redação inicial da documentação técnica. Em nenhum momento ela substituiu as decisões técnicas, a implementação ou a análise dos resultados, que são de responsabilidade do grupo.

## Ferramenta utilizada

| Item | Informação |
|---|---|
| Ferramenta | Claude Code (Anthropic) |
| Modelo | Claude Opus 5.5 |
| Data de uso | 27/10/2026 |
| Integrante que conduziu o uso | Kauan Rocha Dalfovo |

## Registro de uso

| Ferramenta | Finalidade | Materiais gerados ou modificados | Como foi verificado | Integrante responsável |
|---|---|---|---|---|
| Claude Code | Leitura do enunciado, da rubrica e do repositório para levantar o que faltava na entrega da M2 | Nenhum arquivo; diagnóstico usado como lista de tarefas | Conferência pela equipe contra o enunciado e a rubrica | Kauan |
| Claude Code | Estruturação do repositório | Pastas e arquivos vazios em `docs/`, `src/`, `notebooks/` e `Data/`; `requirements.txt` inicial; `.gitignore`; `.dockerignore` | Execução dos imports dos módulos e conferência dos arquivos copiados para a imagem Docker | Kauan |
| Claude Code | Organização do README | Reorganização das seções, tabela de links, correção dos blocos de comando e preenchimento das seções de objetivos, entradas e saídas, estágio atual e exemplo mínimo | Revisão pela equipe e conferência com o código | Kauan |
| Claude Code | Redação inicial da documentação | Rascunhos de `docs/proposta.md`, `docs/dados.md`, `docs/relatorio_m2.md`, `docs/decisoes.md`, `docs/contribuicoes.md` e `docs/roteiro_video_m2.md` | Revisão pela equipe, conferência das informações com o código e com a documentação do dataset, e preenchimento dos dados que dependiam do grupo | Kauan |
| Claude Code | Apoio à análise dos resultados do experimento 1 | Cálculo do acerto por caractere e contagem dos padrões de erro a partir de `resultados_exp01.csv`; redação de `docs/experimentos/exp01.md` e da seção 6 do relatório; lista de IDs em `Data/splits/avaliacao_ids.txt` | Valores reproduzíveis a partir do CSV gerado pelo experimento; IDs conferidos com as imagens de `Data/imagens_testes/dataset_original` | Kauan |

## Como o conteúdo foi verificado

- Os rascunhos foram escritos a partir do código e dos documentos já existentes no repositório. Informações que dependiam de resultados ou de decisões do grupo ficaram marcadas como pendentes e foram completadas pelos integrantes.
- Parâmetros e etapas descritos na documentação foram conferidos diretamente nos arquivos de código.
- Justificativas técnicas, responsáveis e planejamento da M3 foram validados pela equipe antes da entrega.

## Responsabilidade

O grupo revisou todo o conteúdo gerado com apoio de IA e responde integralmente pelo material entregue.
