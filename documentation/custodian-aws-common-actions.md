# 📌 Cloud Custodian AWS Common Actions  

## 🔹 **Auto-Tag User: Automate Ownership Tracking**  

### ✨ **What is Auto-Tag User?**  
The `auto-tag-user` action in Cloud Custodian **automatically assigns a tag** to newly created or modified resources based on the identity of the user who initiated the action. This helps in:  

✅ **Tracking ownership** of cloud resources.  
✅ **Ensuring compliance** by enforcing mandatory tags.  
✅ **Improving security** by linking resources to their creators.  

---

## 🔍 **How It Works**  
1️⃣ **Monitors AWS CloudTrail events** for resource creation/modification.  
2️⃣ **Checks if the specified tag exists** on the resource.  
3️⃣ **If missing, Cloud Custodian adds the tag** with the user’s IAM identity.  

---

## 📝 **Example: Auto-Tagging EC2 Instances**  
The following policy **automatically assigns an `OwnerContact` tag** to EC2 instances when they are launched, using the IAM identity of the user who triggered the action.  

```yaml
policies:
  - name: ec2-auto-tag-ownercontact
    resource: ec2
    description: |
      Automatically tags new EC2 instances with the OwnerContact tag,
      using the identity of the user who launched the instance.
    mode:
      type: cloudtrail
      role: arn:aws:iam::123456789000:role/custodian-auto-tagger
      events:
        - RunInstances
    filters:
      - tag:OwnerContact: absent
    actions:
      - type: auto-tag-user
        tag: OwnerContact
```

🔹 **What Happens?**  
📌 Whenever an EC2 instance is created, this policy **checks for the `OwnerContact` tag**.  
📌 If the tag is **missing**, Cloud Custodian automatically **adds the IAM user ID** of the instance creator.  

---

## 🎯 **Why Use Auto-Tagging?**  
✅ **Improved Visibility:** Instantly see who created a resource.  
✅ **Stronger Governance:** Enforce tagging policies with no manual effort.  
✅ **Better Cost Allocation:** Track cloud expenses by team or user.  
✅ **Security & Compliance:** Detect unauthorized resource creation in real-time.  

---

## ⚠ **Key Considerations**  
⚠ **Tagging Delays:** Some AWS services do not support immediate tagging, causing short delays (seconds to minutes, worst-case hours).  
⚠ **Race Conditions:** If another automation modifies the resource before tagging completes, the tag may be lost.  
⚠ **CloudTrail Dependency:** This action relies on AWS CloudTrail logs, which may not always capture precise IAM identities in certain automated operations.  

---

## 🛠 **Supported Auto-Tag User Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `tag`          | `string`   | The tag key to apply (e.g., `OwnerContact`). **(Required)** |
| `type`         | `enum`     | Must be `auto-tag-user`. **(Required)** |
| `update`       | `boolean`  | If `true`, updates the tag if it already exists. |
| `user-type`    | `array`    | Specifies user types to track (`IAMUser`, `AssumedRole`, `FederatedUser`). |
| `value`        | `enum`     | Determines the identity attribute to use (`userName`, `arn`, `sourceIPAddress`, `principalId`). |

---

## ✅ **Best Practices for Auto-Tagging**  
💡 **Apply Auto-Tagging to Critical Resources:** Use it for EC2, RDS, S3, IAM roles, Lambda functions, and networking components.  
💡 **Combine with Compliance Policies:** Use tagging data to enforce security and cost policies automatically.  
💡 **Regularly Audit Tags:** Set up a Cloud Custodian policy to periodically check and correct missing or inaccurate tags.  

---

## 🔹 **Copy-Related-Tag: Propagate Tags Automatically**  

### ✨ **What is Copy-Related-Tag?**  
The `copy-related-tag` action in Cloud Custodian **automatically copies tags from a related resource** to its associated resource. This is useful when tags applied to a parent resource need to be inherited by dependent or child resources.  

**Common Use Cases:**  
✅ **Copy EBS Volume tags** to their snapshots.  
✅ **Inherit VPC tags** to Subnets.  
✅ **Propagate tags from EC2 instances** to EBS volumes.  

---

## 🔍 **How It Works**  
1️⃣ **Identify the resource that has the tags** you want to copy.  
2️⃣ **Determine the key attribute** that links the child resource to the parent.  
3️⃣ **Define the tag keys to copy** (or use `"*"` to copy all tags).  
4️⃣ **Apply copied tags** to the associated resource automatically.  

---

## 📝 **Example: Copy Tags from EBS Volume to Snapshot**  
This policy ensures that **all tags from an EBS Volume are copied to its snapshots**.  

```yaml
policies:
  - name: copy-tags-from-ebs-volume-to-snapshot
    resource: ebs-snapshot
    actions:
      - type: copy-related-tag
        resource: ebs
        skip_missing: True
        key: VolumeId
        tags: '*'
```

🔹 **What Happens?**  
📌 Whenever an **EBS snapshot is created**, this policy **copies all tags from its parent EBS Volume**.  
📌 If a related volume **does not exist**, it **skips the operation** instead of raising an error (`skip_missing: True`).  

---

## 📝 **Example: Copy Tags from an Unsupported Resource**  
If Cloud Custodian **does not natively support a resource type**, you can use the AWS **Resource Groups Tagging API** to fetch tags using an **ARN-based reference**.  

```yaml
policies:
  - name: copy-tags-from-unsupported-resource
    resource: ebs-snapshot
    actions:
      - type: copy-related-tag
        resource: resourcegroupstaggingapi
        key: tag:a-resource-tag
        tags: '*'
```

🔹 **What Happens?**  
📌 This policy **retrieves tags from an ARN-based resource** and applies them to the EBS snapshot.  
📌 It is useful for **copying tags from resources not directly supported by Cloud Custodian**.  

---

## 🎯 **Why Use Copy-Related-Tag?**  
✅ **Automates Tag Consistency:** Ensures all related resources inherit relevant tags.  
✅ **Reduces Manual Effort:** No need to manually copy or apply tags.  
✅ **Improves Cost Tracking:** Helps organizations track spending by propagating tags across resources.  
✅ **Enhances Governance & Compliance:** Ensures mandatory tags are applied to all linked resources.  

---

## ⚠ **Key Considerations**  
⚠ **Skip Missing Option (`skip_missing`)**:  
   - If set to `True` (default), missing parent resources do **not** trigger an error.  
   - If set to `False`, an error will be raised when the related resource is missing.  

⚠ **Wildcards for Tags (`tags: '*'`)**:  
   - Using `"*"` copies **all tags** from the related resource.  
   - Alternatively, you can **specify an array of tag keys** (e.g., `tags: ["Environment", "Owner"]`).  

---

## 🛠 **Supported Copy-Related-Tag Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`          | `string`   | The attribute that links the child resource to the parent (e.g., `VolumeId` for EBS Snapshots). **(Required)** |
| `resource`     | `string`   | The parent resource type from which tags should be copied (e.g., `ebs`). **(Required)** |
| `skip_missing` | `boolean`  | If `True`, ignores errors when a related resource is not found. Defaults to `True`. |
| `tags`         | `array`/`enum` | List of tag keys to copy or `"*"` to copy all tags. **(Required)** |
| `type`         | `enum`     | Must be `copy-related-tag`. **(Required)** |

---

## ✅ **Best Practices for Copying Related Tags**  
💡 **Use Copy-Related-Tag for Cost Allocation:** Ensure billing tags from EC2 instances are inherited by attached storage (EBS, snapshots).  
💡 **Combine with Auto-Tagging:** First apply owner/contact tags to the parent resource, then propagate them to children.  
💡 **Monitor Tag Consistency:** Periodically audit tags to ensure they are properly copied across resources.  

---

