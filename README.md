# Projeto Disciplina Processamento de Imagens
## Leitura automatica de placas de carro
#### Alunos: Gustavo Odilon da Costa, João Vitor Loch Martins, Kauan Rocha Dalfovo

### Contexto e Problema Investigado
Com o aumento do fluxo de veículos nas vias e nas entradas e saídas de estabelecimentos, o monitoramento desse fluxo vem se tornando cada vez mais importante, tanto por questões de segurança, como para fiscalizar rodovias e identificar carros que cometem infrações de transito, quanto para facilitar processos de empresas, como a cobrança de estacionamento ou controle de acesso a condominios. O monitoramento via cameras nesse contexto supre uma grande lacuna, porém a dependencia de pessoas para monitorar esses casos abre precedentes para falhas e erros humanos. Para tirar essa responsabilidade do olho humano uma alternativa é o ALPR (Automatic Licence Plate Recognition) uma ferramenta que automaticamente detecta uma placa de um veículo e lê seu conteúdo.

### Objetivo Geral
Desenvolver um sistema o qual ao ser fornecido uma imagem detectará as placas de veículos presentes e informará o texto escrito nelas.

### Resumo da Solução Proposta
A solução proposta é um pipeline onde o usuário pode fornecer uma imagem (a principio uma imagem mas pode evoluir para um vídeo) contendo algum veículo e o sistema fará um pré-processamento da imagem, binarizando ajustando inclinação e filtrando ruídos, e então usará uma IA treinada para fazer o recorte do trecho da imagem contendo a placa do veículo, para então com a imagem da placa separada ser feita a leitura dos caracteres de identificação da placa.

### Tecnologias usadas
O sistema será feito em Python, usará modelos de IA pré-treinados YOLO para fazer o fine-tunning, visto que já existem modelos treinados para a detecção de placas porém não de placas brasileiras. Serão utilizadas as bibliotecas Pillow e CV2 para o processamento das imagens.

### Conjunto de dados
O conjunto de dados usados para o treinamento do modelo de IA e a validação dos resultados do sistema será o RodoSol-ALPR, um dataset brasileiro coletado pela UFPR em paradas de pedágio ao longo da ES-060 no Espirito Santo. O Dataset conta com 20.000 imagens de Carros, Motos e Caminhões com anotações das coordenadas das bordas da placa (Canto inferior esquerdo e canto superior direito), se a placa é no padrão Brasileiro ou Mercosul, e a combinação de letras e numeros escrita na placa. O Dataset já foi obtido através do contato do aluno João Vitor Loch Martins com os pesquisadores do Dataset e foi assinado um "license-agreement" para o uso academico dos dados. 

Link do github do dataset: https://github.com/raysonlaroca/rodosol-alpr-dataset
Link da apresentação: https://youtu.be/FeMPxT-Z_Ko
