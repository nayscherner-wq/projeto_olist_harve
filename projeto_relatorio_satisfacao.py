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

#importando CVS criados em projeto_satisfacao.py

nota_por_status = pd.read_csv("nota_por_status.csv")
pedido_avaliacao = pd.read_csv("pedido_avaliacao.csv")
recorrencia_atraso = pd.read_csv("recorrencia_por_atraso.csv")
atrasos_estado = pd.read_csv("atrasos_estado.csv")


# ============================================================
# GRÁFICO - NOTA MÉDIA POR STATUS DE ENTREGA
# ============================================================

nota_status = (
    nota_por_status
    .sort_values(
        "nota_media",
        ascending=True
    )
)

# Criar gráfico

fig, ax = plt.subplots(
    figsize=(9, 5)
)


ax.barh(
    nota_status["status_entrega"],
    nota_status["nota_media"]
)

# Título

ax.set_title(
    "Nota Média por Status de Entrega",
    fontsize=16,
    pad=15
)

# Eixos

ax.set_xlabel(
    "Nota média",
    fontsize=11
)

ax.set_ylabel(
    "Status da entrega",
    fontsize=11
)

# Limite da escala

ax.set_xlim(
    0,
    5
)

# Valores nas barras

for i, valor in enumerate(
    nota_status["nota_media"]
):

    ax.text(
        valor,
        i,
        f"  {valor:.2f}",
        va="center",
        fontsize=10,
        fontweight="bold"
    )


# Grade

ax.grid(
    axis="x",
    alpha=0.3
)

plt.tight_layout()

# Salvar

plt.savefig("C:\pandas\graficos\d3_nota_status.png",dpi=300,bbox_inches="tight")

plt.show()

# ============================================================
# GRÁFICO - PEDIDOS POR STATUS DE ENTREGA
# ============================================================

pedidos_status = (
    nota_por_status
    .sort_values(
        "qtd_pedidos",
        ascending=True
    )
)

fig, ax = plt.subplots(
    figsize=(9, 5)
)


ax.barh(
    pedidos_status["status_entrega"],
    pedidos_status["qtd_pedidos"]
)


# Título

ax.set_title(
    "Pedidos por Status de Entrega",
    fontsize=16,
    pad=15
)


# Eixos

ax.set_xlabel(
    "Quantidade de pedidos",
    fontsize=11
)

ax.set_ylabel(
    "Status da entrega",
    fontsize=11
)


# Valores nas barras

total_pedidos_status = pedidos_status["qtd_pedidos"].sum()


for i, valor in enumerate(
    pedidos_status["qtd_pedidos"]
):

    percentual = (
        valor
        /
        total_pedidos_status
        * 100
    )

    ax.text(
        valor,
        i,
        f"  {valor:,.0f}".replace(",", ".")
        + f" ({percentual:.1f}%)",
        va="center",
        fontsize=10,
        fontweight="bold"
    )

# Grade

ax.grid(
    axis="x",
    alpha=0.3
)

plt.tight_layout()

# Salvar

plt.savefig("C:\pandas\graficos\d3_pedidos_status.png", dpi=300,bbox_inches="tight")

plt.show()

# ============================================================
# GRÁFICO - RECORRÊNCIA X ATRASO
# ============================================================

recorrencia_plot = (
    recorrencia_atraso
    .copy()
)

# Criar rótulos mais claros

recorrencia_plot["situacao"] = (
    recorrencia_plot["teve_atraso"]
    .map({
        False: "Sem atraso",
        True: "Com atraso"
    })
)

# Ordenar

recorrencia_plot = (
    recorrencia_plot
    .sort_values(
        "percentual_recorrentes",
        ascending=True
    )
)

fig, ax = plt.subplots(
    figsize=(9, 5)
)

barras = ax.barh(
    recorrencia_plot["situacao"],
    recorrencia_plot["percentual_recorrentes"]
)

# Título

