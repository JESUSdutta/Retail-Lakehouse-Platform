# Databricks notebook source
# MAGIC %md
# MAGIC Cell 1: Read Source Tables

# COMMAND ----------

orders_df = spark.table("retail_dev.orders_source")

customers_df = spark.table("retail_dev.customers_source")

products_df = spark.table("retail_dev.products_source")

returns_df = spark.table("retail_dev.returns_source")

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 2: Create Null Check Function

# COMMAND ----------

from pyspark.sql.functions import col, sum

def check_nulls(df, table_name):
    
    null_counts = df.select([
        sum(col(c).isNull().cast("int")).alias(c)
        for c in df.columns
    ])
    
    print(f"\nNull Check for {table_name}")
    
    display(null_counts)

# COMMAND ----------

check_nulls(orders_df, "orders")

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 3: Duplicate Check Function
# MAGIC
# MAGIC For Orders:

# COMMAND ----------

def check_duplicates(df, primary_key):
    
    duplicate_count = (
        df.groupBy(primary_key)
          .count()
          .filter("count > 1")
          .count()
    )
    
    print(
        f"Duplicate records based on {primary_key}: {duplicate_count}"
    )

# COMMAND ----------

check_duplicates(
    orders_df,
    "Order_ID"
)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 4: Business Rule Validation

# COMMAND ----------

from pyspark.sql.functions import col

# COMMAND ----------

invalid_orders = orders_df.filter(
    (col("Sales") <= 0)
    |
    (col("Quantity") <= 0)
)

# COMMAND ----------

print(
    "Invalid Orders:",
    invalid_orders.count()
)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 5: Future Date Check

# COMMAND ----------

from pyspark.sql.functions import current_date
from pyspark.sql.functions import to_date

# COMMAND ----------

orders_df = orders_df.withColumn(
    "Order_Date",
    to_date(col("Order_Date"))
)

future_date_records = orders_df.filter(
    col("Order_Date") > current_date()
)

print(
    "Future Date Records:",
    future_date_records.count()
)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 6: Validation Summary Report

# COMMAND ----------

validation_summary = [
    ("orders", orders_df.count()),
    ("invalid_orders", invalid_orders.count()),
    ("future_date_records", future_date_records.count())
]

summary_df = spark.createDataFrame(
    validation_summary,
    [
        "check_name",
        "record_count"
    ]
)

display(summary_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 7: Create Rejected Records DataFrame

# COMMAND ----------

rejected_orders_df = orders_df.filter(
    (col("Sales") <= 0)
    |
    (col("Quantity") <= 0)
)

display(rejected_orders_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Cell 8: Validation Runner

# COMMAND ----------

check_nulls(orders_df, "orders")

check_duplicates(
    orders_df,
    "Order_ID"
)

print(
    "Invalid Orders:",
    invalid_orders.count()
)

print(
    "Future Date Records:",
    future_date_records.count()
)