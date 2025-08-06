## 🛰️ CloudWatch Events (CWE) Integration with Cloud Custodian
<!-- ai:aws-cwe-integration -->

---

### 📌 Overview

**Amazon CloudWatch Events (CWE)** is a real-time event delivery service that enables automated responses to changes in your AWS environment. It supports various event sources, including:

- **CloudTrail API Activity** – Tracks all AWS API calls for audit and response.
- **EC2 Instance Status Changes** – Detects system or instance-level events.
- **Auto Scaling Group Events** – Monitors lifecycle changes in scaling activities.
- **Scheduled (Cron) Events** – Triggers actions on a defined interval (e.g., hourly, daily).

---

### 🤖 Real-Time Policy Enforcement with Custodian

Cloud Custodian integrates tightly with CWE to enable **real-time, serverless execution of policies** through AWS Lambda.

Each policy is deployed as an independent Lambda function and is automatically triggered based on the defined event source. This architecture allows organizations to:

- Enforce compliance immediately at the time of resource creation
- Auto-tag or quarantine resources before they become active
- Eliminate the lag between resource provisioning and policy enforcement

> ✅ This model helps ensure **mandatory compliance**, particularly for high-risk resources like EC2 or IAM.

---

### ⚙️ How Custodian Executes on Events

When a CloudWatch Event is triggered:

1. **Custodian captures the event** payload.
2. It **rebuilds the resource’s current state** using live AWS APIs.
3. The resource is evaluated against the policy’s **filters**.
4. If conditions match, Custodian executes the specified **actions**.

This workflow allows for fine-grained control and immediate intervention, based on actionable events across your AWS infrastructure.

---

### 💡 Example: Auto-Tag EC2 Instances at Launch

```yaml
policies:
  - name: ec2-tag-on-launch
    resource: ec2
    mode:
      type: cloudtrail
      events:
        - RunInstances
    actions:
      - type: mark
        tag: foo
        value: bar
```

This policy:
- Triggers automatically when an EC2 instance is launched via the **RunInstances** API call.
- Applies the tag `foo=bar` to the new instance before it becomes operational.

---

### 🧠 Understanding the Event Mapping

For full control over custom API events, use an expanded form with explicit mapping:

```yaml
events:
  - source: ec2.amazonaws.com
    event: RunInstances
    ids: "responseElements.instancesSet.items[].instanceId"
```

