import pymysql
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text

#acessando o banco de dados

#credenciais = {"hostname":"database-1.c1ee0sccomfv.sa-east-1.rds.amazonaws.com",
#"username":"admin",
#"password":"T9#mX4!qZp",
#"port":3306,
#"database":"modulosql"}

#CONN_STR= "mysql+pymysql://{}:{}@{}:{}/{}".format(
#    credenciais["username"], quote_plus(credenciais["password"]),
#    credenciais["hostname"], credenciais["port"],
#    credenciais["database"])

#print(CONN_STR)

#conn_obj = create_engine(CONN_STR).connect()

#selecionando as tabelas
#query = text("SELECT * FROM olist_geolocation_dataset")
#query1 = text("SELECT * FROM olist_order_customer_dataset")
#query2 = text("SELECT * FROM olist_products_dataset")
#query3 = text("SELECT * FROM olist_order_items_dataset")
#query4 = text("SELECT * FROM olist_order_payments_dataset")
#query5 = text("SELECT * FROM olist_order_reviews_dataset")
#query6 = text("SELECT * FROM olist_orders_dataset")
#query7 = text("SELECT * FROM olist_sellers_dataset")

#criando os dataframes
#df = pd.read_sql(query,conn_obj)
#df1 = pd.read_sql(query1,conn_obj)
#df2= pd.read_sql(query2,conn_obj)
#df3 = pd.read_sql(query3,conn_obj)
#df4 = pd.read_sql(query4,conn_obj)
#df5 = pd.read_sql(query5,conn_obj)
#df6 = pd.read_sql(query6,conn_obj)
#df7 = pd.read_sql(query7,conn_obj)

#conn_obj.close()

#criando os csvs
#comentado pois os dfs já foram convergidos para csv

#df.to_csv("olist_geolocation_dataset.csv", index = False) 
#df1.to_csv("olist_order_customer_dataset.csv", index = False) 
#df2.to_csv("olist_products_dataset.csv", index = False) 
#df3.to_csv("olist_order_items_dataset.csv", index = False) 
#df4.to_csv("olist_order_payments_dataset.csv", index = False) 
#df5.to_csv("olist_order_reviews_dataset.csv", index = False)
#df6.to_csv("olist_orders_dataset.csv", index = False)
#df7.to_csv("olist_sellers_dataset.csv", index = False)

geo_location = pd.read_csv("olist_geolocation_dataset.csv")

customers = pd.read_csv("olist_order_customer_dataset.csv")

products = pd.read_csv("olist_products_dataset.csv")

order_items = pd.read_csv("olist_order_items_dataset.csv")

payments = pd.read_csv("olist_order_payments_dataset.csv")

reviews = pd.read_csv("olist_order_reviews_dataset.csv")

orders = pd.read_csv("olist_orders_dataset.csv") 

sellers = pd.read_csv("olist_sellers_dataset.csv") 

#conhecendo as tabelas

print("\nGeo Localização")
print(geo_location.shape)
print(geo_location.columns)

print("\nClientes")
print(customers.shape)
print(customers.columns)

print("\nProdutos")
print(products.shape)
print(products.columns)

print("\nOrdem Items")
print(order_items.shape)
print(order_items.columns)

print("\nAvaliações")
print(reviews.shape)
print(reviews.columns)

print("\nPedidos")
print(orders.shape)
print(orders.columns)

print("\nVendedores")
print(sellers.shape)
print(sellers.columns)