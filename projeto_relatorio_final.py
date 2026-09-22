from PyPDF2 import PdfMerger
import os

# ============================================================
# CAMINHO DA PASTA
# ============================================================

pasta = r"C:\pandas\relatorio_final"


# ============================================================
# PDFS NA ORDEM DESEJADA
# ============================================================

arquivos = [
    "relatorio_vendas.pdf",
    "relatorio_clientes.pdf",
    "relatorio_satisfacao.pdf",
    "relatorio_produtos.pdf"
]


# ============================================================
# CAMINHO DO PDF FINAL
# ============================================================

arquivo_final = os.path.join(
    pasta,
    "relatorio_olist_completo.pdf"
)


# ============================================================
# CRIAR MERGE
# ============================================================

merger = PdfMerger()


# ============================================================
# ADICIONAR OS PDFs NA ORDEM
# ============================================================

for arquivo in arquivos:

    caminho = os.path.join(
        pasta,
        arquivo
    )

    if not os.path.exists(caminho):

        print(
            f"ERRO: arquivo não encontrado: {caminho}"
        )

        merger.close()
        exit()

    print(
        f"Adicionando: {arquivo}"
    )

    merger.append(caminho)


# ============================================================
# SALVAR PDF FINAL
# ============================================================

merger.write(arquivo_final)

merger.close()


# ============================================================
# FINAL
# ============================================================

print()
print("=" * 60)
print("PDF FINAL CRIADO COM SUCESSO!")
print("=" * 60)
print()
print(f"Arquivo: {arquivo_final}")