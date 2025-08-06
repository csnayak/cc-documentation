## Execution Mode: `pull`

### Description
The `pull` mode executes policies manually by querying cloud resources on demand. It is the **default mode** when `mode` is not specified in the policy. The execution is triggered by running `custodian run` from the command line.

---

### Usage Characteristics

#### ✅ What You Can Do
- Run policies manually from the CLI.
- Use real-time queries to fetch resource state.
- Perform local testing, debugging, or one-time audits.
- Integrate into automation scripts or tools where manual invocation is preferred.

#### ❌ What You Can't Do
- Schedule periodic runs.
- Trigger actions automatically based on cloud events.
- Deploy to serverless infrastructure for hands-free execution.

---

### CLI Example

```bash
custodian run --output-dir=./out policy.yml
```

---

### Policy Example – Tag EC2 Instances Missing `Environment`

```yaml
policies:
  - name: tag-missing-environment
    resource: aws.ec2
    mode:
      type: pull
    filters:
      - "tag:Environment": absent
    actions:
      - tag:
          tags:
            Environment: Unknown
```

---

### Optional Declaration

You can omit the `mode` section completely. Cloud Custodian will still run in pull mode by default.

**Without `mode`:**
```yaml
policies:
  - name: default-pull-mode
    resource: aws.ebs
    filters:
      - Attachments: []
    actions:
      - delete
```

---

## Schema – `pull`

| Field | Type | Allowed Values | Required | Description |
|-------|------|----------------|----------|-------------|
| `type` | `string` | `pull` | ✅ Yes | Defines execution type. `pull` is default and runs manually using CLI. |

**YAML Schema Snippet**:
```yaml
mode:
  type: pull
```

---

## Execution Mode: `asg-instance-state`

### Description
The `asg-instance-state` mode is used to trigger Cloud Custodian policies when an **Auto Scaling Group (ASG) lifecycle event** occurs for an EC2 instance.

This execution mode uses **AWS Lambda** to react to instance-level state changes within an ASG such as instance launch or termination events.

It supports standard event types defined by the Auto Scaling lifecycle hook mechanism.

---

### Supported Events

The following ASG instance state events are supported:

- `launch-success`
- `launch-failure`
- `terminate-success`
- `terminate-failure`

These can be specified in the `events` property of the `mode` block.

---

### Use Cases

#### ✅ What You Can Do
- Automatically remediate or tag EC2 instances based on ASG launch/termination events.
- Track and enforce policies on ASG activity in real-time.
- Capture failed launches or terminations for further analysis.

#### ❌ What You Can't Do
- Use for non-ASG triggered instance state changes.
- Run this mode outside of AWS Lambda.
- Trigger policies on general EC2 lifecycle events (use CloudTrail or EventBridge modes instead).

---

### Policy Example – Tag Instances on Launch

```yaml
policies:
  - name: tag-asg-instance
    resource: aws.ec2
    mode:
      type: asg-instance-state
      events:
        - launch-success
    filters:
      - "tag:Owner": absent
    actions:
      - tag:
          tags:
            Owner: "unknown"
```

---

## Schema – `asg-instance-state`

| Field               | Type      | Allowed Values                                      | Required | Description |
|--------------------|-----------|-----------------------------------------------------|----------|-------------|
| `type`             | `string`  | `asg-instance-state`                                | ✅ Yes   | Defines the execution mode. |
| `events`           | `array`   | `launch-success`, `launch-failure`, `terminate-success`, `terminate-failure` | No | ASG lifecycle events that trigger the policy. |
| `concurrency`      | `integer` | —                                                   | No       | Controls the number of concurrent Lambda executions. |
| `dead_letter_config` | `object`| —                                                   | No       | Configuration for failed message delivery (DLQ). |
| `environment`      | `object`  | —                                                   | No       | Environment variables for the Lambda function. |
| `execution-options`| `object`  | —                                                   | No       | Additional execution options. |
| `function-prefix`  | `string`  | —                                                   | No       | Prefix for naming the Lambda function. |
| `handler`          | `string`  | —                                                   | No       | Lambda function handler. |
| `kms_key_arn`      | `string`  | —                                                   | No       | KMS key for encrypting environment variables. |
| `layers`           | `array`   | list of strings                                     | No       | Lambda layers to attach. |
| `member-role`      | `string`  | —                                                   | No       | Role for cross-account member execution. |
| `memory`           | `number`  | —                                                   | No       | Memory allocation for the Lambda function (MB). |
| `packages`         | `array`   | list of strings                                     | No       | Python packages to include in the Lambda deployment. |
| `pattern`          | `object`  | — (must have at least one key)                     | No       | Additional event pattern matching. |
| `role`             | `string`  | —                                                   | No       | IAM role to associate with the Lambda. |
| `runtime`          | `string`  | `python3.8`, `python3.9`, `python3.10`, `python3.11`, `python3.12` | No | Lambda runtime version. |
| `security_groups`  | `array`   | —                                                   | No       | List of security groups to associate with the Lambda. |
| `subnets`          | `array`   | —                                                   | No       | Subnets for running the Lambda in VPC mode. |
| `tags`             | `object`  | —                                                   | No       | Tags to apply to the Lambda function. |
| `timeout`          | `number`  | —                                                   | No       | Maximum execution time for the Lambda (in seconds). |
| `tracing_config`   | `object`  | —                                                   | No       | AWS X-Ray tracing configuration. |

---

## Execution Mode: `cloudtrail`

### Description
The `cloudtrail` mode enables **event-driven policy execution** in response to specific **CloudTrail API calls**. This mode deploys the policy as an AWS Lambda function and uses **CloudWatch Event Rules** (now EventBridge) to listen for matched CloudTrail events.

When an event such as an instance launch or bucket creation is logged, the policy is triggered in near real-time.

---

### Use Cases

#### ✅ What You Can Do
- Enforce real-time governance based on API activity.
- Respond immediately to specific resource creation, modification, or deletion events.
- Monitor security-sensitive API calls (e.g., IAM changes, public access granted, encryption disabled).

#### ❌ What You Can't Do
- Poll or scan existing resources on a schedule (use `pull` or `periodic` for that).
- Work outside the scope of CloudTrail-supported events.
- Trigger based on resource state without an API call.

---

### Event Formats Supported

The `events` field supports two formats:

1. **Simple Event Name**:
   ```yaml
   events:
     - RunInstances
   ```

2. **Detailed Event Matcher**:
   ```yaml
   events:
     - source: ec2.amazonaws.com
       event: RunInstances
       ids: "responseElements.instancesSet.items[].instanceId"
   ```

---

### Policy Example – Tag EC2 on Launch

```yaml
policies:
  - name: tag-on-launch
    resource: aws.ec2
    mode:
      type: cloudtrail
      events:
        - RunInstances
    filters:
      - "tag:Owner": absent
    actions:
      - tag:
          tags:
            Owner: unknown
```

---

## Schema – `cloudtrail`