- `source`: Identifies the AWS service emitting the event.
- `event`: Specifies the exact API operation to monitor.
- `ids`: Uses [JMESPath](https://jmespath.org/) to extract relevant resource identifiers from the event payload.

> ℹ️ This expanded form is useful for less common APIs where Custodian does not provide a built-in shortcut.

---

### 🚀 Fast Execution & Low Latency

Policies triggered via CWE operate with low-latency, often within **a few seconds (P99 SLA)** from the time the AWS event is generated. This enables:

- **Proactive resource management**
- **Minimal exposure windows**
- **Smooth integration with security and compliance pipelines**

---

### ✅ Summary

- **CloudWatch Events (CWE)** enables **real-time, event-driven policy execution** in Cloud Custodian.
- Policies run as **independent Lambda functions**, triggered automatically by AWS events.
- **CloudTrail events** allow broad and granular policy control across AWS services.
- Use shortcut syntax or the detailed `source`, `event`, and `ids` structure for custom triggers.
- Supports fast response times to reduce risk and automate compliance from the moment resources are created.

---

Here's the **clean, AI-friendly, and improved version** of the **EC2 Instance State Events** section, matching the tone and structure of the earlier CloudWatch Events section:

---

```markdown
## ⚡ EC2 Instance State Events Integration
<!-- ai:aws-ec2-instance-state-events -->

---

### 📌 Overview

Cloud Custodian supports **EC2 instance state events**, allowing policies to react in real time when an instance transitions through specific lifecycle states (such as `pending`, `running`, `stopped`, or `terminated`).

This mode enables organizations to **enforce policies before an EC2 instance becomes fully operational**, helping prevent non-compliant infrastructure from being used.

---

### 🚀 Use Case: Enforcing Encrypted EBS Volumes on Launch

You can define a policy that triggers during the `pending` state (right after an EC2 instance is launched, but before it is running), allowing you to:

- Inspect the attached volumes
- Check for encryption
- Terminate non-compliant instances before they become accessible

---

### 💡 Example: Terminate EC2 Instances with Unencrypted EBS Volumes

```yaml
policies:
  - name: ec2-require-encrypted-volumes
    resource: ec2
    mode:
      type: ec2-instance-state
      events:
        - pending
    filters:
      - type: ebs
        key: Encrypted
        value: False
    actions:
      - mark
      - terminate
```

Explanation:
- **mode.type**: `ec2-instance-state` indicates this policy listens for EC2 lifecycle events.
- **events**: List of states to respond to (e.g., `pending`, `running`, etc.).
- **filters**: Evaluates if the instance has any attached EBS volumes that are not encrypted.
- **actions**:
  - `mark`: Optionally tag the instance as non-compliant.
  - `terminate`: Immediately stop and delete the instance before it is usable.

> ⚠️ This is a strong enforcement mechanism — use it carefully in production environments.

---

### ✅ Summary

- **EC2 Instance State Events** provide real-time lifecycle hooks.
- Policies can react to key instance states like `pending` or `running`.
- Enables proactive enforcement (e.g., encryption, tagging, security checks) **before exposure**.
- Recommended for security-critical policies where prevention is better than remediation.

---
```

Here’s the improved and structured documentation for **Periodic Function (Scheduled Execution)** support in Cloud Custodian, in line with the format we're using — AI-friendly, clear, and human-readable:

---

```markdown
## ⏱️ Scheduled (Periodic) Execution
<!-- ai:aws-periodic-scheduled-mode -->

---

### 📌 Overview

Cloud Custodian supports **scheduled policy execution** using AWS Lambda and CloudWatch Events (now EventBridge). This mode is ideal for:

- **Regular audits** (e.g., daily scans for non-compliant resources)
- **Cost optimization routines**
- **Security posture checks on a schedule**

You can use either:
- **`rate()` syntax** for intervals (e.g., hourly, daily)
- **`cron()` expressions** for precise scheduling (e.g., at 3 AM every Sunday)

---

### 🔁 When to Use

Use **periodic mode** when you want to:

- Perform recurring checks without needing manual triggers
- Avoid event-based complexity (like CloudTrail)
- Catch drift or misconfigurations that weren’t triggered by an event

---

### 🔐 IAM Role Configuration

You must specify the IAM role the Lambda function will assume during execution. There are **two options**:

1. **Using `--assume` in CLI**  
   When running via CLI with `--assume`, the role passed will be attached to the Lambda automatically:
   ```bash
   custodian run --assume arn:aws:iam::111122223333:role/MyExecutionRole policy.yml
   ```
   In this case, you do **not** need to define `role` inside the policy.

2. **Defining Role in the Policy**  
   If not using `--assume`, you must define the `role` directly in the policy’s `mode` block.

   > ✅ Use `{account_id}` placeholder in the role ARN to make the policy **multi-account ready**:
   ```yaml
   role: arn:aws:iam::{account_id}:role/custodian-lambda-role
   ```

---

### 💡 Example: Daily S3 Compliance Check

```yaml
policies:
  - name: s3-bucket-check
    resource: s3
    mode:
      type: periodic
      schedule: "rate(1 day)"
      role: arn:aws:iam::{account_id}:role/some-role
```

This policy:
- Runs **once per day**
- Evaluates all S3 buckets for compliance (you can add filters/actions as needed)
- Uses a cross-account compatible execution role

---

### 🧠 Notes

- Lambda functions have a **maximum timeout of 15 minutes**. Ensure your policy completes within that time.
- Cloud Custodian will **automatically package and deploy** the policy as a Lambda function.
- Scheduled policies are fully **serverless** and scale based on the AWS region/account.

---

### ✅ Summary

- **Periodic mode** is used for scheduled, recurring policy execution.
- Supports both `rate()` and `cron()` expressions for flexible timing.
- IAM role must be defined unless `--assume` is used at deployment time.
- `{account_id}` placeholder allows reusable policies across multiple accounts.
- Best suited for **ongoing governance**, **cost audits**, and **security hygiene**.

---
```

Here’s the **enhanced and AI-friendly documentation** for **EventBridge Scheduler** support in Cloud Custodian, refined for clarity and organized for both human readers and automated systems.

---

```markdown
## 📅 EventBridge Scheduler Integration
<!-- ai:aws-eventbridge-scheduler-mode -->

---

### 📌 Overview

Cloud Custodian supports **AWS EventBridge Scheduler**, a modern alternative to CloudWatch Events for advanced scheduling of Lambda-executed policies. This integration supports:

- `rate()` and `cron()` expressions
- **One-time schedules**
- **Timezone support**
- **Start and end dates**

EventBridge Scheduler enables **more granular control** over scheduled policy execution, making it ideal for precise, time-bound governance scenarios.

---

### 🕓 Key Features

- **Flexible Scheduling Types**: Use `rate`, `cron`, or one-time schedules.
- **Time-bound Execution**: Define optional `start-date` and `end-date` in ISO 8601 format.
- **Timezone-Aware**: Use any valid [IANA timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) (e.g., `Asia/Seoul`, `America/New_York`).
- **Schedule Groups**: Organize schedules using `group-name`. The group must pre-exist in EventBridge Scheduler.
- **Scheduler Execution Role**: A dedicated role (`scheduler-role`) is required to allow EventBridge Scheduler to invoke the Lambda function.

---

### 🔐 Required IAM Roles

You must specify:
- `role`: The **Lambda execution role** used by the policy.
- `scheduler-role`: The **EventBridge Scheduler role** that invokes the Lambda.

Both roles must be defined explicitly in the policy.

---

### 💡 Example: Scheduled Daily S3 Scan with Timezone & Group

```yaml
policies:
  - name: s3-bucket-check
    resource: s3
    mode:
      type: schedule
      role: arn:aws:iam::{account_id}:role/some-role
      schedule: "rate(1 day)"
      scheduler-role: arn:aws:iam::{account_id}:role/some-scheduler-role
      timezone: Asia/Seoul
      group-name: MySchedGroup
      start-date: "2024-04-04T00:05:23"
```

This policy:
- Runs daily using EventBridge Scheduler
- Starts from April 4th, 2024 at 00:05:23 in the `Asia/Seoul` timezone
- Is associated with the schedule group `MySchedGroup`

---

### 🧠 Operational Note: Switching Between Modes

When switching a policy between `periodic` mode and `schedule` mode:

- **Old CloudWatch rules or EventBridge schedules are not automatically removed** by `custodian run`.
- Custodian cannot detect historical mode configurations.
  
To clean up old Lambda functions, rules, and schedules:

1. **Comment out** the policy in your YAML file.
2. Run the cleanup tool:
   ```bash
   python tools/ops/mugc.py
   ```
3. **Uncomment** the policy and redeploy:
   ```bash
   custodian run -s out policy.yml
   ```

This ensures no orphaned schedules remain after switching modes.

---

### ✅ Summary

- Use **EventBridge Scheduler** for precise, flexible, timezone-aware scheduling.
- Supports one-time and recurring schedules.
- Requires both a **Lambda role** and a **scheduler role**.
- Can be organized into **schedule groups**.
- Cleanup of previous mode schedules is manual unless using `mugc.py`.

---
```

Here's the enhanced and AI-structured documentation for **Event Pattern Filtering** in Cloud Custodian — precise, well-organized, and aligned with the format we've been using:

---

```markdown
## 🎯 Event Pattern Filtering
<!-- ai:aws-event-pattern-filtering -->

---

### 📌 Overview

AWS **CloudWatch Events (EventBridge)** supports advanced **content-based filtering** using **event patterns**, allowing you to match against the content of the event payload itself. Cloud Custodian exposes this functionality using the optional `pattern` key in the `mode` block of a policy.

This provides **fine-grained control** over when a Lambda policy should be invoked — avoiding unnecessary executions and reducing noise.

---

### 🧩 How It Works in Cloud Custodian

In Custodian:
- The `pattern` is merged with the **default event pattern** generated by the tool.
- If the final pattern does **not match an incoming event**, the policy's Lambda **will not be triggered**.

> ✅ Pattern filtering happens **before** the Lambda is invoked, saving compute and preventing unwanted evaluations.

---

### 📖 Resources

- AWS EventBridge Content Filtering:  
  https://docs.aws.amazon.com/eventbridge/latest/userguide/content-filtering-with-event-patterns.html  
- AWS Blog on Advanced Event Rules:  
  https://aws.amazon.com/blogs/compute/reducing-custom-code-by-using-advanced-rules-in-amazon-eventbridge/

---

### 💡 Example: Ignore Subnet Creation by Specific User

```yaml
policies:
  - name: subnet-detect
    resource: aws.subnet
    mode:
      type: cloudtrail
      role: CustodianDemoRole
      events:
        - source: ec2.amazonaws.com
          event: CreateSubnet
          ids: responseElements.subnet.subnetId
      pattern:
        detail:
          userIdentity:
            userName: [{'anything-but': 'deputy'}]
```

Explanation:
- This policy listens for the `CreateSubnet` API call.
- But it **only triggers** if the action was **not performed** by the IAM user named `deputy`.
- This is controlled by the **pattern filtering** under `mode.pattern`.

> 🧠 Use of `anything-but` allows you to **exclude certain users or roles** from triggering the policy.

---

### ✅ Summary

- **Pattern filtering** allows deeper control over when a Custodian policy Lambda should run.
- The `pattern` is merged with the default event rule, applying pre-invocation filtering.
- Supports all native EventBridge pattern matching features (e.g., string matching, negation, prefix filtering).
- Helps avoid unnecessary policy execution and enhances performance/security precision.

---
```

Here’s the final, polished section on **AWS Config Rules support** in Cloud Custodian — structured for AI-parsing and optimized for developer readability.

---

```markdown
## 🧬 AWS Config Rule Integration
<!-- ai:aws-config-rule-mode -->

---

### 📌 Overview

Cloud Custodian supports deploying policies as **AWS Config custom rules**, allowing enforcement of compliance whenever a configuration change is detected in your AWS environment.

This mode enables **declarative compliance-as-code** without requiring direct event wiring — AWS Config tracks changes and invokes the associated Lambda function automatically.

> ⏱️ Typical event delivery latency is **1–15 minutes**, though **tag-only changes** may take longer (up to 6 hours).

---

### 🎯 Use Case

Use Config Rule mode when you want:
- Policies to automatically evaluate **on configuration change**
- Native integration with the **AWS Config Console**
- Persistent compliance tracking for **auditing and reporting**

---

### ⚙️ IAM Role Requirements

To use this mode, your Lambda execution role must have the following permissions:

- `AWSLambdaBasicExecutionRole`
- `AWSConfigRulesExecutionRole`
- Any additional permissions needed to evaluate filters or perform actions (e.g., `ec2:StopInstances`)

The role should be specified in the `mode.role` block.

---

### 💡 Example: EC2 Config Rule Based on a Tag

```yaml
policies:
  - name: my-first-policy
    mode:
      type: config-rule
      role: arn:aws:iam::123456789012:role/some-role
    resource: ec2
    filters:
      - "tag:Custodian": present
    actions:
      - stop
```

Explanation:
- When **AWS Config** detects a configuration change on an EC2 instance,
- It invokes the **Lambda function deployed by Cloud Custodian**,
- If the EC2 instance has a tag named `Custodian`, it will be stopped.

---

### ⚙️ Setup Steps

1. **Enable AWS Config** in your AWS account:
   - Go to the **AWS Config Console**
   - If you see the welcome/setup screen, complete the onboarding

2. **Deploy the policy using Cloud Custodian**:
   ```bash
   custodian run -s . custodian.yml
   ```

3. ✅ You should see output like:
   ```
   INFO Provisioning policy lambda my-first-policy
   INFO Publishing custodian policy lambda function custodian-my-first-policy
   ```

4. **Check AWS Console**:
   - Go to **AWS Lambda** to confirm the function was created
   - Go to **AWS Config > Rules** to see the new custom rule

---

### 🧪 Test Your Config Rule

To validate the policy:

- Launch an EC2 instance with a `Custodian` tag (any value)
- Wait for AWS Config to detect the change (can take 15 minutes or more)
- The instance should automatically stop based on your policy

> 🧼 Make sure no leftover resources (like EC2s from previous quickstarts) have the `Custodian` tag before testing.

---

### ✅ Summary

- **Config Rule mode** allows policies to run automatically based on resource configuration changes.
- Native integration with **AWS Config** enables compliance tracking.
- Best suited for **ongoing enforcement**, **auditing**, and **posture management**.
- Requires specific IAM roles and proper setup of AWS Config in the account.

---
```
Here is the improved and well-structured section on **Lambda Configuration** in Cloud Custodian — consistent with the rest of the Lambda execution modes, and designed to be AI-friendly and reader-focused.

---

```markdown
## ⚙️ Lambda Configuration Options
<!-- ai:aws-lambda-configuration-options -->

---

### 📌 Overview

Cloud Custodian allows you to fully configure deployed Lambda functions using key-value options under the `mode` block of a policy. These settings directly map to standard **AWS Lambda configuration parameters**.

You can customize properties such as:
- IAM execution roles
- Tags
- Memory and timeout settings (if needed)
- Environment variables (via extended settings)

> 🧭 For a full list of configurable options, refer to:  
> [AWS Lambda Function Configuration Documentation](https://docs.aws.amazon.com/lambda/latest/dg/configuration-console.html)

---

### 🧰 Commonly Used Configuration Options

The following example demonstrates how to configure common Lambda attributes when deploying a Custodian policy using the `cloudtrail` execution mode.

```yaml
mode:
  type: cloudtrail
  events:
    - CreateBucket

  ##### ROLE #####
  # IAM execution role for the Lambda function
  # Option 1: Specify by name
  role: Custodian
  # Option 2: Or use full ARN
  # role: arn:aws:iam::123456789012:role/Custodian

  ##### TAGS #####
  # Tags assigned to the Lambda function
  tags:
    Application: Custodian
    CreatedBy: CloudCustodian
```

---

### 🔐 Role Specification

- The `role` defines which **IAM role** the Lambda will assume during execution.
- You can specify it either by **role name** or as a **full ARN**.
- The role must have permissions appropriate to the policy’s actions (e.g., `s3:PutBucketTagging`, `ec2:StopInstances`).

---

### 🏷️ Lambda Tags

You can assign **tags** to the Lambda function using the `tags:` block. This is helpful for:
- Identifying Lambda ownership
- Tracking automation scope
- Applying lifecycle or cost management policies

Example:
```yaml
tags:
  Environment: Production
  ManagedBy: CloudCustodian
```

---

### ✅ Summary

- Cloud Custodian exposes direct configuration of AWS Lambda properties under the `mode` block.
- You can control IAM roles, tags, and other Lambda metadata.
- Most commonly used with `cloudtrail`, `periodic`, `schedule`, `config-rule`, and `ec2-instance-state` modes.
- These settings follow standard AWS Lambda configuration behavior and naming conventions.

---
```

Here is the final enhanced and structured section for **Execution Options** in Cloud Custodian Lambda policies. This completes the Lambda execution model documentation — all in a consistent, AI-friendly, and readable format.

---

```markdown
## 🛠️ Execution Options in Lambda
<!-- ai:aws-lambda-execution-options -->

---

### 📌 Overview

When running policies in **AWS Lambda**, Cloud Custodian uses a different execution environment compared to local CLI execution. While some defaults are preset, you can override them using the `execution-options` block inside the `mode` configuration.

These options mirror flags used in the CLI (`--region`, `--assume`, `--output-dir`, etc.) and control how Custodian behaves **at runtime inside Lambda**.

---

### ⚙️ Default Lambda Behavior

Without any overrides, Lambda policies behave as follows:

- ✅ **Metrics** collection is enabled
- 📁 **Output directory** is randomly set under `/tmp/`
- ❌ **Caching** of AWS resource data is **disabled**
- 🔐 **Account ID** is automatically retrieved using `sts:GetCallerIdentity`
- 🌍 **Region** is auto-set based on the Lambda’s `AWS_DEFAULT_REGION` environment variable

---

### 🧰 Available `execution-options` Keys

You can customize any of the following:

| Key              | Description |
|------------------|-------------|
| `region`         | Override AWS region |
| `cache`          | Enable or specify cache location |
| `profile`        | AWS CLI profile name (not typically used in Lambda) |
| `account_id`     | Override detected account ID |
| `assume_role`    | Cross-account execution role ARN |
| `log_group`      | Custom CloudWatch log group |
| `metrics`        | Set to `aws` or `none` |
| `output_dir`     | Override `/tmp` path |
| `cache_period`   | Set custom cache TTL (in seconds) |
| `dryrun`         | Enable dry-run mode (no changes made) |

---

### 🔄 Example: Cross-Account Execution

```yaml
policies:
  - name: my-first-policy-cross-account
    resource: ec2
    mode:
      type: periodic
      schedule: "rate(1 day)"
      role: arn:aws:iam::123456789012:role/lambda-role
      execution-options:
        assume_role: arn:aws:iam::210987654321:role/target-role
        metrics: aws
    filters:
      - "tag:Custodian": present
    actions:
      - stop
```

This policy:
- Is scheduled daily using periodic mode
- Executes in **Account A**, but uses `assume_role` to manage resources in **Account B**
- Sends metrics using the **assumed role**

---

### 🧭 Execution Mode Constraints

Not all modes support cross-account or cross-region execution:

| Mode        | Cross-Account | Cross-Region |
|-------------|----------------|----------------|
| `config-rule` | ❌ No            | ✅ Yes           |
| `cloudtrail`  | ❌ No            | ❌ No            |
| `periodic`    | ✅ Yes           | ✅ Yes           |

> ✅ Use `periodic` mode when cross-account or multi-region execution is needed.

---

### ✅ Summary

- `execution-options` allow you to override Custodian's runtime behavior inside Lambda.
- Useful for **cross-account execution**, **output control**, **metrics**, and **dry-run testing**.
- Only certain execution modes support advanced configurations like `assume_role`.

---
```

