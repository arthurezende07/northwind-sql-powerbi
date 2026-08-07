# Northwind Traders - Análise de Dados

[![verificar](https://github.com/arthurezende07/northwind-sql-powerbi/actions/workflows/verificar.yml/badge.svg)](https://github.com/arthurezende07/northwind-sql-powerbi/actions/workflows/verificar.yml)
Projeto de Análise de Dados com SQLite Online e Power BI, utilizando dataset Northwind Traders (kaggle).

O Desenvolvimento consiste em simular uma situação real, a partir da realização de consultas SQL para criação de views e tratamento de dados. Posteriormente, foi realizado a visualização através de dashboards interativos no Power BI.

## Contexto
Northwind Traders é uma empresa fictícia de importação e exportação de alimentos especiais para empresas, representando um negócio B2B internacional. Dessa forma, cabe ao júnior analisar, identificar e gerar insights que possam agregar valor a empresa.

## Ferramentas
- SQLite Online - importação, limpeza via views e queries de análise.
- Power BI DeskTop - visualizações e Dasboards interativos

## Estrutura das pastas
- 'data/raw/' - datasets originais do Kaggle
- 'data/exports/' - queries exportadas em CSV
- 'database/' - banco de dados .db do SQLite
- 'queries/' - views de limpeza e análise (Q1 a Q7)
- 'powerbi/' - arquivo .pbix com os dashboards

## Queries realizadas
- Q1 - Receita Total por mês
- Q2 - Receita por categoria
- Q3 - Top Produtos
- Q4 - Receita por país
- Q5 - Impacto do desconto
- Q6 - Top clientes
- Q7 - Tempo de envio por país

## Dashboards
- **Página 1** - Visão Geral de Vendas e Portfólio de Categorias
<img width="1432" height="801" alt="image" src="https://github.com/user-attachments/assets/03f44350-ed97-4a90-ac0a-588dcd618886" />

- **Página 2** - Clientes, geografia e eficiência operacional
<img width="1451" height="805" alt="image" src="https://github.com/user-attachments/assets/4d80c02b-961d-4b2f-8452-3865c3c717d4" />

## Verificação

```bash
pip install -r requirements.txt
python verificar.py
```

Verde é exit 0, vermelho é exit 1. Responde uma pergunta só: **o que este README afirma ainda bate com o dado que o repositório carrega?**

1. **SQL.** Cada arquivo de `queries/` é executado contra `database/SQLite.db` e o resultado é comparado linha a linha com o CSV correspondente em `data/exports/`. É o teste que responde "esse export saiu mesmo dessa query, nesse banco?" — sem ele, os sete CSVs são só arquivos que alguém disse que vieram do SQL.
2. **Insights.** Cada afirmação da seção abaixo vira um teste. O pico no último trimestre, as três categorias abaixo de 10% da receita, o item de categoria fraca entre os dez mais vendidos, o país que fatura mais e espera 50% a mais, a concentração nos três maiores clientes. Insight que não passa não é opinião, é erro.
3. **Dashboard.** O `.pbix` é um zip: dá para ler quantas páginas ele tem e quantos visuais cada uma carrega sem abrir o Power BI, e conferir contra o que este README descreve.

Roda offline; o banco e os exports são versionados. Também fica vermelho se uma frase for reescrita a ponto de a afirmação sumir do texto: insight editado é insight que precisa ser reverificado, não ignorado em silêncio.

## Insights e Tomada de Decisão
Com a realização de todo o fluxo de tratamento e visuzalização de dados, foi possível identificar alguns pontos importantes, tais como:

- **Sazonalidade**: Pico de receita no último trimestre dos anos. Pode ser marcado por festividades.
  - **Ação**: Garantir planejamento de estoque e logística para antecipação no aumento do período.
  - **Observação**: Queda abrupta em Maio de 2015 significa o fim do período de dados, não necessariamente um crise nas vendas.

- **Alto Portfólio**: É possível identificar que, dentro da diversidade de categorias, existem muitos produtos sendo vendidos. Para além, as categorias que possuem receita abaixo dos 10% do total, como Condiments, Produce e Grains & Cereals, ofertam demasiados itens que não geram tanto valor, com receitas 'próximas a zero' no catálogo, enquanto existem itens que estão dentre os dez mais vendidos pela empresa.
  - **Ação 1**: Reavaliar categorias e produtos vendidos. É possível reduzir a venda de itens de categorias inferiores, por serem commodities ou artigos de apoio. Assim, a Northwind agregará maior valor aos produtos que     mais vende.
  - **Ação 2**: Há possibilidade de agrupamento de produtos tier A com tier C, a fim de garantir maior valor e escoar estoque de produtos que tendem a decrescer.

- **Distribuição Geográfica**: É nítido que o transporte no continente europeu merece reformulações. Países vizinhos que possuem receitas similares ou até maiores estão recebendo seus produtos em 50% a mais do tempo. Tais ações podem ocasionar perda de cliente que gera alta receita para a empresa.
  - **Ação**: Revisão de rotas com transportadora para garantir que os países sejam abastecidos de forma uniforme.

- **Alta concentração em poucos clientes**: Através da tabela de Receita por Cliente, os três maiores clientes concentram 25% da receita — QUICK-Stop, Ernst Handel e Save-a-lot Markets, com 8% cada. Numa distribuição uniforme entre os 89 clientes da base, os três juntos responderiam por 3%. É oito vezes mais peso do que caberia a eles.
  - **Ação 1**: Criar plano de diversificação de carteira de cliente para diminuir a concentração de clientes em até 12 meses.
  - **Ação 2**: Manter contato regular com as maiores compradoras a fim de fidelizar esses clientes
  - **Ação 3**: Prestar serviços para pequenas empresas. São mercados com potenciais inexplorados que podem vir a ser grandes empresas.
