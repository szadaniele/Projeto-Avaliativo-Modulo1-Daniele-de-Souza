# Projeto Avaliativo — Módulo 1 | Análise de Dados com Python [T6]

**Pipeline de dados com Python, PostgreSQL e arquitetura Medallion (Raw, Silver e Gold)**

## 1. Apresentação

Este projeto foi desenvolvido para a avaliação do **Módulo 1 do curso Análise de Dados com Python**, ministrado pelo **SENAI**, instituição parceira do programa **SCTEC**.

A proposta é construir um pipeline de ingestão, tratamento e análise de dados públicos sobre **viagens a serviço da administração pública federal**, disponibilizados pelo **Portal da Transparência do Governo Federal**. A solução utiliza **Python, SQL e PostgreSQL** e organiza o processamento em três camadas: **Raw, Silver e Gold**.

O fluxo preserva os registros de origem, aplica regras de padronização e integridade, estrutura dados analíticos e produz consultas e visualizações sobre os gastos públicos com viagens.

### Objetivo geral

Desenvolver e implementar um pipeline de dados reproduzível e documentado para transformar registros brutos de viagens oficiais em informações estruturadas e rastreáveis, adequadas à análise exploratória e à construção de indicadores de apoio à tomada de decisão.

### Objetivos específicos

- Automatizar a leitura e a ingestão de arquivos ZIP e CSV com Python.
- Preservar os dados de origem na camada **Raw**.
- Aplicar limpeza, conversão de tipos e validações na camada **Silver**.
- Estabelecer e verificar relacionamentos e regras de integridade entre tabelas.
- Construir estruturas e consultas analíticas na camada **Gold**.
- Responder às sete perguntas de negócio por meio de consultas SQL e visualizações.
- Documentar o processo e versionar scripts, testes e resultados com **Git e GitHub**.

## 2. Arquitetura e fluxo de processamento

O pipeline adota a **arquitetura Medallion**, com responsabilidades distintas para cada camada.

| Camada | Responsabilidade |
|---|---|
| **Raw** | Receber os dados originais dos CSVs, preservando seus valores e sua estrutura para rastreabilidade. |
| **Silver** | Padronizar tipos e valores, tratar inconsistências e aplicar regras de qualidade e integridade referencial. |
| **Gold** | Disponibilizar tabelas, visões, agregações e métricas para consultas e análises. |

```text
Arquivo ZIP com quatro CSVs
             |
             v
      1_extrair.py
             |
             v
   PostgreSQL — RAW
             |
             v
     2_transformar.py
             |
             v
   PostgreSQL — SILVER
             |
             v
       Consultas SQL
    + 3_analise.ipynb
             |
             v
   PostgreSQL — GOLD
             |
             v
  7 perguntas de negócio
  + tabelas + 6 gráficos
```

**Observação técnica:** como os dados são inicialmente carregados na camada Raw e depois transformados no banco, a sequência operacional apresenta características de **ELT** (extração, carga e transformação), embora também envolva processos de ETL ao longo do pipeline.

## 3. Fonte e características dos dados

O conjunto de dados reúne quatro arquivos CSV relativos a viagens realizadas em **2025**, disponibilizados para a atividade em um arquivo ZIP.

Os CSVs utilizam separador `;`, codificação `latin-1`, datas no formato `DD/MM/AAAA` e valores monetários representados com vírgula decimal.

| Arquivo | Registros informados |
|---|---:|
| `2025_Viagem.csv` | 341.860 |
| `2025_Pagamento.csv` | 606.916 |
| `2025_Passagem.csv` | 167.260 |
| `2025_Trecho.csv` | 763.349 |
| **Total** | **1.879.385** |

As quantidades acima correspondem à contagem informada para os arquivos originais. Após a carga, podem ser verificadas por consultas SQL às tabelas Raw. As contagens das tabelas Silver podem ser diferentes em razão das regras de validação.

O arquivo `data/viagens_2025_6meses.zip` está versionado por meio do **Git LFS**, utilizado para gerenciar arquivos de maior porte.

## 4. Tecnologias e ferramentas