| Field               | Type      | Allowed Values / Description | Required | Description |
|--------------------|-----------|------------------------------|----------|-------------|
| `type`             | `string`  | `cloudtrail`                 | ✅ Yes   | Execution mode identifier. |
| `events`           | `array`   | List of event names or event objects | No | CloudTrail API events that trigger the policy. |
| `delay`            | `integer` | —                            | No       | Delay in seconds before processing the event. |
| `concurrency`      | `integer` | —                            | No       | Maximum concurrent Lambda executions. |
| `dead_letter_config` | `object` | —                            | No       | Configuration for handling failed Lambda executions. |
| `environment`      | `object`  | —                            | No       | Environment variables for the Lambda. |
| `execution-options`| `object`  | —                            | No       | Additional execution settings. |
| `function-prefix`  | `string`  | —                            | No       | Prefix for Lambda function naming. |
| `handler`          | `string`  | —                            | No       | Lambda handler (defaults usually apply). |
| `kms_key_arn`      | `string`  | —                            | No       | KMS key for encrypting environment vars. |
| `layers`           | `array`   | List of Lambda layers        | No       | Attach external layers to the Lambda. |
| `member-role`      | `string`  | —                            | No       | Cross-account execution role. |
| `memory`           | `number`  | —                            | No       | Memory size in MB for the Lambda. |
| `packages`         | `array`   | Python packages              | No       | Additional packages bundled with Lambda. |
| `pattern`          | `object`  | Must have at least one key   | No       | EventBridge pattern (for advanced filtering). |
| `role`             | `string`  | IAM role ARN                 | No       | Role assumed by the Lambda function. |
| `runtime`          | `string`  | `python3.8`, `3.9`, `3.10`, `3.11`, `3.12` | No | Python runtime version. |
| `security_groups`  | `array`   | —                            | No       | VPC security groups if Lambda is VPC-attached. |
| `subnets`          | `array`   | —                            | No       | Subnets for VPC Lambda execution. |
| `tags`             | `object`  | Key-value pairs              | No       | Tags applied to the Lambda function. |
| `timeout`          | `number`  | Seconds                      | No       | Lambda timeout. |
| `tracing_config`   | `object`  | —                            | No       | AWS X-Ray tracing configuration. |

---

## Execution Mode: `config-poll-rule`

### Description
The `config-poll-rule` mode allows a policy to be scheduled as an **AWS Config periodic rule** that evaluates compliance for resources. Unlike native AWS Config rules, this mode works for **any resource with a CloudFormation type**, even if it's not directly supported by AWS Config.

Cloud Custodian executes the policy on a **fixed schedule**, evaluates all matching resources, and submits the result (`COMPLIANT` or `NON_COMPLIANT`) to AWS Config.

This mode is useful when:
- A resource is not natively supported by AWS Config.
- You need to check compliance involving **related resources** (e.g., VPCs and their flow logs).
- You want the results visible in AWS Config dashboards and rules engine.

---

### Key Behavior

- Periodic execution managed by AWS Config.
- Evaluates resource state independently.
- Reports compliance back to Config.
- Uses a Lambda backend.

---

### Use Cases

#### ✅ What You Can Do
- Schedule compliance evaluations for resources not supported by native Config rules.
- Report evaluations to AWS Config for central tracking and alerts.
- Evaluate complex policies involving linked or indirect resource data.

#### ❌ What You Can't Do
- Use event-based triggers.
- Leverage AWS Config snapshot or event-based resource data directly.
- Skip AWS Config support check unless `ignore-support-check: true` is explicitly defined.

---

### Example 1 – VPC Flow Logs Compliance Check

```yaml
policies:
  - name: vpc-flow-logs
    resource: aws.vpc
    mode:
      type: config-poll-rule
      role: arn:aws:iam::{account_id}:role/ConfigLambdaRole
      ignore-support-check: true
      schedule: One_Hour
    filters:
      - not:
        - type: flow-logs
          destination-type: s3
          enabled: true
          status: active
          traffic-type: all
          destination: arn:aws:s3:::my-vpc-flow-bucket
```

---

### Example 2 – EC2 Instances Without Required Tags

```yaml
policies:
  - name: ec2-tag-compliance
    resource: aws.ec2
    mode:
      type: config-poll-rule
      role: arn:aws:iam::{account_id}:role/ConfigLambdaRole
      ignore-support-check: true
      schedule: Twelve_Hours
    filters:
      - or:
          - "tag:Environment": absent
          - "tag:Owner": absent
    actions:
      - type: mark-for-op
        op: stop
        days: 3
```

---

### Example 3 – Unencrypted EBS Volumes

```yaml
policies:
  - name: ebs-encryption-check
    resource: aws.ebs
    mode:
      type: config-poll-rule
      role: arn:aws:iam::{account_id}:role/ConfigLambdaRole
      ignore-support-check: true
      schedule: Six_Hours
    filters:
      - Encrypted: false
```

---

## Schema – `config-poll-rule`

### Raw Schema (YAML)

```yaml
type: object
properties:
  type:
    enum:
      - config-poll-rule
  schedule:
    enum:
      - One_Hour
      - Three_Hours
      - Six_Hours
      - Twelve_Hours
      - TwentyFour_Hours
  ignore-support-check:
    type: boolean
  role:
    type: string
  concurrency:
    type: integer
  dead_letter_config:
    type: object
  environment:
    type: object
  execution-options:
    type: object
  function-prefix:
    type: string
  handler:
    type: string
  kms_key_arn:
    type: string
  layers:
    type: array
    items:
      type: string
  member-role:
    type: string
  memory:
    type: number
  packages:
    type: array
    items:
      type: string
  pattern:
    type: object
    minProperties: 1
  runtime:
    enum:
      - python3.8
      - python3.9
      - python3.10
      - python3.11
      - python3.12
  security_groups:
    type: array
  subnets:
    type: array
  tags:
    type: object
  timeout:
    type: number
  tracing_config:
    type: object
required:
  - type
```

---

### Schema Table

| Field                  | Type      | Allowed Values / Description                              | Required | Description |
|-----------------------|-----------|-------------------------------------------------------------|----------|-------------|
| `type`                | `string`  | `config-poll-rule`                                          | ✅ Yes   | Execution mode identifier |
| `schedule`            | `string`  | `One_Hour`, `Three_Hours`, `Six_Hours`, `Twelve_Hours`, `TwentyFour_Hours` | No | Frequency of evaluation |
| `ignore-support-check`| `boolean` | —                                                           | No       | Bypass AWS Config native support check |
| `role`                | `string`  | IAM role ARN                                                | No       | IAM role assumed by Lambda |
| `concurrency`         | `integer` | —                                                           | No       | Lambda concurrency limit |
| `dead_letter_config`  | `object`  | —                                                           | No       | DLQ configuration |
| `environment`         | `object`  | —                                                           | No       | Environment variables for Lambda |
| `execution-options`   | `object`  | —                                                           | No       | Custom runtime execution flags |
| `function-prefix`     | `string`  | —                                                           | No       | Prefix for Lambda name |
| `handler`             | `string`  | —                                                           | No       | Lambda handler function |
| `kms_key_arn`         | `string`  | —                                                           | No       | KMS key for environment encryption |
| `layers`              | `array`   | List of strings                                             | No       | Additional Lambda layers |
| `member-role`         | `string`  | —                                                           | No       | Cross-account role |
| `memory`              | `number`  | —                                                           | No       | Lambda memory size (MB) |
| `packages`            | `array`   | List of strings                                             | No       | Extra Python packages |
| `pattern`             | `object`  | At least one property                                       | No       | Advanced matching pattern |
| `runtime`             | `string`  | Python versions: `python3.8` to `python3.12`                | No       | Lambda runtime |
| `security_groups`     | `array`   | —                                                           | No       | Security groups if Lambda is VPC-attached |
| `subnets`             | `array`   | —                                                           | No       | VPC subnets |
| `tags`                | `object`  | Key-value pairs                                             | No       | Lambda tags |
| `timeout`             | `number`  | Seconds                                                     | No       | Lambda timeout duration |
| `tracing_config`      | `object`  | —                                                           | No       | X-Ray tracing settings |



