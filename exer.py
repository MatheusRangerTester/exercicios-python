mport altair as alt
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""  DATAFRAMES """

df = pd.DataFrame({
    "pedido_id" : [101,102,103,104,105,106],
    "cliente_id" : [1,2,1,3,4,2],
    "produto_id" : [10,11,12,10,13,11],
    "nome" : ["Ana", "Bruno", "Ana", "Carla", "Diego", "Bruno"],
    "ativo" : [True,True,False,True,True,True],
    "salario" : [3500, 1800, 4200, 2500, 1900, 5100],
    "regiao" : ["RJ", "SP", "RJ","MG", "ES", "SP"],
    "estado" : ["rj", "sp", "rj", "mg", "es", "sp"],
    "produto" : ["Teclado", "Mouse", "Monitor", "Teclado", "Headset", "Mouse"],
    "qtd" : [2,3,1,4,2,1],
    "preco" : [150.00, 80.00, 1200.00, 150.00, 220.00, 80.00],
    "valor" : [300.00, 240.00, 1200.00, 600.00, 440.00, 80.00],
    "data" : pd.to_datetime([
        "2026-01-05",
        "2026-01-06",
        "2026-01-10",
        "2026-01-11",
        "2026-01-01",
        "2026-01-15",
    ])
})

clientes = pd.DataFrame({
    "cliente_id": [1,2,3],
    "segmento" : [
        "Premium",
        "Regular",
        "Premium"
    ]
})

jan = pd.DataFrame({
    "mes" : ["jan", "jan"],
    "produto": ["mouse", "teclado"],
    "valor" : ["800", "1200"]
})
fev = pd.DataFrame({
    "mes" : ["fev", "fev"],
    "produto": ["mouse", "teclado"],
    "valor" : ["500", "800"]
})
mar = pd.DataFrame({
    "mes" : ["mar", "mar"],
    "produto": ["mouse", "teclado"],
    "valor" : ["200", "9000"]
})

pedidos = pd.DataFrame({
    "pedido_id": [101,102,103,104],
    "cliente_id": [1,2,3,4]
})

despesas = pd.DataFrame({
    "mes":["jan", "fev"],
    "alimentacao": [544, 266],
    "moradia":[1800, 2600],
    "transporte":[100, 300]
})

mensal = pd.DataFrame({
    "mes":["jan", "fev"],
    "vendas": [1009, 2000],
    "regiao":["RJ", "SP"]
})

ativos = df.loc[df["ativo"], ["nome", "salario"]]

primeiras = df.iloc[:5, [0,2]]

df.loc[df["salario"] < 2000, "faixa"] = "entrada"

# print(f"ativos: {ativos} \n\n"
#       f"primeiras: {primeiras} \n\n"
#       f"{df.loc[df["salario"] < 2000, "faixa"]}"
#     )

filtro = (df["regiao"] == "RJ") & (df["valor"] >= 1000)
rj = df.loc[filtro]

rj2 = df.query("regiao == 'RJ' and valor >= 1000")

limite = 1000
rj3 = df.query("regiao == 'RJ' and valor >= @limite")

# print(f"{rj} \n {rj2} \n {rj3}\n\n")

resultado = (
    df.assign(total=lambda d: d["qtd"] * d["preco"])
    .rename(columns={"qtd": "quantidade"})
    .sort_values(["total", "produto"], ascending=[False, True])
    .drop(columns=["coluna_temporaria"], errors="ignore")
)

# print(resultado,"\n")

resumo = (
    df.groupby("regiao", as_index=False, observed=True)
    .agg(
        vendas=("valor", "sum"),
        ticket_medio=("valor", "mean"),
        pedidos=("pedido_id", "nunique")
    )
    .sort_values("vendas", ascending=False)
)

# print(resumo)


pedidos = pedidos.merge(
    clientes[["cliente_id", "segmento"]],
    on="cliente_id",
    how="left",
    validate="many_to_one"
)

todos = pd.concat([jan,fev,mar], ignore_index=True)



long = despesas.melt(
    id_vars=["mes"],
    value_vars=["alimentacao", "moradia", "transporte"],
    var_name="categoria",
    value_name="valor"
)

wide = long.pivot_table(
    index="mes", columns="categoria", values="valor", aggfunc="sum"
)


# Matplotlib
fig, ax = plt.subplots(figsize=(9,5))
ax.bar(resumo["regiao"], resumo["vendas"])
ax.set(
    title="Vendas por região",
    xlabel="Região",
    ylabel="Vendas (R$)"
)

fig.tight_layout()
plt.show()

# Seaborn
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(9,5))
sns.barplot(
    data=df, x="regiao", y="valor",
    estimator="mean", ax=ax
)

ax.set_title= ("Ticket médio por região")
# plt.show()

# Plotly
fig = px.line(
    mensal,
    x="mes",
    y="vendas",
    color="regiao",
    markers=True,
    title="Vendas mensais por região"
)

fig.update_layout(yaxis_title="Vendas (R$)")
# fig.show()

#Altair
alt.renderers.enable("browser")

chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(x=alt.X("regiao:N", title="Região"),
            y=alt.Y("sum(valor):Q", title="Vendas (R$)"),
            tooltip=[alt.Tooltip("regiao:N", title="Região"),
            alt.Tooltip("sum(valor):Q", title="Vendas", format=".2f")
        ]
    )
    .properties(title="Vendas por região", width=600, height=350)
)

# chart.show()