## 🔹 **Invoke-Lambda: Trigger AWS Lambda Functions**  

### ✨ **What is Invoke-Lambda?**  
The `invoke-lambda` action in Cloud Custodian **triggers an AWS Lambda function** to process resources that match a policy’s filters. This allows for custom logic execution, integrating with external workflows, or automating remediation beyond built-in Cloud Custodian actions.  

**Common Use Cases:**  
✅ **Automate Custom Actions:** Invoke a Lambda function to handle policy violations.  
✅ **Integrate with External Systems:** Send notifications, update databases, or trigger CI/CD pipelines.  
✅ **Remediate Policy Breaches:** Automatically enforce compliance by invoking a function that corrects misconfigurations.  

---

## 🔍 **How It Works**  
1️⃣ **Filters resources** based on policy conditions.  
2️⃣ **Batches them into groups of 250** for Lambda invocation (to optimize execution).  
3️⃣ **Invokes the Lambda function**, passing resource details, policy metadata, and Cloud Custodian execution context.  
4️⃣ **Executes the function asynchronously by default** (avoiding execution delays).  

---

## 📝 **Example: Invoking a Lambda Function for Processing**  
The following policy **invokes a Lambda function named `my-function`** whenever a matching resource is detected.  

```yaml
policies:
  - name: invoke-custom-lambda
    resource: ec2
    filters:
      - "tag:Environment": absent
    actions:
      - type: invoke-lambda
        function: my-function
        assume-role: arn:aws:iam::123456789000:role/lambda-invoker
        async: true
```

🔹 **What Happens?**  
📌 If an **EC2 instance is missing the `Environment` tag**, Cloud Custodian **invokes `my-function`**.  
📌 The Lambda function **receives the list of affected resources** in batches of up to **250 instances**.  
📌 Execution is **asynchronous**, meaning it does not block Cloud Custodian from continuing execution.  

---

## 📝 **Example: Synchronous Invocation with Timeout Handling**  
By default, the Lambda **must respond within 90 seconds**. If the function exceeds this timeout, AWS **automatically retries the invocation**.  

To prevent this, use **synchronous invocation** and set an appropriate timeout:  

```yaml
policies:
  - name: invoke-lambda-with-timeout
    resource: s3
    actions:
      - type: invoke-lambda
        function: process-s3-events
        assume-role: arn:aws:iam::123456789000:role/lambda-invoker
        async: false
        timeout: 180
```

🔹 **What Happens?**  
📌 The policy **calls the `process-s3-events` Lambda function** for each affected S3 bucket.  
📌 **Timeout is increased to 180 seconds** to avoid premature re-invocation.  
📌 **Synchronous invocation ensures** Cloud Custodian waits for a response before proceeding.  

---

## 🎯 **Why Use Invoke-Lambda?**  
✅ **Extend Cloud Custodian’s Functionality:** Execute custom workflows and automation.  
✅ **Integrate with Other AWS Services:** Send data to S3, SNS, DynamoDB, or third-party APIs.  
✅ **Control Execution Mode:** Choose between synchronous (`async: false`) and asynchronous (`async: true`) execution.  
✅ **Batch Processing for Efficiency:** Groups resources into batches of 250, reducing API calls.  

---

## ⚠ **Key Considerations**  
⚠ **Lambda Size Limits:** AWS Lambda allows a maximum payload of **128 KB**, so **batching helps optimize execution**.  
⚠ **Execution Timeouts:** If using synchronous invocation, **ensure the timeout is long enough** to complete processing.  
⚠ **IAM Permissions:** The `assume-role` must have **permission to invoke the Lambda function**.  

---

## 🛠 **Supported Invoke-Lambda Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `function`     | `string`   | The name of the Lambda function to invoke. **(Required)** |
| `assume-role`  | `string`   | IAM role ARN to assume before invoking the function. |
| `async`        | `boolean`  | If `true`, invokes the function asynchronously. Defaults to `true`. |
| `batch_size`   | `integer`  | Number of resources to include in each invocation batch. Defaults to `250`. |
| `qualifier`    | `string`   | Lambda function version or alias to invoke. |
| `region`       | `string`   | AWS region where the Lambda function is deployed. |
| `timeout`      | `integer`  | Maximum execution time (in seconds) before timeout. Default is `90s`. |
| `type`         | `enum`     | Must be `invoke-lambda`. **(Required)** |
| `vars`         | `object`   | Custom variables to pass to the Lambda function. |

---

## ✅ **Best Practices for Invoking Lambda Functions**  
💡 **Use Batching Wisely:** Default batch size is **250 resources**, but consider adjusting based on Lambda memory and processing time.  
💡 **Monitor Execution with Logs:** Enable **CloudWatch logging** in your Lambda function to track policy executions.  
💡 **Optimize IAM Roles:** Ensure the role in `assume-role` has **least privilege** permissions for security.  
💡 **Handle Timeouts Gracefully:** Use retries or DLQs (Dead Letter Queues) if Lambda execution might fail due to timeouts.  

---

## 🔹 **Invoke-SFN: Automate Workflows with AWS Step Functions**  

### ✨ **What is Invoke-SFN?**  
The `invoke-sfn` action in Cloud Custodian **triggers an AWS Step Function** to process matching resources. This enables workflow automation, allowing organizations to execute complex sequences of actions based on policy-defined conditions.  

**Common Use Cases:**  
✅ **Trigger Incident Response:** Automatically start remediation workflows when security policies are violated.  
✅ **Enforce Compliance Checks:** Validate resource configurations using automated workflows.  
✅ **Integrate with External Systems:** Pass resource data to external logging, monitoring, or ticketing systems.  

---

## 🔍 **How It Works**  
1️⃣ **Filters resources** based on policy-defined conditions.  
2️⃣ **By default, invokes Step Function separately for each resource**, passing the **resource details and policy metadata** as input.  
3️⃣ **If bulk mode is enabled (`bulk: true`)**, invokes Step Function **once for a batch of resources**, sending their **ARNs under the `resources` key**.  
4️⃣ **Executes the Step Function**, allowing AWS to process the workflow logic.  

---

## 📝 **Example: Invoke Step Function for S3 Log Setup**  
This policy **triggers the `LogIngestSetup` Step Function** for all S3 buckets that are log targets but are missing an `IngestSetup` tag.  

```yaml
policies:
  - name: invoke-step-function
    resource: s3
    filters:
      - is-log-target
      - "tag:IngestSetup": absent
    actions:
      - type: invoke-sfn
        bulk: true
        batch-size: 10
        state-machine: LogIngestSetup
```

🔹 **What Happens?**  
📌 Cloud Custodian **identifies all S3 buckets that match the filters**.  
📌 It **invokes `LogIngestSetup` Step Function** to **process multiple resources in a single execution** (`bulk: true`).  
📌 The Step Function **receives a batch of up to 10 S3 bucket ARNs** for processing.  

---

## 🎯 **Why Use Invoke-SFN?**  
✅ **Automate Complex Workflows:** Leverage AWS Step Functions for multi-step automation.  
✅ **Process Resources in Bulk:** Reduce execution overhead by grouping multiple resources into a single invocation.  
✅ **Extend Cloud Custodian’s Capabilities:** Integrate with Lambda, SNS, SQS, DynamoDB, and other AWS services.  

---

## ⚠ **Key Considerations**  
⚠ **Batch Size Limit (`batch-size`)**:  
   - Step Function input payload **must fit within 32 KB**.  
   - Default batch size is **250**, but can be adjusted as needed.  

⚠ **Bulk Invocation (`bulk: true`)**:  
   - If enabled, Step Function **processes multiple resource ARNs in a single execution**.  
   - If disabled, Step Function **is invoked separately for each resource**.  

⚠ **IAM Permissions**:  
   - The policy execution role **must have permission to invoke the Step Function** (`states:StartExecution`).  