ax.set_title(
    "Percentual de Clientes Recorrentes por Experiência de Entrega",
    fontsize=15,
    pad=15
)

# Eixos

ax.set_xlabel(
    "Clientes recorrentes (%)",
    fontsize=11
)

ax.set_ylabel(
    "Situação da entrega",
    fontsize=11
)

# Valores nas barras

for i, valor in enumerate(
    recorrencia_plot["percentual_recorrentes"]
):

    qtd = recorrencia_plot.iloc[i]["qtd_recorrentes"]

    ax.text(
        valor,
        i,
        f"  {valor:.2f}% ({qtd:,.0f})".replace(",", "."),
        va="center",
        fontsize=10,
        fontweight="bold"
    )

# Grade

ax.grid(
    axis="x",
    alpha=0.3
)

# Limite

ax.set_xlim(
    0,
    max(
        recorrencia_plot["percentual_recorrentes"]
    ) * 1.35
)


plt.tight_layout()


# Salvar

plt.savefig("C:\pandas\graficos\d3_recorrencia_atraso.png", dpi=300,bbox_inches="tight")


plt.show()

# ============================================================
# GRÁFICO - TOP 10 ESTADOS COM MAIOR PERCENTUAL DE ATRASOS
# ============================================================

atrasos_estado_plot = (
    atrasos_estado
    .sort_values(
        "percentual_atrasados",
        ascending=False
    )
    .head(10)
    .sort_values(
        "percentual_atrasados",
        ascending=True
    )
)

fig, ax = plt.subplots(
    figsize=(9, 5)
)


ax.barh(
    atrasos_estado_plot["customer_state"],
    atrasos_estado_plot["percentual_atrasados"]
)

# Título

ax.set_title(
    "Top 10 Estados com Maior Percentual de Pedidos Atrasados",
    fontsize=15,
    pad=15
)

# Eixos

ax.set_xlabel(
    "Pedidos atrasados (%)",
    fontsize=11
)

ax.set_ylabel(
    "Estado",
    fontsize=11
)

# Valores nas barras

for i, valor in enumerate(
    atrasos_estado_plot["percentual_atrasados"]
):

    ax.text(
        valor,
        i,
        f"  {valor:.2f}%",
        va="center",
        fontsize=9,
        fontweight="bold"
    )

# Grade

ax.grid(
    axis="x",
    alpha=0.3
)

# Espaço para os valores

ax.set_xlim(
    0,
    atrasos_estado_plot["percentual_atrasados"].max() * 1.12
)

plt.tight_layout()

# Salvar

plt.savefig("C:\pandas\graficos\d3_atrasos_estado.png",dpi=300,bbox_inches="tight")

plt.show()


# ============================================================
# GERAR PDF - DESAFIO 3 - SATISFAÇÃO
# ============================================================

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)


# ============================================================
# CAMINHO DO PDF
# ============================================================

caminho_pdf = (r"C:\pandas\relatorio_final\relatorio_satisfacao.pdf")


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
    "TituloSatisfacao",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=19,
    leading=21,
    alignment=1,
    spaceAfter=2
)


subtitulo = ParagraphStyle(
    "SubtituloSatisfacao",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9,
    leading=11,
    alignment=1,
    spaceAfter=5
)


insight_titulo = ParagraphStyle(
    "InsightTituloSatisfacao",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=9,
    leading=10
)


texto_insight = ParagraphStyle(
    "TextoInsightSatisfacao",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=7.5,
    leading=8.5
)


kpi_nome = ParagraphStyle(
    "KpiNomeSatisfacao",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=6.5,
    leading=7,
    alignment=1
)


