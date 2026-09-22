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


#importando CVS criados em projeto_produtos.py

categorias_produtos = pd.read_csv("categorias_produtos.csv")
categorias_produtos_volume = pd.read_csv("categorias_produtos_volume.csv")
fotos_volume = pd.read_csv("fotos_vs_volume.csv")
df_preco_volume = pd.read_csv("preco_vs_volume.csv")


# ============================================================
# GRÁFICO - TOP 10 CATEGORIAS POR RECEITA
# ============================================================

categorias_receita = (
    categorias_produtos
    .sort_values(
        "receita_total",
        ascending=False
    )
    .head(10)
    .sort_values(
        "receita_total",
        ascending=True
    )
)

fig, ax = plt.subplots(
    figsize=(9, 5)
)


# Barras

ax.barh(
    categorias_receita["product_category_name"],
    categorias_receita["receita_total"]
)

# TÍTULO

ax.set_title(
    "Top 10 Categorias por Receita",
    fontsize=16,
    pad=15
)

# EIXOS

ax.set_xlabel(
    "Receita total",
    fontsize=11
)

ax.set_ylabel(
    "Categoria",
    fontsize=11
)

# FORMATAR EIXO X EM MILHÕES

def formatar_milhoes(x, pos):

    return f"R$ {x / 1_000_000:.1f} mi"

ax.xaxis.set_major_formatter(
    FuncFormatter(formatar_milhoes)
)


# VALORES NAS BARRAS

for i, valor in enumerate(
    categorias_receita["receita_total"]
):

    valor_formatado = (
        f"R$ {valor:,.0f}"
        .replace(",", ".")
    )

    ax.text(
        valor,
        i,
        f"  {valor_formatado}",
        va="center",
        fontsize=9,
        fontweight="bold"
    )

# GRADE

ax.grid(
    axis="x",
    alpha=0.3
)

# ESPAÇO PARA OS VALORES

ax.set_xlim(
    0,
    categorias_receita["receita_total"].max() * 1.15
)


plt.tight_layout()

# Salvar

plt.savefig("C:\pandas\graficos\d4_top10_receita.png",dpi=300,bbox_inches="tight")

plt.show()

# ============================================================
# GRÁFICO 2 - TOP 10 CATEGORIAS POR VOLUME
# ============================================================

# Criar uma cópia somente com categoria e quantidade
top_volume = categorias_produtos_volume.iloc[:, [0, 1]].copy()

# Renomear as colunas
top_volume.columns = [
    "categoria",
    "qtd"
]

# Garantir que a quantidade seja numérica
top_volume["qtd"] = pd.to_numeric(
    top_volume["qtd"],
    errors="coerce"
)

# Remover possíveis valores vazios
top_volume = top_volume.dropna(
    subset=["qtd"]
)

# Selecionar os 10 maiores
top_volume = (
    top_volume
    .sort_values(
        by="qtd",
        ascending=False
    )
    .head(10)
    .sort_values(
        by="qtd",
        ascending=True
    )
)


# ============================================================
# CRIAR GRÁFICO
# ============================================================

fig, ax = plt.subplots(
    figsize=(9, 5)
)


ax.barh(
    top_volume["categoria"],
    top_volume["qtd"]
)


# ============================================================
# TÍTULO
# ============================================================

ax.set_title(
    "Top 10 Categorias por Volume de Itens",
    fontsize=16,
    pad=15
)


# ============================================================
# EIXOS
# ============================================================

ax.set_xlabel(
    "Quantidade de itens vendidos",
    fontsize=11
)

ax.set_ylabel(
    "Categoria",
    fontsize=11
)


# ============================================================
# VALORES NAS BARRAS
# ============================================================

for i, valor in enumerate(
    top_volume["qtd"]
):

    valor_formatado = (
        f"{valor:,.0f}"
        .replace(",", ".")
    )

    ax.text(
        valor,
        i,
        f"  {valor_formatado}",
        va="center",
        fontsize=9,
        fontweight="bold"
    )


# ============================================================
# GRADE
# ============================================================

ax.grid(
    axis="x",
    alpha=0.3
)


# ============================================================
# ESPAÇO PARA OS VALORES
# ============================================================

ax.set_xlim(
    0,
    top_volume["qtd"].max() * 1.15
)


# ============================================================
# AJUSTE FINAL
# ============================================================

plt.tight_layout()


# SALVAR

plt.savefig("C:\pandas\graficos\d4_top10_volume.png",dpi=300,bbox_inches="tight")

plt.show()

# ============================================================
# GRÁFICO 3 - PREÇO MÉDIO X VOLUME DE VENDAS
# ============================================================

# CONVERSÃO DOS DADOS

categoria = df_preco_volume.iloc[:, 0]

qtd = pd.to_numeric(
    df_preco_volume.iloc[:, 1],
    errors="coerce"
)

