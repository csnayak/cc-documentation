### **What is Cloud Custodian?**  

Cloud Custodian is an **open-source governance-as-code tool** that enables organizations to efficiently manage their cloud environments. It provides a **unified DSL (Domain-Specific Language) and stateless rules engine** to help teams standardize their cloud policies while addressing key operational domains, including:  

---

### **What Can Cloud Custodian Do?**  

Cloud Custodian provides automation for managing cloud resources across AWS, Azure, and Google Cloud. Some key capabilities include:  

- **Enforcing Compliance**  
  - Ensure encryption is enabled for storage and databases.  
  - Prevent public access to S3 buckets, Azure Blob Storage, or GCP Buckets.  

- **Cost Optimization**  
  - Stop, terminate, or resize underutilized instances.  
  - Delete unattached EBS volumes or orphaned snapshots.  

- **Security Enforcement**  
  - Detect and shut down misconfigured security groups.  
  - Rotate IAM keys or delete unused IAM users.  

- **Automated Tagging & Governance**  
  - Apply required tags (e.g., `Owner`, `Environment`, `Application`).  
  - Inherit tags from parent resources (e.g., VPC → Subnet, EC2 → EBS).  

--- 

### **Key Benefits of Cloud Custodian**
1. **Multi-Cloud Support** – Works across AWS, Azure, and Google Cloud Platform (GCP).  
2. **Simple YAML-Based Policies** – Uses an easy-to-read **declarative YAML syntax** instead of complex scripting.  
3. **API & Console Interaction** – Automates cloud resource management via APIs without manual intervention.  
4. **No Need for Custom Scripting** – Eliminates the need for repetitive **boilerplate code** when managing cloud infrastructure.  
5. **Built-In Actions & Filters** – Comes with pre-defined actions like **stopping instances, enforcing encryption, and tagging resources**.  

---

### **How It Works**
- Cloud Custodian **scans cloud resources** and applies policy rules in real-time.  
- **Policies are defined in YAML** and can filter, enforce, or remediate cloud configurations.  
- It integrates **seamlessly with DevOps workflows** and **CI/CD pipelines** to automate cloud governance.  

---

### **What Are Policies in Cloud Custodian?**  

A **policy** in Cloud Custodian is a **set of rules** defined in **YAML format** that describes how cloud resources should be managed. Policies typically consist of:  

1. **Name** – A unique identifier for the policy.  
2. **Resource Type** – The cloud resource it applies to (e.g., `aws.ec2`, `gcp.storage`, `azure.vm`).  
3. **Filters** – Conditions that determine which resources the policy applies to.  
4. **Actions** – What should be done when resources match the filters (e.g., stop an instance, tag a resource).  

Example Policy to **Stop Unused EC2 Instances**:  

```yaml
policies:
  - name: stop-unused-ec2
    resource: aws.ec2
    filters:
      - State.Name: running
      - "tag:Owner": absent
    actions:
      - stop
```

This policy stops **running EC2 instances** that do **not have an "Owner" tag**.

---

### **What Are Generic Filters?**  

Filters allow Cloud Custodian to **identify and target resources** based on their attributes. Some commonly used filters include:  

1. **Tag-Based Filters**  
   - Check for missing, specific, or incorrect tags.  
   ```yaml
   filters:
     - "tag:Environment": absent
   ```
  
2. **Attribute-Based Filters**  
   - Match resources based on size, state, or configuration.  
   ```yaml
   filters:
     - InstanceType: t2.micro
   ```

3. **Age-Based Filters**  
   - Identify resources based on their creation time.  
   ```yaml
   filters:
     - type: value
       key: "LaunchTime"
       value_type: age
       op: greater-than
       value: 30
   ```
   *(Finds instances older than 30 days.)*

4. **Security-Based Filters**  
   - Detect security misconfigurations.  
   ```yaml
   filters:
     - type: security-group
       key: IpPermissions[*].IpRanges
       value: "0.0.0.0/0"
   ```
   *(Finds security groups allowing unrestricted access.)*

---



### **Different Execution Modes in Cloud Custodian**  

Cloud Custodian supports multiple **execution modes** based on how and when policies should be executed:

1. **Pull Mode (Default)**  
   - Runs policies on demand using `custodian run`.  
   - Example:  
     ```sh
     custodian run --output-dir=out policy.yml
     ```
   - Best for **ad-hoc audits** and testing.  

2. **Periodic Mode**  
   - Uses **AWS Lambda, Azure Functions, or GCP Cloud Functions** to run policies at scheduled intervals.  
   - Example:  
     ```yaml
     mode:
       type: periodic
       schedule: "rate(1 day)"
     ```
   - Ideal for **ongoing enforcement**.  

