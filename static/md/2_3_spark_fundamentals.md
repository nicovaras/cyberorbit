## Subtopic 2.3: Data Processing at Scale: Spark Fundamentals

**Goal:** To understand the basics of Apache Spark's architecture and gain hands-on experience using PySpark (the Python API for Spark) to perform fundamental data manipulation tasks with DataFrames and Spark SQL.

**Resources:**
* Apache Spark Documentation: [Spark Overview](https://spark.apache.org/docs/latest/)
* PySpark Documentation: [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/index.html)
* Spark DataFrame Guide: [Spark SQL, DataFrames and Datasets Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
* Spark Architecture Overview: [Spark Cluster Overview](https://spark.apache.org/docs/latest/cluster-overview.html)
* Setup Options:
    * Local Mode: [Running Spark Locally](https://spark.apache.org/docs/latest/spark-standalone.html) (Requires Java, Spark download)
    * Cloud Notebooks: AWS SageMaker Studio, GCP Vertex AI Workbench, Databricks Community Edition often provide Spark environments.
    * Docker: [bitnami/spark Docker Image](https://hub.docker.com/r/bitnami/spark)

---

### Exercise 1: Set Up Spark Environment & Basic Interaction

**Goal:** Initialize a SparkSession and understand the roles of the Driver and Executors conceptually.
**Instructions:**
1.  Set up your Spark environment (Choose one):
    * Install Spark locally and ensure PySpark is accessible in your Python environment.
    * Use a cloud-based notebook service with Spark capabilities.
    * Run a Spark container using Docker.
2.  Start the PySpark shell (`pyspark`) or initialize a `SparkSession` in a Python script/notebook:
    ```python
    from pyspark.sql import SparkSession

    spark = SparkSession.builder \
        .appName("SparkFundamentals") \
        .getOrCreate()

    print(spark.sparkContext.appName)
    # To stop the session later (in script mode)
    # spark.stop()
    ```
3.  Define in your own words the role of the **Spark Driver** program.
4.  Define in your own words the role of **Spark Executors**.
5.  Explain conceptually how the Driver and Executors interact when processing data.

### Exercise 2: Creating DataFrames

**Goal:** Create Spark DataFrames from various sources like existing data structures or files.
**Instructions:**
1.  Using your initialized `SparkSession` (`spark`):
    * Create a DataFrame from a list of tuples or dictionaries (e.g., `data = [("Alice", 1), ("Bob", 2)]; columns = ["name", "id"]`). Use `spark.createDataFrame()`.
    * Create a small sample CSV file (e.g., `people.csv` with columns `name,age,city`).
    * Create a DataFrame by reading the CSV file using `spark.read.csv()` or `spark.read.format("csv").load()`. Make sure to infer the schema or provide it explicitly, and handle headers.
2.  Use the `.printSchema()` method to display the schema of the DataFrames you created.
3.  Use the `.show(5)` method to display the first few rows of the DataFrames.

### Exercise 3: DataFrame Transformations

**Goal:** Apply common transformations to manipulate DataFrames. Understand that transformations are lazy.
**Instructions:**
1.  Using the DataFrame created from your CSV file (or create a sample one):
    * Select specific columns using `.select()`.
    * Filter rows based on a condition using `.filter()` or `.where()` (e.g., `age > 30`).
    * Add a new column derived from existing ones using `.withColumn()` (e.g., `age_next_year = age + 1`).
    * Group data by a column and perform an aggregation (e.g., count occurrences per city) using `.groupBy().agg()`. Use functions from `pyspark.sql.functions`.
2.  Chain multiple transformations together (e.g., filter then select).
3.  Explain what **lazy evaluation** means in the context of Spark transformations. Why is it beneficial?

### Exercise 4: DataFrame Actions

**Goal:** Trigger computation on DataFrames using actions and retrieve results.
**Instructions:**
1.  Using a transformed DataFrame from Exercise 3:
    * Count the total number of rows using `.count()`.
    * Retrieve all rows into the Driver program as a list of Row objects using `.collect()`. Discuss why `.collect()` should be used cautiously on large datasets.
    * Retrieve the first `N` rows using `.take(N)`.
    * Display the first `N` rows using `.show(N)`.
    * Write the DataFrame content back to a file (e.g., Parquet or CSV format) using `df.write.format(...).save(...)`.
2.  Observe that actions (like `.count()`, `.collect()`, `.show()`, `.save()`) trigger the execution of the previously defined transformations.

### Exercise 5: Using Spark SQL

**Goal:** Register a DataFrame as a temporary view and query it using SQL syntax.
**Instructions:**
1.  Using a DataFrame you created earlier (e.g., from `people.csv`):
    * Register the DataFrame as a temporary SQL view using `df.createOrReplaceTempView("people_view")`.
2.  Use `spark.sql()` to execute SQL queries against this view:
    * Select all columns: `SELECT * FROM people_view`.
    * Filter rows: `SELECT name, age FROM people_view WHERE city = 'SomeCity'`.
    * Perform aggregations: `SELECT city, COUNT(*) as count FROM people_view GROUP BY city`.
3.  Use `.show()` on the DataFrame returned by `spark.sql()` to display the query results.
4.  Compare the syntax of performing a specific task (e.g., filtering) using the DataFrame API versus Spark SQL.

### Exercise 6: Understanding Basic Job Execution (Conceptual)

**Goal:** Conceptually understand how Spark breaks down operations into Stages and Tasks.
**Instructions:**
1.  Describe what triggers a Spark **Job**. (Hint: It relates to Actions).
2.  Explain what a **Stage** is in Spark execution. What typically causes a new stage to be created? (Hint: Shuffle operations).
3.  Define what a **Task** is. Where do tasks run?
4.  If using a Spark UI (available in local mode via `localhost:4040` usually, or provided by cloud platforms), perform a simple action (like `.count()` on a moderately sized dataset read from a file) and try to identify the corresponding Job, its Stages, and Tasks in the UI. (This might be challenging depending on the environment).