preco = pd.to_numeric(
    df_preco_volume.iloc[:, 2],
    errors="coerce"
)

# CRIAR DATAFRAME LIMPO

dados_grafico3 = pd.DataFrame({
    "categoria": categoria,
    "qtd": qtd,
    "preco": preco
})

dados_grafico3 = dados_grafico3.dropna(
    subset=["qtd", "preco"]
)

# TOP 5 CATEGORIAS POR VOLUME

top5 = (
    dados_grafico3
    .sort_values(
        "qtd",
        ascending=False
    )
    .head(5)
)

# CRIAR GRÁFICO

fig, ax = plt.subplots(
    figsize=(10, 6)
)

ax.scatter(
    dados_grafico3["preco"],
    dados_grafico3["qtd"],
    s=60,
    alpha=0.7
)

# TOP 5 CATEGORIAS POR VOLUME

top5 = (
    dados_grafico3
    .sort_values(
        "qtd",
        ascending=False
    )
    .head(5)
)

for _, linha in top5.iterrows():

    ax.annotate(
        linha["categoria"],
        (
            linha["preco"],
            linha["qtd"]
        ),
        xytext=(6, 6),
        textcoords="offset points",
        fontsize=8
    )

# TÍTULO

ax.set_title(
    "Preço Médio x Volume de Vendas por Categoria",
    fontsize=16,
    pad=15
)

# EIXOS

ax.set_xlabel(
    "Preço médio (R$)",
    fontsize=11
)

ax.set_ylabel(
    "Quantidade de itens vendidos",
    fontsize=11
)

# ESCALA LOGARÍTMICA NO PREÇO

ax.set_xscale("log")

# GRADE

ax.grid(
    alpha=0.3
)

plt.tight_layout()


plt.savefig("C:\pandas\graficos\d4_preco_vs_volume.png",dpi=300,bbox_inches="tight")

plt.show()

# ============================================================
# GRÁFICO 4 - FOTOS MÉDIAS X VOLUME DE VENDAS
# ============================================================

# PEGAR AS COLUNAS PELA POSIÇÃO

categoria = fotos_volume.iloc[:, 0]

qtd = pd.to_numeric(
    fotos_volume.iloc[:, 1],
    errors="coerce"
)

fotos = pd.to_numeric(
    fotos_volume.iloc[:, 2],
    errors="coerce"
)

# CRIAR DATAFRAME LIMPO

dados_grafico4 = pd.DataFrame({
    "categoria": categoria,
    "qtd": qtd,
    "fotos": fotos
})

dados_grafico4 = dados_grafico4.dropna(
    subset=["qtd", "fotos"]
)

# GRÁFICO

fig, ax = plt.subplots(
    figsize=(10, 6)
)

ax.scatter(
    dados_grafico4["fotos"],
    dados_grafico4["qtd"],
    s=60,
    alpha=0.7
)

# TOP 5 CATEGORIAS POR VOLUME

top5 = (
    dados_grafico4
    .sort_values(
        "qtd",
        ascending=False
    )
    .head(5)
)

for _, linha in top5.iterrows():

    ax.annotate(
        linha["categoria"],
        (
            linha["fotos"],
            linha["qtd"]
        ),
        xytext=(6, 6),
        textcoords="offset points",
        fontsize=8
    )

# TÍTULO

ax.set_title(
    "Fotos Médias x Volume de Vendas por Categoria",
    fontsize=16,
    pad=15
)

# EIXOS

ax.set_xlabel(
    "Média de fotos por produto",
    fontsize=11
)

ax.set_ylabel(
    "Quantidade de itens vendidos",
    fontsize=11
)

# GRADE

ax.grid(
    alpha=0.3
)

plt.tight_layout()

# SALVAR

plt.savefig("C:\pandas\graficos\d4_fotos_vs_volume.png",dpi=300,bbox_inches="tight")

plt.show()

# ============================================================
# GERAR PDF FINAL - RELATÓRIO DE PRODUTOS
# ============================================================

# CAMINHO DO PDF


caminho_pdf = (r"C:\pandas\relatorio_final\relatorio_produtos.pdf")

# ============================================================
# DOCUMENTO - A4 PAISAGEM
# ============================================================

documento = SimpleDocTemplate(
    caminho_pdf,
    pagesize=landscape(A4),
    rightMargin=0.7 * cm,
    leftMargin=0.7 * cm,
    topMargin=0.5 * cm,
    bottomMargin=0.5 * cm
)


# ============================================================
# ESTILOS
# ============================================================

styles = getSampleStyleSheet()

titulo = ParagraphStyle(
    "Titulo",
    parent=styles["Title"],
    fontSize=19,
    alignment=TA_CENTER,
    spaceAfter=3
)

