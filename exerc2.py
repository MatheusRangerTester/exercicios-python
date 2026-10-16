import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent
ARQUIVO = BASE / "data" / "raw" /"vendas.csv"

if not ARQUIVO.exists():
    raise FileNotFoundError(ARQUIVO)

# print(ARQUIVO)

df = pd.read_csv(
    ARQUIVO,
    usecols=["data", "regiao", "preco_unitario"],
    parse_dates=["data"],
    dtype={"regiao":"string"},
    na_values=["","NA","N/A","-"]
    )
print(f"shape: {df.shape}\n")
print(f"5 primeiras linhas do DataFrame:\n {df.head()}\n")
print(f"5 linhas aleatórias: \n{df.sample(5, random_state=42)}\n")
print(f"tipos das colunas:\n{df.info()}\n")
print(f"descrição do DF:\n{df.describe(include="all")}\n")
print(f"soma dos valores vazios:\n{df.isna().sum()}\n")
print(f"valores unicos do DF:\n{df.nunique()}\n")
print(f"valores duplicados:\n{df.duplicated().sum()}\n")

df = df.convert_dtypes()
df["data"] = pd.to_datetime(df['data'], errors="coerce")
df["preco_unitario"] = pd.to_numeric(df["preco_unitario"], errors="coerce")

df["regiao"] = (
    df["regiao"]
    .astype("string")
    .str.strip()
    .str.upper()
)

validos = {"RJ","SP","MG","ES"}
invalidos = ~df["regiao"].isin(validos)

# print(invalidos)


df["data"] = pd.to_datetime(df["data"], errors="coerce")

df["ano"] = df["data"].dt.year
df["mes"] = df["data"].dt.to_period("M")
df["dia_semana"] = df["data"].dt.day_name

mensal = df.groupby("mes", observed=True)["preco_unitario"].sum()

print(mensal)
