## Subtopic 2.2: Managed ML Platforms Introduction

**Goal:** To gain introductory hands-on experience using managed cloud ML platforms (AWS SageMaker or GCP Vertex AI) for common tasks: running training jobs, registering models, and deploying models to endpoints for inference.

**Resources:**
* **AWS SageMaker:**
    * SageMaker Developer Guide: [Amazon SageMaker Developer Guide](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
    * SageMaker Python SDK: [SageMaker Python SDK v2 Documentation](https://sagemaker.readthedocs.io/en/stable/)
    * Example Notebooks: [Amazon SageMaker Examples GitHub](https://github.com/aws/amazon-sagemaker-examples) (Explore built-in algorithm examples)
* **GCP Vertex AI:**
    * Vertex AI Documentation: [Vertex AI Documentation Overview](https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform)
    * Vertex AI Python Client Library: [Vertex AI Client Libraries](https://cloud.google.com/vertex-ai/docs/start/client-libraries)
    * Example Notebooks: [Vertex AI Samples GitHub](https://github.com/GoogleCloudPlatform/vertex-ai-samples) (Explore training and prediction examples)
* **Dataset:** [UCI ML Repository - Iris Dataset](https://archive.ics.uci.edu/ml/datasets/iris) or a similar simple classification/regression dataset.

---

### Exercise 1: Prepare and Upload Data for Training

**Goal:** Prepare a simple dataset and upload it to cloud storage (S3/GCS) in a format suitable for the chosen ML platform.
**Instructions:**
1.  Download the Iris dataset (or similar simple dataset).
2.  Perform minimal preprocessing if needed (e.g., ensure it's in CSV format, potentially split into train/validation sets locally first).
3.  Choose either AWS S3 or GCP GCS. Create a dedicated bucket for your ML project.
4.  Upload the prepared training data (e.g., `iris_train.csv`) and optionally validation data (`iris_validation.csv`) to a specific path within your bucket (e.g., `s3://your-ml-bucket/iris/data/` or `gs://your-ml-bucket/iris/data/`).
5.  Verify the upload using the web console or CLI. Note the S3 URI or GCS URI of your uploaded data.

### Exercise 2: Run a Training Job using a Built-in Algorithm

**Goal:** Launch a model training job on SageMaker or Vertex AI using a readily available algorithm provided by the platform.
**Instructions:**
1.  Choose either AWS SageMaker or GCP Vertex AI.
2.  Navigate to the platform's UI (SageMaker Studio/Console or Vertex AI Workbench/Console).
3.  Initiate a training job configuration:
    * Select a built-in algorithm suitable for your dataset (e.g., XGBoost for classification/regression on SageMaker, or AutoML Tables / Custom Training with a pre-built container on Vertex AI).
    * Configure the job: specify the algorithm source/container, input data path (using the S3/GCS URI from Exercise 1), output path for model artifacts, instance type for training (choose a small/cheap instance), and any necessary hyperparameters (use defaults or simple values).
4.  Launch the training job.
5.  Monitor the job's progress through the UI until it completes successfully. Note where the model artifacts are stored (S3/GCS path).

### Exercise 3: Register the Trained Model

**Goal:** Register the model artifacts produced by the training job into the platform's model registry.
**Instructions:**
1.  Choose the same platform (SageMaker or Vertex AI) as in Exercise 2.
2.  Navigate to the Model Registry section (e.g., "Models" under SageMaker or "Model Registry" under Vertex AI).
3.  Create a new model entry or model version:
    * Provide a name for your model.
    * Specify the location of the model artifacts (the S3/GCS output path from the completed training job in Exercise 2).
    * Specify the container image used for inference (often related to the training container, or a standard inference container provided by the platform).
4.  Complete the registration process.
5.  Verify that the model appears in the registry.

### Exercise 4: Deploy the Model to an Endpoint

**Goal:** Deploy the registered model to a real-time inference endpoint.
**Instructions:**
1.  Choose the same platform (SageMaker or Vertex AI) as in Exercise 3.
2.  Using the UI, select the registered model from Exercise 3.
3.  Initiate the deployment process to create an endpoint:
    * Configure the endpoint: specify the instance type (choose a small/cheap instance), initial instance count (e.g., 1).
    * Associate the specific model version with the endpoint configuration.
4.  Create the endpoint. This process might take several minutes.
5.  Monitor the endpoint status until it shows as "InService" (SageMaker) or "Deployed" / ready (Vertex AI). Note the endpoint name or ID.

### Exercise 5: Invoke the Endpoint for Predictions

**Goal:** Send sample data to the deployed endpoint and receive predictions.
**Instructions:**
1.  Choose the same platform (SageMaker or Vertex AI) as in Exercise 4.
2.  Prepare a sample input payload in the format expected by the model/container (e.g., a CSV string or JSON object representing one or more Iris flower measurements). Consult the documentation for the built-in algorithm you used for the expected format.
3.  Use the platform's UI testing tool, the AWS/GCP CLI, or a small script using the SageMaker/Vertex AI SDK (e.g., `boto3` for SageMaker, `google-cloud-aiplatform` for Vertex AI) to invoke the endpoint.
    * **CLI Example (SageMaker):** `aws sagemaker-runtime invoke-endpoint --endpoint-name <your-endpoint-name> --body <your-payload> --content-type <payload-format> output.json`
    * **CLI Example (Vertex AI):** `gcloud ai endpoints predict <your-endpoint-id> --region=<your-region> --json-request=payload.json` (where payload.json contains the input)
4.  Examine the output/response to see the model's prediction(s).
5.  **Cleanup:** Delete the endpoint and endpoint configuration to avoid ongoing charges. Optionally, delete the model from the registry and the training job history.
