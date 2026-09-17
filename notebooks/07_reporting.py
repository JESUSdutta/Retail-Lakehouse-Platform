# Databricks notebook source
# MAGIC %md
# MAGIC Report 1: Executive KPI Dashboard

# COMMAND ----------

# MAGIC %md
# MAGIC Total Sales

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC SUM(customer_sales) AS total_sales
# MAGIC FROM retail_catalog_proj.gold.customer_gold;

# COMMAND ----------

# MAGIC %md
# MAGIC Total Profit

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC SUM(customer_profit) AS total_profit
# MAGIC FROM retail_catalog_proj.gold.customer_gold;

# COMMAND ----------

# MAGIC %md
# MAGIC Total Customers

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC COUNT(DISTINCT Customer_ID) AS total_customers
# MAGIC FROM retail_catalog_proj.gold.customer_gold;

# COMMAND ----------

# MAGIC %md
# MAGIC Total Orders

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC SUM(total_orders) AS total_orders
# MAGIC FROM retail_catalog_proj.gold.sales_gold;

# COMMAND ----------

# MAGIC %md
# MAGIC Report 2: Top Customers

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail_catalog_proj.gold.customer_gold
# MAGIC ORDER BY customer_sales DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC Visualization: Bar Chart

# COMMAND ----------

# MAGIC %md
# MAGIC Report 3: Top Products

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail_catalog_proj.gold.product_gold
# MAGIC ORDER BY product_sales DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC Report 4: Monthly Sales Trend

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail_catalog_proj.gold.sales_gold
# MAGIC ORDER BY sales_year,sales_month;

# COMMAND ----------

# MAGIC %md
# MAGIC Report 5: Category Performance

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC Category,
# MAGIC SUM(product_sales) AS sales,
# MAGIC SUM(product_profit) AS profit
# MAGIC FROM retail_catalog_proj.gold.product_gold
# MAGIC GROUP BY Category
# MAGIC ORDER BY sales DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC Report 6: Returns Analysis

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC COUNT(*) AS returned_orders
# MAGIC FROM retail_catalog_proj.silver.returns_silver
# MAGIC WHERE Returned_Flag = 'YES';

# COMMAND ----------

# MAGIC %md
# MAGIC Report 7: Regional Analysis

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC Region,
# MAGIC SUM(customer_sales) AS sales,
# MAGIC SUM(customer_profit) AS profit
# MAGIC FROM retail_catalog_proj.gold.customer_gold
# MAGIC GROUP BY Region
# MAGIC ORDER BY sales DESC;