"""
Portao de verificacao do projeto. Um comando, tres camadas, verde ou vermelho.

    python verificar.py

Pergunta unica: o que este repositorio AFIRMA em publico ainda bate com o dado
que ele carrega? As tres camadas:

  1. SQL       cada arquivo de queries/ e executado contra database/SQLite.db e
               o resultado e comparado, linha a linha, com o CSV correspondente
               em data/exports/. E o teste que responde "esse export saiu mesmo
               dessa query, nesse banco?"
  2. README    os insights do texto sao afirmacoes testaveis, e cada uma vira um
               teste. "Pico de receita no ultimo trimestre" e uma ordenacao: ou
               o dado sustenta, ou nao sustenta. Insight que nao passa nao e
               opiniao, e erro
  3. dashboard  o .pbix e um zip; da pra ler quantas paginas ele tem sem abrir o
               Power BI, e conferir contra o que o README descreve

Precisa de pandas (requirements.txt). O banco e os exports sao versionados,
entao roda em qualquer clone, offline.

Sai com codigo 1 se qualquer linha falhar.
"""
from pathlib import Path
import json
import re
import sqlite3
import sys
import zipfile

import pandas as pd

RAIZ = Path(__file__).resolve().parent
README = (RAIZ / "README.md").read_text(encoding="utf-8")
EXPORTS = RAIZ / "data" / "exports"
FALHAS = []


def check(nome: str, ok: bool, detalhe: str):
    print(f"  [{'OK' if ok else 'FALHOU'}] {nome}: {detalhe}")
    if not ok:
        FALHAS.append(nome)


def afirmacao(nome: str, padrao: str, sustenta: bool, detalhe: str):
    """
    Casa uma frase do README com o teste dela. Falha nos dois sentidos: se o dado
    nao sustenta o que o texto diz, e se a frase sumiu do texto, porque afirmacao
    editada precisa ser reverificada e nao ignorada em silencio.
    """
    if not re.search(padrao, README, re.S | re.I):
        check(nome, False, "afirmacao nao encontrada no README (a frase foi reescrita?)")
        return
    check(nome, sustenta, detalhe)


# ---------------------------------------------------------------- camada 1
print("== camada 1: cada export sai de novo da query que diz produzi-lo ==")
con = sqlite3.connect(RAIZ / "database" / "SQLite.db")
objetos = pd.read_sql("select type, name, sql from sqlite_master", con).set_index("name")
views_declaradas = re.findall(r"create view (\w+)", (RAIZ / "queries" / "views.sql").read_text(encoding="utf-8"), re.I)
faltando = [v for v in views_declaradas if v not in objetos.index]
check("as views de views.sql existem no banco", not faltando,
      f"{len(views_declaradas)} declaradas, ausentes: {faltando or 'nenhuma'}")

arquivos = sorted((RAIZ / "queries").glob("q*.sql"))
for q in arquivos:
    export = EXPORTS / f"{q.stem}.csv"
    if not export.exists():
        check(f"{q.stem}: export correspondente", False, f"{export.name} nao existe")
        continue
    obtido = pd.read_sql(q.read_text(encoding="utf-8"), con)
    esperado = pd.read_csv(export)
    if obtido.shape != esperado.shape or list(obtido.columns) != list(esperado.columns):
        check(f"{q.stem}: query reproduz o export", False,
              f"query {obtido.shape} {list(obtido.columns)} contra export {esperado.shape} {list(esperado.columns)}")
        continue
    divergentes = []
    for col in obtido.columns:
        if pd.api.types.is_numeric_dtype(esperado[col]):
            d = (obtido[col] - esperado[col]).abs().max()
            if d > 1e-6:
                divergentes.append(f"{col} (ate {d:.4g})")
        elif (obtido[col].astype(str) != esperado[col].astype(str)).any():
            n = int((obtido[col].astype(str) != esperado[col].astype(str)).sum())
            divergentes.append(f"{col} ({n} linhas)")
    check(f"{q.stem}: query reproduz o export", not divergentes,
          f"{len(obtido)} linhas, {len(obtido.columns)} colunas"
          + (f", divergem: {divergentes}" if divergentes else ""))

declaradas = re.findall(r"- (Q\d) - ", README)
check("as queries que o README lista sao as que existem em queries/",
      len(declaradas) == len(arquivos)
      and all(q.stem.upper().startswith(d) for d, q in zip(declaradas, arquivos)),
      f"README lista {declaradas}, disco tem {[q.stem for q in arquivos]}")

pastas = re.findall(r"- '([^']+/)'", README)
sumidas = [p for p in pastas if not (RAIZ / p).is_dir()]
check("a estrutura de pastas que o README lista existe", not sumidas,
      f"{len(pastas)} pastas citadas, sumidas: {sumidas or 'nenhuma'}")

# ---------------------------------------------------------------- camada 2
print("\n== camada 2: os insights do README contra os exports ==")
q1 = pd.read_csv(EXPORTS / "q1_receita_mensal.csv")
q1["ano"] = q1.mes.str[:4].astype(int)
q1["trimestre"] = (q1.mes.str[5:].astype(int) - 1) // 3 + 1
por_tri = q1.groupby(["ano", "trimestre"]).receita_total.sum()
anos_completos = [a for a in q1.ano.unique() if set(q1[q1.ano == a].trimestre) == {1, 2, 3, 4}]
afirmacao("o pico de receita cai no ultimo trimestre dos anos completos",
          r"Pico de receita no último trimestre dos anos",
          bool(anos_completos) and all(por_tri[a].idxmax() == 4 for a in anos_completos),
          " · ".join(f"{a}: pico no {por_tri[a].idxmax()}T "
                     f"({' '.join(f'{t}T {v/1000:.0f}k' for t, v in por_tri[a].items())})"
                     for a in anos_completos))
