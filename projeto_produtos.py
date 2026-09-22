import pandas as pd

#Carregando os arquivos CSV

order_items = pd.read_csv("olist_order_items_dataset.csv")

products = pd.read_csv("olist_products_dataset.csv")

print("COLUNAS - ORDER ITEMS")
print(order_items.columns)

print("\nCOLUNAS - PRODUCTS")
print(products.columns)

#criar produtos vendidos

produtos_vendidos = order_items.merge(
    products,
    on="product_id",
    how="left"
)

print("\nTOTAL DE ITENS VENDIDOS")
print(len(produtos_vendidos))

print("\nPRIMEIROS REGISTROS")
print(
    produtos_vendidos[
        [
            "order_id",
            "product_id",
            "product_category_name",
            "price",
            "freight_value",
            "product_photos_qty",
            "product_weight_g"
        ]
    ].head(10)
)

print(len(produtos_vendidos))

#agrupar por categoria

categorias = (
    produtos_vendidos
    .groupby("product_category_name")
    .agg(
        qtd_itens=("product_id", "count"),
        receita_total=("price", "sum"),
        preco_medio=("price", "mean"),
        fotos_medias=("product_photos_qty", "mean")
    )
    .reset_index()
)

#ordenar por receita

categorias = categorias.sort_values(
    "receita_total",
    ascending=False
)

print("\nTOP 10 CATEGORIAS POR RECEITA")

print(
    categorias.head(10)
)

#calcular frete e peso por categoria

categorias_frete_peso = (
    produtos_vendidos
    .groupby("product_category_name")
    .agg(
        frete_medio=("freight_value", "mean"),
        peso_medio_g=("product_weight_g", "mean"),
        comprimento_medio_cm=("product_length_cm", "mean"),
        altura_media_cm=("product_height_cm", "mean"),
        largura_media_cm=("product_width_cm", "mean")
    )
    .reset_index()
)

categorias = categorias.merge(
    categorias_frete_peso,
    on="product_category_name",
    how="left"
)

#ordenar pela receita

categorias = categorias.sort_values(
    "receita_total",
    ascending=False
)

print("\nTOP 10 CATEGORIAS POR RECEITA")

print(
    categorias.head(10)
)

categorias.to_csv("categorias_produtos.csv",index=False,encoding="utf-8-sig")

#ordenar por quantidade de itens

categorias_volume = categorias.sort_values(
    "qtd_itens",
    ascending=False
)

print("\nTOP 10 CATEGORIAS POR VOLUME DE VENDAS")

print(
    categorias_volume[
        [
            "product_category_name",
            "qtd_itens",
            "receita_total",
            "preco_medio"
        ]
    ].head(10)
)

categorias_volume.to_csv("categorias_produtos_volume.csv",index=False,encoding="utf-8-sig")

#preço médio x quantidade de vendas

preco_vs_volume = categorias[
    [
        "product_category_name",
        "qtd_itens",
        "preco_medio"
    ]
].copy()

print("\nPREÇO MÉDIO X QUANTIDADE DE VENDAS")

print(preco_vs_volume.head(10))

preco_vs_volume.to_csv("preco_vs_volume.csv",index=False,encoding="utf-8-sig")

#fotos médias x quantidade de vendas

fotos_vs_volume = categorias[
    [
        "product_category_name",
        "qtd_itens",
        "fotos_medias"
    ]
].copy()

print("\nFOTOS MÉDIAS X QUANTIDADE DE VENDAS")

print(fotos_vs_volume.head(10))

fotos_vs_volume.to_csv("fotos_vs_volume.csv",index=False,encoding="utf-8-sig")