---

## 🛠 **Supported Invoke-SFN Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `state-machine` | `string`   | The AWS Step Function to invoke. **(Required)** |
| `bulk`         | `boolean`  | If `true`, invokes Step Function with multiple resources in a single execution. Defaults to `false`. |
| `batch-size`   | `integer`  | Number of resource ARNs to include in each batch (default: 250). |
| `policy`       | `boolean`  | If `true`, includes policy details in the input payload. |
| `type`         | `enum`     | Must be `invoke-sfn`. **(Required)** |

---

## ✅ **Best Practices for Invoking Step Functions**  
💡 **Use Bulk Mode for Efficiency:** Reduce execution overhead by processing resources in groups instead of one at a time.  
💡 **Monitor Execution Logs:** Enable **CloudWatch logging** for Step Functions to track workflow progress.  
💡 **Ensure IAM Role Permissions:** The execution role must have `states:StartExecution` permissions.  
💡 **Optimize Step Function Payloads:** Keep input payloads under **32 KB** to avoid failures.  

---

## 🔹 **Mark-For-Op: Schedule Future Actions on Resources**  

### ✨ **What is Mark-For-Op?**  
The `mark-for-op` action in Cloud Custodian **tags resources for future actions**, allowing administrators to schedule operations like termination, stopping, or deleting resources at a later date.  

This is useful for:  
✅ **Graceful decommissioning** of resources.  
✅ **Cost optimization** by scheduling resource cleanup.  
✅ **Policy enforcement** without immediate impact on running services.  

---

## 🔍 **How It Works**  
1️⃣ **Filters resources** based on predefined conditions.  
2️⃣ **Tags matching resources** with a specified operation (`op`) and a scheduled time (`days` or `hours`).  
3️⃣ **A separate Cloud Custodian policy** later checks for these tags and executes the scheduled action.  

---

## 📝 **Example: Mark EC2 Instances for Termination in 4 Days**  
This policy **tags EC2 instances older than 90 days** for termination in 4 days.  

```yaml
policies:
  - name: ec2-mark-stop
    resource: ec2
    filters:
      - type: image-age
        op: ge
        days: 90
    actions:
      - type: mark-for-op
        tag: custodian_cleanup
        op: terminate
        days: 4
```

🔹 **What Happens?**  
📌 EC2 instances **older than 90 days** are tagged with `custodian_cleanup: terminate@YYYY/MM/DD`.  
📌 Another Cloud Custodian policy can **check for this tag** and terminate the instance on the specified date.  

---

## 📝 **Example: Mark S3 Buckets for Deletion After 7 Days**  
```yaml
policies:
  - name: s3-mark-for-deletion
    resource: s3
    filters:
      - "tag:Environment": absent
    actions:
      - type: mark-for-op
        tag: delete_schedule
        op: delete
        days: 7
```

🔹 **What Happens?**  
📌 S3 buckets **without an `Environment` tag** are scheduled for deletion in 7 days.  
📌 This allows time for users to **correct tagging** before deletion occurs.  

---

## 🎯 **Why Use Mark-For-Op?**  
✅ **Enables Delayed Actions:** Allows resources to be scheduled for operations **without immediate execution**.  
✅ **Improves Governance:** Ensures compliance with cleanup policies while **giving teams time to respond**.  
✅ **Prevents Accidental Deletion:** Users have a window to **correct issues before enforcement**.  

---

## ⚠ **Key Considerations**  
⚠ **Requires a Follow-Up Policy:** A second Cloud Custodian policy must be created to execute the marked action.  
⚠ **Customizable Scheduling:** Supports **delays in hours or days** before an operation is executed.  
⚠ **Timezone Handling (`tz`)**: If running in multiple regions, **specify a timezone** to align execution timing.  

---

## 🛠 **Supported Mark-For-Op Properties**  

| 🔖 **Property**  | 🏷 **Type**  | 🔍 **Description** |
|----------------|------------|----------------|
| `tag`         | `string`   | The tag key used to store the scheduled operation. **(Required)** |
| `op`          | `string`   | The operation to be performed (`terminate`, `stop`, `delete`, etc.). **(Required)** |
| `days`        | `number`   | Number of days to wait before executing the action. |
| `hours`       | `number`   | Number of hours to wait before executing the action. |
| `msg`         | `string`   | Custom message to include in the tag value. |
| `tz`          | `string`   | Timezone for execution scheduling. |
| `type`        | `enum`     | Must be `mark-for-op`. **(Required)** |

---

## ✅ **Best Practices for Scheduled Operations**  
💡 **Ensure a Follow-Up Execution Policy**: Use `marked-for-op` filter in a separate policy to enforce the scheduled action.  
💡 **Use Descriptive Tags**: Clearly define the purpose of the action (e.g., `custodian_cleanup`).  
💡 **Allow Time for Review**: Provide a reasonable delay (e.g., 3-7 days) before enforcing deletions.  

---

## 🔹 **Modify-ECR-Policy: Manage Amazon ECR Permissions**  

### ✨ **What is Modify-ECR-Policy?**  
The `modify-ecr-policy` action in Cloud Custodian **modifies policy statements on Amazon Elastic Container Registry (ECR) repositories**. It allows you to:  

✅ **Restrict or allow access** to ECR repositories.  
✅ **Dynamically update policies** based on security findings.  
✅ **Remove specific policy statements** to clean up permissions.  

---

## 🔍 **How It Works**  
1️⃣ **Identifies ECR repositories or images** that match defined filters.  
2️⃣ **Adds or removes policy statements** to enforce security and access control.  
3️⃣ **Modifies the ECR repository policy** dynamically based on compliance requirements.  

---

## 📝 **Example: Prevent Unauthorized Image Pulls**  
The following policy **adds a `Deny` rule to prevent unauthenticated users from pulling container images** while removing any existing policy statements.  

```yaml
policies:
  - name: ecr-image-prevent-pull
    resource: ecr-image
    filters:
      - type: finding
    actions:
      - type: modify-ecr-policy
        add-statements: [{
            "Sid": "ReplaceWithMe",
            "Effect": "Deny",
            "Principal": "*",
            "Action": ["ecr:BatchGetImage"]
        }]
        remove-statements: "*"
```

🔹 **What Happens?**  
📌 The policy **denies all users** from pulling images (`ecr:BatchGetImage`).  
📌 **Removes all existing policy statements** (`remove-statements: "*"`) to enforce strict security.  

---

## 🎯 **Why Use Modify-ECR-Policy?**  
✅ **Enhances Security:** Prevent unauthorized access to container images.  
✅ **Automates Policy Management:** Adjusts permissions dynamically based on findings.  
✅ **Improves Compliance:** Ensures ECR policies align with security best practices.  

---

## ⚠ **Key Considerations**  
⚠ **Use Caution When Removing Policies:** Setting `remove-statements: "*"` will erase all existing permissions.  
⚠ **Ensure IAM Roles Are Accounted For:** If removing all policies, ensure authorized roles/users still have necessary permissions.  
⚠ **Condition-Based Restrictions:** You can **apply conditions** to limit actions based on IP, time, or other parameters.  

---

## 🛠 **Supported Modify-ECR-Policy Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `add-statements`  | `array`    | List of policy statements to add. Must include `Sid`, `Effect`, `Principal`, and `Action`. |
| `remove-statements` | `string/array` | `"*"` removes all statements, `"matched"` removes only those that match a filter, or specify a list of statement IDs. |
| `type`          | `enum`     | Must be `modify-ecr-policy`. **(Required)** |

---

## ✅ **Best Practices for ECR Policy Management**  
💡 **Regularly Audit ECR Policies:** Use Cloud Custodian to scan and validate policy settings.  
💡 **Apply Least Privilege:** Restrict access only to necessary roles and users.  
💡 **Use Condition-Based Controls:** Apply fine-grained restrictions for better security.  

