import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

#-------------------------------------------------------------------------------------------------------------
# BIBLIOTECA PARA CRIAÇÃO DO PDF


from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import cm


#--------------------------------------------------------------------------------------------


#importando CVS criados em projeto_clientes.py

df_clientes = pd.read_csv("df_clientes.csv")

df_clientes.columns = (
    df_clientes.columns
    .str.strip()
)


# ============================================================
# GRÁFICO - CLIENTES NOVOS X RECORRENTES
# ============================================================

clientes_tipo = (
    df_clientes["tipo_cliente"]
    .value_counts()
)

# Garantir a ordem das categorias

ordem = [
    "Novo",
    "Recorrente"
]

clientes_tipo = clientes_tipo.reindex(
    ordem,
    fill_value=0
)

# Criar gráfico

fig, ax = plt.subplots(
    figsize=(8, 5)
)

ax.bar(
    clientes_tipo.index,
    clientes_tipo.values
)

# Título

ax.set_title(
    "Clientes Novos x Recorrentes",
    fontsize=16,
    pad=15
)

# Eixos

ax.set_xlabel(
    "Tipo de cliente",
    fontsize=11
)

ax.set_ylabel(
    "Quantidade de clientes",
    fontsize=11
)

# Valores nas barras

total_clientes = clientes_tipo.sum()

for i, valor in enumerate(
    clientes_tipo.values
):

    percentual = (
        valor
        /
        total_clientes
        * 100
    )

    ax.text(
        i,
        valor,
        f"{valor:,.0f}".replace(",", ".")
        + f" ({percentual:.1f}%)",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold"
    )

# Grade

ax.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

# Salvar

plt.savefig("C:\pandas\graficos\d2_clientes_tipo.png",dpi=300,bbox_inches="tight")

plt.show()

# ============================================================
# GRÁFICO - TOP 10 CLIENTES POR VALOR TOTAL
# ============================================================

top_clientes = (
    df_clientes
    .sort_values(
        "valor_total",
        ascending=False
    )
    .head(10)
    .sort_values(
        "valor_total",
        ascending=True
    )
)

# Criar gráfico

fig, ax = plt.subplots(
    figsize=(10, 6)
)

top_clientes = top_clientes.copy()

top_clientes["cliente"] = [
    f"Cliente {i}"
    for i in range(10, 0, -1)
]

ax.barh(
    top_clientes["cliente"],
    top_clientes["valor_total"]
)

# Título

ax.set_title(
    "Top 10 Clientes por Valor Total",
    fontsize=16,
    pad=15
)

# Eixos

ax.set_xlabel(
    "Valor total comprado",
    fontsize=11
)

ax.set_ylabel(
    "Cliente",
    fontsize=11
)

# Valores nas barras

