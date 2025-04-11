## Subtopic 2.1: Cloud Foundations: Core IaaS/PaaS Services

**Goal:** To gain hands-on experience provisioning and managing fundamental Infrastructure as a Service (IaaS) and Platform as a Service (PaaS) components on major cloud platforms (AWS and/or GCP), specifically Virtual Machines (EC2/Compute Engine), Object Storage (S3/GCS), and Identity & Access Management (IAM).

**Resources:**
* **AWS:**
    * AWS Free Tier information: [AWS Free Tier](https://aws.amazon.com/free/)
    * Amazon EC2 Documentation: [EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html)
    * Amazon S3 Documentation: [S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
    * AWS IAM Documentation: [IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
    * AWS CLI: [Command Line Interface User Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
* **GCP:**
    * GCP Free Tier information: [GCP Free Tier](https://cloud.google.com/free)
    * Google Compute Engine (GCE) Documentation: [GCE Overview](https://cloud.google.com/compute/docs/overview)
    * Google Cloud Storage (GCS) Documentation: [GCS Overview](https://cloud.google.com/storage/docs/introduction)
    * Google Cloud IAM Documentation: [Cloud IAM Overview](https://cloud.google.com/iam/docs/overview)
    * `gcloud` CLI: [gcloud CLI Overview](https://cloud.google.com/sdk/gcloud)

---

### Exercise 1: Launch and Connect to a Virtual Machine

**Goal:** Practice launching a basic Linux VM on AWS (EC2) or GCP (Compute Engine) and connecting to it via SSH.
**Instructions:**
1.  Choose either AWS or GCP for this exercise.
2.  Using the AWS Management Console or GCP Cloud Console:
    * Navigate to the EC2 / Compute Engine service.
    * Configure and launch a new virtual machine instance using a common Linux distribution (e.g., Ubuntu or Amazon Linux 2). Select a free-tier eligible instance type if possible (e.g., t2.micro on AWS, e2-micro on GCP).
    * Configure a security group (AWS) or firewall rule (GCP) to allow SSH traffic (port 22) from your IP address.
    * Create or associate an SSH key pair for connecting to the instance. Download the private key securely.
3.  Using an SSH client (like `ssh` command line, PuTTY) and the downloaded private key, connect to the public IP address of your running instance.
4.  Run a basic command (e.g., `uname -a`, `ls /`) to verify the connection.
5.  Terminate the instance after verification to avoid unnecessary charges.

### Exercise 2: Basic Object Storage Operations (S3/GCS)

**Goal:** Create an object storage bucket and perform basic file operations using the web console or CLI.
**Instructions:**
1.  Choose either AWS S3 or GCP Cloud Storage.
2.  Using the Web Console:
    * Navigate to the S3 / Cloud Storage service.
    * Create a new bucket with a globally unique name. Use default settings for region and access control initially.
    * Upload a small text file or image file from your local machine to the bucket.
    * Download the file back from the bucket to your local machine.
    * Delete the uploaded file from the bucket.
    * Delete the bucket itself.
3.  **Challenge:** Repeat steps 2c (upload) and 2d (download) using the AWS CLI (`aws s3 cp ...`) or GCP `gcloud storage cp ...` command. (Requires CLI setup).

### Exercise 3: Create an IAM User with Limited Permissions

**Goal:** Understand basic IAM concepts by creating a user with specific, restricted permissions.
**Instructions:**
1.  Choose either AWS IAM or GCP IAM.
2.  Using the IAM section of the Web Console:
    * Create a new IAM user (e.g., `limited-s3-user`).
    * Choose programmatic access (generate access key ID and secret access key) and/or console access (create a password). Securely store any generated credentials.
3.  Create a new policy or use a managed policy that grants **read-only** access to a specific S3 bucket (AWS) or specific Cloud Storage bucket (GCP). For example, allow actions like `s3:GetObject`, `s3:ListBucket` on AWS, or `storage.objects.get`, `storage.objects.list` on GCP for the target bucket.
4.  Attach this limited policy directly to the user you created (or add the user to a group with this policy).
5.  (Requires CLI setup) Configure the AWS CLI or `gcloud` CLI to use the credentials of the new `limited-s3-user`.
6.  Attempt to list objects in the target bucket using the CLI (`aws s3 ls s3://your-bucket-name` or `gcloud storage ls gs://your-bucket-name`). Verify this succeeds.
7.  Attempt to upload a file to the bucket using the CLI (`aws s3 cp file.txt s3://your-bucket-name` or `gcloud storage cp file.txt gs://your-bucket-name`). Verify this **fails** due to lack of permissions.
8.  Clean up by deleting the IAM user and associated credentials/policies if no longer needed.

### Exercise 4: Understanding Roles vs Users (Conceptual)

**Goal:** Differentiate between IAM users and IAM roles and understand when to use roles.
**Instructions:**
1.  Define what an IAM User typically represents. How are credentials managed for users?
2.  Define what an IAM Role is. How does it grant permissions without long-lived credentials? What entities can typically *assume* a role (e.g., EC2 instances, Lambda functions, other users, users from another account)?
3.  Describe a scenario where using an IAM Role assigned to an EC2 instance is more secure and manageable than embedding AWS access keys directly within an application running on that EC2 instance.
4.  Explain the concept of a "Trust Policy" (AWS) or "Trust Relationship" associated with a role. What does it define?
