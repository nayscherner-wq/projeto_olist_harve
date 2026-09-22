import pandas as pd

#Carregando os arquivos CSV

orders = pd.read_csv("olist_orders_dataset.csv")

reviews = pd.read_csv("olist_order_reviews_dataset.csv")

customers = pd.read_csv("olist_order_customer_dataset.csv")



#converter datas

orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"]
)

orders["order_estimated_delivery_date"] = pd.to_datetime(
    orders["order_estimated_delivery_date"]
)

#filtrar pedidos com entrega realizada

orders_entregues = orders[
    orders["order_delivered_customer_date"].notna()
    &
    orders["order_estimated_delivery_date"].notna()
].copy()

#calcular delta entrega

orders_entregues["data_entrega_real"] = (
    orders_entregues["order_delivered_customer_date"]
    .dt.normalize()
)

orders_entregues["data_entrega_estimada"] = (
    orders_entregues["order_estimated_delivery_date"]
    .dt.normalize()
)


orders_entregues["delta_dias"] = (
    orders_entregues["data_entrega_real"]
    -
    orders_entregues["data_entrega_estimada"]
).dt.days


#classificar entregas:

def classificar_entrega(delta):

    if delta < 0:
        return "Adiantado"

    elif delta == 0:
        return "No prazo"

    else:
        return "Atrasado"


orders_entregues["status_entrega"] = (
    orders_entregues["delta_dias"]
    .apply(classificar_entrega)
)

print(orders_entregues["status_entrega"].value_counts())


print("PERCENTUAL POR STATUS")

percentual_status = (
    orders_entregues["status_entrega"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(percentual_status)

#preparar as avaliações

reviews_pedido = (
    reviews
    .groupby("order_id")
    .agg(
        nota_media=("review_score", "mean")
    )
    .reset_index()
)

#juntar avaliacões com status_entrega

pedidos_avaliacao = orders_entregues[
    [
        "order_id",
        "customer_id",
        "status_entrega",
        "delta_dias"
    ]
].merge(
    reviews_pedido,
    on="order_id",
    how="left"
)

pedidos_avaliacao.to_csv("pedido_avaliacao.csv",index=False,encoding="utf-8-sig")

#nota média por status

nota_por_status = (
    pedidos_avaliacao
    .groupby("status_entrega")
    .agg(
        nota_media=("nota_media", "mean"),
        qtd_pedidos=("order_id", "nunique")
    )
    .reset_index()
)

print(nota_por_status)

nota_por_status.to_csv("nota_por_status.csv",index=False,encoding="utf-8-sig")

#atrasos vs recorrencia

pedidos_clientes = orders_entregues[
    [
        "order_id",
        "customer_id"
    ]
].merge(
    customers[
        [
            "customer_id",
            "customer_unique_id"
        ]
    ],
    on="customer_id",
    how="left"
)

pedidos_por_cliente = (
    pedidos_clientes
    .groupby("customer_unique_id")
    .agg(
        qtd_pedidos=("order_id", "nunique")
    )
    .reset_index()
)

pedidos_por_cliente["tipo_cliente"] = (
    pedidos_por_cliente["qtd_pedidos"]
    .apply(
        lambda x: "Recorrente"
        if x > 1
        else "Novo"
    )
)

pedidos_com_recorrencia = pedidos_avaliacao.merge(
    customers[
        [
            "customer_id",
            "customer_unique_id"
        ]
    ],
    on="customer_id",
    how="left"
).merge(
    pedidos_por_cliente[
        [
            "customer_unique_id",
            "qtd_pedidos",
            "tipo_cliente"
        ]
    ],
    on="customer_unique_id",
    how="left"
)
#identificar se os clientes com recorrencia tiveram atrasos
atraso_por_cliente = (
    orders_entregues.merge(
        customers[
            [
                "customer_id",
                "customer_unique_id"
            ]
        ],
        on="customer_id",
        how="left"
    )
    .groupby("customer_unique_id")
    .agg(
        teve_atraso=(
            "status_entrega", 
            lambda x: (x == "Atrasado").any()
        )
    )
    .reset_index()
)

#juntar atrasos com recorrencia
clientes_analise = pedidos_por_cliente.merge(
    atraso_por_cliente,
    on="customer_unique_id",
    how="left"
)

print(clientes_analise["teve_atraso"].value_counts())

#recorrencia por experiencia de entrega

recorrencia_atraso = (
    clientes_analise
    .groupby("teve_atraso")
    .agg(
        qtd_clientes=("customer_unique_id", "nunique"),
        qtd_recorrentes=(
            "tipo_cliente",
            lambda x: (x == "Recorrente").sum()
        )
    )
    .reset_index()
)

recorrencia_atraso["percentual_recorrentes"] = (
    recorrencia_atraso["qtd_recorrentes"]
    /
    recorrencia_atraso["qtd_clientes"]
    * 100
).round(2)

print("\nRECORRENCIA X ATRASO")

print(recorrencia_atraso)

recorrencia_atraso.to_csv("recorrencia_por_atraso.csv",index=False,encoding="utf-8-sig")

#percentual de pedidos atrasados por estado

pedidos_estado = orders_entregues.merge(
    customers[
        [
            "customer_id",
            "customer_state"
        ]
    ],
    on="customer_id",
    how="left"
)

atrasos_estado = (
    pedidos_estado
    .groupby("customer_state")
    .agg(
        qtd_pedidos=("order_id", "nunique"),
        qtd_atrasados=(
            "status_entrega",
            lambda x: (x == "Atrasado").sum()
        )
    )
    .reset_index()
)

atrasos_estado["percentual_atrasados"] = (
    atrasos_estado["qtd_atrasados"]
    /
    atrasos_estado["qtd_pedidos"]
    * 100
).round(2)

atrasos_estado = atrasos_estado.sort_values(
    "percentual_atrasados",
    ascending=False
)

print("\nPERCENTUAL DE PEDIDOS ATRASADOS POR ESTADO")

print(atrasos_estado)

atrasos_estado.to_csv("atrasos_estado.csv",index=False,encoding="utf-8-sig")

#percentual de pedidos atrasados por cidade

pedidos_cidade = orders_entregues.merge(
    customers[
        [
            "customer_id",
            "customer_city"
        ]
    ],
    on="customer_id",
    how="left"
)

atrasos_cidade = (
    pedidos_cidade
    .groupby("customer_city")
    .agg(
        qtd_pedidos=("order_id", "nunique"),
        qtd_atrasados=(
            "status_entrega",
            lambda x: (x == "Atrasado").sum()
        )
    )
    .reset_index()
)

atrasos_cidade["percentual_atrasados"] = (
    atrasos_cidade["qtd_atrasados"]
    /
    atrasos_cidade["qtd_pedidos"]
    * 100
).round(2)

atrasos_cidade = atrasos_cidade.sort_values(
    "percentual_atrasados",
    ascending=False
)

print("\nPERCENTUAL DE PEDIDOS ATRASADOS POR CIDADE")

print(atrasos_cidade.head(20))