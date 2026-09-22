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


#importando CVS criados em projeto_vendas.py

vendas_mes = pd.read_csv("vendas_mes.csv",sep=";")
vendas_pagamento = pd.read_csv("vendas_pagamento.csv",sep=";")
vendas_estado = pd.read_csv("vendas_estado.csv",sep=";")
tempo_entrega_estado = pd.read_csv("tempo_entrega_estado.csv",sep=";")

#converter data

vendas_mes["ano_mes"] = pd.to_datetime(
    vendas_mes["ano_mes"],
    errors="coerce"
)

print("\nTIPO DA COLUNA ANO_MES:")
print(vendas_mes["ano_mes"].dtype)
#---------------------------------------------------------------------------------------
# GRÁFICO - EVOLUÇÃO DA RECEITA
# Identificar o maior valor de receita

indice_pico = vendas_mes["valor_total"].idxmax()

mes_pico = vendas_mes.loc[
    indice_pico,
    "ano_mes"
]

valor_pico = vendas_mes.loc[
    indice_pico,
    "valor_total"
]

# Criar o gráfico

fig, ax = plt.subplots(
    figsize=(11, 5.5)
)

ax.plot(
    vendas_mes["ano_mes"],
    vendas_mes["valor_total"],
    marker="o",
    linewidth=2
)

# Título

ax.set_title(
    "Evolução da Receita Mensal",
    fontsize=16,
    pad=18
)

# Eixos

ax.set_xlabel(
    "Mês",
    fontsize=11
)

ax.set_ylabel(
    "Receita",
    fontsize=11
)

# Formatação dos meses

ax.set_xticks(
    vendas_mes["ano_mes"]
)

ax.set_xticklabels(
    vendas_mes["ano_mes"].dt.strftime("%m/%Y"),
    rotation=45,
    ha="right"
)

# Formatação do eixo Y

def formatar_milhoes(valor, pos):

    if valor >= 1_000_000:
        return f"R$ {valor / 1_000_000:.1f} mi"

    elif valor >= 1_000:
        return f"R$ {valor / 1_000:.0f} mil"

    else:
        return f"R$ {valor:.0f}"

ax.yaxis.set_major_formatter(
    FuncFormatter(formatar_milhoes)
)

# Grade

ax.grid(
    axis="y",
    alpha=0.3
)

# Destacar o pico

ax.scatter(
    mes_pico,
    valor_pico,
    s=100,
    zorder=5
)

# Formatar valor do pico

valor_formatado = (
    f"R$ {valor_pico:,.0f}"
    .replace(",", "X")
    .replace(".", ",")
    .replace("X", ".")
)

# Anotação do pico

ax.annotate(
    f"Pico: {valor_formatado}",
    xy=(
        mes_pico,
        valor_pico
    ),
    xytext=(
        -35,
        -25
    ),
    textcoords="offset points",
    ha="right",
    va="center",
    fontsize=10,
    fontweight="bold",
    arrowprops=dict(
        arrowstyle="->",
        connectionstyle="arc3"
    )
)

plt.tight_layout()

plt.savefig("C:\pandas\graficos\d1_evolucao_receita.png", dpi=300,bbox_inches="tight")

plt.show()

#-------------------------------------------------------------------------------------------------
# GRÁFICO - RECEITA POR FORMA DE PAGAMENTO

# Ordenar pela receita

vendas_pagamento = vendas_pagamento.sort_values(
    "valor_total",
    ascending=True
)

# Calcular percentual da receita

receita_total_pagamento = vendas_pagamento["valor_total"].sum()

vendas_pagamento["percentual"] = (
    vendas_pagamento["valor_total"]
    /
    receita_total_pagamento
    * 100
)

# Criar o gráfico

fig, ax = plt.subplots(
    figsize=(10, 5.5)
)


ax.barh(
    vendas_pagamento["payment_type"],
    vendas_pagamento["valor_total"]
)

# Título

ax.set_title(
    "Receita por Forma de Pagamento",
    fontsize=16,
    pad=15
)

# Eixos

ax.set_xlabel(
    "Receita",
    fontsize=11
)

ax.set_ylabel(
    "Forma de pagamento",
    fontsize=11
)

# Formatação do eixo X

ax.xaxis.set_major_formatter(
    FuncFormatter(formatar_milhoes)
)

# Adicionar valores nas barras

for i, valor in enumerate(
    vendas_pagamento["valor_total"]
):

    percentual = vendas_pagamento.iloc[
        i
    ]["percentual"]

    valor_formatado = (
        f"R$ {valor:,.0f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    ax.text(
        valor,
        i,
        f"  {valor_formatado} ({percentual:.1f}%)",
        va="center",
        fontsize=9,
        fontweight="bold"
    )

# Grade

