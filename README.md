# Projeto Avaliativo Módulo 1 — Análise de Dados com Python [T6]

<p align="center">
  <strong>Pipeline ETL com Python, PostgreSQL e Arquitetura Medallion</strong>
</p>
Este projeto foi desenvolvido como parte da avaliação do **Módulo 1 do curso Análise de Dados com Python**, oferecido pelo **SENAI**, instituição parceira do programa **SCTEC**

O desafio consiste em desenvolver um pipeline completo de dados utilizando Python e SQL, aplicando conceitos de Engenharia e Análise de Dados para transformar dados públicos em informações estruturadas e úteis para a tomada de decisão.

A base utilizada é proveniente do **Portal da Transparência do Governo Federal**, contendo registros de viagens a serviço. A proposta é automatizar a extração, preservar os dados originais, realizar o tratamento e a modelagem e, por fim, construir análises que permitam compreender os gastos públicos relacionados a essas viagens.

**Objetivo:** 
- Automatizar o download e a extração dos arquivos disponibilizados em formato CSV.
- Preservar os dados originais na camada Raw.
- Realizar limpeza, conversão de tipos e validação dos dados na camada Silver.
- Garantir integridade referencial entre as tabelas.
- Construir agregações na camada Gold utilizando SQL.
- Responder perguntas de negócio por meio de consultas, tabelas e visualizações.
- Desenvolver um fluxo de processamento organizado, reproduzível e documentado.


## Arquitetura do projeto

O pipeline foi desenvolvido seguindo a **Arquitetura Medallion**, organizada em três camadas:

| Camada | Descrição |
|---|---|
|**Raw** | Armazena os dados originais, preservando sua estrutura e conteúdo. |
|**Silver** | Realiza o tratamento, a tipagem dos dados e os relacionamentos entre as tabelas. |
|**Gold** | Disponibiliza dados agregados e métricas para responder às perguntas de negócio. |

### Fluxo ETL

1. **Extract:** download automatizado do arquivo ZIP e leitura dos quatro arquivos CSV.
2. **Transform:** conversão de valores e datas, tratamento dos dados e cálculo de indicadores.
3. **Load:** carregamento nas tabelas Raw e Silver e construção das estruturas analíticas Gold.

## Tecnologias e ferramentas

- **Python:** desenvolvimento do pipeline ETL e análises.
- **Pandas:** leitura, processamento e manipulação dos dados.
- **PostgreSQL:** armazenamento e modelagem das camadas Raw, Silver e Gold.
- **SQL:** consultas, relacionamentos, agregações e criação de estruturas analíticas.
- **Matplotlib:** construção dos gráficos.
- **Jupyter Notebook:** exploração e apresentação das análises.
- **Git e GitHub:** versionamento e organização do desenvolvimento.

## Análises e perguntas de negócio

O projeto responde às sete perguntas propostas no desafio:

| Nº | Pergunta de negócio |
|---|---|
| 01 | Quais são os cinco órgãos com maior custo total em viagens? |
| 02 | Quais são os três destinos com maior custo médio por viagem? |
| 03 | Qual foi a viagem de maior duração e qual foi seu custo total? |
| 04 | Qual tipo de pagamento apresenta o maior valor médio? |
| 05 | Qual é o meio de transporte mais utilizado nos trechos? |
| 06 | Qual UF de destino aparece no maior número de trechos? |
| 07 | Qual órgão pagador apresentou o maior valor total? |

As consultas SQL, tabelas de resultados, gráficos e interpretações estão documentados no notebook `3_analise.ipynb`

## 1. Contexto e problema

Os arquivos de viagens chegam em formato CSV, separados por `;`, codificados em `latin-1`, com datas em `DD/MM/AAAA` e valores em reais com vírgula. O sistema organiza esses dados numa arquitetura **Medallion (Raw → Silver → Gold)**, permitindo comparações de custos de viagens e pagamentos, duração e destinos.

A base entregue possui:

| Arquivo | Linhas de dados |
|---|---:|
| 2025_Viagem.csv | 341.860 |
| 2025_Pagamento.csv | 606.916 |
| 2025_Passagem.csv | 167.260 |
| 2025_Trecho.csv | 763.349 |
| **TOTAL** | **1.879.385** |