subtitulo = ParagraphStyle(
    "Subtitulo",
    parent=styles["BodyText"],
    fontSize=9,
    alignment=TA_CENTER,
    spaceAfter=5
)


# ============================================================
# ELEMENTOS
# ============================================================

elementos = []


# ============================================================
# TÍTULO
# ============================================================

elementos.append(
    Paragraph(
        "ANÁLISE DE PRODUTOS",
        titulo
    )
)

elementos.append(
    Paragraph(
        "Categorias, volume de vendas e características dos produtos",
        subtitulo
    )
)


# ============================================================
# KPIs
# ============================================================

total_categorias = len(dados_grafico3)

total_itens = dados_grafico3["qtd"].sum()

preco_medio_geral = dados_grafico3["preco"].mean()

categoria_maior_volume = (
    dados_grafico3
    .sort_values(
        "qtd",
        ascending=False
    )
    .iloc[0]
)

categoria_maior_preco = (
    dados_grafico3
    .sort_values(
        "preco",
        ascending=False
    )
    .iloc[0]
)


def moeda(valor):

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def numero(valor):

    return (
        f"{valor:,.0f}"
        .replace(",", ".")
    )


dados_kpis = [
    [
        "CATEGORIAS",
        "ITENS VENDIDOS",
        "PREÇO MÉDIO",
        "MAIOR VOLUME"
    ],
    [
        numero(total_categorias),
        numero(total_itens),
        moeda(preco_medio_geral),
        categoria_maior_volume["categoria"]
    ]
]


tabela_kpis = Table(
    dados_kpis,
    colWidths=[
        6.8 * cm,
        6.8 * cm,
        6.8 * cm,
        7.5 * cm
    ],
    rowHeights=[
        0.55 * cm,
        0.75 * cm
    ]
)


tabela_kpis.setStyle(
    TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            colors.HexColor("#1F77B4")
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white
        ),
        (
            "FONTNAME",
            (0, 0),
            (-1, 0),
            "Helvetica-Bold"
        ),
        (
            "FONTNAME",
            (0, 1),
            (-1, 1),
            "Helvetica-Bold"
        ),
        (
            "FONTSIZE",
            (0, 0),
            (-1, -1),
            8
        ),
        (
            "ALIGN",
            (0, 0),
            (-1, -1),
            "CENTER"
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.4,
            colors.grey
        )
    ])
)

elementos.append(tabela_kpis)

elementos.append(
    Spacer(1, 0.15 * cm)
)


# ============================================================
# INFORMAÇÕES COMPLEMENTARES
# ============================================================

informacoes = Table(
    [[
        Paragraph(
            f"<b>Maior volume:</b> "
            f"{categoria_maior_volume['categoria']} "
            f"({numero(categoria_maior_volume['qtd'])} itens)",
            styles["BodyText"]
        ),
        Paragraph(
            f"<b>Maior preço médio:</b> "
            f"{categoria_maior_preco['categoria']} "
            f"({moeda(categoria_maior_preco['preco'])})",
            styles["BodyText"]
        )
    ]],
    colWidths=[
        14 * cm,
        14 * cm
    ]
)

informacoes.setStyle(
    TableStyle([
        (
            "ALIGN",
            (0, 0),
            (-1, -1),
            "CENTER"
        )
    ])
)

elementos.append(informacoes)

elementos.append(
    Spacer(1, 0.15 * cm)
)


# ============================================================
# GRÁFICOS
# ============================================================

grafico1 = Image(
    r"C:\pandas\graficos\d4_top10_receita.png",
    width=13.8 * cm,
    height=6.0 * cm
)

grafico2 = Image(
    r"C:\pandas\graficos\d4_top10_volume.png",
    width=13.8 * cm,
    height=6.0 * cm
)

grafico3 = Image(
    r"C:\pandas\graficos\d4_preco_vs_volume.png",
    width=13.8 * cm,
    height=6.0 * cm
)

grafico4 = Image(
    r"C:\pandas\graficos\d4_fotos_vs_volume.png",
    width=13.8 * cm,
    height=6.0 * cm
)


# ============================================================
# ORGANIZAR 2 x 2
# ============================================================

grade_graficos = Table(
    [
        [grafico1, grafico2],
        [grafico3, grafico4]
    ],
    colWidths=[
        14 * cm,
        14 * cm
    ],
    rowHeights=[
        6.0 * cm,
        6.0 * cm
    ]
)


grade_graficos.setStyle(
    TableStyle([
        (
            "ALIGN",
            (0, 0),
            (-1, -1),
            "CENTER"
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
    ])
)


elementos.append(grade_graficos)


# ============================================================
# GERAR PDF
# ============================================================

documento.build(elementos)

print("\n==============================================")
print("PDF DE PRODUTOS CRIADO COM SUCESSO!")
print("==============================================")
print(caminho_pdf)