| Tecnologia | Aplicação |
|---|---|
| **Python** | Automação dos processos de ingestão, transformação e análise. |
| **Pandas** | Leitura, processamento e manipulação de dados tabulares. |
| **PostgreSQL** | Armazenamento relacional das camadas Raw, Silver e Gold. |
| **SQL** | Definição de tabelas, relacionamentos, consultas e agregações. |
| **Matplotlib** | Geração das visualizações gráficas. |
| **Jupyter Notebook** | Execução e documentação da análise exploratória. |
| **Pytest** | Testes automatizados das funções de transformação. |
| **Git e GitHub** | Controle de versão, rastreamento das alterações e publicação do código. |
| **Git LFS** | Versionamento do arquivo ZIP de dados. |

## 5. Organização do repositório

```text
Projeto-Avaliativo-Modulo1-Daniele-de-Souza/
├── data/
│   ├── .gitkeep
│   └── viagens_2025_6meses.zip
├── graficos/
│   ├── .gitkeep
│   └── 01_...png a 06_...png
├── sql/
│   ├── 0_criar_database.sql
│   ├── 0_criar_tabelas.sql
│   ├── 3_criar_gold.sql
│   └── teste_gold.sql
├── testes/
│   └── test_transformacoes.py
├── 0_criar_banco.sql
├── 1_extrair.py
├── 2_transformar.py
├── 3_analise.ipynb
├── banco.py
├── config.py
├── transformacoes.py
├── requirements.txt
├── pytest.ini
├── .env.example
├── .gitignore
├── .gitattributes
└── README.md
```

| Arquivo | Finalidade |
|---|---|
| `0_criar_banco.sql` | Script principal de preparação do banco e das tabelas. |
| `sql/0_criar_database.sql` | Criação do banco de dados. |
| `sql/0_criar_tabelas.sql` | Criação das oito tabelas Raw e Silver. |
| `banco.py` | Rotinas de conexão com o PostgreSQL. |
| `config.py` | Caminhos, parâmetros e leitura de variáveis do arquivo `.env`. |
| `1_extrair.py` | Leitura do ZIP/CSV e carga da camada Raw. |
| `2_transformar.py` | Processamento e carga da camada Silver. |
| `transformacoes.py` | Funções de limpeza, conversão e cálculo. |
| `sql/3_criar_gold.sql` | Definição de estruturas analíticas Gold. |
| `sql/teste_gold.sql` | Consultas de verificação da camada Gold. |
| `3_analise.ipynb` | Consultas, respostas às perguntas e geração de gráficos. |
| `testes/test_transformacoes.py` | Testes automatizados das funções de transformação. |
| `.env.example` | Modelo de configuração sem credenciais reais. |
| `.gitignore` | Exclusão de arquivos locais, temporários ou sensíveis. |
| `.gitattributes` | Regras de versionamento do ZIP pelo Git LFS. |


## 6. Pré-requisitos

- **Python 3.10** ou superior.
- **PostgreSQL** instalado e acessível.
- **Git** e **Git LFS**, necessários para clonar o repositório e recuperar o arquivo ZIP.
- **pgAdmin** (recomendado) para a configuração e inspeção do banco.
- **Visual Studio Code** com as extensões Python e Jupyter (recomendado).

## 7. Instalação e configuração — Windows / PowerShell

Clone o repositório e entre na pasta do projeto:

```powershell
git clone https://github.com/szadaniele/Projeto-Avaliativo-Modulo1-Daniele-de-Souza.git
cd Projeto-Avaliativo-Modulo1-Daniele-de-Souza

git lfs install
git lfs pull
```

Crie e ative um ambiente virtual e instale as dependências:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se o PowerShell bloquear a ativação, permita a execução de scripts somente na sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Crie seu arquivo local de variáveis de ambiente:

```powershell
Copy-Item .env.example .env
```

Edite o `.env` e configure a conexão com o PostgreSQL, incluindo `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD` e `POSTGRES_DATABASE`, conforme necessário. **Nunca publique senhas ou tokens reais no GitHub.**

### Disponibilidade da base