---

## Execution Mode: `config-rule`

### Description  
The `config-rule` mode registers a Cloud Custodian policy as an **AWS Config Managed Rule** using AWS Lambda. It is triggered **automatically** by AWS Config whenever a **resource undergoes a configuration change**.

This is the preferred method for resources **natively supported by AWS Config** and is tightly integrated with the AWS Config rule evaluation engine.

---

### Key Behavior

- **Triggered by AWS Config** on relevant configuration changes.
- Executes using **Lambda** behind the scenes.
- Suitable for **real-time compliance monitoring** of AWS-supported resource types.
- Automatically receives configuration snapshots as input.

---

### Use Cases

#### ✅ What You Can Do
- Monitor resource changes in near real-time.
- Report evaluation results (`COMPLIANT` / `NON_COMPLIANT`) directly in AWS Config.
- Maintain full compliance visibility across the AWS Config dashboard.

#### ❌ What You Can't Do
- Evaluate resources not natively supported by AWS Config.
- Use polling or schedule-based evaluation (use `config-poll-rule` instead).
- Use filters based on related resources not part of the configuration item.

---

### Example 1 – Enforce S3 Bucket Encryption

```yaml
policies:
  - name: s3-encryption-check
    resource: aws.s3
    mode:
      type: config-rule
      role: arn:aws:iam::{account_id}:role/ConfigLambdaRole
    filters:
      - type: encryption
        enabled: false
```

---

### Example 2 – Require Tag on RDS Instances

```yaml
policies:
  - name: rds-tag-enforcement
    resource: aws.rds
    mode:
      type: config-rule
      role: arn:aws:iam::{account_id}:role/ConfigLambdaRole
    filters:
      - "tag:Environment": absent
```

---

### Example 3 – Check IAM Role Inline Policies

```yaml
policies:
  - name: iam-inline-policy-check
    resource: aws.iam-role
    mode:
      type: config-rule
      role: arn:aws:iam::{account_id}:role/ConfigLambdaRole
    filters:
      - type: has-inline-policy
        value: true
```

---

## Raw Schema – `config-rule`

```yaml
type: object
properties:
  type:
    enum:
      - config-rule
  concurrency:
    type: integer
  dead_letter_config:
    type: object
  environment:
    type: object
  execution-options:
    type: object
  function-prefix:
    type: string
  handler:
    type: string
  kms_key_arn:
    type: string
  layers:
    type: array
    items:
      type: string
  member-role:
    type: string
  memory:
    type: number
  packages:
    type: array
    items:
      type: string
  pattern:
    type: object
    minProperties: 1
  role:
    type: string
  runtime:
    enum:
      - python3.8
      - python3.9
      - python3.10
      - python3.11
      - python3.12
  security_groups:
    type: array
  subnets:
    type: array
  tags:
    type: object
  timeout:
    type: number
  tracing_config:
    type: object
required:
  - type
```

---

## Schema Table – `config-rule`

| Field               | Type      | Allowed Values / Description                             | Required | Description |
|--------------------|-----------|------------------------------------------------------------|----------|-------------|
| `type`             | `string`  | `config-rule`                                              | ✅ Yes   | Execution mode identifier |
| `role`             | `string`  | IAM role ARN                                               | No       | Role assumed by Lambda |
| `concurrency`      | `integer` | —                                                          | No       | Lambda concurrency setting |
| `dead_letter_config` | `object`| —                                                          | No       | DLQ setup for failed executions |
| `environment`      | `object`  | —                                                          | No       | Lambda environment variables |
| `execution-options`| `object`  | —                                                          | No       | Additional runtime configuration |
| `function-prefix`  | `string`  | —                                                          | No       | Prefix used for Lambda function name |
| `handler`          | `string`  | —                                                          | No       | Lambda handler override |
| `kms_key_arn`      | `string`  | —                                                          | No       | KMS key for environment variable encryption |
| `layers`           | `array`   | List of strings                                            | No       | Lambda layers to attach |
| `member-role`      | `string`  | —                                                          | No       | IAM role used for member accounts |
| `memory`           | `number`  | —                                                          | No       | Lambda memory allocation (MB) |
| `packages`         | `array`   | List of strings                                            | No       | Python packages to include in Lambda bundle |
| `pattern`          | `object`  | Must have at least one property                            | No       | Custom event pattern |
| `runtime`          | `string`  | `python3.8`, `3.9`, `3.10`, `3.11`, `3.12`                 | No       | Lambda runtime version |
| `security_groups`  | `array`   | —                                                          | No       | VPC security groups |
| `subnets`          | `array`   | —                                                          | No       | Subnets for VPC Lambda setup |
| `tags`             | `object`  | Key-value map                                              | No       | Tags for the Lambda function |
| `timeout`          | `number`  | Seconds                                                    | No       | Lambda timeout setting |
| `tracing_config`   | `object`  | —                                                          | No       | AWS X-Ray tracing configuration |

---

## Execution Mode: `ec2-instance-state`

### Description  
The `ec2-instance-state` mode executes a Cloud Custodian policy using **AWS Lambda** whenever an **EC2 instance changes its state**. This mode supports all standard EC2 lifecycle states such as `pending`, `running`, `stopped`, and `terminated`.

This is useful for **real-time reaction** to instance activity — enabling actions such as tagging, alerting, or enforcement as soon as the instance enters a defined state.

---

### Key Behavior

- Uses AWS **EC2 instance state change notifications** via CloudWatch Events.
- Executes the policy on transitions to the defined EC2 states.
- Can act on instances immediately after launch, stop, or termination.

---

### Supported EC2 State Events

You can trigger policies on one or more of the following states:

- `pending`
- `running`
- `shutting-down`
- `stopped`
- `stopping`
- `terminated`

---

### Use Cases

#### ✅ What You Can Do
- Enforce tagging immediately after instance launch.
- Send alerts when instances are stopped or terminated.
- Automate lifecycle tagging (e.g., cost-center or owner).
- Validate configuration post-launch.

#### ❌ What You Can't Do
- Trigger on non-EC2 lifecycle events (use `cloudtrail` for broader API activity).
- Use periodic scanning (use `pull` or `periodic` for scheduled evaluations).
- Filter based on historical state changes — operates on current transition only.

---

### Example 1 – Tag EC2 Instances on Launch

```yaml
policies:
  - name: tag-on-ec2-launch
    resource: aws.ec2
    mode:
      type: ec2-instance-state
      events:
        - running
      role: arn:aws:iam::{account_id}:role/LambdaExecutionRole
    filters:
      - "tag:Environment": absent
    actions:
      - tag:
          tags:
            Environment: Unknown
```

---

### Example 2 – Alert on Terminated EC2 Instances

```yaml
policies:
  - name: notify-on-ec2-termination
    resource: aws.ec2
    mode:
      type: ec2-instance-state
      events:
        - terminated
      role: arn:aws:iam::{account_id}:role/LambdaExecutionRole
    actions:
      - type: notify
        to:
          - email@example.com
        transport:
          type: sns
          topic: arn:aws:sns:us-east-1:{account_id}:MyTopic
```