ax.grid(
    axis="x",
    alpha=0.3
)


plt.tight_layout()

plt.savefig("C:\pandas\graficos\d1_receita_pagamento.png", dpi=300,bbox_inches="tight")

plt.show()

#-------------------------------------------------------------------------------------------------
# GRÁFICO - RECEITA POR ESTADO

# Ordenar pela receita

vendas_estado = vendas_estado.sort_values(
    "valor_total",
    ascending=True
)

# Criar o gráfico

fig, ax = plt.subplots(
    figsize=(10, 8)
)

ax.barh(
    vendas_estado["customer_state"],
    vendas_estado["valor_total"]
)

# Título

ax.set_title(
    "Receita por Estado",
    fontsize=16,
    pad=15
)

# Eixos

ax.set_xlabel(
    "Receita",
    fontsize=11
)

ax.set_ylabel(
    "Estado",
    fontsize=11
)

# Formatação do eixo X

ax.xaxis.set_major_formatter(
    FuncFormatter(formatar_milhoes)
)

# Adicionar valores nas barras

for i, valor in enumerate(
    vendas_estado["valor_total"]
):

    valor_formatado = (
        f"R$ {valor:,.0f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    ax.text(
        valor,
        i,
        f"  {valor_formatado}",
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

plt.savefig("C:\pandas\graficos\d1_receita_estado.png",dpi=300,bbox_inches="tight")

plt.show()

#----------------------------------------------------------------------------------------------------
# GRÁFICO - TEMPO MÉDIO DE ENTREGA POR ESTADO

# Ordenar pelo tempo médio

tempo_entrega_estado = tempo_entrega_estado.sort_values(
    "tempo_medio",
    ascending=True
)

# Criar o gráfico

fig, ax = plt.subplots(
    figsize=(10, 8)
)

ax.barh(
    tempo_entrega_estado["customer_state"],
    tempo_entrega_estado["tempo_medio"]
)

# Título

ax.set_title(
    "Tempo Médio de Entrega por Estado",
    fontsize=16,
    pad=15
)

# Eixos

ax.set_xlabel(
    "Tempo médio (dias)",
    fontsize=11
)

ax.set_ylabel(
    "Estado",
    fontsize=11
)

# Adicionar valores nas barras

for i, valor in enumerate(
    tempo_entrega_estado["tempo_medio"]
):

    ax.text(
        valor,
        i,
        f"  {valor:.1f} dias",
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

plt.savefig("C:\pandas\graficos\d1_tempo_entrega_estado.png",dpi=300,bbox_inches="tight")

plt.show()

# ============================================================
# KPIs - Vendas
# ============================================================

# Receita total

receita_total = vendas_mes["valor_total"].sum()


# Quantidade total de pedidos

pedidos_total = vendas_mes["qtd_pedidos"].sum()

# Ticket médio

ticket_medio = (receita_total/pedidos_total)


# Ler resumo da entrega

resumo_entrega = pd.read_csv("resumo_entrega.csv",sep=";")

tempo_medio = resumo_entrega.loc[
    resumo_entrega["Métrica"] == "Tempo médio de entrega",
    "Dias"
].iloc[0]


tempo_mediano = resumo_entrega.loc[
    resumo_entrega["Métrica"] == "Mediana do tempo de entrega",
    "Dias"
].iloc[0]


# Identificar o mês de maior receita

indice_pico = vendas_mes["valor_total"].idxmax()

mes_pico = vendas_mes.loc[
    indice_pico,
    "ano_mes"
]

valor_pico = vendas_mes.loc[
    indice_pico,
    "valor_total"
]


print("\n")
print("=" * 60)
print("KPIs - VENDAS")
print("=" * 60)

print(
    f"Receita total: R$ {receita_total:,.2f}"
)

print(
    f"Total de pedidos: {pedidos_total:,.0f}"
)

print(
    f"Ticket médio: R$ {ticket_medio:,.2f}"
)

print(
    f"Tempo médio de entrega: {tempo_medio:.2f} dias"
)

print(
    f"Mediana do tempo de entrega: {tempo_mediano:.2f} dias"
)

print(
    f"Pico de receita: {mes_pico.strftime('%m/%Y')}"
)

print(
    f"Valor do pico: R$ {valor_pico:,.2f}"
)

# ============================================================
# CRIAR PDF - VENDAS
# ============================================================

caminho_pdf = (r"C:\pandas\relatorio_final\relatorio_vendas.pdf")

# Configuração do documento

documento = SimpleDocTemplate(
    caminho_pdf,
    pagesize=landscape(A4),
    rightMargin=1 * cm,
    leftMargin=1 * cm,
    topMargin=1 * cm,
    bottomMargin=1 * cm
)

# Estilos

styles = getSampleStyleSheet()

titulo = ParagraphStyle(
    "Titulo",
    parent=styles["Title"],
    fontSize=22,
    leading=26,
    alignment=TA_LEFT,
    spaceAfter=10
)

subtitulo = ParagraphStyle(
    "Subtitulo",
    parent=styles["Normal"],
    fontSize=11,
    leading=14,
    alignment=TA_LEFT,
    spaceAfter=10
)

texto = ParagraphStyle(
    "Texto",
    parent=styles["Normal"],
    fontSize=9,
    leading=12
)


# Conteúdo do PDF

elementos = []


# ============================================================
# TÍTULO
# ============================================================

elementos.append(
    Paragraph(
        "KPI - VENDAS",
        titulo
    )
)


elementos.append(
    Paragraph(
        "Como evoluíram as vendas e quais fatores se destacam "
        "no desempenho comercial e logístico?",
        subtitulo
    )
)


# ============================================================
# KPIs
# ============================================================

def formatar_reais(valor):

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


kpis = [
    [
        Paragraph(
            "<b>RECEITA TOTAL</b><br/>"
            + formatar_reais(receita_total),
            texto
        ),

        Paragraph(
            "<b>TOTAL DE PEDIDOS</b><br/>"
            + f"{pedidos_total:,.0f}".replace(",", "."),
            texto
        ),

        Paragraph(
            "<b>TICKET MÉDIO</b><br/>"
            + formatar_reais(ticket_medio),
            texto
        ),

        Paragraph(
            "<b>TEMPO MÉDIO</b><br/>"
            + f"{tempo_medio:.2f} dias",
            texto
        ),

        Paragraph(
            "<b>MEDIANA</b><br/>"
            + f"{tempo_mediano:.2f} dias",
            texto
        )
    ]
]


tabela_kpis = Table(
    kpis,
    colWidths=[
        5.1 * cm,
        5.1 * cm,
        5.1 * cm,
        5.1 * cm,
        5.1 * cm
    ]
)


tabela_kpis.setStyle(
    TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, -1),
            colors.whitesmoke
        ),
        (
            "BOX",
            (0, 0),
            (-1, -1),
            0.5,
            colors.lightgrey
        ),
        (
            "INNERGRID",
            (0, 0),
            (-1, -1),
            0.5,
            colors.lightgrey
        ),
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
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            8
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            8
        )
    ])
)


