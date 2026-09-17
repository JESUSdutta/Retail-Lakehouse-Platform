# Databricks notebook source
orders_data = [
    ("O1001","2025-01-01","C001","P001",2,500,80),
    ("O1002","2025-01-02","C002","P003",1,300,50),
    ("O1003","2025-01-03","C001","P002",4,1200,200),
    ("O1004","2025-01-04","C003","P001",1,250,40),
    ("O1005","2025-01-05","C004","P004",3,900,120),
    ("O1006","2025-01-06","C002","P002",2,600,90),
    ("O1007","2025-01-07","C005","P003",1,350,60),
    ("O1008","2025-01-08","C001","P004",5,1500,250),
    ("O1009","2025-01-09","C006","P001",2,500,70),
    ("O1010","2025-01-10","C003","P002",3,900,150)
]

orders_df = spark.createDataFrame(
    orders_data,
    [
        "Order_ID",
        "Order_Date",
        "Customer_ID",
        "Product_ID",
        "Quantity",
        "Sales",
        "Profit"
    ]
)

display(orders_df)

# COMMAND ----------

customers_data = [
    ("C001","Sourin Dutta","Consumer","South","Karnataka"),
    ("C002","Rahul Sharma","Corporate","West","Maharashtra"),
    ("C003","Priya Singh","Consumer","North","Delhi"),
    ("C004","Amit Kumar","Home Office","East","West Bengal"),
    ("C005","Neha Verma","Corporate","South","Telangana"),
    ("C006","Rohit Das","Consumer","East","Odisha")
]

customers_df = spark.createDataFrame(
    customers_data,
    [
        "Customer_ID",
        "Customer_Name",
        "Segment",
        "Region",
        "State"
    ]
)

display(customers_df)

# COMMAND ----------

products_data = [
    ("P001","Laptop","Technology","Computers"),
    ("P002","Office Chair","Furniture","Chairs"),
    ("P003","Printer","Technology","Printers"),
    ("P004","Standing Desk","Furniture","Tables")
]

products_df = spark.createDataFrame(
    products_data,
    [
        "Product_ID",
        "Product_Name",
        "Category",
        "Sub_Category"
    ]
)

display(products_df)

# COMMAND ----------

returns_data = [
    ("O1002","Yes"),
    ("O1008","Yes")
]

returns_df = spark.createDataFrame(
    returns_data,
    [
        "Order_ID",
        "Returned_Flag"
    ]
)

display(returns_df)

# COMMAND ----------

print("Orders:", orders_df.count())
print("Customers:", customers_df.count())
print("Products:", products_df.count())
print("Returns:", returns_df.count())

# COMMAND ----------

orders_df.printSchema()

customers_df.printSchema()

products_df.printSchema()

returns_df.printSchema()

# COMMAND ----------

orders_df.write.mode("overwrite").saveAsTable(
    "retail_catalog_proj.retail_dev.orders_source"
)

customers_df.write.mode("overwrite").saveAsTable(
    "retail_catalog_proj.retail_dev.customers_source"
)

products_df.write.mode("overwrite").saveAsTable(
    "retail_catalog_proj.retail_dev.products_source"
)

returns_df.write.mode("overwrite").saveAsTable(
    "retail_catalog_proj.retail_dev.returns_source"
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN retail_catalog_proj.retail_dev;