---

## 🔹 **Modify-Policy: Manage IAM Policies for SQS Queues**  

### ✨ **What is Modify-Policy?**  
The `modify-policy` action in Cloud Custodian **modifies IAM policies on AWS SQS Queues**, allowing you to:  

✅ **Restrict or allow access** to SQS queues.  
✅ **Enforce security best practices** by removing unwanted policies.  
✅ **Automatically adjust permissions** based on compliance and security requirements.  

---

## 🔍 **How It Works**  
1️⃣ **Filters SQS queues** based on defined conditions (e.g., cross-account access).  
2️⃣ **Adds or removes IAM policy statements** to control permissions.  
3️⃣ **Modifies the SQS queue policy** dynamically to enforce security policies.  

---

## 📝 **Example: Remove Cross-Account Access from SQS Queues**  
The following policy **removes all existing IAM policy statements on SQS queues that allow cross-account access**, while **adding a restricted policy statement** allowing only `sqs:GetQueueAttributes` access.  

```yaml
policies:
  - name: sqs-yank-cross-account
    resource: sqs
    filters:
      - type: cross-account
    actions:
      - type: modify-policy
        add-statements: [{
            "Sid": "ReplaceWithMe",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["sqs:GetQueueAttributes"],
            "Resource": queue_url
        }]
        remove-statements: '*'
```

🔹 **What Happens?**  
📌 If an SQS queue **has cross-account access**, its policy **is reset** to remove all statements (`remove-statements: "*"`)  
📌 **Only `sqs:GetQueueAttributes` permission is added**, restricting further actions.  

---

## 🎯 **Why Use Modify-Policy?**  
✅ **Enhances Security:** Prevents unauthorized cross-account access to SQS queues.  
✅ **Automates IAM Policy Management:** Dynamically modifies policies without manual intervention.  
✅ **Improves Compliance:** Ensures IAM policies align with best practices.  

---

## ⚠ **Key Considerations**  
⚠ **Use Caution When Removing Policies:** Setting `remove-statements: "*"` **removes all existing IAM permissions** on the SQS queue.  
⚠ **Least Privilege Principle:** Only grant permissions that are absolutely necessary.  
⚠ **Ensure IAM Roles Are Accounted For:** If removing all policies, ensure that required AWS roles still have access.  

---

## 🛠 **Supported Modify-Policy Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `add-statements`  | `array`    | List of policy statements to add. Must include `Sid`, `Effect`, `Principal`, `Action`, and `Resource`. |
| `remove-statements` | `string/array` | `"*"` removes all statements, `"matched"` removes only those that match a filter, or specify a list of statement IDs. |
| `type`          | `enum`     | Must be `modify-policy`. **(Required)** |

---

## ✅ **Best Practices for SQS Policy Management**  
💡 **Regularly Audit SQS Policies:** Use Cloud Custodian to scan for unwanted access.  
💡 **Apply Least Privilege:** Restrict access only to necessary roles and users.  
💡 **Monitor IAM Policy Changes:** Enable CloudTrail logging to detect unauthorized changes.  

---

## 🔹 **Modify-Security-Groups: Manage Redshift Cluster Security**  

### ✨ **What is Modify-Security-Groups?**  
The `modify-security-groups` action in Cloud Custodian **updates security group assignments on Amazon Redshift clusters**, allowing you to:  

✅ **Enforce network security policies** by adding or removing security groups.  
✅ **Automatically adjust security groups** based on predefined rules.  
✅ **Isolate Redshift clusters** from unauthorized network access.  

---

## 🔍 **How It Works**  
1️⃣ **Identifies Redshift clusters** that match policy-defined conditions.  
2️⃣ **Modifies security group associations** by adding or removing groups.  
3️⃣ **Optionally assigns security groups dynamically** based on tags.  
4️⃣ **Ensures compliance** by restricting or allowing access as needed.  

---

## 📝 **Example: Restrict Redshift Cluster Access**  
This policy **removes all existing security groups** and assigns a new one to enforce strict access controls.  

```yaml
policies:
  - name: restrict-redshift-security
    resource: redshift
    filters:
      - type: value
        key: PubliclyAccessible
        value: true
    actions:
      - type: modify-security-groups
        remove: all
        add: sg-12345678
```

🔹 **What Happens?**  
📌 Any **publicly accessible Redshift cluster** is **assigned a secure security group (`sg-12345678`)**.  
📌 **Existing security groups are removed (`remove: all`)** to eliminate unauthorized access.  

---

## 📝 **Example: Assign Security Groups Based on Tags**  
This policy **dynamically assigns security groups based on tag values**.  

```yaml
policies:
  - name: redshift-assign-sg-by-tag
    resource: redshift
    actions:
      - type: modify-security-groups
        add-by-tag:
          key: Department
          values: ["Finance", "HR"]
```

🔹 **What Happens?**  
📌 If a Redshift cluster has a `Department` tag matching `"Finance"` or `"HR"`, it **receives the corresponding security group**.  

---

## 🎯 **Why Use Modify-Security-Groups?**  
✅ **Improves Security:** Prevents unauthorized access to Redshift clusters.  
✅ **Automates Network Control:** Dynamically assigns security groups based on compliance rules.  
✅ **Enhances Governance:** Enforces company-wide network access policies.  

---

## ⚠ **Key Considerations**  
⚠ **Removing All Security Groups (`remove: all`) Can Break Connectivity:** Ensure at least one security group is added when removing others.  
⚠ **Network Isolation (`isolation-group`)**: Assigns clusters to a restricted security group, preventing unintended access.  
⚠ **Tag-Based Security Group Assignment**: Enables automatic grouping of Redshift clusters by department or environment.  

---

## 🛠 **Supported Modify-Security-Groups Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `add`         | `string/array` | Security group(s) to add. |
| `remove`      | `string/array` | Security groups to remove (`all`, `matched`, `network-location`). |
| `add-by-tag`  | `object` | Assign security groups dynamically based on tag key-values. |
| `isolation-group` | `string/array` | Enforces a dedicated security group for network isolation. |
| `type`        | `enum`     | Must be `modify-security-groups`. **(Required)** |

---

## ✅ **Best Practices for Redshift Security Management**  
💡 **Regularly Audit Security Group Assignments:** Use Cloud Custodian to review which groups are assigned to Redshift clusters.  
💡 **Use Isolation Groups for Critical Data:** Assign dedicated security groups to prevent unauthorized access.  
💡 **Leverage Tags for Dynamic Security Grouping:** Group clusters automatically based on business unit, environment, or function.  

---

## 🔹 **Normalize-Tag: Standardize Tag Values**  

### ✨ **What is Normalize-Tag?**  
The `normalize-tag` action in Cloud Custodian **modifies the format of tag values** to ensure consistency across cloud resources. This helps maintain clean and structured tagging for better governance, compliance, and cost tracking.  

**Common Use Cases:**  
✅ **Ensure Tag Uniformity** – Convert all tags to uppercase, lowercase, or title case.  
✅ **Remove Unwanted Text** – Strip specific text from tag values.  
✅ **Standardize Naming Conventions** – Avoid inconsistencies in tags across AWS resources.  

---

## 🔍 **How It Works**  
1️⃣ **Identifies resources** with specific tags.  
2️⃣ **Transforms tag values** based on predefined rules.  
3️⃣ **Applies the modified tag value** to the resource.  

---

## 📝 **Example: Convert EC2 Tag Values to Lowercase**  
This policy **normalizes the tag value by converting it to lowercase** for all running EC2 instances with the `testing8882` tag.  