elementos.append(tabela_kpis)

elementos.append(
    Spacer(1, 0.3 * cm)
)


# ============================================================
# GRÁFICOS
# ============================================================

grafico1 = Image("C:\pandas\graficos\d1_evolucao_receita.png")

grafico2 = Image("C:\pandas\graficos\d1_receita_pagamento.png")

grafico3 = Image("C:\pandas\graficos\d1_receita_estado.png")

grafico4 = Image("C:\pandas\graficos\d1_tempo_entrega_estado.png")


# Tamanho dos gráficos

grafico1.drawHeight = 5.3 * cm
grafico1.drawWidth = 9.8 * cm

grafico2.drawHeight = 5.3 * cm
grafico2.drawWidth = 9.8 * cm

grafico3.drawHeight = 5.3 * cm
grafico3.drawWidth = 9.8 * cm

grafico4.drawHeight = 5.3 * cm
grafico4.drawWidth = 9.8 * cm


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
        5.7 * cm,
        5.7 * cm
    ]
)


tabela_graficos.setStyle(
    TableStyle([
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
            2
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            2
        )
    ])
)


elementos.append(tabela_graficos)

# ============================================================
# PRINCIPAIS INSIGHTS
# ============================================================

elementos.append(
    Spacer(1, 0.05 * cm)
)

elementos.append(
    Paragraph(
        "<b>PRINCIPAIS INSIGHTS</b>",
        ParagraphStyle(
            "InsightTitulo",
            parent=styles["Normal"],
            fontSize=10,
            leading=12
        )
    )
)

insights = [
    "A receita apresentou crescimento ao longo do período analisado, "
    "atingindo o pico de R$ 1.153.229,37 em 11/2017.",

    "O cartão de crédito concentrou a maior parcela da receita, "
    "representando 78,3% do valor analisado.",

    "O tempo médio de entrega foi de 12,13 dias, enquanto a mediana "
    "foi de 9,85 dias, indicando diferença entre as duas medidas.",

    "Há diferenças relevantes no tempo médio de entrega entre os estados, "
    "com valores que variam de acordo com a região."
]

for insight in insights:

    elementos.append(
        Paragraph(
            "• " + insight,
            texto
        )
    )

    elementos.append(
        Spacer(1, 0.08 * cm)
    )

# ============================================================
# GERAR PDF
# ============================================================

documento.build(elementos)


print("\nPDF criado com sucesso!")
print(caminho_pdf)