---

## Raw Schema – `ec2-instance-state`

```yaml
type: object
properties:
  type:
    enum:
      - ec2-instance-state
  events:
    type: array
    items:
      enum:
        - pending
        - running
        - shutting-down
        - stopped
        - stopping
        - terminated
  concurrency:
    type: integer
  dead_letter_config:
    type: object
  environment:
    type: object
  execution-options:
    type: object
  function-prefix:
    type: string
  handler:
    type: string
  kms_key_arn:
    type: string
  layers:
    type: array
    items:
      type: string
  member-role:
    type: string
  memory:
    type: number
  packages:
    type: array
    items:
      type: string
  pattern:
    type: object
    minProperties: 1
  role:
    type: string
  runtime:
    enum:
      - python3.8
      - python3.9
      - python3.10
      - python3.11
      - python3.12
  security_groups:
    type: array
  subnets:
    type: array
  tags:
    type: object
  timeout:
    type: number
  tracing_config:
    type: object
required:
  - type
```

---

## Schema Table – `ec2-instance-state`

| Field               | Type      | Allowed Values / Description                              | Required | Description |
|--------------------|-----------|-------------------------------------------------------------|----------|-------------|
| `type`             | `string`  | `ec2-instance-state`                                        | ✅ Yes   | Execution mode identifier |
| `events`           | `array`   | `pending`, `running`, `shutting-down`, `stopped`, `stopping`, `terminated` | No | EC2 state transitions that trigger the policy |
| `role`             | `string`  | IAM role ARN                                                | No       | Lambda execution role |
| `concurrency`      | `integer` | —                                                           | No       | Max concurrent Lambda executions |
| `dead_letter_config` | `object`| —                                                           | No       | DLQ for failed executions |
| `environment`      | `object`  | —                                                           | No       | Lambda environment variables |
| `execution-options`| `object`  | —                                                           | No       | Runtime behavior flags |
| `function-prefix`  | `string`  | —                                                           | No       | Prefix for Lambda name |
| `handler`          | `string`  | —                                                           | No       | Lambda handler override |
| `kms_key_arn`      | `string`  | —                                                           | No       | KMS encryption key for environment vars |
| `layers`           | `array`   | List of Lambda layer ARNs                                   | No       | Additional Lambda layers |
| `member-role`      | `string`  | —                                                           | No       | IAM role for cross-account execution |
| `memory`           | `number`  | —                                                           | No       | Memory (MB) allocated to Lambda |
| `packages`         | `array`   | List of strings                                             | No       | Python packages to include |
| `pattern`          | `object`  | Must have at least one property                             | No       | EventBridge pattern override |
| `runtime`          | `string`  | `python3.8` to `python3.12`                                 | No       | Python runtime version |
| `security_groups`  | `array`   | —                                                           | No       | VPC security groups |
| `subnets`          | `array`   | —                                                           | No       | VPC subnets |
| `tags`             | `object`  | Key-value tag map                                           | No       | Lambda function tags |
| `timeout`          | `number`  | Seconds                                                     | No       | Lambda timeout duration |
| `tracing_config`   | `object`  | —                                                           | No       | AWS X-Ray tracing config |

---

## Execution Mode: `guard-duty`

### Description  
The `guard-duty` execution mode integrates with **AWS GuardDuty**, a threat detection service that monitors AWS accounts and workloads for malicious or unauthorized behavior.

This mode allows policies to be triggered **automatically** when **GuardDuty generates findings**, enabling **automated incident response** to detected security threats.

---

### Key Behavior

- Policies are executed by AWS Lambda in response to **GuardDuty findings**.
- Enables real-time reaction to high-confidence threats such as:
  - Unusual network behavior
  - IAM anomalies
  - Instance compromise indicators

---

### Use Cases

#### ✅ What You Can Do
- Automatically quarantine compromised EC2 instances.
- Notify security teams on critical GuardDuty findings.
- Tag affected resources for investigation or tracking.
- Trigger remediation workflows (e.g., block access, revoke permissions).

#### ❌ What You Can't Do
- Trigger on non-GuardDuty events (use `cloudtrail` or `event` for broader API triggers).
- Customize event sources beyond GuardDuty finding patterns.
- Periodically evaluate resource state (use `pull` or `config-poll-rule` for that).

---

### Example 1 – Stop Instance on Finding

```yaml
policies:
  - name: stop-instance-on-guardduty
    resource: aws.ec2
    mode:
      type: guard-duty
      role: arn:aws:iam::{account_id}:role/LambdaExecutionRole
    filters:
      - type: event
        key: detail.type
        value: UnauthorizedAccess:EC2/SSHBruteForce
      - State.Name: running
    actions:
      - stop
```

---

### Example 2 – Notify on IAM Anomaly

```yaml
policies:
  - name: notify-iam-threat
    resource: aws.iam-user
    mode:
      type: guard-duty
      role: arn:aws:iam::{account_id}:role/SecurityNotifierRole
    filters:
      - type: event
        key: detail.type
        value: UnauthorizedAccess:IAMUser/ConsoleLogin
    actions:
      - type: notify
        to:
          - security@example.com
        transport:
          type: sns
          topic: arn:aws:sns:us-east-1:{account_id}:SecurityAlerts
```

---

## Raw Schema – `guard-duty`

```yaml
type: object
properties:
  type:
    enum:
      - guard-duty
  concurrency:
    type: integer
  dead_letter_config:
    type: object
  environment:
    type: object
  execution-options:
    type: object
  function-prefix:
    type: string
  handler:
    type: string
  kms_key_arn:
    type: string
  layers:
    type: array
    items:
      type: string
  member-role:
    type: string
  memory:
    type: number
  packages:
    type: array
    items:
      type: string
  pattern:
    type: object
    minProperties: 1
  role:
    type: string
  runtime:
    enum:
      - python3.8
      - python3.9
      - python3.10
      - python3.11
      - python3.12
  security_groups:
    type: array
  subnets:
    type: array
  tags:
    type: object
  timeout:
    type: number
  tracing_config:
    type: object
required:
  - type
```

---

## Schema Table – `guard-duty`

| Field               | Type      | Allowed Values / Description         | Required | Description |
|--------------------|-----------|--------------------------------------|----------|-------------|
| `type`             | `string`  | `guard-duty`                         | ✅ Yes   | Execution mode identifier |
| `role`             | `string`  | IAM role ARN                         | No       | Role assumed by Lambda function |
| `concurrency`      | `integer` | —                                    | No       | Maximum concurrent Lambda executions |
| `dead_letter_config` | `object`| —                                    | No       | DLQ configuration for failed executions |
| `environment`      | `object`  | —                                    | No       | Lambda environment variables |
| `execution-options`| `object`  | —                                    | No       | Advanced execution settings |
| `function-prefix`  | `string`  | —                                    | No       | Lambda function name prefix |
| `handler`          | `string`  | —                                    | No       | Lambda handler entry point |
| `kms_key_arn`      | `string`  | —                                    | No       | KMS key for encrypting Lambda environment |
| `layers`           | `array`   | List of strings                      | No       | Lambda layers to attach |
| `member-role`      | `string`  | —                                    | No       | IAM role for cross-account execution |
| `memory`           | `number`  | —                                    | No       | Memory size for the Lambda (MB) |
| `packages`         | `array`   | List of strings                      | No       | Python packages to include |
| `pattern`          | `object`  | Must have at least one property      | No       | Custom event pattern override |
| `runtime`          | `string`  | `python3.8` to `python3.12`          | No       | Python runtime for Lambda |
| `security_groups`  | `array`   | —                                    | No       | Security groups for VPC-attached Lambda |
| `subnets`          | `array`   | —                                    | No       | Subnets for VPC Lambda |
| `tags`             | `object`  | Key-value map                        | No       | Lambda function tags |
| `timeout`          | `number`  | Seconds                              | No       | Max Lambda execution time |
| `tracing_config`   | `object`  | —                                    | No       | AWS X-Ray tracing setup |