3. **Event-Driven Mode**  
   - Runs policies **when an event occurs**, like an instance launch or S3 bucket creation.  
   - Example:  
     ```yaml
     mode:
       type: cloudtrail
       events:
         - RunInstances
     ```
   - Best for **real-time enforcement**.  

4. **Embedded Mode**  
   - Executes policies **as part of another system**, useful for CI/CD pipelines.  

---

### **Few Cloud Custodian Policy Examples**  

#### **1. Auto-Delete Unused S3 Buckets**  
```yaml
policies:
  - name: delete-unused-s3
    resource: aws.s3
    filters:
      - type: metrics
        name: NumberOfObjects
        value: 0
    actions:
      - delete
```
*(Deletes S3 buckets with zero objects.)*

#### **2. Enforce Encryption on RDS Databases**  
```yaml
policies:
  - name: ensure-rds-encryption
    resource: aws.rds
    filters:
      - StorageEncrypted: false
    actions:
      - notify
```
*(Sends an alert if an unencrypted RDS database is found.)*

#### **3. Remove Publicly Accessible Security Groups**  
```yaml
policies:
  - name: remove-public-sg
    resource: aws.security-group
    filters:
      - type: ingress
        Ports: [22, 3389]
        Cidr: "0.0.0.0/0"
    actions:
      - delete
```
*(Deletes security groups that allow unrestricted SSH/RDP access.)*

---

### **Installation of Cloud Custodian (Windows & Linux)**

Cloud Custodian is a Python-based tool that runs in a virtual environment. Below are step-by-step instructions for installing it on both **Windows** and **Linux (Ubuntu 22.04)**.

---

### **1. Prerequisites**
Before installing Cloud Custodian, ensure you have the following:

- **Python 3.8+** (Check version: `python3 --version` or `python --version`)
- **Pip** (Included with Python)
- **A virtual environment** (Recommended to isolate dependencies)

---

### **2. Install Cloud Custodian on Linux (Ubuntu 22.04)**

#### **Step 1: Install Dependencies**
Update your system and install Python-related packages:
```sh
sudo apt update && sudo apt install -y python3 python3-pip python3-venv
```
Verify Python version:
```sh
python3 --version
```

#### **Step 2: Create a Virtual Environment**
To keep dependencies isolated, set up a **Python virtual environment**:
```sh
python3 -m venv custodian-env
source custodian-env/bin/activate
```

#### **Step 3: Install Cloud Custodian**
Inside the virtual environment, install Cloud Custodian:
```sh
pip install c7n
```
Verify installation:
```sh
custodian version
```

#### **Step 4: Run a Sample Policy**
Create a **test policy** (`policy.yml`) to list all running EC2 instances:
```yaml
policies:
  - name: list-ec2
    resource: aws.ec2
```
Run the policy:
```sh
custodian run --output-dir=output policy.yml
```
View the results:
```sh
cat output/list-ec2/resources.json
```

---

### **3. Install Cloud Custodian on Windows**