kpi_valor = ParagraphStyle(
    "KpiValorSatisfacao",
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
# KPIs - SATISFAÇÃO
# ============================================================

total_pedidos = (
    nota_por_status["qtd_pedidos"]
    .sum()
)


pedidos_atrasados = (
    nota_por_status.loc[
        nota_por_status["status_entrega"] == "Atrasado",
        "qtd_pedidos"
    ]
    .iloc[0]
)


percentual_atrasados = (
    pedidos_atrasados
    /
    total_pedidos
    * 100
)


nota_media_geral = (
    pedido_avaliacao["nota_media"]
    .mean()
)


nota_media_atrasados = (
    nota_por_status.loc[
        nota_por_status["status_entrega"] == "Atrasado",
        "nota_media"
    ]
    .iloc[0]
)


clientes_recorrentes = (
    recorrencia_atraso["qtd_recorrentes"]
    .sum()
)


total_clientes = (
    recorrencia_atraso["qtd_clientes"]
    .sum()
)


percentual_recorrentes = (
    clientes_recorrentes
    /
    total_clientes
    * 100
)


# ============================================================
# LISTA DE ELEMENTOS
# ============================================================

elementos = []


# ============================================================
# TÍTULO
# ============================================================

elementos.append(
    Paragraph(
        "SATISFAÇÃO DO CLIENTE",
        titulo
    )
)


elementos.append(
    Paragraph(
        "Como a experiência de entrega se relaciona com a satisfação e a recorrência?",
        subtitulo
    )
)


# ============================================================
# KPIs
# ============================================================

kpis_satisfacao = [

    (
        "TOTAL DE PEDIDOS",
        formatar_numero(total_pedidos)
    ),

    (
        "NOTA MÉDIA GERAL",
        f"{nota_media_geral:.2f}"
    ),

    (
        "% DE PEDIDOS ATRASADOS",
        f"{percentual_atrasados:.2f}%"
    ),

    (
        "NOTA MÉDIA — ATRASADOS",
        f"{nota_media_atrasados:.2f}"
    ),

    (
        "% DE CLIENTES RECORRENTES",
        f"{percentual_recorrentes:.2f}%"
    )
]


cards_satisfacao = []


for nome, valor in kpis_satisfacao:

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


    cards_satisfacao.append(card)


tabela_kpis = Table(
    [
        cards_satisfacao
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
    r"C:\pandas\graficos\d3_nota_status.png"
)


grafico2 = Image(
    r"C:\pandas\graficos\d3_pedidos_status.png"
)


grafico3 = Image(
    r"C:\pandas\graficos\d3_recorrencia_atraso.png"
)


grafico4 = Image(
    r"C:\pandas\graficos\d3_atrasos_estado.png"
)


# ============================================================
# TAMANHO DOS GRÁFICOS
# ============================================================

grafico1.drawWidth = 9.8 * cm
grafico1.drawHeight = 5.0 * cm


grafico2.drawWidth = 9.8 * cm
grafico2.drawHeight = 5.0 * cm


grafico3.drawWidth = 9.8 * cm
grafico3.drawHeight = 5.0 * cm


grafico4.drawWidth = 9.8 * cm
grafico4.drawHeight = 5.0 * cm


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
        5.2 * cm,
        5.2 * cm
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
        0.03 * cm
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


insights_satisfacao = [

    "Pedidos entregues com atraso apresentam nota média de "
    f"{nota_media_atrasados:.2f}, abaixo das notas observadas "
    "para pedidos adiantados e no prazo.",

    "Os pedidos classificados como adiantados representam "
    f"{(
        nota_por_status.loc[
            nota_por_status['status_entrega'] == 'Adiantado',
            'qtd_pedidos'
        ].iloc[0]
        / total_pedidos * 100
    ):.1f}% da base analisada.",

    "A proporção de clientes recorrentes foi de "
    f"{percentual_recorrentes:.2f}% na base analisada.",

    "Entre os clientes que tiveram pedidos atrasados, "
    "4,66% são recorrentes, enquanto entre aqueles sem atraso "
    "o percentual é de 2,88%."
]


for insight in insights_satisfacao:

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
print("PDF DO DESAFIO 3 CRIADO COM SUCESSO!")
print("=" * 60)
print()
print(caminho_pdf)