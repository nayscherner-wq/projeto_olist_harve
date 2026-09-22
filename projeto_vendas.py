import pandas as pd

customers = pd.read_csv("olist_order_customer_dataset.csv")

products = pd.read_csv("olist_products_dataset.csv")

order_items = pd.read_csv("olist_order_items_dataset.csv")

payments = pd.read_csv("olist_order_payments_dataset.csv")

orders = pd.read_csv("olist_orders_dataset.csv") 


#conhecendo as tabelas


print("\nClientes")
print(customers.shape)
print(customers.columns)

print("\nProdutos")
print(products.shape)
print(products.columns)

print("\nOrdem Items")
print(order_items.shape)
print(order_items.columns)

print("\nPedidos")
print(orders.shape)
print(orders.columns)

print("\nPagamentos")
print(payments.shape)
print(payments.columns)

print(customers.head())
print(products.head())
print(order_items.head())
print(orders.head())
print(payments.head())

#corrigindo datas


orders["order_approved_at"] = pd.to_datetime(    orders["order_approved_at"])
orders["order_delivered_customer_date"] = pd.to_datetime(orders["order_delivered_customer_date"])

orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
orders["ano"] = orders["order_purchase_timestamp"].dt.year
orders["mes"] = orders["order_purchase_timestamp"].dt.month
orders["ano_mes"] = orders["order_purchase_timestamp"].dt.to_period("M")

#filtrando apenas os pedidos que foram aprovados e entregues:

orders_entregues = orders[
    orders["order_approved_at"].notna() &
    orders["order_delivered_customer_date"].notna()
].copy()

print("Pedidos antes do filtro:", len(orders))
print("Pedidos antes do filtro:", len(orders_entregues))

#quantidade de pedidos por mês: contando valores únicos nunique()
vendas_mes = (orders_entregues.groupby("ano_mes")["order_id"].nunique().reset_index())

print(vendas_mes)

#calcular o valor das vendas

vendas = orders_entregues.merge(order_items, on="order_id",how="left")

print(vendas.head())

# criar o valor das vendas

vendas["valor_total_item"] = (vendas["price"] + vendas["freight_value"])

#colocar mês e ano na tabela vendas_mes

vendas_mes = (
    vendas
    .groupby("ano_mes")
    .agg(
        qtd_pedidos=("order_id", "nunique"),
        valor_total=("valor_total_item", "sum")
    )
    .reset_index()
)

#criar ticket médio

vendas_mes["ticket_medio"] = (vendas_mes["valor_total"] /vendas_mes["qtd_pedidos"])

vendas_mes.to_csv('vendas_mes.csv',index=False,sep=';',encoding='utf-8-sig')

#analisando a região

vendas = vendas.merge(
    customers[
        [
            "customer_id",
            "customer_city",
            "customer_state"
        ]
    ],
    on="customer_id",
    how="left"
)

vendas_estado = (
    vendas
    .groupby("customer_state")
    .agg(
        qtd_pedidos=("order_id", "nunique"),
        valor_total=("valor_total_item", "sum")
    )
    .reset_index()
    .sort_values("valor_total", ascending=False)
)
print(vendas_estado)

vendas_estado.to_csv('vendas_estado.csv',index=False,sep=';',encoding='utf-8-sig')

#forma de pagamento

vendas_pagamento = (
    payments
    .groupby("payment_type")
    .agg(
        qtd_pedidos=("order_id", "nunique"),
        valor_total=("payment_value", "sum")
    )
    .reset_index()
    .sort_values("valor_total", ascending=False)
)

print(vendas_pagamento)

vendas_pagamento.to_csv('vendas_pagamento.csv',index=False,sep=';',encoding='utf-8-sig')

#calcular o tempo de entrega

orders_entregues["tempo_entrega"] = (
    orders_entregues["order_delivered_customer_date"]
    - orders_entregues["order_approved_at"]
)

orders_entregues["tempo_entrega_dias"] = (
    orders_entregues["tempo_entrega"].dt.total_seconds()
    / (24 * 60 * 60)
)

orders_entregues.to_csv('orders_entregues.csv',index=False,sep=';',encoding='utf-8-sig')

#calculos de tempo de entrega

media_entrega = round(
    orders_entregues["tempo_entrega_dias"].mean(),
    2
)

print("Tempo médio de entrega:", media_entrega, "dias")

mediana_entrega = round(
    orders_entregues["tempo_entrega_dias"].median(),
    2
)

print("Mediana do tempo de entrega:", mediana_entrega, "dias")

resumo_entrega = pd.DataFrame({
    "Métrica": [
        "Tempo médio de entrega",
        "Mediana do tempo de entrega"
    ],
    "Dias": [
        round(
            orders_entregues["tempo_entrega_dias"].mean(),
            2
        ),
        round(
            orders_entregues["tempo_entrega_dias"].median(),
            2
        )
    ]
})

print(resumo_entrega)

resumo_entrega.to_csv('resumo_entrega.csv',index=False,sep=';',encoding='utf-8-sig')

#tempo médio de entrega por estado

tempo_entrega_estado = (
    orders_entregues
    .merge(
        customers[
            [
                "customer_id",
                "customer_state"
            ]
        ],
        on="customer_id",
        how="left"
    )
    .groupby("customer_state")
    .agg(
        tempo_medio=(
            "tempo_entrega_dias",
            "mean"
        ),
        tempo_mediano=(
            "tempo_entrega_dias",
            "median"
        ),
        qtd_pedidos=(
            "order_id",
            "nunique"
        )
    )
    .reset_index()
)

print(tempo_entrega_estado)

tempo_entrega_estado.to_csv('tempo_entrega_estado.csv',index=False,sep=';',encoding='utf-8-sig')