---

## Execution Mode: `hub-finding` / `hub-action`

### Description  
The `hub-finding` (or alias: `hub-action`) mode integrates with **AWS Security Hub** by deploying a Cloud Custodian policy as a **custom console action**. This allows users to **manually invoke the policy** from the Security Hub UI against individual **findings or insight results**.

This mode provisions:
- An **AWS Lambda** function with the policy logic.
- A **Security Hub custom action** associated with the Lambda.
- The custom action is prefixed with the resource type (e.g., `ec2:Remediate`).

---

### Key Behavior

- The policy is **invoked manually** from the Security Hub console.
- Applies to specific Security Hub **findings** or **insights**.
- Useful for **manual incident remediation** workflows.

---

### Use Cases

#### ✅ What You Can Do
- Perform manual remediation from the Security Hub console.
- Bundle multiple actions (e.g., snapshot, tag, stop) for quick response.
- Apply custom policy logic interactively.

#### ❌ What You Can't Do
- Trigger policies automatically on finding creation (use `guard-duty` for automation).
- Trigger from outside Security Hub's console (i.e., not event-based).
- Evaluate scheduled or state-based compliance (use `config-rule` or `pull`).

---

### Example – Manual EC2 Remediation from Security Hub

```yaml
policies:
  - name: remediate-compromised-ec2
    resource: aws.ec2
    mode:
      type: hub-action
      role: arn:aws:iam::{account_id}:role/SecurityHubRemediationRole
    actions:
      - snapshot
      - type: set-instance-profile
        name: null
      - stop
```

This policy:
- Appears in the Security Hub UI as a custom action.
- Can be invoked on selected EC2-related findings.
- Creates a snapshot, removes the instance profile, and stops the instance.

---

## Raw Schema – `hub-finding` / `hub-action`

```yaml
type: object
properties:
  type:
    enum:
      - hub-finding
      - hub-action
  concurrency:
    type: integer
  dead_letter_config:
    type: object
  environment:
    type: object
  execution-options:
    type: object
  function-prefix:
    type: string
  handler:
    type: string
  kms_key_arn:
    type: string
  layers:
    type: array
    items:
      type: string
  member-role:
    type: string
  memory:
    type: number
  packages:
    type: array
    items:
      type: string
  pattern:
    type: object
    minProperties: 1
  role:
    type: string
  runtime:
    enum:
      - python3.8
      - python3.9
      - python3.10
      - python3.11
      - python3.12
  security_groups:
    type: array
  subnets:
    type: array
  tags:
    type: object
  timeout:
    type: number
  tracing_config:
    type: object
required:
  - type
```

---

## Schema Table – `hub-finding` / `hub-action`

| Field               | Type      | Allowed Values / Description                  | Required | Description |
|--------------------|-----------|-----------------------------------------------|----------|-------------|
| `type`             | `string`  | `hub-finding`, `hub-action`                   | ✅ Yes   | Execution mode identifier |
| `role`             | `string`  | IAM role ARN                                  | No       | IAM role assumed by Lambda |
| `concurrency`      | `integer` | —                                             | No       | Lambda concurrency setting |
| `dead_letter_config` | `object`| —                                             | No       | DLQ config for failure handling |
| `environment`      | `object`  | —                                             | No       | Environment variables for Lambda |
| `execution-options`| `object`  | —                                             | No       | Extra execution settings |
| `function-prefix`  | `string`  | —                                             | No       | Prefix for Lambda function name |
| `handler`          | `string`  | —                                             | No       | Lambda function handler |
| `kms_key_arn`      | `string`  | —                                             | No       | KMS encryption key |
| `layers`           | `array`   | List of strings                               | No       | Lambda layers to attach |
| `member-role`      | `string`  | —                                             | No       | IAM role for cross-account execution |
| `memory`           | `number`  | —                                             | No       | Memory size for the Lambda (MB) |
| `packages`         | `array`   | List of strings                               | No       | Python packages to include |
| `pattern`          | `object`  | Must have at least one property               | No       | Custom event pattern matching |
| `runtime`          | `string`  | `python3.8` to `python3.12`                   | No       | Lambda Python runtime version |
| `security_groups`  | `array`   | —                                             | No       | VPC security groups for Lambda |
| `subnets`          | `array`   | —                                             | No       | Subnets for VPC-attached Lambda |
| `tags`             | `object`  | Key-value tag map                             | No       | Lambda resource tags |
| `timeout`          | `number`  | Seconds                                       | No       | Lambda execution timeout |
| `tracing_config`   | `object`  | —                                             | No       | AWS X-Ray tracing configuration |

---


## Execution Mode: `hub-finding`

### Description  
The `hub-finding` mode provisions a **Lambda function** that triggers automatically on **Security Hub finding ingestion events**.

Unlike `hub-action`, which is **manually triggered** from the Security Hub console, `hub-finding` enables **event-driven automated remediation** whenever a new finding is detected by Security Hub (e.g., from GuardDuty or other integrated products).

This mode supports remediation for:
- AWS-native resources.
- Additional resource types through **Cloud Custodian’s extended finding support** (e.g., `Other` resources in findings).

---

### Key Behavior

- Responds to **incoming Security Hub findings** using CloudWatch Events.
- Executes based on content inside the finding JSON (e.g., `ProductFields`, `ResourceType`, etc.).
- Can automate cleanup, notifications, tagging, or any supported Custodian action.

---

### Use Cases

#### ✅ What You Can Do
- Automatically remediate IAM users when GuardDuty raises access alerts.
- Respond to findings from Security Hub partners or integrations.
- Work with extended resource data (`Other`) that is not natively supported by Security Hub.

#### ❌ What You Can't Do
- Trigger remediation manually from the Security Hub console (use `hub-action` for that).
- Trigger for resources unrelated to Security Hub findings.
- Customize triggers outside the Security Hub event flow.

---

### Example 1 – Remove IAM Access Keys on GuardDuty Finding

```yaml
policies:
  - name: guardduty-remediate-iam
    resource: aws.iam-user
    mode:
      type: hub-finding
      role: arn:aws:iam::{account_id}:role/LambdaExecutionRole
    filters:
      - type: event
        key: detail.findings[].ProductFields.aws/securityhub/ProductName
        value: GuardDuty
    actions:
      - remove-keys
```

---

### Example 2 – Disable Public S3 Bucket on Finding

```yaml
policies:
  - name: disable-s3-public-access
    resource: aws.s3
    mode:
      type: hub-finding
      role: arn:aws:iam::{account_id}:role/SecurityHubS3Remediator
    filters:
      - type: event
        key: detail.findings[].Types[]
        op: contains
        value: "S3 Bucket has public read ACL"
    actions:
      - type: set-public-block
        state: true
```

