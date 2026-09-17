# Databricks notebook source
# MAGIC %md
# MAGIC Cell 1: Read Silver Tables

# COMMAND ----------

orders_df = spark.table(
    "retail_catalog_proj.silver.orders_silver"
)

customers_df = spark.table(
    "retail_catalog_proj.silver.customers_silver"
)

products_df = spark.table(
    "retail_catalog_proj.silver.products_silver"
)

returns_df = spark.table(
    "retail_catalog_proj.silver.returns_silver"
)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 2: Create Sales Gold Table

# COMMAND ----------

from pyspark.sql.functions import (
    year,
    month,
    sum,
    countDistinct
)

# COMMAND ----------

sales_gold = (
    orders_df
    .groupBy(
        year("Order_Date").alias("sales_year"),
        month("Order_Date").alias("sales_month")
    )
    .agg(
        sum("Sales").alias("total_sales"),
        sum("Profit").alias("total_profit"),
        countDistinct("Order_ID").alias("total_orders")
    )
)

# COMMAND ----------

display(sales_gold)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 3: Create Customer Gold Table

# COMMAND ----------

customer_gold = (
    orders_df
    .join(
        customers_df,
        "Customer_ID",
        "left"
    )
    .groupBy(
        "Customer_ID",
        "Customer_Name",
        "Segment",
        "Region",
        "State"
    )
    .agg(
        sum("Sales").alias("customer_sales"),
        sum("Profit").alias("customer_profit")
    )
)

# COMMAND ----------

display(customer_gold)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 4: Create Product Gold Table

# COMMAND ----------

product_gold = (
    orders_df
    .join(
        products_df,
        "Product_ID",
        "left"
    )
    .groupBy(
        "Product_ID",
        "Product_Name",
        "Category"
    )
    .agg(
        sum("Sales").alias("product_sales"),
        sum("Profit").alias("product_profit")
    )
)

# COMMAND ----------

display(product_gold)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 5: Save Gold Tables

# COMMAND ----------

sales_gold.write.option("mergeSchema", "true").mode("overwrite").saveAsTable(
    "retail_catalog_proj.gold.sales_gold"
)

customer_gold.write.option("mergeSchema", "true").mode("overwrite").saveAsTable(
    "retail_catalog_proj.gold.customer_gold"
)

product_gold.write.option("mergeSchema", "true").mode("overwrite").saveAsTable(
    "retail_catalog_proj.gold.product_gold"
)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 6: Verify Tables

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN retail_catalog_proj.gold;

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 7: Create Gold Audit Table

# COMMAND ----------

from pyspark.sql.functions import current_timestamp

audit_data = [
    (
        "sales_gold",
        spark.table(
            "retail_catalog_proj.gold.sales_gold"
        ).count()
    ),
    (
        "customer_gold",
        spark.table(
            "retail_catalog_proj.gold.customer_gold"
        ).count()
    ),
    (
        "product_gold",
        spark.table(
            "retail_catalog_proj.gold.product_gold"
        ).count()
    )
]

audit_df = spark.createDataFrame(
    audit_data,
    ["table_name","record_count"]
).withColumn(
    "audit_timestamp",
    current_timestamp()
)

# COMMAND ----------

audit_df.write.mode("append").saveAsTable(
    "retail_catalog_proj.audit.gold_audit"
)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 8: Business Queries

# COMMAND ----------

# MAGIC %md
# MAGIC Top Customers

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail_catalog_proj.gold.customer_gold
# MAGIC ORDER BY customer_sales DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC Top Products

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail_catalog_proj.gold.product_gold
# MAGIC ORDER BY product_sales DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC Monthly Sales Performance

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail_catalog_proj.gold.sales_gold
# MAGIC ORDER BY sales_year, sales_month;