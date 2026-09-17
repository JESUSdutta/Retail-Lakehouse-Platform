# Databricks notebook source
# MAGIC %md
# MAGIC Cell 1: Read Source Tables

# COMMAND ----------

orders_df = spark.table("retail_catalog_proj.retail_dev.orders_source")

customers_df = spark.table("retail_catalog_proj.retail_dev.customers_source")

products_df = spark.table("retail_catalog_proj.retail_dev.products_source")

returns_df = spark.table("retail_catalog_proj.retail_dev.returns_source")

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 2: Add Metadata Columns

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

# COMMAND ----------

# MAGIC %md
# MAGIC Orders

# COMMAND ----------

orders_bronze = (
    orders_df
    .withColumn("ingestion_timestamp", current_timestamp())
    .withColumn("record_source", lit("orders_source"))
)

# COMMAND ----------

# MAGIC %md
# MAGIC Customers

# COMMAND ----------

customers_bronze = (
    customers_df
    .withColumn("ingestion_timestamp", current_timestamp())
    .withColumn("record_source", lit("customers_source"))
)

# COMMAND ----------

# MAGIC %md
# MAGIC Products

# COMMAND ----------

products_bronze = (
    products_df
    .withColumn("ingestion_timestamp", current_timestamp())
    .withColumn("record_source", lit("products_source"))
)

# COMMAND ----------

# MAGIC %md
# MAGIC Returns

# COMMAND ----------

returns_bronze = (
    returns_df
    .withColumn("ingestion_timestamp", current_timestamp())
    .withColumn("record_source", lit("returns_source"))
)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 3: Save Bronze Tables

# COMMAND ----------

orders_bronze.write.mode("overwrite").saveAsTable(
    "retail_catalog_proj.bronze.orders_bronze"
)

# COMMAND ----------

customers_bronze.write.mode("overwrite").saveAsTable(
    "retail_catalog_proj.bronze.customers_bronze"
)

# COMMAND ----------

products_bronze.write.mode("overwrite").saveAsTable(
    "retail_catalog_proj.bronze.products_bronze"
)

# COMMAND ----------

returns_bronze.write.mode("overwrite").saveAsTable(
    "retail_catalog_proj.bronze.returns_bronze"
)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 4: Verification

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN retail_catalog_proj.bronze;

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 5: Validate Bronze Data    

# COMMAND ----------

spark.table("retail_catalog_proj.bronze.orders_bronze").show()

# COMMAND ----------

spark.table("retail_catalog_proj.bronze.customers_bronze").show()

# COMMAND ----------

bronze_audit = [
    ("orders_bronze",
     spark.table("retail_catalog_proj.bronze.orders_bronze").count()),
    
    ("customers_bronze",
     spark.table("retail_catalog_proj.bronze.customers_bronze").count()),
    
    ("products_bronze",
     spark.table("retail_catalog_proj.bronze.products_bronze").count()),
    
    ("returns_bronze",
     spark.table("retail_catalog_proj.bronze.returns_bronze").count())
]

audit_df = spark.createDataFrame(
    bronze_audit,
    ["table_name", "record_count"]
)

display(audit_df)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS retail_catalog_proj.audit;

# COMMAND ----------

audit_df.write.mode("append").saveAsTable(
    "retail_catalog_proj.audit.bronze_audit"
)