---

## Raw Schema – `hub-finding`

```yaml
type: object
properties:
  type:
    enum:
      - hub-finding
      - hub-action
  concurrency:
    type: integer
  dead_letter_config:
    type: object
  environment:
    type: object
  execution-options:
    type: object
  function-prefix:
    type: string
  handler:
    type: string
  kms_key_arn:
    type: string
  layers:
    type: array
    items:
      type: string
  member-role:
    type: string
  memory:
    type: number
  packages:
    type: array
    items:
      type: string
  pattern:
    type: object
    minProperties: 1
  role:
    type: string
  runtime:
    enum:
      - python3.8
      - python3.9
      - python3.10
      - python3.11
      - python3.12
  security_groups:
    type: array
  subnets:
    type: array
  tags:
    type: object
  timeout:
    type: number
  tracing_config:
    type: object
required:
  - type
```

---

## Schema Table – `hub-finding`

| Field               | Type      | Allowed Values / Description                  | Required | Description |
|--------------------|-----------|-----------------------------------------------|----------|-------------|
| `type`             | `string`  | `hub-finding`, `hub-action`                   | ✅ Yes   | Execution mode identifier |
| `role`             | `string`  | IAM role ARN                                  | No       | Role assumed by Lambda |
| `concurrency`      | `integer` | —                                             | No       | Lambda concurrency cap |
| `dead_letter_config` | `object`| —                                             | No       | Dead letter queue setup |
| `environment`      | `object`  | —                                             | No       | Lambda environment variables |
| `execution-options`| `object`  | —                                             | No       | Additional runtime flags |
| `function-prefix`  | `string`  | —                                             | No       | Prefix for Lambda function name |
| `handler`          | `string`  | —                                             | No       | Lambda handler name |
| `kms_key_arn`      | `string`  | —                                             | No       | KMS key for encrypting Lambda environment |
| `layers`           | `array`   | List of strings                               | No       | Lambda layer ARNs |
| `member-role`      | `string`  | —                                             | No       | Cross-account IAM role |
| `memory`           | `number`  | —                                             | No       | Lambda memory allocation (MB) |
| `packages`         | `array`   | List of strings                               | No       | Python packages to bundle |
| `pattern`          | `object`  | Requires at least one property                | No       | Event pattern for filtering |
| `runtime`          | `string`  | `python3.8` to `python3.12`                   | No       | Python runtime version |
| `security_groups`  | `array`   | —                                             | No       | VPC security groups |
| `subnets`          | `array`   | —                                             | No       | VPC subnets for Lambda |
| `tags`             | `object`  | Key-value pairs                               | No       | Tags to apply to Lambda |
| `timeout`          | `number`  | Seconds                                       | No       | Lambda timeout duration |
| `tracing_config`   | `object`  | —                                             | No       | AWS X-Ray tracing config |

---

## Execution Mode: `periodic`

### Description  
The `periodic` execution mode allows you to run Cloud Custodian policies **at a scheduled interval** by deploying them as **AWS Lambda functions** triggered by **EventBridge cron rules**.

It combines the logic of `pull` mode with serverless automation — useful for continuous audits, maintenance tasks, tagging enforcement, and compliance enforcement without manual triggers.

---

### Key Behavior

- Runs on a **custom schedule** (e.g., every 1 hour, once per day).
- Executes as **Lambda function** in the cloud.
- Ideal for **ongoing enforcement** of cloud governance and cost optimization policies.

---

### Use Cases

#### ✅ What You Can Do
- Automatically tag resources daily or weekly.
- Clean up unused or non-compliant resources on a schedule.
- Perform cost optimization scans at night.
- Enforce security baselines like encryption, public access, and tag compliance.

#### ❌ What You Can't Do
- React to real-time cloud events (use `cloudtrail`, `ec2-instance-state`, etc.).
- Run policies without an explicitly defined schedule.
- Depend on manual trigger from CLI (use `pull` for that).

---

## 📅 Cron Schedule Format

Supports standard **AWS cron expressions** using EventBridge syntax:
```
cron(Minutes Hours Day-of-month Month Day-of-week Year)
```
Example:
- `cron(0 2 * * ? *)` – every day at 2 AM
- `rate(1 day)` – every day
- `rate(3 hours)` – every 3 hours

---

## ✅ Examples

---

### Example 1 – Stop Unused EC2 Instances Daily

```yaml
policies:
  - name: ec2-stop-unused
    resource: aws.ec2
    mode:
      type: periodic
      schedule: "rate(1 day)"
      role: arn:aws:iam::{account_id}:role/LambdaExecutionRole
    filters:
      - State.Name: running
      - "tag:Owner": absent
    actions:
      - stop
```

---

### Example 2 – Delete Unattached EBS Volumes Every 6 Hours

```yaml
policies:
  - name: cleanup-ebs
    resource: aws.ebs
    mode:
      type: periodic
      schedule: "rate(6 hours)"
      role: arn:aws:iam::{account_id}:role/EBSCleaner
    filters:
      - Attachments: []
    actions:
      - delete
```

---

### Example 3 – Notify on Public S3 Buckets Every Hour

```yaml
policies:
  - name: s3-public-bucket-check
    resource: aws.s3
    mode:
      type: periodic
      schedule: "rate(1 hour)"
      role: arn:aws:iam::{account_id}:role/S3Audit
    filters:
      - type: cross-account
    actions:
      - type: notify
        to:
          - security@example.com
        transport:
          type: sns
          topic: arn:aws:sns:us-east-1:{account_id}:SecurityAlerts
```

---

### Example 4 – Auto-Tag EC2 Instances Weekly

```yaml
policies:
  - name: ec2-tag-audit
    resource: aws.ec2
    mode:
      type: periodic
      schedule: "cron(0 0 ? * MON *)"  # Every Monday at midnight UTC
      role: arn:aws:iam::{account_id}:role/TaggerRole
    filters:
      - "tag:Environment": absent
    actions:
      - type: tag
        tags:
          Environment: unknown
```

---

### Example 5 – Cleanup Orphaned Security Groups Every 3 Days

```yaml
policies:
  - name: delete-unused-security-groups
    resource: aws.security-group
    mode:
      type: periodic
      schedule: "rate(3 days)"
      role: arn:aws:iam::{account_id}:role/SecGroupCleaner
    filters:
      - type: unused
    actions:
      - delete
```

---

### Example 6 – Enforce RDS Encryption Policy Daily

```yaml
policies:
  - name: rds-encryption-check
    resource: aws.rds
    mode:
      type: periodic
      schedule: "rate(1 day)"
      role: arn:aws:iam::{account_id}:role/RDSAudit
    filters:
      - StorageEncrypted: false
    actions:
      - type: mark-for-op
        tag: custodian_cleanup
        op: delete
        days: 3
```

---

## 🔧 Raw Schema – `periodic`

```yaml
type: object
properties:
  type:
    enum:
      - periodic
  schedule:
    type: string
  concurrency:
    type: integer
  dead_letter_config:
    type: object
  environment:
    type: object
  execution-options:
    type: object
  function-prefix:
    type: string
  handler:
    type: string
  kms_key_arn:
    type: string
  layers:
    type: array
    items:
      type: string
  member-role:
    type: string
  memory:
    type: number
  packages:
    type: array
    items:
      type: string
  pattern:
    type: object
    minProperties: 1
  role:
    type: string
  runtime:
    enum:
      - python3.8
      - python3.9
      - python3.10
      - python3.11
      - python3.12
  security_groups:
    type: array
  subnets:
    type: array
  tags:
    type: object
  timeout:
    type: number
  tracing_config:
    type: object
required:
  - type
```