O arquivo `data/viagens_2025_6meses.zip` é recuperado pelo Git LFS. Verifique sua existência antes de executar a extração. Conforme a lógica descrita no projeto, a rotina de ingestão pode utilizar esse arquivo localmente, sem precisar realizar um novo download.

## 8. Criação do banco de dados e execução

### 8.1 Criar o banco e as tabelas

No **pgAdmin**:

1. Conecte-se ao servidor PostgreSQL.
2. Em **Databases**, crie um banco chamado `transparencia`.
3. Abra o **Query Tool** conectado ao banco `transparencia`.
4. Execute `sql/0_criar_tabelas.sql` para criar as tabelas Raw e Silver.
5. Confira o resultado em **Schemas > public > Tables**.

**Alternativa:** o projeto também disponibiliza `0_criar_banco.sql` e `sql/0_criar_database.sql` para cenários de preparação do banco via SQL. Escolha **um** procedimento compatível com seu cliente e sua configuração; não é necessário executar os scripts alternativos repetidamente.

### 8.2 Executar a extração, transformação e validação

Com o ambiente virtual ativo, execute na pasta raiz:

```powershell
python 1_extrair.py
python 2_transformar.py
python -m pytest testes/ -v
```

### 8.3 Executar a análise Gold

Abra `3_analise.ipynb` no VS Code, selecione o interpretador do ambiente `.venv` como kernel e execute as células em sequência (**Run All**).

Conforme a implementação descrita no projeto, o notebook utiliza consultas e estruturas SQL para responder às perguntas de negócio, gerar as tabelas analíticas Gold e salvar seis gráficos PNG em `graficos/`.

**Ordem lógica do processamento:** preparação do PostgreSQL → `1_extrair.py` → `2_transformar.py` → `3_analise.ipynb`.

### 8.4 Conferir as quantidades carregadas

```sql
SELECT COUNT(*) AS total FROM raw_viagem;      -- referência: 341860
SELECT COUNT(*) AS total FROM raw_pagamento;   -- referência: 606916
SELECT COUNT(*) AS total FROM raw_passagem;    -- referência: 167260
SELECT COUNT(*) AS total FROM raw_trecho;      -- referência: 763349

SELECT COUNT(*) AS total FROM silver_viagem;
SELECT COUNT(*) AS total FROM silver_pagamento;
SELECT COUNT(*) AS total FROM silver_passagem;
SELECT COUNT(*) AS total FROM silver_trecho;

SELECT *
FROM gold_resumo_orgaos
ORDER BY total_pago DESC
LIMIT 5;
```

## 9. Regras de tratamento e qualidade dos dados

### Camada Raw

As tabelas `raw_viagem`, `raw_pagamento`, `raw_passagem` e `raw_trecho` recebem os registros de origem em formato textual, preservando representações originais, como zeros à esquerda e campos ainda não convertidos.

### Camada Silver

As tabelas `silver_viagem`, `silver_pagamento`, `silver_passagem` e `silver_trecho` aplicam tipagem e regras de integridade, incluindo chaves e restrições de unicidade conforme a modelagem do projeto.

Principais transformações documentadas:

- **Datas:** conversão de `DD/MM/AAAA` para o tipo `DATE` no PostgreSQL.
- **Valores monetários:** conversão de notações como `1.272,97` para valores numéricos (`1272.97`).
- **Custo total da viagem:** `valor_total = valor_diarias + valor_passagens + valor_outros_gastos - valor_devolucao`.
- **Duração da viagem:** `duracao_dias = (data_fim - data_inicio) + 1`, incluindo as datas inicial e final.
- **Campos ausentes:** preenchimento com `Sem informação` nos campos previstos ou uso de `NULL`, conforme a regra aplicável.
- **Limites de comprimento:** adequação de strings ao esquema da Silver, preservando a versão original na Raw.
- **Integridade:** relacionamentos por `id_viagem` e unicidade de `(id_viagem, sequencia_trecho)` na tabela de trechos, conforme a modelagem descrita.