for i, valor in enumerate(
    top_clientes["valor_total"]
):

    valor_formatado = (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    ax.text(
        valor,
        i,
        f"  {valor_formatado}",
        va="center",
        fontsize=8,
        fontweight="bold"
    )

# Grade

ax.grid(
    axis="x",
    alpha=0.3
)

plt.tight_layout()

# Salvar

plt.savefig("C:\pandas\graficos\d2_top10_clientes.png",dpi=300,bbox_inches="tight")

plt.show()

# ============================================================
# GRÁFICO - CLIENTES RECORRENTES POR ESTADO
# ============================================================

clientes_recorrentes_estado = (
    df_clientes[
        df_clientes["tipo_cliente"] == "Recorrente"
    ]
    .groupby("customer_state")
    .agg(
        qtd_recorrentes=(
            "customer_unique_id",
            "nunique"
        )
    )
    .reset_index()
    .sort_values(
        "qtd_recorrentes",
        ascending=True
    )
)

# Criar gráfico

fig, ax = plt.subplots(
    figsize=(10, 8)
)

ax.barh(
    clientes_recorrentes_estado["customer_state"],
    clientes_recorrentes_estado["qtd_recorrentes"]
)

# Título

ax.set_title(
    "Clientes Recorrentes por Estado",
    fontsize=16,
    pad=15
)

# Eixos

ax.set_xlabel(
    "Quantidade de clientes recorrentes",
    fontsize=11
)

ax.set_ylabel(
    "Estado",
    fontsize=11
)

# Valores nas barras

for i, valor in enumerate(
    clientes_recorrentes_estado["qtd_recorrentes"]
):

    ax.text(
        valor,
        i,
        f"  {valor:,.0f}".replace(",", "."),
        va="center",
        fontsize=8
    )

# Grade

ax.grid(
    axis="x",
    alpha=0.3
)

plt.tight_layout()

# Salvar

plt.savefig("C:\pandas\graficos\d2_recorrentes_estado.png",dpi=300,bbox_inches="tight")

plt.show()

# ============================================================
# GRÁFICO - CLIENTES POR FAIXA DE VALOR
# ============================================================

faixas = [
    0,
    100,
    250,
    500,
    1000,
    float("inf")
]

nomes_faixas = [
    "Até R$ 100",
    "R$ 100 a R$ 250",
    "R$ 250 a R$ 500",
    "R$ 500 a R$ 1.000",
    "Acima de R$ 1.000"
]

df_clientes["faixa_valor"] = pd.cut(
    df_clientes["valor_total"],
    bins=faixas,
    labels=nomes_faixas,
    include_lowest=True
)

clientes_faixa = (
    df_clientes["faixa_valor"]
    .value_counts()
    .reindex(nomes_faixas)
)

# Criar gráfico

fig, ax = plt.subplots(
    figsize=(10, 6)
)

ax.bar(
    clientes_faixa.index,
    clientes_faixa.values
)

# Título

ax.set_title(
    "Distribuição de Clientes por Faixa de Valor",
    fontsize=16,
    pad=15
)

# Eixos

ax.set_xlabel(
    "Valor total comprado",
    fontsize=11
)

ax.set_ylabel(
    "Quantidade de clientes",
    fontsize=11
)

# Valores nas barras

total_clientes = clientes_faixa.sum()

for i, valor in enumerate(
    clientes_faixa.values
):

    percentual = (
        valor
        /
        total_clientes
        * 100
    )

    ax.text(
        i,
        valor,
        f"{valor:,.0f}".replace(",", ".")
        + f" ({percentual:.1f}%)",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold"
    )

# Grade

ax.grid(
    axis="y",
    alpha=0.3
)

nomes_faixas_grafico = [
    "Até\nR$ 100",
    "R$ 100 a\nR$ 250",
    "R$ 250 a\nR$ 500",
    "R$ 500 a\nR$ 1.000",
    "Acima de\nR$ 1.000"
]

plt.xticks(
    range(len(nomes_faixas_grafico)),
    nomes_faixas_grafico,
    rotation=0
)


plt.tight_layout()

# Salvar

plt.savefig("C:\pandas\graficos\d2_faixa_valor.png",dpi=300,bbox_inches="tight")

plt.show()

# ============================================================
# KPIs - CLIENTES
# ============================================================

total_clientes = (
    df_clientes["customer_unique_id"]
    .nunique()
)

clientes_recorrentes = (
    df_clientes[
        df_clientes["tipo_cliente"] == "Recorrente"
    ]["customer_unique_id"]
    .nunique()
)

percentual_recorrentes = (
    clientes_recorrentes
    /
    total_clientes
    * 100
)

valor_total_clientes = (
    df_clientes["valor_total"]
    .sum()
)

ticket_medio_clientes = (
    df_clientes["valor_total"]
    .sum()
    /
    df_clientes["qtd_pedidos"].sum()
)


print("\n")
print("=" * 60)
print("KPIs - CLIENTES")
print("=" * 60)

print(
    f"Total de clientes: "
    f"{total_clientes:,}".replace(",", ".")
)

print(
    f"Clientes recorrentes: "
    f"{clientes_recorrentes:,}".replace(",", ".")
)

print(
    f"Percentual de recorrentes: "
    f"{percentual_recorrentes:.2f}%"
)

print(
    f"Valor total comprado: "
    f"R$ {valor_total_clientes:,.2f}"
    .replace(",", "X")
    .replace(".", ",")
    .replace("X", ".")
)

print(
    f"Ticket médio: "
    f"R$ {ticket_medio_clientes:,.2f}"
    .replace(",", "X")
    .replace(".", ",")
    .replace("X", ".")
)

# ============================================================
# CLIENTES PDF
# ============================================================
# CAMINHO DO PDF
# ============================================================

caminho_pdf = (r"C:\pandas\relatorio_final\relatorio_clientes.pdf")


# ============================================================
# CONFIGURAÇÃO DO DOCUMENTO
# ============================================================

documento = SimpleDocTemplate(
    caminho_pdf,
    pagesize=landscape(A4),
    rightMargin=0.7 * cm,
    leftMargin=0.7 * cm,
    topMargin=0.6 * cm,
    bottomMargin=0.6 * cm
)


# ============================================================
# ESTILOS
# ============================================================

styles = getSampleStyleSheet()


titulo = ParagraphStyle(
    "TituloClientes",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=19,
    leading=21,
    alignment=1,
    spaceAfter=2
)


subtitulo = ParagraphStyle(
    "SubtituloClientes",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9,
    leading=11,
    alignment=1,
    spaceAfter=5
)


insight_titulo = ParagraphStyle(
    "InsightTituloClientes",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=9,
    leading=10
)


texto_insight = ParagraphStyle(
    "TextoInsightClientes",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=7.5,
    leading=8.5
)


kpi_nome = ParagraphStyle(
    "KpiNomeClientes",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=6.5,
    leading=7,
    alignment=1
)


kpi_valor = ParagraphStyle(
    "KpiValorClientes",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=12,
    alignment=1
)


# ============================================================
# FUNÇÕES DE FORMATAÇÃO
# ============================================================

def formatar_numero(valor):

    return f"{valor:,.0f}".replace(",", ".")


def formatar_moeda(valor):

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# ============================================================
# KPIs
# ============================================================

total_clientes = (
    df_clientes["customer_unique_id"]
    .nunique()
)


clientes_recorrentes = (
    df_clientes[
        df_clientes["tipo_cliente"] == "Recorrente"
    ]["customer_unique_id"]
    .nunique()
)


percentual_recorrentes = (
    clientes_recorrentes
    /
    total_clientes
    * 100
)


valor_total_clientes = (
    df_clientes["valor_total"]
    .sum()
)


ticket_medio_clientes = (
    df_clientes["valor_total"].sum()
    /
    df_clientes["qtd_pedidos"].sum()
)


# ============================================================
# LISTA DE ELEMENTOS DO PDF
# ============================================================

elementos = []


# ============================================================
# TÍTULO
# ============================================================

elementos.append(
    Paragraph(
        "CLIENTES",
        titulo
    )
)


elementos.append(
    Paragraph(
        "Quem são os clientes e qual é o perfil dos clientes recorrentes?",
        subtitulo
    )
)


# ============================================================
# KPIs
# ============================================================

kpis_clientes = [

    (
        "TOTAL DE CLIENTES",
        formatar_numero(total_clientes)
    ),

    (
        "CLIENTES RECORRENTES",
        formatar_numero(clientes_recorrentes)
    ),

    (
        "% RECORRENTES",
        f"{percentual_recorrentes:.2f}%"
    ),

    (
        "VALOR TOTAL COMPRADO",
        formatar_moeda(valor_total_clientes)
    ),

    (
        "TICKET MÉDIO",
        formatar_moeda(ticket_medio_clientes)
    )
]


cards_clientes = []


for nome, valor in kpis_clientes:

    card = Table(
        [
            [
                Paragraph(
                    nome,
                    kpi_nome
                )
            ],
            [
                Paragraph(
                    valor,
                    kpi_valor
                )
            ]
        ],
        colWidths=[5.1 * cm],
        rowHeights=[
            0.45 * cm,
            0.65 * cm
        ]
    )


    card.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    colors.grey
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    2
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    2
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    1
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    1
                )
            ]
        )
    )


    cards_clientes.append(card)