---

## 📋 Schema Table – `periodic`

| Field               | Type      | Allowed Values / Description              | Required | Description |
|--------------------|-----------|-------------------------------------------|----------|-------------|
| `type`             | `string`  | `periodic`                                | ✅ Yes   | Execution mode identifier |
| `schedule`         | `string`  | Cron or rate expression                   | No       | Defines frequency (e.g., `rate(1 day)`) |
| `role`             | `string`  | IAM role ARN                              | No       | IAM role assumed by Lambda |
| `concurrency`      | `integer` | —                                         | No       | Lambda concurrency limit |
| `dead_letter_config` | `object`| —                                         | No       | Dead letter queue configuration |
| `environment`      | `object`  | —                                         | No       | Lambda environment variables |
| `execution-options`| `object`  | —                                         | No       | Runtime behavior options |
| `function-prefix`  | `string`  | —                                         | No       | Lambda function name prefix |
| `handler`          | `string`  | —                                         | No       | Lambda handler override |
| `kms_key_arn`      | `string`  | —                                         | No       | KMS encryption key for env vars |
| `layers`           | `array`   | List of strings                           | No       | Lambda layers to include |
| `member-role`      | `string`  | —                                         | No       | Role for cross-account execution |
| `memory`           | `number`  | —                                         | No       | Lambda memory allocation |
| `packages`         | `array`   | List of strings                           | No       | Extra Python packages to include |
| `pattern`          | `object`  | Must include at least one property        | No       | Advanced EventBridge pattern matching |
| `runtime`          | `string`  | `python3.8` to `python3.12`               | No       | Lambda Python runtime version |
| `security_groups`  | `array`   | —                                         | No       | VPC security groups |
| `subnets`          | `array`   | —                                         | No       | VPC subnets |
| `tags`             | `object`  | Key-value pairs                           | No       | Tags for the Lambda |
| `timeout`          | `number`  | —                                         | No       | Lambda execution timeout |
| `tracing_config`   | `object`  | —                                         | No       | AWS X-Ray tracing configuration |

---

## Execution Mode: `phd`

### Description  
The `phd` execution mode allows Cloud Custodian policies to react to **AWS Personal Health Dashboard (PHD) events**. These events notify customers about issues related to **AWS service disruptions, maintenance, and operational health** that affect their account or resources.

This mode uses **AWS Lambda** and **CloudWatch Events** to execute policies when **PHD events** such as outages, scheduled changes, or account-level notifications are published.

---

### Key Behavior

- Executes policy when AWS publishes a PHD event (e.g., a scheduled maintenance or outage).
- Supports filtering by **event category**, **status**, and **event type**.
- Allows proactive or reactive measures for upcoming or active issues.

---

### Use Cases

#### ✅ What You Can Do
- Notify stakeholders on critical service issues affecting resources.
- Snapshot or back up affected EC2, RDS, or EBS resources before scheduled maintenance.
- Tag or isolate impacted resources for tracking or remediation.

#### ❌ What You Can't Do
- Trigger based on general resource state changes (use `pull`, `periodic`, or `config-rule`).
- Act on custom health events not surfaced by AWS PHD.
- Use for services not covered by PHD.

---

## 🧭 Event Filtering Options

### Event Categories:
- `issue` – Outage or disruption
- `accountNotification` – Informational notifications
- `scheduledChange` – Maintenance schedules

### Statuses:
- `open` – Currently active
- `upcoming` – Announced but not active yet
- `closed` – Resolved or completed

---

## ✅ Examples

---

### Example 1 – Notify on Upcoming Scheduled Changes

```yaml
policies:
  - name: notify-on-scheduled-change
    resource: aws.rds
    mode:
      type: phd
      role: arn:aws:iam::{account_id}:role/NotifyRole
      categories:
        - scheduledChange
      statuses:
        - upcoming
    actions:
      - type: notify
        to:
          - ops@example.com
        transport:
          type: sns
          topic: arn:aws:sns:us-east-1:{account_id}:PHDEvents
```

---

### Example 2 – Snapshot EBS Volumes Before Maintenance

```yaml
policies:
  - name: snapshot-ebs-before-maintenance
    resource: aws.ebs
    mode:
      type: phd
      role: arn:aws:iam::{account_id}:role/PHDSnapshotRole
      categories:
        - scheduledChange
      statuses:
        - upcoming
      events:
        - AWS_EBS_MAINTENANCE_EVENT
    actions:
      - snapshot
```

---

### Example 3 – Tag EC2 Instances Impacted by Open Issues

```yaml
policies:
  - name: tag-ec2-on-outage
    resource: aws.ec2
    mode:
      type: phd
      role: arn:aws:iam::{account_id}:role/TagOnIssue
      categories:
        - issue
      statuses:
        - open
    actions:
      - type: tag
        tags:
          Status: Degraded
```

---

## 🧾 Raw Schema – `phd`

```yaml
type: object
properties:
  type:
    enum:
      - phd
  categories:
    type: array
    items:
      enum:
        - issue
        - accountNotification
        - scheduledChange
  statuses:
    type: array
    items:
      enum:
        - open
        - upcoming
        - closed
  events:
    type: array
    items:
      type: string
  concurrency:
    type: integer
  dead_letter_config:
    type: object
  environment:
    type: object
  execution-options:
    type: object
  function-prefix:
    type: string
  handler:
    type: string
  kms_key_arn:
    type: string
  layers:
    type: array
    items:
      type: string
  member-role:
    type: string
  memory:
    type: number
  packages:
    type: array
    items:
      type: string
  pattern:
    type: object
    minProperties: 1
  role:
    type: string
  runtime:
    enum:
      - python3.8
      - python3.9
      - python3.10
      - python3.11
      - python3.12
  security_groups:
    type: array
  subnets:
    type: array
  tags:
    type: object
  timeout:
    type: number
  tracing_config:
    type: object
required:
  - type
```

---

## 📋 Schema Table – `phd`