Registros que não atendem às regras podem deixar de ser carregados na Silver, permanecendo disponíveis na Raw para auditoria e revisão.

**Atenção à recarga:** os scripts são descritos como capazes de limpar e recarregar tabelas por meio de `TRUNCATE`. Execute-os somente em um banco destinado ao projeto, pois essa operação remove os dados existentes das tabelas afetadas.

### Camada Gold

A camada analítica reúne a tabela `gold_resumo_orgaos` e as visões `gold_visao_pagamentos` e `gold_visao_trechos`. A documentação do projeto prevê pré-agregação de pagamentos por viagem para evitar multiplicações indevidas de valores durante operações de `JOIN`.

## 10. Perguntas de negócio e visualizações

As análises abrangem sete questões propostas no desafio:

| Nº | Pergunta |
|---:|---|
| 1 | Quais são os cinco órgãos com maior custo total em viagens? |
| 2 | Quais são os três destinos com maior custo médio por viagem? |
| 3 | Qual foi a viagem de maior duração e qual foi seu custo total? |
| 4 | Qual tipo de pagamento apresenta o maior valor médio? |
| 5 | Qual é o meio de transporte mais utilizado nos trechos? |
| 6 | Qual unidade federativa de destino aparece no maior número de trechos? |
| 7 | Qual órgão pagador apresentou o maior valor total? |

Segundo a organização do notebook, **três perguntas são respondidas diretamente com dados Silver e quatro utilizam estruturas da Gold**. As respostas, consultas e tabelas estão reunidas em [`3_analise.ipynb`](3_analise.ipynb).

### Gráficos gerados

| Visualização | Arquivo |
|---|---|
| Órgãos com maiores custos | [`01_orgaos_maiores_custos.png`](graficos/01_orgaos_maiores_custos.png) |
| Destinos com maior custo médio | [`02_destinos_custo_medio.png`](graficos/02_destinos_custo_medio.png) |
| Viagem de maior duração | [`03_viagem_mais_longa.png`](graficos/03_viagem_mais_longa.png) |
| Valor médio por tipo de pagamento | [`04_pagamento_valor_medio.png`](graficos/04_pagamento_valor_medio.png) |
| Meios de transporte utilizados | [`05_transportes.png`](graficos/05_transportes.png) |
| Unidades federativas de destino | [`06_ufs_destino.png`](graficos/06_ufs_destino.png) |

Os resultados numéricos dependem dos dados efetivamente carregados e das consultas executadas; o README não apresenta valores analíticos fictícios.

## 11. Validação e limitações

A documentação do projeto registra:

- Inspeção dos quatro CSVs de origem, incluindo contagens e cabeçalhos.
- Testes automatizados para funções de conversão e transformação em `testes/test_transformacoes.py`.
- Consultas SQL de conferência das tabelas Raw, Silver e Gold.
- Notebook com as sete perguntas de negócio e seis visualizações.

**Limitação de execução:** para reproduzir todas as análises, é necessário configurar e executar o PostgreSQL localmente. A presença do notebook, dos scripts e dos gráficos versionados não substitui a validação de uma execução completa do pipeline em outro ambiente.

## 12. Considerações finais

O desenvolvimento integra práticas de **Engenharia e Análise de Dados**, desde a ingestão de arquivos heterogêneos e a modelagem relacional até a preparação de conjuntos de dados analíticos e a comunicação dos resultados.

A separação em camadas Raw, Silver e Gold contribui para a organização do processamento e para a rastreabilidade dos dados. O uso de testes, scripts SQL, notebook e versionamento com Git/GitHub favorece a manutenção, a documentação e a reprodutibilidade da solução.

### Possibilidades de evolução

- Ampliar os indicadores e comparar períodos adicionais.
- Incluir **testes de integração e testes de ponta a ponta** do pipeline, além dos testes unitários existentes.
- Automatizar relatórios de rejeição e indicadores de qualidade dos registros.
- Implementar logging estruturado, monitoramento e execução agendada.
- Otimizar as consultas e analisar o desempenho do PostgreSQL.
- Desenvolver relatórios e painéis para acompanhamento periódico dos gastos.