```yaml
policies:
  - name: ec2-service-transform-lower
    resource: ec2
    comment: |
      ec2-service-tag-value-to-lower
    query:
      - instance-state-name: running
    filters:
      - "tag:testing8882": present
    actions:
      - type: normalize-tag
        key: lower_key
        action: lower
```

🔹 **What Happens?**  
📌 Any running EC2 instance with the tag `testing8882` **will have its value converted to lowercase**.  

---

## 📝 **Example: Strip a Specific Word from a Tag**  
This policy **removes the word `"blah"` from the tag value** of `strip_key` on EC2 instances.  

```yaml
policies:
  - name: ec2-service-strip
    resource: ec2
    comment: |
      ec2-service-tag-strip-blah
    query:
      - instance-state-name: running
    filters:
      - "tag:testing8882": present
    actions:
      - type: normalize-tag
        key: strip_key
        action: strip
        value: blah
```

🔹 **What Happens?**  
📌 If the tag value contains `"blah"`, it **will be removed**, ensuring cleaner tag formatting.  

---

## 🎯 **Why Use Normalize-Tag?**  
✅ **Improves Tag Consistency:** Enforces a uniform tag format across resources.  
✅ **Simplifies Resource Management:** Makes filtering and querying resources easier.  
✅ **Enhances Governance & Compliance:** Ensures that all resources follow company-wide tagging standards.  

---

## ⚠ **Key Considerations**  
⚠ **Case-Sensitive Tag Matching:** Ensure that the tag key names are correctly defined for normalization.  
⚠ **Impact on Existing Automation:** If other automation depends on specific tag values, review changes carefully.  
⚠ **Stripping Removes Specific Text Only:** The `strip` action removes **only the specified word** from tag values.  

---

## 🛠 **Supported Normalize-Tag Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The tag key whose value will be modified. **(Required)** |
| `action`      | `string`   | The transformation action (`upper`, `lower`, `titlestrip`, `replace`). **(Required)** |
| `value`       | `string`   | The value to strip or replace (if applicable). |
| `type`        | `enum`     | Must be `normalize-tag`. **(Required)** |

---

## ✅ **Best Practices for Tag Normalization**  
💡 **Standardize Tags Across All Resources:** Use `normalize-tag` across EC2, S3, RDS, and IAM to enforce naming conventions.  
💡 **Avoid Unnecessary Tag Variations:** Convert all tags to a standard format (`lower`, `upper`, `title`) for easy searching.  
💡 **Regularly Audit Tags:** Run periodic checks to detect and fix inconsistent tags.  

---

## 🔹 **Notify: Send Automated Alerts via SQS or SNS**  

### ✨ **What is Notify?**  
The `notify` action in Cloud Custodian **sends event notifications** when a policy is triggered. Instead of directly producing human-readable messages, **notifications are sent to an AWS SQS queue or SNS topic**, where they can be processed by external tools like **c7n-mailer** to format and deliver messages.  

**Common Use Cases:**  
✅ **Alert Security Teams** – Notify teams when security policies are violated.  
✅ **Notify Resource Owners** – Send notifications to users who created or own a resource.  
✅ **Automate Incident Response** – Integrate with external systems via SNS/SQS for automated workflows.  

---

## 🔍 **How It Works**  
1️⃣ **Identifies resources that match a policy’s filters** (e.g., non-compliant instances).  
2️⃣ **Generates a notification event** containing resource details.  
3️⃣ **Sends the notification to an AWS SQS queue or SNS topic** for processing.  
4️⃣ **A separate process (c7n-mailer) formats and delivers** the final message.  

---

## 📝 **Example: Notify When Terminating an EC2 Instance**  
This policy **sends a notification when a non-compliant EC2 instance is terminated**, delivering messages via SQS.  

```yaml
policies:
  - name: ec2-bad-instance-kill
    resource: ec2
    filters:
      - Name: bad-instance
    actions:
      - terminate
      - type: notify
        to:
          - event-user
          - resource-creator
          - email@address
        owner_absent_contact:
          - other_email@address
        template: policy-template
        transport:
          type: sqs
          region: us-east-1
          queue: xyz
```

🔹 **What Happens?**  
📌 If an **EC2 instance with `Name: bad-instance` is terminated**, Cloud Custodian **sends a notification to the SQS queue `xyz`**.  
📌 **c7n-mailer** picks up the message, **formats it using `policy-template`**, and sends an email notification.  

---

## 📝 **Example: Notify via SNS with Custom Attributes**  
This policy **publishes notifications to an SNS topic** with additional attributes.  

```yaml
policies:
  - name: ec2-notify-with-attributes
    resource: ec2
    filters:
      - Name: bad-instance
    actions:
      - type: notify
        to:
          - event-user
          - resource-creator
          - email@address
        owner_absent_contact:
          - other_email@address
        template: policy-template
        transport:
          type: sns
          region: us-east-1
          topic: your-notify-topic
          attributes:
            attribute_key: attribute_value
            attribute_key_2: attribute_value_2
```

🔹 **What Happens?**  
📌 Cloud Custodian **publishes a notification to SNS topic `your-notify-topic`**.  
📌 The SNS message **includes custom attributes** (`attribute_key`, `attribute_key_2`).  
📌 **c7n-mailer formats the message and sends notifications** to recipients.  

---

## 🎯 **Why Use Notify?**  
✅ **Automates Alerts:** Sends real-time notifications for policy violations.  
✅ **Supports Multiple Transports:** Integrates with SQS (queue-based processing) or SNS (publish-subscribe messaging).  
✅ **Customizable Templates:** Uses `c7n-mailer` to format messages for email, Slack, or other channels.  
✅ **Dynamic Recipient Resolution:** Sends notifications to **resource owners, event users, or predefined contacts**.  

---

## ⚠ **Key Considerations**  
⚠ **Requires c7n-mailer for Email Delivery:** Notifications are not directly human-readable; they must be processed by **c7n-mailer** to format and deliver emails.  
⚠ **Transport Type Defines Behavior:**  
   - **SQS** – Messages are queued for external processing.  
   - **SNS** – Messages are published to a topic for immediate fan-out delivery.  
⚠ **Ensure IAM Permissions Are Configured:** The execution role must have `sns:Publish` or `sqs:SendMessage` permissions.  

---

## 🛠 **Supported Notify Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `to`          | `array`   | Recipients (e.g., `event-user`, `resource-creator`, email addresses). **(Required)** |
| `owner_absent_contact` | `array` | Backup recipients if the owner cannot be determined. |
| `template`    | `string`   | Name of the template used by **c7n-mailer** to format the message. |
| `subject`     | `string`   | Subject line for email notifications. |
| `transport`   | `object`   | Defines the transport method (`sqs` or `sns`). **(Required)** |
| `assume_role` | `boolean`  | Whether to assume an IAM role for message delivery. |

🔹 **Transport-Specific Properties**  

| 🔖 **Transport Type** | 🏷 **Properties** | 🔍 **Description** |
|----------------|------------|----------------|
| **SQS**       | `queue`, `region` | Sends notifications to an SQS queue for processing. |
| **SNS**       | `topic`, `region`, `attributes` | Publishes notifications to an SNS topic with optional attributes. |

---

## ✅ **Best Practices for Notifications**  
💡 **Use SQS for Asynchronous Processing:** Queue notifications for external tools to process and format before delivery.  
💡 **Use SNS for Real-Time Alerts:** Publish notifications to SNS for immediate fan-out to multiple subscribers.  
💡 **Ensure c7n-mailer is Set Up:** Without `c7n-mailer`, notifications may not be readable.  
💡 **Define a Clear Notification Strategy:** Use recipient groups (`to`, `owner_absent_contact`) for targeted communication.  

---

## 🔹 **Post-Item: Create AWS OpsCenter Incidents for Policy Violations**  

