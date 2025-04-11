## Subtopic 2.6: Infrastructure as Code (IaC) Basics

**Goal:** To understand the principles of Infrastructure as Code and gain basic hands-on experience using Terraform or AWS CloudFormation to define, provision, and manage simple cloud resources declaratively.

**Resources:**

  * **Terraform:**
      * Terraform Introduction: [Introduction to Terraform](https://developer.hashicorp.com/terraform/intro)
      * Terraform CLI Workflow: [Core Terraform Workflow](https://developer.hashicorp.com/terraform/intro/core-workflow)
      * Terraform AWS Provider Docs: [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
      * Terraform GCP Provider Docs: [GCP Provider Documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
      * Install Terraform: [Install Terraform](https://developer.hashicorp.com/terraform/install)
  * **AWS CloudFormation:**
      * CloudFormation User Guide: [What is AWS CloudFormation?](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
      * CloudFormation Templates: [Working with AWS CloudFormation Templates](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-guide.html) (JSON/YAML)
      * CloudFormation CLI: [Using the AWS CLI with CloudFormation](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/index.html)

-----

### Exercise 1: Define Infrastructure as Code Principles

**Goal:** Articulate the core benefits and concepts behind Infrastructure as Code.
**Instructions:**

1.  Define **Infrastructure as Code (IaC)**. What is the fundamental idea?
2.  Describe at least three key benefits of using IaC compared to manually managing infrastructure through web consoles (e.g., repeatability, version control, automation, disaster recovery).
3.  Explain the difference between **Declarative** IaC (like Terraform, CloudFormation) and **Imperative** IaC (like scripting with AWS CLI/SDKs). Which approach is generally preferred for IaC tools and why?
4.  Define **Idempotency** in the context of IaC tools. Why is it an important property?

### Exercise 2: Setup IaC Tool and Authentication

**Goal:** Install Terraform or configure access for CloudFormation and ensure authentication with your chosen cloud provider (AWS or GCP).
**Instructions:**

  * **For Terraform:**
    1.  Install the Terraform CLI following the official documentation.
    2.  Configure authentication for your chosen cloud provider (AWS or GCP). Common methods include:
          * Setting environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `GOOGLE_APPLICATION_CREDENTIALS`).
          * Using shared credential files (`~/.aws/credentials`).
          * Using instance profiles/roles if running Terraform from within the cloud environment (more advanced).
    3.  Verify installation by running `terraform version`.
  * **For AWS CloudFormation:**
    1.  Ensure you have the AWS CLI installed and configured with appropriate credentials (e.g., via `aws configure`). You will use the CLI or the AWS Console to deploy templates.

### Exercise 3: Define a Simple Resource (S3/GCS Bucket)

**Goal:** Write a basic IaC configuration file to define a cloud storage bucket.
**Instructions:**

  * **For Terraform:**
    1.  Create a new directory for your Terraform project.
    2.  Create a file named `main.tf`.
    3.  Configure the required provider (e.g., `aws` or `google`) within the `main.tf` file, specifying the region.
    4.  Define an `aws_s3_bucket` or `google_storage_bucket` resource block in `main.tf`. Give the resource a logical name (e.g., `my_terraform_bucket`) and set the required arguments, such as a unique `bucket` name (for S3) or `name` (for GCS), and `location` (for GCS).
  * **For AWS CloudFormation:**
    1.  Create a new file named `s3_template.yaml` (or `.json`).
    2.  Define the basic CloudFormation template structure (`AWSTemplateFormatVersion`, `Description`, `Resources`).
    3.  Under `Resources`, define a logical ID (e.g., `MyS3Bucket`) for your bucket.
    4.  Specify the `Type` as `AWS::S3::Bucket`.
    5.  Under `Properties`, specify required properties like `BucketName` (optional, CFN can generate one) or other configurations like `AccessControl`.

### Exercise 4: Provision the Resource (Plan & Apply / Create Stack)

**Goal:** Use the IaC tool to preview and provision the defined resource in your cloud account.
**Instructions:**

  * **For Terraform:**
    1.  Open a terminal in your Terraform project directory.
    2.  Run `terraform init`. Explain what this command does (initializes backend, downloads provider plugins).
    3.  Run `terraform plan`. Analyze the output. What does it tell you will happen?
    4.  Run `terraform apply`. Confirm by typing `yes` when prompted.
    5.  Verify in the AWS/GCP console that the bucket has been created.
  * **For AWS CloudFormation:**
    1.  Use the AWS CLI or the CloudFormation section of the AWS Console.
    2.  **CLI:** Run `aws cloudformation create-stack --stack-name my-s3-stack --template-body file://s3_template.yaml`.
    3.  **Console:** Navigate to CloudFormation, click "Create stack", upload your template file, provide a stack name, and proceed through the steps.
    4.  Monitor the stack creation status in the console until it reaches `CREATE_COMPLETE`.
    5.  Verify in the S3 console that the bucket has been created.

### Exercise 5: Update the Resource Configuration

**Goal:** Modify the IaC configuration and apply the changes to the existing resource.
**Instructions:**

  * **For Terraform:**
    1.  Modify your `main.tf` file. For example, add a tag to the S3/GCS bucket resource definition.
    2.  Run `terraform plan` again. Observe the output indicating a resource modification.
    3.  Run `terraform apply` and confirm.
    4.  Verify the change (e.g., the new tag) in the AWS/GCP console.
  * **For AWS CloudFormation:**
    1.  Modify your `s3_template.yaml` file (e.g., add a `Tags` property to the bucket resource).
    2.  Use the AWS CLI or Console to update the stack.
    3.  **CLI:** Run `aws cloudformation update-stack --stack-name my-s3-stack --template-body file://s3_template.yaml`.
    4.  **Console:** Navigate to the stack, click "Update", choose "Replace current template", upload the modified template, and proceed.
    5.  Monitor the stack update status until it reaches `UPDATE_COMPLETE`.
    6.  Verify the change in the S3 console.

### Exercise 6: Destroy the Resource (Destroy / Delete Stack)

**Goal:** Use the IaC tool to cleanly remove the provisioned resources.
**Instructions:**

  * **For Terraform:**
    1.  In your Terraform project directory, run `terraform destroy`.
    2.  Review the resources that will be destroyed and confirm by typing `yes`.
    3.  Verify in the AWS/GCP console that the bucket has been deleted.
  * **For AWS CloudFormation:**
    1.  Use the AWS CLI or Console to delete the stack.
    2.  **CLI:** Run `aws cloudformation delete-stack --stack-name my-s3-stack`.
    3.  **Console:** Navigate to the stack, click "Delete".
    4.  Monitor the stack deletion status until it disappears or shows `DELETE_COMPLETE`.
    5.  Verify in the S3 console that the bucket has been deleted.