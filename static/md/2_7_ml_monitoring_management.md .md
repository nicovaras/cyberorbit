## Subtopic 2.7: Monitoring and Managing Production ML Models

**Goal:** To understand the key aspects of monitoring machine learning models in production, including different types of metrics to track (operational and ML-specific), common monitoring tools/strategies, and the concept of model drift and retraining triggers.

**Resources:**

  * MLOps Monitoring Concepts:
      * [Google Cloud: Overview of MLOps Monitoring](https://www.google.com/search?q=https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning%23monitoring)
      * [AWS Blog: Monitoring ML Models in Production](https://www.google.com/search?q=https://aws.amazon.com/blogs/machine-learning/monitoring-machine-learning-models-in-production/)
      * [WhyLogs/LangKit (Example Tools for Drift/Data Quality)](https://www.google.com/search?q=https://whylogs.ai/whylogs), [LangKit GitHub](https://github.com/whylabs/langkit)
  * Cloud Native Monitoring Tools (Conceptual):
      * [AWS CloudWatch](https://aws.amazon.com/cloudwatch/)
      * [Google Cloud Monitoring](https://cloud.google.com/monitoring)
      * [Prometheus](https://prometheus.io/) & [Grafana](https://grafana.com/)
  * Model Drift Explained: [Blog post or article explaining concept drift, data drift](https://www.google.com/search?q=https://towardsdatascience.com/model-drift-in-machine-learning-474e9f17b40e)
  * Python Logging: [Logging HOWTO](https://docs.python.org/3/howto/logging.html)

-----

### Exercise 1: Identify Key Monitoring Metrics for ML Models

**Goal:** Categorize and list important metrics for monitoring deployed ML models.
**Instructions:**

1.  Distinguish between **Operational/System Metrics** and **ML Performance Metrics**.
2.  List at least three key Operational/System Metrics relevant for an ML model serving endpoint (e.g., API endpoint deployed via SageMaker/Vertex AI). Examples: Latency (p50, p90, p99), Error Rate (e.g., 4xx, 5xx HTTP errors), Resource Utilization (CPU/Memory/GPU).
3.  List at least three key ML Performance Metrics relevant for a classification or regression model. Examples: Accuracy, Precision, Recall, F1-Score, MAE, RMSE (Note: These often require ground truth, which may be delayed).
4.  Define **Data Drift**. Give an example of how the distribution of input features might change over time.
5.  Define **Concept Drift**. Give an example of how the relationship between input features and the target variable might change.
6.  List at least two metrics specifically used to detect Data Drift (e.g., Population Stability Index (PSI), Kolmogorov-Smirnov test statistic, distribution distance measures like Wasserstein).

### Exercise 2: Implementing Basic Application Logging

**Goal:** Add structured logging to a simple Python application simulating an ML model prediction.
**Instructions:**

1.  Create a simple Python function `predict(input_data)` that simulates making a prediction (e.g., returns a random class or value based on input length).
2.  Import Python's `logging` module.
3.  Configure basic logging (e.g., `logging.basicConfig`) to output messages to the console or a file, including timestamp, log level, and message. Set the logging level to `INFO`.
4.  Add informative log statements within your `predict` function:
      * Log the received `input_data` at the `INFO` level.
      * Log the generated prediction at the `INFO` level.
      * Add a `DEBUG` level log statement for some internal step (it shouldn't appear with the current level setting).
      * Simulate an error condition (e.g., if `input_data` is invalid) and log an `ERROR` or `EXCEPTION` level message using `logging.error()` or `logging.exception()`.
5.  Call your `predict` function with valid and invalid data to see the different log outputs.

### Exercise 3: Conceptualizing a Monitoring Dashboard

**Goal:** Design the layout and key components of a dashboard for monitoring a production ML model.
**Instructions:**

1.  Imagine you have deployed a customer churn prediction model as an API endpoint.
2.  Sketch or describe the layout of a monitoring dashboard (e.g., using Grafana, CloudWatch Dashboards, or just conceptually).
3.  Specify at least 4-5 key charts or widgets you would include:
      * What operational metrics would you display (e.g., QPS, Latency p99, Error Rate %)? What chart type (e.g., Time Series Line)?
      * What data quality/drift metrics would you display for key input features (e.g., PSI for 'customer_age', distribution histogram for 'monthly_charges')?
      * How would you display model performance over time (e.g., Accuracy/F1-Score based on delayed ground truth)?
      * Would you include alerting status?
4.  Briefly explain the purpose of each chosen chart/widget.

### Exercise 4: Defining Alerting Rules

**Goal:** Define specific conditions that should trigger alerts based on monitoring metrics.
**Instructions:**

1.  Based on the metrics identified in Exercise 1 and the dashboard in Exercise 3 for the churn model:
2.  Define an alerting rule for high **API Error Rate**. Specify the metric, threshold (e.g., \> 5% over 5 minutes), and severity (e.g., Critical).
3.  Define an alerting rule for high **Prediction Latency**. Specify the metric (e.g., p99 latency), threshold (e.g., \> 500ms over 10 minutes), and severity (e.g., Warning).
4.  Define an alerting rule for significant **Data Drift** in a key feature (e.g., 'customer_age'). Specify the drift metric (e.g., PSI), threshold (e.g., \> 0.2 compared to training data baseline), and severity (e.g., Warning/Critical).
5.  Define an alerting rule for a drop in **Model Performance** (assuming delayed ground truth is available). Specify the metric (e.g., F1 Score), threshold (e.g., \< 0.7 averaged over the last 24 hours), and severity (e.g., Critical).

### Exercise 5: Designing a Retraining Strategy

**Goal:** Outline different strategies for triggering model retraining based on monitoring feedback.
**Instructions:**

1.  Describe a **Scheduled Retraining** strategy. What are its pros and cons? When might it be appropriate?
2.  Describe a **Performance-Based Retraining** strategy. What specific metrics (from Exercise 1 or 4) could trigger retraining? What are the challenges (e.g., availability of ground truth)?
3.  Describe a **Drift-Based Retraining** strategy. What specific drift metrics could trigger retraining? How does this potentially allow for earlier intervention compared to performance-based triggers?
4.  Outline the high-level steps involved in an automated retraining pipeline triggered by one of these strategies (e.g., trigger received -\> fetch new data -\> retrain model -\> evaluate model -\> potentially deploy). What role could a tool like Airflow (Subtopic 2.5) play here?

### Project: Basic Monitoring & Logging Implementation

**Goal:** Implement basic logging and metric tracking for a simulated ML model API using standard Python libraries.
**Instructions:**

1.  Create a simple web application using Flask or FastAPI that has one endpoint (e.g., `/predict`).
2.  This endpoint should accept some input data (e.g., JSON payload).
3.  Inside the endpoint handler:
      * Use the `logging` module (configured for structured logging if possible, e.g., JSON format) to log the request input and the prediction output.
      * Simulate a prediction process (no real model needed).
      * Simulate calculating prediction latency (use `time.time()`). Log the latency.
      * (Optional) Use a library like `prometheus_client` to expose a simple custom metric (e.g., a counter for prediction requests, a histogram for latency).
4.  Run the application locally.
5.  Send a few requests to the endpoint (using `curl` or Postman).
6.  Observe the structured logs generated.
7.  (Optional) If using `prometheus_client`, access the metrics endpoint (usually `/metrics`) to see the exposed metrics.
    **Portfolio Guidance:**
  * Structure your code clearly (e.g., `app.py`, `requirements.txt`).
  * Add a `README.md` explaining the purpose, how to run the application (including installing dependencies), and how to send requests.
  * Include example log output in the README.
  * If Prometheus metrics are implemented, show an example of the `/metrics` output.
  * Upload the code and README to a GitHub repository.