### ✨ **What is Post-Item?**  
The `post-item` action in Cloud Custodian **creates an OpsItem in AWS Systems Manager OpsCenter** when a policy violation is detected. This enables IT and security teams to **track, investigate, and resolve operational issues** efficiently.  

**Common Use Cases:**  
✅ **Automate Incident Management** – Flag non-compliant resources as OpsItems.  
✅ **Integrate with ITSM Workflows** – Send alerts to AWS OpsCenter for operational tracking.  
✅ **Leverage AWS Deduplication Logic** – Prevent duplicate OpsItems for the same issue.  

---

## 🔍 **How It Works**  
1️⃣ **Identifies policy-violating resources** (e.g., EC2 instances with excessive IAM permissions).  
2️⃣ **Creates an OpsItem in AWS OpsCenter** to track the issue.  
3️⃣ **Supports deduplication** by associating multiple resources with the same open OpsItem.  
4️⃣ **Prioritizes incidents** using predefined severity levels (`1-5`).  

---

## 📝 **Example: Flag EC2 Instances with Over-Privileged IAM Actions**  
This policy **creates an OpsItem for EC2 instances that have `iam:CreateUser` permissions**, which could indicate excessive privileges.  

```yaml
policies:
  - name: over-privileged-ec2
    resource: aws.ec2
    filters:
      - type: check-permissions
        match: allowed
        actions:
          - iam:CreateUser
    actions:
      - type: post-item
        priority: 3
```

🔹 **What Happens?**  
📌 If an **EC2 instance has `iam:CreateUser` permissions**, an **OpsItem is created in AWS OpsCenter**.  
📌 The **priority is set to `3`**, indicating a moderate-level issue.  
📌 AWS OpsCenter **deduplicates findings** to prevent redundant OpsItems.  

---

## 📝 **Example: Report SQS Queues with Cross-Account Access**  
This policy **flags SQS queues with cross-account access as an OpsItem** and schedules them for deletion in 5 days.  

```yaml
policies:
  - name: sqs-cross-account-access
    resource: aws.sqs
    filters:
      - type: cross-account
    actions:
      - type: mark-for-op
        days: 5
        op: delete
      - type: post-item
        title: SQS Cross Account Access
        description: |
          Cross Account Access detected in SQS resource IAM Policy.
        tags:
          Topic: Security
```

🔹 **What Happens?**  
📌 If an **SQS queue has cross-account access**, an **OpsItem is created** to alert administrators.  
📌 The queue is **scheduled for deletion in 5 days (`mark-for-op`)**.  
📌 The OpsItem is **tagged with `Topic: Security`** for tracking.  

---

## 🎯 **Why Use Post-Item?**  
✅ **Enhances IT Incident Management:** Integrates Cloud Custodian with AWS OpsCenter for structured remediation.  
✅ **Automates Compliance Enforcement:** Identifies and tracks security risks automatically.  
✅ **Leverages Built-in AWS Deduplication:** Prevents multiple OpsItems for the same issue.  
✅ **Supports Priority Levels:** Assigns incident severity (`1-5`) for better response coordination.  

---

## ⚠ **Key Considerations**  
⚠ **AWS OpsCenter Must Be Enabled:** Ensure AWS Systems Manager OpsCenter is active in your account.  
⚠ **Prioritize Critical Findings:** Use appropriate priority levels (`1` is highest, `5` is lowest).  
⚠ **Use Tags for Categorization:** Adding tags helps organize and track OpsItems efficiently.  

---

## 🛠 **Supported Post-Item Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `title`       | `string`   | The title of the OpsItem (default: policy name). |
| `description` | `string`   | Detailed explanation of the issue. |
| `priority`    | `enum`     | Incident priority (`1` = highest, `5` = lowest). |
| `tags`        | `object`   | Key-value pairs to categorize OpsItems. |
| `topics`      | `string`   | Topic for grouping OpsItems. |
| `type`        | `enum`     | Must be `post-item`. **(Required)** |

---

## ✅ **Best Practices for Incident Management**  
💡 **Use High Priority for Critical Issues:** Assign `priority: 1` for severe security threats.  
💡 **Tag Items for Better Organization:** Use tags (`Security`, `Compliance`, `Cost Optimization`) to categorize OpsItems.  
💡 **Monitor OpsCenter for Open Incidents:** Regularly check AWS OpsCenter for unresolved findings.  
💡 **Combine with Other Actions:** Pair `post-item` with `mark-for-op` to schedule resource remediation.  

---

## 🔹 **Put-Metric: Send Custom Metrics to AWS CloudWatch**  

### ✨ **What is Put-Metric?**  
The `put-metric` action in Cloud Custodian **publishes custom CloudWatch metrics** based on a resource attribute or an expression. This allows organizations to **track, visualize, and analyze policy-driven data** in real time.  

**Common Use Cases:**  
✅ **Monitor Cloud Resource Usage** – Track attached EBS volumes, active EC2 instances, or network activity.  
✅ **Enhance Compliance Visibility** – Measure compliance trends for tagging, security settings, or cost optimizations.  
✅ **Trigger Alerts & Automations** – Set CloudWatch alarms based on policy-defined thresholds.  

---

## 🔍 **How It Works**  
1️⃣ **Filters AWS resources** based on policy criteria.  
2️⃣ **Extracts a specific value** from matching resources (`key` parameter).  
3️⃣ **Computes a metric value** using an operation (`count`, `sum`, `average`, etc.).  
4️⃣ **Sends the computed metric** to a CloudWatch namespace.  

---

## 📝 **Example: Track the Number of Attached EBS Volumes on EC2**  
This policy **publishes a metric tracking the number of EBS volumes attached to EC2 instances** under the `Usage Metrics` namespace.  

```yaml
policies:
  - name: track-attached-ebs
    resource: ec2
    comment: |
      Put the count of the number of EBS attached disks to an instance
    filters:
      - Name: tracked-ec2-instance
    actions:
      - type: put-metric
        key: Reservations[].Instances[].BlockDeviceMappings[].DeviceName
        namespace: Usage Metrics
        metric_name: Attached Disks
        op: count
        units: Count
```

🔹 **What Happens?**  
📌 For each EC2 instance, **Cloud Custodian counts the number of attached EBS volumes**.  
📌 The metric **is published to CloudWatch** under `Usage Metrics → Attached Disks`.  
📌 CloudWatch **can now visualize, alert, or automate actions** based on disk usage trends.  

---

## 📝 **Example: Monitor S3 Buckets Without Encryption**  
This policy **tracks the number of unencrypted S3 buckets** and sends a metric to CloudWatch.  

```yaml
policies:
  - name: s3-unencrypted-tracking
    resource: s3
    filters:
      - type: value
        key: ServerSideEncryptionConfiguration.Rules
        value: absent
    actions:
      - type: put-metric
        key: Name
        namespace: Security Metrics
        metric_name: Unencrypted Buckets
        op: count
        units: Count
```

🔹 **What Happens?**  
📌 Cloud Custodian **counts the number of unencrypted S3 buckets**.  
📌 The count is **published as a CloudWatch metric under `Security Metrics`**.  
📌 **CloudWatch alarms can be triggered** if too many unencrypted buckets exist.  

---

## 🎯 **Why Use Put-Metric?**  
✅ **Gain Real-Time Insights:** Track policy-driven metrics across AWS resources.  
✅ **Enhance Visibility & Reporting:** Send custom metrics to **CloudWatch dashboards**.  
✅ **Trigger Alarms & Automations:** Use CloudWatch **to alert or take actions based on metric thresholds**.  
✅ **Measure Compliance Trends:** Track changes over time, such as **security risks or cost inefficiencies**.  

---