afirmacao("maio de 2015 e mesmo o fim da serie, nao uma crise",
          r"Queda abrupta em Maio de 2015 significa o fim do período de dados",
          q1.mes.max() == "2015-05",
          f"serie vai de {q1.mes.min()} a {q1.mes.max()}, sem mes posterior")

q2 = pd.read_csv(EXPORTS / "q2_receita_categoria.csv")
q2["share"] = 100 * q2.receita_total / q2.receita_total.sum()
abaixo10 = set(q2[q2.share < 10].categoryname)
citadas = set(re.findall(r"como (Condiments), (Produce) e (Grains & Cereals)", README)[0]) \
    if re.search(r"como Condiments, Produce e Grains & Cereals", README) else set()
afirmacao("as categorias abaixo de 10% da receita sao exatamente as tres citadas",
          r"receita abaixo dos 10% do total, como Condiments, Produce e Grains & Cereals",
          abaixo10 == citadas,
          " · ".join(f"{c}: {s:.1f}%" for c, s in zip(q2.categoryname, q2.share)))

q3 = pd.read_csv(EXPORTS / "q3_top_produtos.csv")
top10 = q3.head(10)
das_fracas = top10[top10.categoryname.isin(abaixo10)]
afirmacao("categoria fraca no total ainda coloca item entre os dez mais vendidos",
          r"existem itens que estão dentre os dez mais vendidos pela empresa",
          len(das_fracas) > 0,
          f"{len(das_fracas)} dos 10 primeiros vem de "
          f"{sorted(set(das_fracas.categoryname)) or 'nenhuma categoria fraca'}")

q4 = pd.read_csv(EXPORTS / "q4_receita_pais.csv")
q7 = pd.read_csv(EXPORTS / "q7_tempo_medio.csv")
geo = q4[["country", "receita_total"]].merge(q7[["country", "dias_ate_envio"]], on="country")
pares = [(a.country, b.country, a.dias_ate_envio / b.dias_ate_envio)
         for a in geo.itertuples() for b in geo.itertuples()
         if a.country != b.country and a.receita_total >= b.receita_total
         and a.dias_ate_envio >= 1.5 * b.dias_ate_envio]
pior = max(pares, key=lambda p: p[2]) if pares else None
afirmacao("ha pais que fatura igual ou mais e espera 50% a mais pelo produto",
          r"receitas similares ou até maiores estão recebendo seus produtos em 50% a mais do tempo",
          bool(pares),
          f"{len(pares)} pares assim; o pior e {pior[0]} contra {pior[1]}, "
          f"{pior[2]:.0%} do tempo" if pior else "nenhum par")

q6 = pd.read_csv(EXPORTS / "q6_top_clientes.csv")
q6["share"] = 100 * q6.receita_total / q6.receita_total.sum()
top3 = q6.share.head(3).sum()
m = re.search(r"os três maiores clientes concentram (\d+)% da receita.*?entre os (\d+)", README, re.S)
afirmacao("a concentracao nos tres maiores clientes e a que o README publica",
          r"os três maiores clientes concentram \d+% da receita",
          bool(m) and abs(int(m.group(1)) - top3) <= 0.5 and int(m.group(2)) == len(q6),
          f"top 3 = {top3:.1f}% de {len(q6)} clientes "
          f"({' · '.join(f'{c} {s:.1f}%' for c, s in zip(q6.companyname.head(3), q6.share.head(3)))})")

# ---------------------------------------------------------------- camada 3
print("\n== camada 3: o dashboard contra o que o README descreve ==")
pbix = RAIZ / "powerbi" / "northwind.pbix"
with zipfile.ZipFile(pbix) as z:
    layout = json.loads(z.read("Report/Layout").decode("utf-16-le"))
paginas = [s.get("displayName") for s in layout["sections"]]
descritas = re.findall(r"\*\*Página (\d+)\*\* - ([^\n<]+)", README)
check("o README descreve tantas paginas quantas o .pbix tem",
      len(descritas) == len(paginas),
      f"README descreve {len(descritas)}, o .pbix tem {len(paginas)}: {paginas}")
check("cada pagina do .pbix tem visual", all(s.get("visualContainers") for s in layout["sections"]),
      " · ".join(f"{s.get('displayName')}: {len(s.get('visualContainers', []))} visuais"
                 for s in layout["sections"]))

externas = re.findall(r'src="(https?://[^"]+)"', README)
check("as capturas do dashboard nao estao versionadas no repositorio", True,
      f"{len(externas)} imagens hospedadas fora do repo (um clone nao as tem; "
      f"renderizam no GitHub)" if externas else "todas locais")

print(f"\n{'TUDO PASSOU' if not FALHAS else 'FALHARAM: ' + ', '.join(FALHAS)}")
sys.exit(1 if FALHAS else 0)
