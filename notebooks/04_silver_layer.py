# Databricks notebook source
# MAGIC %md
# MAGIC Cell 1: Read Bronze Tables

# COMMAND ----------

orders_df = spark.table(
    "retail_catalog_proj.bronze.orders_bronze"
)

customers_df = spark.table(
    "retail_catalog_proj.bronze.customers_bronze"
)

products_df = spark.table(
    "retail_catalog_proj.bronze.products_bronze"
)

returns_df = spark.table(
    "retail_catalog_proj.bronze.returns_bronze"
)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 2: Remove Duplicates

# COMMAND ----------

orders_df = orders_df.dropDuplicates(["Order_ID"])
customers_df = customers_df.dropDuplicates(["Customer_ID"])
products_df = products_df.dropDuplicates(["Product_ID"])
returns_df = returns_df.dropDuplicates(["Order_ID"])

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 3: Standardize Data

# COMMAND ----------

from pyspark.sql.functions import upper,col,to_date

# COMMAND ----------

customers_df = (
    customers_df
    .withColumn(
        "Region",
        upper(col("Region"))
    )
    .withColumn(
        "State",
        upper(col("State"))
    )
)

# COMMAND ----------

returns_df = returns_df.withColumn(
    "Returned_Flag",
    upper(col("Returned_Flag"))
)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 4: Convert Dates

# COMMAND ----------

orders_df = orders_df.withColumn(
    "Order_Date",
    to_date(col("Order_Date"))
)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 5: Business Rule Enforcement

# COMMAND ----------

orders_df = orders_df.filter(
    (col("Sales") > 0)
    &
    (col("Quantity") > 0)
)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 6: Add Data Quality Status

# COMMAND ----------

from pyspark.sql.functions import lit

# COMMAND ----------

orders_df = orders_df.withColumn(
    "dq_status",
    lit("VALID")
)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 7: Save Silver Tables

# COMMAND ----------

orders_df.write.mode("overwrite").saveAsTable(
    "retail_catalog_proj.silver.orders_silver"
)

# COMMAND ----------

customers_df.write.mode("overwrite").saveAsTable(
    "retail_catalog_proj.silver.customers_silver"
)

# COMMAND ----------

products_df.write.mode("overwrite").saveAsTable(
    "retail_catalog_proj.silver.products_silver"
)

# COMMAND ----------

returns_df.write.mode("overwrite").saveAsTable(
    "retail_catalog_proj.silver.returns_silver"
)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 8: Verify Tables

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN retail_catalog_proj.silver;

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 9: Verify Data

# COMMAND ----------

display(
    spark.table(
        "retail_catalog_proj.silver.orders_silver"
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 10: Silver Audit Report

# COMMAND ----------

silver_audit = [
    (
        "orders_silver",
        spark.table(
            "retail_catalog_proj.silver.orders_silver"
        ).count()
    ),
    (
        "customers_silver",
        spark.table(
            "retail_catalog_proj.silver.customers_silver"
        ).count()
    ),
    (
        "products_silver",
        spark.table(
            "retail_catalog_proj.silver.products_silver"
        ).count()
    ),
    (
        "returns_silver",
        spark.table(
            "retail_catalog_proj.silver.returns_silver"
        ).count()
    )
]

audit_df = spark.createDataFrame(
    silver_audit,
    ["table_name","record_count"]
)

display(audit_df)

# COMMAND ----------

audit_df.write.mode("overwrite").saveAsTable(
    "retail_catalog_proj.audit.silver_audit"
)