Estes totais foram conferidos nos quatro arquivos do ZIP original. Após executar a carga, confirme os valores com consultas SQL; registros inválidos podem ser rejeitados na Silver.

## 2. Arquitetura e arquivos

```text
ZIP CSVs 2025 (dados originais)
       |
       v
1_extrair.py -----------> PostgreSQL: 4 tabelas RAW (texto, sem constraints)
       |                               |
       |                               v
       +----------------------> 2_transformar.py
                                       |
                                       v
                               4 tabelas SILVER
                              (DATE, NUMERIC, PK/FK,
                               NOT NULL, CHECK, UNIQUE)
                                       |
                                       v
                               3_analise.ipynb
                                       |
                                       v
                              TABELA + VIEWS GOLD
                              7 perguntas + 6 graficos
```

| Arquivo | Finalidade |
|---|---|
| `0_criar_banco.sql` | Cria o banco (se necessário) e 8 tabelas |
| `sql/0_criar_database.sql` | Cria somente o banco (se for usar pgAdmin) |
| `sql/0_criar_tabelas.sql` | Cria as 8 tabelas (alternativa ao script principal) |
| `config.py`  | Parâmetros e leitura do `.env` |.
| `banco.py` | Conexão com PostgreSQL |
| `transformacoes.py` | Funções de limpeza e cálculo |
| `1_extrair.py` | Baixa/lê ZIP, carrega as tabelas Raw |
| `2_transformar.py` | Transforma Raw → Silver |
| `3_analise.ipynb` | Gold, sete respostas, tabelas e gráficos |
| `sql/3_criar_gold.sql` | Cria a tabela Gold e as views Gold |
| `testes/test_transformacoes.py` | Testes de datas, decimais e cálculos |
| `.env.example` | Modelo de configurações sem senha |
| `.gitignore`s | Não publica senhas, arquivos grandes ou temporários |

## 3. Pré-requisitos

Instale **Python 3.10+**, **PostgreSQL** e o gerenciador gráfico **pgAdmin**, **VS Code**, extensões **Python** e **Jupyter** do VS Code, e **Git**. 

## 4. Instalação — Windows / PowerShell no VS Code

Abra a pasta do projeto pelo menu **File > Open Folder** no VS Code. Abra um terminal com **Terminal > New Terminal**. Execute:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se o PowerShell impedir a ativação, tente apenas nesta sessão:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Copie `.env.example` para `.env` e preencha `POSTGRES_PASSWORD` com a senha do PostgreSQL.

```powershell
Copy-Item .env.example .env
```

### Base de dados

Nessa versão **com dados**, o ZIP já está disponível em `data/viagens_2025_6meses.zip`. A extração usará este arquivo automaticamente, sem internet.

## 5. Criar banco e tabelas no PostgreSQL

1. Abra o pgAdmin e conecte-se ao PostgreSQL.
2. Na árvore à esquerda, clique em `Databases > Create > Database`.
3. Nomeie o banco como **transparencia** e salve.
4. Selecione o banco **transparencia**, abra **Query Tool**.
5. Abra `sql/0_criar_tabelas.sql`, clique em executar.
6. Confira `Schemas > public > Tables` e as oito tabelas criadas.

## 6. Executar o pipeline

No terminal do VS Code, com ambiente virtual ativo:

```powershell
python 1_extrair.py
python 2_transformar.py
python -m pytest testes/ -v
```

Abra `3_analise.ipynb` no VS Code, selecione o kernel `.venv` e clique em **Run All**. O notebook executa as consultas, recria a tabela e as views Gold, apresenta os resultados das sete perguntas em tabelas e gera seis gráficos em PNG na pasta `graficos/`. Execute-o somente depois de criar as tabelas e carregar os dados nas fases anteriores.

### Ordem obrigatória

`0_criar_banco.sql` → `1_extrair.py` → `2_transformar.py` → `3_analise.ipynb`.

### Conferência SQL