| Field               | Type      | Allowed Values / Description                       | Required | Description |
|--------------------|-----------|----------------------------------------------------|----------|-------------|
| `type`             | `string`  | `phd`                                              | ✅ Yes   | Execution mode identifier |
| `categories`       | `array`   | `issue`, `accountNotification`, `scheduledChange` | No       | Filter by event category |
| `statuses`         | `array`   | `open`, `upcoming`, `closed`                      | No       | Filter by current event status |
| `events`           | `array`   | List of specific AWS PHD event codes              | No       | Filter by specific event types |
| `role`             | `string`  | IAM role ARN                                      | No       | IAM role assumed by Lambda |
| `concurrency`      | `integer` | —                                                 | No       | Lambda concurrency setting |
| `dead_letter_config` | `object`| —                                                 | No       | DLQ configuration |
| `environment`      | `object`  | —                                                 | No       | Lambda environment variables |
| `execution-options`| `object`  | —                                                 | No       | Lambda execution behavior flags |
| `function-prefix`  | `string`  | —                                                 | No       | Prefix for Lambda function name |
| `handler`          | `string`  | —                                                 | No       | Lambda handler name |
| `kms_key_arn`      | `string`  | —                                                 | No       | KMS key for encryption |
| `layers`           | `array`   | List of strings                                   | No       | Lambda layers to attach |
| `member-role`      | `string`  | —                                                 | No       | Role for cross-account execution |
| `memory`           | `number`  | —                                                 | No       | Memory (MB) for Lambda |
| `packages`         | `array`   | List of strings                                   | No       | Python packages to include |
| `pattern`          | `object`  | Minimum one property                              | No       | EventBridge pattern override |
| `runtime`          | `string`  | `python3.8` to `python3.12`                       | No       | Python runtime for Lambda |
| `security_groups`  | `array`   | —                                                 | No       | Security groups for VPC Lambda |
| `subnets`          | `array`   | —                                                 | No       | Subnets for VPC Lambda |
| `tags`             | `object`  | Key-value map                                     | No       | Tags to apply to Lambda |
| `timeout`          | `number`  | Seconds                                           | No       | Lambda timeout duration |
| `tracing_config`   | `object`  | —                                                 | No       | AWS X-Ray tracing config |

---

## Execution Mode: `schedule`

### Description  
The `schedule` execution mode allows policies to run on a **defined cron schedule using AWS EventBridge Scheduler**. Like `periodic`, this mode runs Custodian in Lambda in pull mode, but leverages **EventBridge Scheduler**, which provides **advanced scheduling features** such as time zones, start and end dates, and optional group names.

---

### Key Behavior

- Executes policies **based on a defined schedule** (e.g., daily, weekly, hourly).
- Uses **EventBridge Scheduler** (not CloudWatch Events).
- Supports enhanced controls like **start/end time**, **timezone**, and **grouping**.
- Ideal for time-sensitive or regional scheduling needs.

---

### Use Cases

#### ✅ What You Can Do
- Run policies on specific dates and times, optionally within a time window.
- Define execution schedules per **timezone**.
- Use **grouping** to manage multiple scheduled policies logically.
- Apply cleanups, tagging enforcement, or compliance checks regionally or on schedule.

#### ❌ What You Can't Do
- React to events (use `cloudtrail`, `phd`, etc.).
- Use this mode with unsupported AWS regions where EventBridge Scheduler is unavailable.
- Trigger policies on demand (use `pull` mode instead).

---

### Example 1 – Tag EC2 Instances Every Monday at 7 AM UTC

```yaml
policies:
  - name: weekly-ec2-tag-check
    resource: aws.ec2
    mode:
      type: schedule
      schedule: "cron(0 7 ? * MON *)"
      role: arn:aws:iam::{account_id}:role/LambdaScheduler
      timezone: UTC
    filters:
      - "tag:Owner": absent
    actions:
      - type: tag
        tags:
          Owner: unknown
```

---

### Example 2 – Delete Orphaned Snapshots Monthly

```yaml
policies:
  - name: cleanup-snapshots
    resource: aws.ebs-snapshot
    mode:
      type: schedule
      schedule: "cron(0 3 1 * ? *)"
      role: arn:aws:iam::{account_id}:role/SnapshotCleanup
      timezone: America/New_York
      start-date: "2024-01-01T00:00:00Z"
      end-date: "2025-01-01T00:00:00Z"
    filters:
      - type: age
        days: 30
    actions:
      - delete
```

---

### Example 3 – Regional Tag Compliance Group

```yaml
policies:
  - name: tag-compliance-eu
    resource: aws.ec2
    mode:
      type: schedule
      schedule: "cron(30 6 * * ? *)"
      group-name: "eu-schedule-group"
      role: arn:aws:iam::{account_id}:role/RegionScheduler
      timezone: Europe/Frankfurt
    filters:
      - "tag:Environment": absent
    actions:
      - mark
```

---

## 🧾 Raw Schema – `schedule`

```yaml
type: object
properties:
  type:
    enum:
      - schedule
  schedule:
    type: string
  scheduler-role:
    type: string
  group-name:
    type: string
  start-date:
    type: string
  end-date:
    type: string
  timezone:
    type: string
  concurrency:
    type: integer
  dead_letter_config:
    type: object
  environment:
    type: object
  execution-options:
    type: object
  function-prefix:
    type: string
  handler:
    type: string
  kms_key_arn:
    type: string
  layers:
    type: array
    items:
      type: string
  member-role:
    type: string
  memory:
    type: number
  packages:
    type: array
    items:
      type: string
  pattern:
    type: object
    minProperties: 1
  role:
    type: string
  runtime:
    enum:
      - python3.8
      - python3.9
      - python3.10
      - python3.11
      - python3.12
  security_groups:
    type: array
  subnets:
    type: array
  tags:
    type: object
  timeout:
    type: number
  tracing_config:
    type: object
required:
  - type
  - schedule
```

---

## 📋 Schema Table – `schedule`

| Field              | Type      | Allowed Values / Description            | Required | Description |
|-------------------|-----------|-----------------------------------------|----------|-------------|
| `type`            | `string`  | `schedule`                              | ✅ Yes   | Execution mode identifier |
| `schedule`        | `string`  | Cron or rate expression (EventBridge)   | ✅ Yes   | Schedule format (`cron(...)`) |
| `scheduler-role`  | `string`  | IAM role ARN                            | No       | Role used by EventBridge Scheduler |
| `group-name`      | `string`  | —                                       | No       | Logical grouping for schedule |
| `start-date`      | `string`  | ISO 8601 date-time string               | No       | Date when the schedule becomes active |
| `end-date`        | `string`  | ISO 8601 date-time string               | No       | Date when the schedule ends |
| `timezone`        | `string`  | e.g., `UTC`, `America/New_York`         | No       | Timezone for the schedule |
| `role`            | `string`  | IAM role ARN                            | No       | Lambda execution role |
| `concurrency`     | `integer` | —                                       | No       | Lambda concurrency setting |
| `dead_letter_config`| `object`| —                                       | No       | DLQ configuration |
| `environment`     | `object`  | —                                       | No       | Lambda environment variables |
| `execution-options`| `object` | —                                       | No       | Additional Lambda settings |
| `function-prefix` | `string`  | —                                       | No       | Prefix for Lambda function name |
| `handler`         | `string`  | —                                       | No       | Lambda handler entry point |
| `kms_key_arn`     | `string`  | —                                       | No       | KMS key for environment encryption |
| `layers`          | `array`   | List of strings                         | No       | Lambda layer ARNs |
| `member-role`     | `string`  | —                                       | No       | Cross-account execution role |
| `memory`          | `number`  | —                                       | No       | Memory allocated to Lambda |
| `packages`        | `array`   | List of Python packages                 | No       | Include custom packages |
| `pattern`         | `object`  | Must include at least one key           | No       | EventBridge event pattern override |
| `runtime`         | `string`  | `python3.8` to `python3.12`             | No       | Lambda runtime version |
| `security_groups` | `array`   | —                                       | No       | Security groups for VPC Lambda |
| `subnets`         | `array`   | —                                       | No       | Subnets for VPC Lambda |
| `tags`            | `object`  | Key-value map                           | No       | Tags for Lambda function |
| `timeout`         | `number`  | —                                       | No       | Max execution time in seconds |
| `tracing_config`  | `object`  | —                                       | No       | AWS X-Ray tracing configuration |

---

