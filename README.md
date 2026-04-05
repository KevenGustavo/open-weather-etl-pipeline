# **OpenWeather ETL Pipeline**

Este repositório contém uma solução completa de Engenharia de Dados focada na orquestração de um pipeline ETL (Extract, Transform, Load). O projeto foi desenhado para coletar dados climáticos da API OpenWeather, aplicar tratamentos e normalizações, e persistir as informações em um banco de dados relacional. Toda a infraestrutura foi conteinerizada para garantir isolamento e facilidade de deploy.

**Sobre o Projeto**

O objetivo desta aplicação é demonstrar a construção de uma arquitetura de dados escalável e reproduzível. O fluxo é totalmente automatizado e orquestrado, garantindo que os dados meteorológicos (neste caso, parametrizados para a cidade de São Paulo) sejam atualizados e tratados periodicamente sem intervenção manual.  
O pipeline resolve problemas comuns no consumo de APIs RESTful, como:

* Desestruturação de formatos JSON complexos e aninhados.  
* Conversão e normalização de fusos horários (Timezones).  
* Tipagem de dados e limpeza de colunas desnecessárias.  
* Gestão de dependências e passagem de estado entre tarefas utilizando arquivos temporários (Parquet).

**Arquitetura de Dados**

O fluxo de dados foi desenhado em três camadas principais:

1. **Extract (Extração):** Conexão via protocolo HTTP com a API do OpenWeather. Os dados brutos são extraídos em formato JSON e carregados em memória.  
2. **Transform (Transformação):** Utilização da biblioteca Pandas para limpar e estruturar o dado bruto. As operações incluem achatamento (flattening) de dicionários, deleção de atributos não utilizados, renomeação de colunas para o padrão do banco e conversão de timestamps Unix para o fuso horário local.  
3. **Load (Carregamento):** Ingestão dos dados transformados em uma instância local do PostgreSQL, utilizando SQLAlchemy como ORM para gerenciar a conexão e a inserção segura dos registros.

**Orquestração:** O Apache Airflow gerencia o agendamento (cron scheduling) e a dependência temporal entre as tarefas de extração, transformação e carga (DAG).

**Tecnologias e Ferramentas**

* **Linguagem:** Python 3.12  
* **Manipulação de Dados:** Pandas, Apache Parquet  
* **Orquestração:** Apache Airflow  
* **Banco de Dados:** PostgreSQL 14  
* **Infraestrutura & DevOps:** Docker, Docker Compose  
* **Gerenciamento de Dependências:** uv (Python package manager)

**Estrutura do Repositório**

* **config/**: Arquivos de configuração do airflow.  
* **dags/**: Scripts de definição das DAGs do Apache Airflow (ex: weather\_dag.py).  
* **data/**: Diretório temporário para armazenamento local de arquivos JSON brutos e arquivos Parquet intermediários.  
* **notebooks/**: Jupyter Notebooks utilizados para análise exploratória inicial e testes das funções de transformação.  
* **src/**: Código-fonte principal da aplicação.  
  * extract\_data.py: Módulo de requisição à API.  
  * transform\_data.py: Funções de limpeza e tratamento Pandas.  
  * load\_data.py: Conexão e injeção no PostgreSQL.  
* **docker-compose.yml**: Configuração dos serviços do Airflow e suas dependências (Redis, PostgreSQL do Airflow, etc.).

**Pré-requisitos**

Para executar este projeto em seu ambiente local, é necessário ter instalado:

* **Docker** e **Docker Compose**  
* **Python 3.12+**  
* Instância do **PostgreSQL** rodando localmente (na porta padrão 5432).  
* Chave de acesso ativa da [OpenWeather API](https://openweathermap.org/api).

**Instalação e Execução**

**1\. Clone o repositório**  
Faça o clone deste repositório para a sua máquina local.  

**2\. Configuração do Ambiente**  
Crie um arquivo .env dentro da pasta config/ e adicione as suas credenciais de banco de dados e da API:

* API\_KEY=sua\_chave\_aqui  
* DATABASE=nome\_do\_seu\_banco  
* USER=seu\_usuario  
* PASSWORD=sua\_senha

**3\. Preparação do Banco de Dados Local**  
Acesse o seu PostgreSQL via terminal ou interface gráfica (DBeaver, pgAdmin) e crie o banco de dados e o usuário correspondentes aos que você definiu no passo anterior. Garanta que o usuário tenha privilégios para criar tabelas.  

**4\. Subindo a Infraestrutura com Docker**  
Na raiz do projeto, inicie os serviços do Airflow em segundo plano:  
Rode o comando docker-compose up \-d no seu terminal.  

**5\. Acessando o Apache Airflow**  
Abra o navegador e acesse http://localhost:8080.  
Faça o login com as credenciais padrão do container (usuário e senha definidos no docker-compose).  

**6\. Executando a Pipeline**  
Na interface do Airflow, localize a DAG do projeto (ex: youtube\_weather\_pipeline). Ative a DAG no botão de "Unpause" e clique em "Trigger DAG" (botão de play) para iniciar a extração. Você pode acompanhar o status das tarefas em tempo real pelos logs.