#### **Step 1: Install Python**
1. Download and install **Python 3.8+** from [python.org](https://www.python.org/downloads/).
2. During installation, **check the box** for **"Add Python to PATH"**.
3. Verify installation by running in **Command Prompt (cmd)**:
   ```sh
   python --version
   ```

#### **Step 2: Create a Virtual Environment**
Open **PowerShell** and run:
```sh
python -m venv custodian-env
custodian-env\Scripts\activate
```

#### **Step 3: Install Cloud Custodian**
Once the virtual environment is activated, install Cloud Custodian:
```sh
pip install c7n
```
Verify installation:
```sh
custodian version
```

#### **Step 4: Run a Sample Policy**
Create a **test policy** (`policy.yml`) in the working directory:
```yaml
policies:
  - name: list-ec2
    resource: aws.ec2
```
Run the policy:
```sh
custodian run --output-dir=output policy.yml
```
Check the results:
```sh
type output\list-ec2\resources.json
```

---

### **4. Troubleshooting & Debugging**
If you encounter issues, use these debugging techniques:

#### **Enable Debug Logging**
Run Cloud Custodian with verbose logs to troubleshoot issues:
```sh
custodian run --debug policy.yml
```

#### **Validate Policy Structure**
Ensure your policy is correctly formatted:
```sh
custodian validate policy.yml
```

#### **Manually Inspect Output**
Check `output/` directory for logs and reports:
```sh
ls -l output/  # Linux/macOS
dir output\  # Windows
```

#### **Update Cloud Custodian**
Ensure you have the latest version:
```sh
pip install --upgrade c7n
```

---

### **Essential Cloud Custodian Commands for AWS**  

Cloud Custodian provides various commands for managing, validating, and executing policies specifically for AWS resources. Below are key AWS-specific commands with usage examples.  

---

### **1. `custodian -h` (Help Command)**  
This command displays the **help menu**, listing available commands and options. It is useful for understanding command-line arguments.  

#### **Usage:**  
```sh
custodian -h
```
#### **Example Output:**
```
usage: custodian [-h] [--verbose] {run,schema,validate,report} ...
Cloud Custodian - Policy Management for AWS Infrastructure

optional arguments:
  -h, --help            Show this help message and exit
  --verbose             Enable verbose logging
Available Commands:
  run                   Execute policies
  validate              Check policy syntax
  schema                View available resources, actions, and filters
  report                Generate a summary of policy execution results
```
---

### **2. `custodian schema` (List Available AWS Resources)**  
This command lists **all AWS resources** that Cloud Custodian can manage.  

#### **Usage:**  
```sh
custodian schema
```
#### **Example Output (Truncated for AWS resources):**
```
Available AWS resources:
  aws.ec2
  aws.s3
  aws.rds
  aws.iam-user
  aws.vpc
  aws.lambda
  aws.security-group
```
*(Lists supported AWS services that Cloud Custodian can manage.)*

---

### **3. `custodian schema mode` (List AWS Execution Modes)**  
This command displays the **execution modes** available for AWS Cloud Custodian policies, such as event-driven, periodic, and pull modes.  

#### **Usage:**  
```sh
custodian schema mode
```
#### **Example Output:**
```
Available execution modes:
  pull          # Run policies on-demand
  periodic      # Run policies on a scheduled basis
  cloudtrail    # Trigger policies based on AWS CloudTrail events
  event         # AWS Lambda event-driven execution
```
*(Useful for setting up real-time compliance enforcement in AWS.)*

---

### **4. `custodian validate` (Validate AWS Policies Before Execution)**  
Before running a policy, use `validate` to check for **syntax errors** and **logical issues** in AWS policies.  

#### **Usage:**  
```sh
custodian validate aws-policy.yml
```
#### **Example Output:**
```
2024-02-21 11:15:32,501: custodian.policy:INFO Policy validated successfully: aws-policy.yml
```
*(Ensures that your AWS-specific policy is correctly structured.)*

Example: **Validate an AWS EC2 stop policy**
```yaml
policies:
  - name: stop-unused-ec2
    resource: aws.ec2
    filters:
      - State.Name: running
      - "tag:Owner": absent
    actions:
      - stop
```
Run validation:
```sh
custodian validate stop-unused-ec2.yml
```
---

### **5. `custodian run` (Execute an AWS Policy)**  
This command **executes the policy**, finds matching AWS resources, and applies defined actions.  

#### **Usage:**  
```sh
custodian run --output-dir=aws-output aws-policy.yml
```
#### **Example Output:**
```
2024-02-21 11:20:45,210: custodian.policy:INFO Running policy stop-unused-ec2
2024-02-21 11:20:47,321: custodian.policy:INFO Found 5 matching EC2 instances
2024-02-21 11:20:49,102: custodian.actions:INFO Stopping EC2 instances: i-12345, i-67890, i-abcdef
```
*(Stops unused EC2 instances based on the policy.)*

---

### **6. `custodian schema --json > schema.json` (Export AWS Schema as JSON)**  
This command **exports the AWS-specific Cloud Custodian schema** as a JSON file. Useful for integrating with **CI/CD pipelines** or **YAML validation tools**.  

#### **Usage:**  
```sh
custodian schema --json > aws-schema.json
```
#### **Example Output:**
Creates an `aws-schema.json` file containing **AWS resource types, filters, and actions**.

To check supported actions for **AWS S3**:
```sh
custodian schema aws.s3
```
Example output:
```
actions:
  - delete
  - encrypt-keys
  - notify
  - tag
  - remove-global-grants
```
---

### **7. `custodian report` (Generate AWS Policy Execution Reports)**  
This command generates a **report of resources matched by a policy**, making it easier to analyze the impact of Cloud Custodian policies.

#### **Usage:**  
```sh
custodian report --output-dir=aws-output aws-policy.yml
```
#### **Example Output:**
```
Policy: stop-unused-ec2
+---------------+----------------+----------------+----------------+
| Instance ID   | State          | Owner Tag      | Stopped By Custodian |
+---------------+----------------+----------------+----------------+
| i-12345       | running        | absent         | Yes            |
| i-67890       | running        | absent         | Yes            |
+---------------+----------------+----------------+----------------+
```
*(Displays all AWS EC2 instances that were stopped due to the policy.)*

#### **Save Report as a CSV File:**  
```sh
custodian report --output-dir=aws-output --format csv aws-policy.yml > ec2-report.csv
```
*(Exports policy execution results to a CSV file for further analysis.)*

---