```sql
SELECT COUNT(*) FROM raw_viagem;      -- esperado: 341860
SELECT COUNT(*) FROM raw_pagamento;   -- esperado: 606916
SELECT COUNT(*) FROM raw_passagem;    -- esperado: 167260
SELECT COUNT(*) FROM raw_trecho;      -- esperado: 763349
SELECT COUNT(*) FROM silver_viagem;
SELECT COUNT(*) FROM silver_pagamento;
SELECT COUNT(*) FROM silver_passagem;
SELECT COUNT(*) FROM silver_trecho;
SELECT * FROM gold_resumo_orgaos ORDER BY total_pago DESC LIMIT 5;
```

## 7. Dicionário e tratamento

**Raw:** quatro tabelas `raw_viagem`, `raw_pagamento`, `raw_passagem`, `raw_trecho`, com *todas* as colunas dos CSVs como VARCHAR e **sem constraints**. Formatos brutos, zeros à esquerda e campos extras não se perdem.

**Silver:** tabelas tipadas `silver_viagem`, `silver_pagamento`, `silver_passagem`, `silver_trecho`, com PK, FK e oito constraints extras. As tabelas filhas referenciam `silver_viagem.id_viagem`. `silver_trecho` restringe `(id_viagem, sequencia_trecho)` a valores únicos. Dados inválidos são descartados da Silver com contagens no terminal, mas permanecem intactos na Raw.

- Datas em `DD/MM/AAAA` passam para `DATE` (ISO `AAAA-MM-DD`).
- Valores em `1.272,97` viram `NUMERIC` 1272.97.
- `valor_total = valor_diarias + valor_passagens + valor_outros_gastos - valor_devolucao`.
- `duracao_dias = (data_fim - data_inicio) + 1`, inclusive.
- Campos obrigatórios sem valor recebem `Sem informação`; outros campos em branco podem virar `NULL`.
- Strings maiores que as larguras da Silver são limitadas a essas larguras; os originais ficam completos na Raw.
- Em recargas, Raw usa TRUNCATE; Silver também é zerada e carregada novamente, evitando duplicidade.

**Gold:** `gold_resumo_orgaos` (tabela), `gold_visao_pagamentos` e `gold_visao_trechos` (views). O notebook recria essas estruturas a cada execução. O uso de pré-agregação de pagamento por viagem evita duplicações geradas por JOIN.

## 8. Sete perguntas respondidas

**Três diretamente da Silver:** cinco órgãos superiores com maior custo de viagem; três destinos com maior custo médio por viagem; viagem mais longa e seu custo.  
**Quatro usando Gold:** tipo de pagamento com maior valor médio; transporte mais usado; UF de destino com mais trechos; órgão pagador com maior valor desembolsado.

O notebook cria três gráficos Silver e três gráficos Gold, todos com título, eixos nomeados e legenda. O resultado depende da execução local no PostgreSQL; **não são apresentados números fictícios**.

## 9. Conclusões

O projeto permitiu desenvolver os conceitos fundamentais de Engenharia e Análise de Dados:

- Extração e carregamento automatizado de dados.
- Manipulação e tratamento de grandes volumes de informações com Pandas.
- Conversão e padronização de tipos de dados.
- Construção de consultas SQL com JOIN, GROUP BY e funções de agregação.
- Implementação da Arquitetura Medallion.
- Análise exploratória e identificação de padrões.
- Construção de gráficos para apresentação dos resultados.
- Organização e versionamento do código com Git e GitHub.

## 10. Sugestões de melhorias

Como possibilidades de evolução do projeto, destacam-se:

- Ampliação das análises com novos indicadores.
- Implementação de testes automatizados para validação do pipeline.
- Otimização das consultas para melhorar o desempenho.
- Salvar um relatório automatizado de registros inválidos.
- Adicionar logs e execução agendada.
- Criar métricas mensais e comparar os seis meses analisados.

## 11. Situação de validação

- Quatro CSVs originais inspecionados, com contagem de registros e conferência dos cabeçalhos.
- Funções de conversão cobertas por testes automatizados simples.
- Notebook criado com instruções, SQL e gráficos; sua execução completa depende de PostgreSQL disponível localmente.