tabela_kpis = Table(
    [
        cards_clientes
    ],
    colWidths=[
        5.15 * cm,
        5.15 * cm,
        5.15 * cm,
        5.15 * cm,
        5.15 * cm
    ]
)


tabela_kpis.setStyle(
    TableStyle(
        [
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                1
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                1
            )
        ]
    )
)


elementos.append(
    tabela_kpis
)


elementos.append(
    Spacer(
        1,
        0.12 * cm
    )
)


# ============================================================
# CARREGAR OS GRÁFICOS
# ============================================================

grafico1 = Image(
    r"C:\pandas\graficos\d2_clientes_tipo.png"
)


grafico2 = Image(
    r"C:\pandas\graficos\d2_top10_clientes.png"
)


grafico3 = Image(
    r"C:\pandas\graficos\d2_recorrentes_estado.png"
)


grafico4 = Image(
    r"C:\pandas\graficos\d2_faixa_valor.png"
)


# ============================================================
# TAMANHO DOS GRÁFICOS
# ============================================================

grafico1.drawWidth = 9.8 * cm
grafico1.drawHeight = 5.1 * cm


grafico2.drawWidth = 9.8 * cm
grafico2.drawHeight = 5.1 * cm


grafico3.drawWidth = 9.8 * cm
grafico3.drawHeight = 5.1 * cm


grafico4.drawWidth = 9.8 * cm
grafico4.drawHeight = 5.1 * cm


# ============================================================
# TABELA DOS GRÁFICOS
# ============================================================

tabela_graficos = Table(
    [
        [
            grafico1,
            grafico2
        ],

        [
            grafico3,
            grafico4
        ]
    ],
    colWidths=[
        13.2 * cm,
        13.2 * cm
    ],
    rowHeights=[
        5.35 * cm,
        5.35 * cm
    ]
)


tabela_graficos.setStyle(
    TableStyle(
        [
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                0
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                0
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                0
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                0
            )
        ]
    )
)


elementos.append(
    tabela_graficos
)


elementos.append(
    Spacer(
        1,
        0.04 * cm
    )
)


# ============================================================
# PRINCIPAIS INSIGHTS
# ============================================================

elementos.append(
    Paragraph(
        "PRINCIPAIS INSIGHTS",
        insight_titulo
    )
)


insights_clientes = [

    "A base possui 93.343 clientes, sendo "
    "2.800 recorrentes, equivalentes a 3,0% do total.",

    "46,3% dos clientes realizaram compras de até R$ 100, "
    "enquanto 39,0% estão na faixa entre R$ 100 e R$ 250.",

    "Clientes com valor total comprado acima de R$ 1.000 "
    "representam 1,2% da base.",

    "Os clientes recorrentes estão concentrados principalmente "
    "em SP, RJ e MG."
]


for insight in insights_clientes:

    elementos.append(
        Paragraph(
            "• " + insight,
            texto_insight
        )
    )

    elementos.append(
        Spacer(
            1,
            0.02 * cm
        )
    )


# ============================================================
# GERAR PDF
# ============================================================

documento.build(
    elementos
)


print()
print("=" * 60)
print("PDF DO DESAFIO 2 CRIADO COM SUCESSO!")
print("=" * 60)
print()
print(caminho_pdf)