## ⚠ **Key Considerations**  
⚠ **CloudWatch Limits on Metrics** – Custom metrics **incur costs**, so **use carefully to avoid excessive charges**.  
⚠ **Choose the Right Units** – Ensure that **metric units align** with the data being measured (e.g., `Bytes`, `Count`, `Percent`).  
⚠ **Understand Aggregation (`op`)** – Default is `count`, but other options include `sum`, `average`, or `distinct_count`.  

---

## 🛠 **Supported Put-Metric Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The attribute from the resource to extract for metric calculation. **(Required)** |
| `namespace`   | `string`   | The CloudWatch namespace under which the metric is published. **(Required)** |
| `metric_name` | `string`   | Name of the CloudWatch metric. **(Required)** |
| `op`         | `enum`     | Aggregation method (`count`, `sum`, `average`, `distinct_count`). Default: `count`. |
| `units`      | `enum`     | Unit of measurement (`Count`, `Percent`, `Bytes`, etc.). Default: `Count`. |

---

## ✅ **Best Practices for CloudWatch Metrics**  
💡 **Use Consistent Namespaces:** Organize metrics under logical categories like `Security Metrics`, `Usage Metrics`, or `Compliance Metrics`.  
💡 **Set CloudWatch Alarms for Key Metrics:** Use metrics to **automatically detect anomalies** in resource behavior.  
💡 **Limit Unnecessary Metrics:** Avoid excessive metric creation to prevent **CloudWatch billing increases**.  
💡 **Leverage Metrics for Governance:** Use dashboards to **track long-term trends in security, compliance, and costs**.  

---

## 🔹 **Rename-Tag: Rename Tags While Preserving Values**  

### ✨ **What is Rename-Tag?**  
The `rename-tag` action in Cloud Custodian **renames a tag on a resource by creating a new tag with the same value and removing the old tag**. This helps in **standardizing tag naming conventions** across AWS resources.  

**Common Use Cases:**  
✅ **Standardize Tag Names** – Rename inconsistent or outdated tags across multiple resources.  
✅ **Improve Governance & Cost Allocation** – Ensure tags follow a structured naming convention for tracking.  
✅ **Fix Tagging Errors** – Correct misnamed tags without losing tag values.  

---

## 🔍 **How It Works**  
1️⃣ **Finds resources with the old tag (`old_key`)**.  
2️⃣ **Creates a new tag (`new_key`)** with the same value.  
3️⃣ **Deletes the old tag (`old_key`)** from the resource.  

---

## 📝 **Example: Rename "EnvironmentName" to "Environment"**  
This policy **renames the `EnvironmentName` tag to `Environment` on all EC2 instances**.  

```yaml
policies:
  - name: rename-environment-tag
    resource: ec2
    filters:
      - "tag:EnvironmentName": present
    actions:
      - type: rename-tag
        old_key: EnvironmentName
        new_key: Environment
```

🔹 **What Happens?**  
📌 If an EC2 instance **has the tag `EnvironmentName`**, Cloud Custodian **copies its value to a new tag `Environment`**.  
📌 The **old tag (`EnvironmentName`) is then removed**.  

---

## 🎯 **Why Use Rename-Tag?**  
✅ **Ensures Tag Consistency:** Standardizes tag names across AWS environments.  
✅ **Improves Cost & Resource Tracking:** Enables accurate cost allocation and compliance reporting.  
✅ **Automates Tag Correction:** Fixes misnamed or legacy tags across all resources.  

---

## ⚠ **Key Considerations**  
⚠ **Tag Value is Preserved:** Only the key is changed; the value remains the same.  
⚠ **Ensure Correct Tag Mapping:** Double-check old and new tag names to avoid unexpected renaming.  
⚠ **Use for Governance Cleanup:** Useful for **enforcing company-wide tag naming policies**.  

---

## 🛠 **Supported Rename-Tag Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `old_key`      | `string`   | The name of the tag to rename. **(Required)** |
| `new_key`      | `string`   | The new tag name to apply. **(Required)** |
| `type`         | `enum`     | Must be `rename-tag`. **(Required)** |

---

## ✅ **Best Practices for Tag Renaming**  
💡 **Audit Tags Before Renaming:** Ensure the old tag exists across resources before renaming.  
💡 **Use in Combination with `normalize-tag`:** Normalize tag values **after renaming for better consistency**.  
💡 **Monitor Changes:** Track tag modifications using AWS Config or CloudTrail for governance.  

---

## 🔹 **Tag: Automatically Apply Tags to AWS Resources**  

### ✨ **What is Tag?**  
The `tag` action in Cloud Custodian **applies one or more tags** to AWS resources that match a policy’s filters. This helps organizations **enforce tagging policies, improve governance, and enhance cost tracking**.  

**Common Use Cases:**  
✅ **Ensure Required Tags Are Present** – Automatically tag untagged or misconfigured resources.  
✅ **Enhance Cost Allocation** – Assign ownership, environment, and purpose-based tags.  
✅ **Improve Compliance & Governance** – Enforce consistent tagging across all cloud resources.  

---

## 🔍 **How It Works**  
1️⃣ **Filters resources** based on tag presence or specific conditions.  
2️⃣ **Applies the defined tags** to the matching resources.  
3️⃣ **Ensures consistent metadata** for cost tracking, compliance, and automation.  

---

## 📝 **Example: Tag AWS Secrets Manager Resources Missing Required Tags**  
This policy **tags AWS Secrets Manager secrets that do not have an `Environment` or `ResourceOwner` tag**.  

```yaml
policies:
  - name: multiple-tags-example
    comment: |
      Tags any secrets missing either the Environment or ResourceOwner tag
    resource: aws.secrets-manager
    filters:
      - or:
          - "tag:Environment": absent
          - "tag:ResourceOwner": absent
    actions:
      - type: tag
        tags:
          Environment: Staging
          ResourceOwner: Avengers
```

🔹 **What Happens?**  
📌 If a **Secret in AWS Secrets Manager is missing `Environment` or `ResourceOwner` tags**, Cloud Custodian **automatically applies the tags**.  
📌 The **Environment tag is set to `Staging`** and **ResourceOwner is set to `Avengers`**.  

---

## 🎯 **Why Use Tag?**  
✅ **Automates Tagging for Unmanaged Resources:** Applies missing tags without manual intervention.  
✅ **Ensures Consistent Metadata:** Helps maintain **structured tagging for governance**.  
✅ **Improves Cost & Security Auditing:** Facilitates cost allocation and compliance tracking.  

---

## ⚠ **Key Considerations**  
⚠ **Tag Values Must Be Defined:** Ensure all required tags have meaningful values.  
⚠ **AWS Tagging Limits:** Each resource **supports a maximum of 50 tags** (check AWS limits).  
⚠ **Use Descriptive Naming Conventions:** Avoid redundant or unclear tag names.  

---

## 🛠 **Supported Tag Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `tags`        | `object`   | Key-value pairs defining the tags to apply. **(Required)** |
| `key`         | `string`   | **(Deprecated)** Single tag key (use `tags` instead). |
| `value`       | `string`   | **(Deprecated)** Value for `key` (use `tags` instead). |
| `type`        | `enum`     | Must be `tag` or `mark`. **(Required)** |

---

## ✅ **Best Practices for Automated Tagging**  
💡 **Use Meaningful Tag Keys:** Define clear categories like `Environment`, `Owner`, and `Application`.  
💡 **Automate Tag Enforcement:** Combine with `mark-for-op` or `remove-tag` for full lifecycle control.  
💡 **Audit Tags Regularly:** Use Cloud Custodian to **scan for missing or incorrect tags**.  

---

## 🔹 **Tag-Trim: Automatically Remove Excess Tags from EC2 Resources**  

### ✨ **What is Tag-Trim?**  
The `tag-trim` action in Cloud Custodian **removes tags from EC2 resources** to free up space for new tags. Since AWS **limits resources to 50 tags**, this action helps **manage tag limits dynamically** while preserving essential tags.  

