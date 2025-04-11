## Subtopic 2.5: Workflow Orchestration with Airflow

**Goal:** To understand the concepts of Directed Acyclic Graphs (DAGs) and operators in Apache Airflow, and gain hands-on experience defining, scheduling, and monitoring basic workflows using the Airflow UI and DAG files.

**Resources:**

  * Apache Airflow Official Documentation: [Airflow Concepts](https://airflow.apache.org/docs/apache-airflow/stable/concepts/index.html)
  * Airflow Tutorial: [Airflow Tutorial](https://www.google.com/search?q=https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)
  * Airflow Operators: [Operators Reference](https://www.google.com/search?q=https://airflow.apache.org/docs/apache-airflow/stable/operators/index.html) (See BashOperator, PythonOperator)
  * Airflow Setup (Docker Recommended): [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
  * Airflow GitHub: [Airflow Repository](https://github.com/apache/airflow)

-----

### Exercise 1: Set Up Airflow Environment (Docker)

**Goal:** Initialize a local Airflow environment using the official Docker Compose setup.
**Instructions:**

1.  Ensure you have Docker and Docker Compose installed on your system.
2.  Follow the Airflow documentation's guide ([Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)) to download the `docker-compose.yaml` file.
3.  Create the necessary `dags`, `logs`, and `plugins` directories as specified in the documentation.
4.  Initialize the Airflow environment using `docker compose up -d` (or the recommended initialization command).
5.  Access the Airflow Web UI in your browser (usually `http://localhost:8080`). Log in with the default credentials (often `airflow`/`airflow`).
6.  Explore the UI sections: DAGs, Browse (DAG Runs, Tasks Instances), Admin.

### Exercise 2: Define a Basic DAG Structure

**Goal:** Create a simple Python file representing an Airflow DAG with basic metadata.
**Instructions:**

1.  In your local `dags` folder (which should be mounted into the Airflow containers), create a new Python file (e.g., `my_first_dag.py`).
2.  Import necessary modules: `datetime`, `DAG`, `EmptyOperator` from `airflow`.
3.  Define default arguments for the DAG (e.g., `owner`, `start_date`, `retries`). Use a fixed `start_date` in the past (e.g., `datetime(2024, 1, 1)`).
4.  Instantiate the `DAG` object:
      * Provide a unique `dag_id` (e.g., `my_first_dag`).
      * Pass the `default_args`.
      * Set a `schedule` (e.g., `None` for manual trigger, `'@daily'`, or a cron expression).
      * Add a `description` and `catchup=False`.
5.  Define two simple tasks using `EmptyOperator` (placeholder tasks), assigning them unique `task_id`s (e.g., `start_task`, `end_task`) and linking them to your `dag` instance.
6.  Save the file. Wait a short time and check the Airflow UI DAGs list to see if your DAG appears (it might be paused initially). Unpause it if necessary.

### Exercise 3: Using BashOperator and PythonOperator

**Goal:** Implement tasks using common operators to execute bash commands and Python functions.
**Instructions:**

1.  Modify your `my_first_dag.py` file.
2.  Import `BashOperator` and `PythonOperator`.
3.  Replace one `EmptyOperator` with a `BashOperator`:
      * Give it a relevant `task_id` (e.g., `print_date`).
      * Set the `bash_command` parameter to a simple command like `"echo 'Today is $(date)'"`.
4.  Define a simple Python function (e.g., `my_python_function()`) that prints a message or performs a basic calculation.
5.  Replace the other `EmptyOperator` with a `PythonOperator`:
      * Give it a relevant `task_id` (e.g., `run_python_code`).
      * Set the `python_callable` parameter to the Python function you defined.
6.  Save the file and check for updates/errors in the Airflow UI.

### Exercise 4: Defining Task Dependencies

**Goal:** Establish the execution order between tasks within the DAG.
**Instructions:**

1.  In your `my_first_dag.py` file, use Airflow's dependency-setting syntax to define the execution order:
      * Make the `print_date` task run first.
      * Make the `run_python_code` task run after `print_date` completes successfully.
      * Common ways to set dependencies:
          * Bitshift operators: `start_task >> middle_task >> end_task`
          * `set_downstream`/`set_upstream` methods: `start_task.set_downstream(middle_task)`
2.  Save the file. View the DAG's Graph view in the Airflow UI to visually confirm the dependency arrows reflect your intended order.

### Exercise 5: Triggering and Monitoring DAG Runs

**Goal:** Manually trigger a DAG run and monitor its progress through the Airflow UI.
**Instructions:**

1.  Ensure your DAG (`my_first_dag`) is unpaused in the Airflow UI.
2.  Manually trigger a run of the DAG using the "Trigger DAG" button (play icon) in the UI.
3.  Navigate to the "Browse" -\> "DAG Runs" section and find the run you just triggered.
4.  Click on the DAG run to view its status and the status of its individual task instances.
5.  Use the "Graph", "Gantt", and "Logs" views for the DAG run to:
      * Visualize the execution flow.
      * See the duration of each task.
      * View the standard output/logs generated by your `BashOperator` and `PythonOperator` tasks.
6.  Troubleshoot any task failures by examining the logs.

### Project: Simple ETL DAG

**Goal:** Create a basic Extract-Transform-Load DAG.
**Instructions:**

1.  Define a new DAG file (e.g., `simple_etl_dag.py`).
2.  Create three tasks:
      * **Extract:** Use `BashOperator` to simulate downloading data (e.g., use `curl` to fetch data from a public API like JSONPlaceholder - `https://jsonplaceholder.typicode.com/posts/1` - and save it to a temporary file in the Airflow worker, e.g., `/tmp/data.json`).
      * **Transform:** Use `PythonOperator` to execute a Python function that reads the temporary file, performs a simple transformation (e.g., extracts only the `title` field from the JSON), and saves the result to another temporary file (e.g., `/tmp/transformed_data.txt`).
      * **Load:** Use `BashOperator` to simulate loading the data (e.g., print the content of the transformed file using `cat /tmp/transformed_data.txt` and add a message like "Data loaded\!").
3.  Set the dependencies: Extract \>\> Transform \>\> Load.
4.  Test the DAG by triggering it manually and checking the logs for each step.
    **Portfolio Guidance:**
  * Save your `simple_etl_dag.py` file.
  * Create a `README.md` explaining what the DAG does, how to set up Airflow (referencing the Docker method), and how to run the DAG.
  * Include a screenshot of the successful DAG run from the Airflow UI Graph view in your README.
  * Upload the DAG file and README to a GitHub repository.