**Common Use Cases:**  
✅ **Prevent Tag Limit Issues** – Ensure new tags can be added by trimming unnecessary ones.  
✅ **Automate Tag Cleanup** – Maintain only relevant tags while removing outdated or excessive tags.  
✅ **Preserve Critical Tags** – Specify which tags must always be retained during trimming.  

---

## 🔍 **How It Works**  
1️⃣ **Identifies EC2 instances** that exceed the specified tag threshold.  
2️⃣ **Removes tags** until the desired number of available tag slots (`space`) is met.  
3️⃣ **Preserves specified tags**, ensuring important metadata remains intact.  

---

## 📝 **Example: Free Up Tag Slots on EC2 Instances**  
This policy **removes excess tags from EC2 instances** with **48 or more tags**, ensuring at least **3 free tag slots** while preserving critical tags.  

```yaml
policies:
  - name: ec2-tag-trim
    comment: |
      Any instances with 48 or more tags get tags removed until
      they match the target tag count, in this case 47 so we
      free up a tag slot for another usage.
    resource: ec2
    filters:
      - type: value
        key: "length(Tags)"
        op: ge
        value: 48
    actions:
      - type: tag-trim
        space: 3
        preserve:
          - OwnerContact
          - ASV
          - CMDBEnvironment
          - downtime
          - custodian_status
```

🔹 **What Happens?**  
📌 **EC2 instances with 48+ tags are targeted** for tag trimming.  
📌 **Tags are removed until 3 free slots are available** for new tags.  
📌 **Preserved tags (`OwnerContact`, `ASV`, etc.) are not removed**, ensuring business-critical metadata remains intact.  

---

## 🎯 **Why Use Tag-Trim?**  
✅ **Prevents AWS Tag Limit Issues:** Frees up space for new tags without exceeding AWS's **50-tag limit**.  
✅ **Automates Tag Management:** No manual cleanup required—Cloud Custodian ensures compliance dynamically.  
✅ **Preserves Essential Metadata:** Ensures key tags remain intact while removing non-essential ones.  

---

## ⚠ **Key Considerations**  
⚠ **Works Only for EC2 Resources:** This action is **specific to EC2 instances** and does not apply to other AWS services.  
⚠ **Ensure Important Tags Are Preserved:** Always define the `preserve` list to avoid unintended tag loss.  
⚠ **Monitor Tag Usage Trends:** Use `put-metric` or AWS **Tag Policies** to track tag consumption over time.  

---

## 🛠 **Supported Tag-Trim Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `space`       | `integer`   | Number of tag slots to free up. **(Required)** |
| `preserve`    | `array`     | List of tags to retain on the resource. |
| `type`        | `enum`      | Must be `tag-trim`. **(Required)** |

---

## ✅ **Best Practices for Tag Management**  
💡 **Define a Tagging Strategy:** Establish a governance framework for **mandatory, optional, and transient tags**.  
💡 **Monitor Resource Tag Limits:** Use Cloud Custodian or AWS Config to track **tag usage trends**.  
💡 **Combine with `tag` & `normalize-tag`:** **First trim tags (`tag-trim`), then enforce correct tagging (`tag`, `normalize-tag`)**.  

---

## 🔹 **Webhook: Trigger External APIs from Cloud Custodian**  

### ✨ **What is Webhook?**  
The `webhook` action in Cloud Custodian **calls an external API (webhook)** with resource and policy details. This enables **integration with external systems**, such as logging platforms, ticketing systems, or automation tools.  

**Common Use Cases:**  
✅ **Trigger External Workflows** – Notify external systems when a policy is enforced.  
✅ **Send Custom Alerts** – Push events to third-party monitoring or incident response platforms.  
✅ **Automate Remediation** – Call a webhook to execute automated corrective actions.  

---

## 🔍 **How It Works**  
1️⃣ **Cloud Custodian filters resources** based on policy conditions.  
2️⃣ **Extracts relevant attributes** using JMESPath queries (`query-params`).  
3️⃣ **Sends an HTTP request** (`POST`, `GET`, `PUT`, etc.) to a specified webhook (`url`).  
4️⃣ **Optionally includes a payload** (`body`) with resource data.  

---

## 📝 **Example: Send EC2 Resource Data to Webhook**  
This policy **calls an external webhook when an EC2 instance matches the filters**, sending the resource and policy name as query parameters.  

```yaml
policies:
  - name: call-webhook
    resource: ec2
    description: |
      Call webhook with list of resource groups
    actions:
      - type: webhook
        url: http://foo.com
        query-params:
          resource_name: resource.name
          policy_name: policy.name
```

🔹 **What Happens?**  
📌 When an EC2 instance **matches the policy**, Cloud Custodian **sends an HTTP request to `http://foo.com`**.  
📌 The request **includes the resource name and policy name as query parameters**.  

---

## 📝 **Example: Send a JSON Payload to a Webhook**  
This policy **sends a structured JSON payload to a webhook** for external processing.  

```yaml
policies:
  - name: notify-external-system
    resource: s3
    filters:
      - "tag:Compliance": absent
    actions:
      - type: webhook
        url: https://webhook.example.com/api
        method: POST
        headers:
          Content-Type: application/json
          Authorization: Bearer YOUR_TOKEN
        body: |
          {
            "bucket": "{{ resource.Name }}",
            "region": "{{ resource.Region }}",
            "policy": "{{ policy.name }}"
          }
```

🔹 **What Happens?**  
📌 If an **S3 bucket is missing the `Compliance` tag**, Cloud Custodian **sends a `POST` request to `https://webhook.example.com/api`**.  
📌 The request includes **a JSON body** with details about the affected S3 bucket.  
📌 The webhook **can process the request**, log it, or trigger an automated response.  

---

## 🎯 **Why Use Webhook?**  
✅ **Integrates Cloud Custodian with External Systems:** Send real-time alerts to ITSM tools, SIEM solutions, or custom automation scripts.  
✅ **Supports Custom Headers & Authentication:** Define headers (`Authorization`, `Content-Type`) for secure API calls.  
✅ **Flexible Data Formats:** Send data via **query parameters or a JSON body**.  
✅ **Batch Processing Available:** Reduce API calls by **batching multiple resources into a single request**.  

---

## ⚠ **Key Considerations**  
⚠ **Ensure Webhook Reliability:** External APIs **must handle incoming requests** efficiently.  
⚠ **Rate Limits & API Quotas:** Check the webhook’s rate limits to avoid throttling.  
⚠ **Secure Webhook Endpoints:** Use **authentication, SSL (HTTPS), and access controls** to prevent misuse.  

---

## 🛠 **Supported Webhook Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `url`         | `string`   | The webhook URL to call. **(Required)** |
| `method`      | `string`   | HTTP method (`POST`, `GET`, `PUT`, `PATCH`, `DELETE`). Default: `POST`. |
| `headers`     | `object`   | Custom HTTP headers (e.g., `Authorization`, `Content-Type`). |
| `query-params` | `object`  | Query string parameters populated from JMESPath expressions. |
| `body`        | `string`   | JSON-formatted request payload. |
| `batch`       | `boolean`  | If `true`, batches multiple resource events into a single request. |
| `batch-size`  | `number`   | Number of resources per batch request. |

---

## ✅ **Best Practices for Webhook Integrations**  
💡 **Use Secure APIs:** Ensure the webhook **supports authentication and HTTPS**.  
💡 **Batch Requests for Efficiency:** Reduce API calls by **processing multiple resources at once**.  
💡 **Handle Webhook Failures Gracefully:** Implement **retries or logging mechanisms** in case of failures.  
💡 **Combine with Notification Services:** Use `webhook` **alongside `notify` for complete alerting workflows**.  

---

