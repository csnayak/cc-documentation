# 📌 Cloud Custodian AWS Common Filters

## 🔹 **Alarm: Filter Log Metric Filters Based on Associated Alarms**  

### ✨ **What is Alarm?**  
The `alarm` filter in Cloud Custodian **identifies AWS log metric filters that have associated CloudWatch Alarms**. This allows organizations to **audit and manage log-based alarms** efficiently.  

**Common Use Cases:**  
✅ **Identify Log Metrics with Missing Alarms** – Ensure critical logs have active CloudWatch alarms.  
✅ **Audit Alarm Configurations** – Check whether specific alarms exist or meet predefined conditions.  
✅ **Enforce Monitoring Standards** – Ensure all security-critical log metrics have alerting enabled.  

---

## 🔍 **How It Works**  
1️⃣ **Filters AWS log metric filters** based on their associated CloudWatch alarms.  
2️⃣ **Evaluates alarm properties** using conditions (`eq`, `regex`, `contains`, etc.).  
3️⃣ **Returns matching log metric filters** that meet the criteria.  

---

## 📝 **Example: Find Log Metrics That Have Alarms**  
This policy **finds all log metric filters that are associated with an active CloudWatch alarm**.  

```yaml
policies:
  - name: log-metrics-with-alarms
    resource: aws.log-metric
    filters:
      - type: alarm
        key: AlarmName
        value: present
```

🔹 **What Happens?**  
📌 Cloud Custodian **searches for AWS log metric filters** that have **associated CloudWatch alarms**.  
📌 If an **alarm exists**, the log metric filter **is included in the results**.  

---

## 📝 **Example: Find Log Metrics Without Alarms**  
This policy **detects log metric filters that do NOT have an associated CloudWatch alarm**, ensuring that logs are properly monitored.  

```yaml
policies:
  - name: log-metrics-without-alarms
    resource: aws.log-metric
    filters:
      - type: alarm
        key: AlarmName
        value: absent
```

🔹 **What Happens?**  
📌 Cloud Custodian **finds log metric filters that do NOT have associated alarms**.  
📌 This helps **identify unmonitored logs** that need CloudWatch alarms configured.  

---

## 📝 **Example: Identify Log Metrics Linked to a Specific Alarm**  
This policy **filters log metric filters that are linked to an alarm with a specific name pattern**.  

```yaml
policies:
  - name: log-metrics-specific-alarm
    resource: aws.log-metric
    filters:
      - type: alarm
        key: AlarmName
        value_regex: "^SecurityAlert-.*"
```

🔹 **What Happens?**  
📌 Cloud Custodian **finds log metric filters that are associated with alarms named `SecurityAlert-...`**.  
📌 Helps **track log-based security alarms** for compliance and monitoring.  

---

## 🎯 **Why Use Alarm Filtering?**  
✅ **Ensures Proper Log Monitoring:** Identifies log metrics without necessary alarms.  
✅ **Automates Security & Compliance Audits:** Validates that critical log metrics have monitoring enabled.  
✅ **Supports Regex & Complex Filtering:** Allows **pattern-based filtering** for alarm names or configurations.  

---

## ⚠ **Key Considerations**  
⚠ **Ensure Alarms Are Properly Named:** Use meaningful and consistent alarm naming conventions.  
⚠ **Combine with Other Filters for Advanced Audits:** Filter based on **log retention, metric patterns, or missing alarms**.  
⚠ **Use Regex for Flexible Matching:** Use `value_regex` to **match multiple alarm name patterns** dynamically.  

---

## 🛠 **Supported Alarm Filter Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The attribute to filter by (e.g., `AlarmName`, `StateValue`). |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value for the filter. |
| `value_regex` | `string`   | Regular expression pattern for matching values. |
| `value_type` | `enum`     | Data type (`age`, `integer`, `cidr`, `date`, etc.). |

---

## ✅ **Best Practices for Log Metric & Alarm Auditing**  
💡 **Ensure Critical Logs Have Active Alarms:** Identify logs that need monitoring but lack alerts.  
💡 **Use Regular Expressions for Pattern Matching:** Search for specific alarm categories (`SecurityAlert-*`).  
💡 **Automate Compliance Audits:** Run policies regularly to detect unmonitored log metrics.  

---

## 🔹 **API-Cache: Filter AppSync GraphQL APIs Based on Cache Attributes**  

### ✨ **What is API-Cache?**  
The `api-cache` filter in Cloud Custodian **filters AWS AppSync GraphQL APIs based on their caching configuration**. This allows organizations to **audit, optimize, and enforce caching policies** for GraphQL APIs.  

**Common Use Cases:**  
✅ **Ensure Efficient Caching** – Identify APIs that lack caching or have suboptimal configurations.  
✅ **Optimize Performance & Cost** – Ensure APIs use appropriate caching levels to reduce request costs.  
✅ **Enforce Compliance** – Verify that all APIs meet organizational caching policies.  

---

## 🔍 **How It Works**  
1️⃣ **Filters AWS AppSync GraphQL APIs** based on API cache attributes.  
2️⃣ **Evaluates cache settings** using conditions (`eq`, `regex`, `contains`, etc.).  
3️⃣ **Returns matching APIs** that meet the defined caching criteria.  

---

## 📝 **Example: Find APIs Using Full Request Caching**  
This policy **identifies GraphQL APIs that use `FULL_REQUEST_CACHING`** to ensure compliance with performance best practices.  

```yaml
policies:
  - name: filter-graphql-api-cache
    resource: aws.graphql-api
    filters:
      - type: api-cache
        key: 'apiCachingBehavior'
        value: 'FULL_REQUEST_CACHING'
```

🔹 **What Happens?**  
📌 Cloud Custodian **filters GraphQL APIs** that have `apiCachingBehavior` set to `FULL_REQUEST_CACHING`.  
📌 This ensures **APIs are optimized for reduced latency and request costs**.  

---

## 📝 **Example: Detect APIs Without Caching Enabled**  
This policy **finds AppSync GraphQL APIs that do NOT have caching configured**, helping identify potential performance bottlenecks.  

```yaml
policies:
  - name: detect-graphql-no-cache
    resource: aws.graphql-api
    filters:
      - type: api-cache
        key: 'ttl'
        value: 0
```

🔹 **What Happens?**  
📌 Cloud Custodian **identifies GraphQL APIs where the `ttl` (time-to-live) is set to `0`**, meaning caching is disabled.  
📌 Helps **detect APIs that may cause unnecessary AWS costs and performance issues**.  

---

## 🎯 **Why Use API-Cache Filtering?**  
✅ **Improves GraphQL API Performance:** Ensures proper caching settings for fast responses.  
✅ **Optimizes AWS Costs:** Reduces AppSync request volume by leveraging caching.  
✅ **Enhances Compliance & Security:** Enforces caching policies for predictable API performance.  

---

## ⚠ **Key Considerations**  
⚠ **Match API Caching to Workload Needs:** Some APIs require `PER_RESOLVER_CACHING` instead of `FULL_REQUEST_CACHING`.  
⚠ **Monitor TTL Values:** A `ttl` of `0` disables caching, while higher values optimize cost and performance.  
⚠ **Use Regex for Flexible Filtering:** Use `value_regex` to **match multiple caching settings dynamically**.  

---

## 🛠 **Supported API-Cache Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The API cache attribute to filter by (e.g., `apiCachingBehavior`, `ttl`). |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value for the filter. |
| `value_regex` | `string`   | Regular expression pattern for matching values. |
| `value_type` | `enum`     | Data type (`integer`, `size`, `expiration`, etc.). |

---

## ✅ **Best Practices for GraphQL API Caching**  
💡 **Enable Caching for Frequently Used APIs:** Reduce costs and improve API response times.  
💡 **Use TTLs That Balance Performance & Freshness:** Ensure `ttl` is optimized for API workload patterns.  
💡 **Monitor API Caching Metrics:** Use AWS CloudWatch to track cache hit/miss rates.  

---

## 🔹 **Bedrock-Model-Invocation-Logging: Check AWS Bedrock Model Invocation Logging Configuration**  

### ✨ **What is Bedrock-Model-Invocation-Logging?**  
The `bedrock-model-invocation-logging` filter in Cloud Custodian **verifies the model invocation logging configuration** for AWS Bedrock. This helps organizations **ensure compliance, security, and auditing of AI model usage**.  

**Common Use Cases:**  
✅ **Verify Logging is Enabled** – Ensure model invocations are being recorded.  
✅ **Enforce Compliance Requirements** – Ensure logging settings meet organizational security policies.  
✅ **Audit Model Invocation Data Storage** – Track where inference logs are being delivered.  

---

## 🔍 **How It Works**  
1️⃣ **Queries AWS Bedrock** for model invocation logging configurations.  
2️⃣ **Checks for specific attributes** like `imageDataDeliveryEnabled`, `textDataDeliveryEnabled`, etc.  
3️⃣ **Filters accounts based on defined conditions** (e.g., logging must be enabled).  

---

## 📝 **Example: Check if Image Data Logging is Enabled**  
This policy **verifies that Bedrock model invocation logging is enabled for image data**.  

```yaml
policies:
  - name: bedrock-model-invocation-logging-configuration
    resource: account
    filters:
      - type: bedrock-model-invocation-logging
        attrs:
          - imageDataDeliveryEnabled: True
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves the Bedrock logging configuration** for the account.  
📌 It **checks if `imageDataDeliveryEnabled` is set to `True`**, ensuring model inferences are logged.  

---

## 📝 **Example: Check Logging for Multiple Attributes**  
This policy **ensures both image and text data logging are enabled for Bedrock model invocations**.  

```yaml
policies:
  - name: bedrock-model-invocation-logging-multi-check
    resource: account
    filters:
      - type: bedrock-model-invocation-logging
        attrs:
          - and:
              - imageDataDeliveryEnabled: True
              - textDataDeliveryEnabled: True
```

🔹 **What Happens?**  
📌 Cloud Custodian **checks if both `imageDataDeliveryEnabled` and `textDataDeliveryEnabled` are set to `True`**.  
📌 Ensures **all AI model inferences are logged** for compliance.  

---

## 🎯 **Why Use Bedrock-Model-Invocation-Logging?**  
✅ **Ensures AI Model Transparency:** Monitors how AWS Bedrock models are being used.  
✅ **Improves Security & Compliance:** Helps meet regulatory requirements for AI logging.  
✅ **Prevents Unauthorized Model Usage:** Ensures logging is enabled for audit trails.  

---

## ⚠ **Key Considerations**  
⚠ **Ensure Logging is Configured Correctly:** AWS Bedrock allows multiple logging options—validate all required settings.  
⚠ **Monitor Log Destination:** Logs should be stored in a secure, compliant location (e.g., S3, CloudWatch).  
⚠ **Use Logical Operators for Complex Checks:** Combine attributes with `and`, `or`, and `not` filters for **granular control**.  

---

## 🛠 **Supported Bedrock-Model-Invocation-Logging Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `attrs`       | `array`    | List of attributes to filter by (e.g., `imageDataDeliveryEnabled`, `textDataDeliveryEnabled`). |
| `count`       | `number`   | Number of matching attributes required. |
| `count_op`    | `enum`     | Comparison operator (`eq`, `lt`, `gt`, etc.). |
| `type`        | `enum`     | Must be `bedrock-model-invocation-logging`. **(Required)** |

---

## ✅ **Best Practices for AI Model Invocation Logging**  
💡 **Ensure Logging is Enabled for All Data Types:** Monitor image, text, and embedding data usage.  
💡 **Store Logs in a Secure Location:** Use **S3 with encryption, CloudWatch Logs, or AWS Security Lake**.  
💡 **Monitor Bedrock API Usage:** Track AI model usage trends for governance and cost control.  

---

## 🔹 **Bucket-Replication: Validate S3 Bucket Replication Configurations**  

### ✨ **What is Bucket-Replication?**  
The `bucket-replication` filter in Cloud Custodian **checks the replication configuration of S3 buckets**, ensuring **data redundancy, compliance, and disaster recovery best practices**.  

**Common Use Cases:**  
✅ **Ensure Replication is Enabled** – Verify that critical S3 buckets have replication configured.  
✅ **Validate Replication Rules** – Ensure objects with specific prefixes or tags are being replicated.  
✅ **Enforce Compliance & Data Redundancy** – Verify replication for backup, multi-region availability, or cross-account configurations.  

---

## 🔍 **How It Works**  
1️⃣ **Queries AWS S3** for bucket replication configurations.  
2️⃣ **Filters based on replication status, object filters, and other attributes.**  
3️⃣ **Returns matching S3 buckets** that meet or violate policy-defined replication rules.  

---

## 📝 **Example: Find S3 Buckets with Replication Enabled**  
This policy **filters S3 buckets where replication is enabled** and **objects with the prefix `test` and a tag `Owner: c7n` are being replicated**.  

```yaml
policies:
  - name: s3-bucket-replication
    resource: s3
    filters:
      - type: bucket-replication
        attrs:
          - Status: Enabled
          - Filter:
              And:
                Prefix: test
                Tags:
                  - Key: Owner
                    Value: c7n
          - ExistingObjectReplication: Enabled
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves S3 bucket replication configurations**.  
📌 The policy **matches buckets that have replication enabled**, specifically for:  
   - **Objects with the `test` prefix.**  
   - **Objects tagged with `Owner: c7n`**.  
   - **Existing objects are also replicated (`ExistingObjectReplication: Enabled`)**.  

---

## 📝 **Example: Identify Buckets Without Replication**  
This policy **finds S3 buckets that do NOT have replication enabled**, helping identify potential data redundancy risks.  

```yaml
policies:
  - name: s3-no-replication
    resource: s3
    filters:
      - type: bucket-replication
        attrs:
          - Status: Disabled
```

🔹 **What Happens?**  
📌 Cloud Custodian **detects S3 buckets where replication is disabled**.  
📌 Helps teams **enforce backup policies and ensure data durability across regions**.  

---

## 🎯 **Why Use Bucket-Replication Filtering?**  
✅ **Ensures Data Redundancy & Disaster Recovery:** Detects misconfigured replication settings.  
✅ **Supports Compliance Audits:** Ensures S3 buckets adhere to **backup and data retention policies**.  
✅ **Verifies Replication Scope:** Filters by **prefix-based and tag-based replication settings**.  

---

## ⚠ **Key Considerations**  
⚠ **Replication Must Be Preconfigured:** Ensure that replication rules exist before applying policies.  
⚠ **Cross-Region Replication (CRR) Requires IAM Permissions:** Ensure the replication role has correct S3 permissions.  
⚠ **Existing Object Replication (`ExistingObjectReplication`) is Optional:** It must be explicitly enabled for **pre-existing objects**.  

---

## 🛠 **Supported Bucket-Replication Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `attrs`       | `array`    | List of attributes to filter by (e.g., `Status`, `ExistingObjectReplication`). |
| `count`       | `number`   | Number of matching attributes required. |
| `count_op`    | `enum`     | Comparison operator (`eq`, `lt`, `gt`, etc.). |
| `type`        | `enum`     | Must be `bucket-replication`. **(Required)** |

---

## ✅ **Best Practices for S3 Replication Management**  
💡 **Ensure Replication is Configured for Critical Buckets:** Use replication for **disaster recovery and cross-region availability**.  
💡 **Monitor Replication Status Regularly:** Use Cloud Custodian to detect **disabled or misconfigured replication settings**.  
💡 **Verify IAM Roles for Replication Permissions:** Ensure the replication IAM role **has correct access to source and destination buckets**.  

---

## 🔹 **Check-Permissions: Verify IAM Permissions for AWS Resources**  

### ✨ **What is Check-Permissions?**  
The `check-permissions` filter in Cloud Custodian **examines IAM permissions associated with AWS resources**, helping organizations enforce **least privilege access**, **detect over-permissioned users**, and **audit security policies**.  

**Common Use Cases:**  
✅ **Identify Over-Permissioned Users** – Detect IAM users or roles with excessive privileges.  
✅ **Audit Compliance & Least Privilege Access** – Ensure IAM policies follow security best practices.  
✅ **Check for Specific Allowed or Denied Actions** – Find resources with permissions to perform critical operations.  

---

## 🔍 **How It Works**  
1️⃣ **Examines IAM policies** attached to users, roles, or resources.  
2️⃣ **Checks whether specific actions are allowed or denied** (`match: allowed` or `match: denied`).  
3️⃣ **Returns matching resources** that meet the filter criteria.  

---

## 📝 **Example: Find IAM Users Who Can Create New Users**  
This policy **identifies IAM users with the `iam:CreateUser` permission**, which allows them to create new IAM users.  

```yaml
policies:
  - name: super-users
    resource: aws.iam-user
    filters:
      - type: check-permissions
        match: allowed
        actions:
         - iam:CreateUser
```

🔹 **What Happens?**  
📌 Cloud Custodian **checks IAM policies attached to users**.  
📌 If a user **has permission to create other IAM users (`iam:CreateUser`)**, they are **included in the results**.  

---

## 📝 **Example: Find Admin Users with Full AWS Access (`*:*`)**  
This policy **detects IAM users with administrator-level privileges**, meaning they have full access to **all AWS services and actions**.  

```yaml
policies:
  - name: admin-users
    resource: aws.iam-user
    filters:
      - type: check-permissions
        match: allowed
        actions:
          - '*:*'
```

🔹 **What Happens?**  
📌 Cloud Custodian **scans IAM user policies** for unrestricted permissions.  
📌 Users **with full AWS access (`*:*`)** are flagged, helping security teams **identify over-permissioned users**.  

---

## 📝 **Example: Find Users Denied Access to S3 Buckets**  
This policy **detects IAM users who are explicitly denied access to `s3:ListBucket` operations**.  

```yaml
policies:
  - name: restricted-s3-users
    resource: aws.iam-user
    filters:
      - type: check-permissions
        match: denied
        actions:
          - s3:ListBucket
```

🔹 **What Happens?**  
📌 Cloud Custodian **checks IAM policies for explicit deny rules** related to `s3:ListBucket`.  
📌 **Users without bucket access** are flagged, helping administrators enforce security policies.  

---

## 🎯 **Why Use Check-Permissions?**  
✅ **Ensures Least Privilege Access:** Detects over-permissioned users and roles.  
✅ **Automates IAM Audits:** Helps track security risks in IAM policies.  
✅ **Supports Both Allowed & Denied Actions:** Flexible filtering for compliance enforcement.  

---

## ⚠ **Key Considerations**  
⚠ **Check IAM Boundaries When Needed:** Permission boundaries are checked **by default** but can be disabled.  
⚠ **Match Operator (`and` / `or`) Defines Behavior:** Use `and` to **require all permissions**, or `or` to **match any one**.  
⚠ **Wildcard Matching (`*:*`) is Powerful:** Be cautious when searching for full admin permissions—this may include intended system users.  

---

## 🛠 **Supported Check-Permissions Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `actions`      | `array`    | List of AWS actions to check (`iam:CreateUser`, `s3:ListBucket`, etc.). **(Required)** |
| `match`        | `enum`     | Whether the action should be `allowed` or `denied`. **(Required)** |
| `match-operator` | `enum`   | `and` (all actions must match) or `or` (any action can match). Default: `or`. |
| `boundaries`   | `boolean`  | Whether to consider permission boundaries. Default: `true`. |
| `type`         | `enum`     | Must be `check-permissions`. **(Required)** |

---

## ✅ **Best Practices for IAM Permission Audits**  
💡 **Regularly Scan IAM Users & Roles:** Detect permission changes that could introduce security risks.  
💡 **Restrict High-Risk Actions:** Ensure only authorized users can perform actions like `iam:CreateUser` or `s3:PutBucketPolicy`.  
💡 **Monitor for Unrestricted Access:** Track users with `*:*` permissions and limit admin roles as needed.  

---

## 🔹 **Client-Properties: Filter AWS WorkSpaces Directories Based on Client Properties**  

### ✨ **What is Client-Properties?**  
The `client-properties` filter in Cloud Custodian **evaluates WorkSpaces directory configurations** based on client properties, such as **reconnect behavior, authentication settings, and security controls**.  

**Common Use Cases:**  
✅ **Ensure Secure Authentication Settings** – Verify WorkSpaces directories meet security policies.  
✅ **Check Reconnect Policies** – Ensure users can or cannot reconnect based on compliance rules.  
✅ **Enforce Configuration Standards** – Ensure all WorkSpaces directories adhere to organizational policies.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves WorkSpaces directory configurations**.  
2️⃣ **Filters directories based on client properties** (e.g., `ReconnectEnabled`, `LoginTrailEnabled`).  
3️⃣ **Returns directories that match or violate the defined settings**.  

---

## 📝 **Example: Find WorkSpaces Directories with Reconnect Enabled**  
This policy **identifies WorkSpaces directories where reconnecting is enabled**.  

```yaml
policies:
  - name: workspace-client-credentials
    resource: aws.workspaces-directory
    filters:
      - type: client-properties
        key: ReconnectEnabled
        value: ENABLED
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves WorkSpaces directory client properties**.  
📌 Directories **with `ReconnectEnabled: ENABLED` are included in the results**.  
📌 Helps organizations **enforce policies on WorkSpaces session persistence**.  

---

## 📝 **Example: Identify WorkSpaces Directories with Login Trail Disabled**  
This policy **flags directories where login tracking (`LoginTrailEnabled`) is not enabled**, which may indicate **audit compliance gaps**.  

```yaml
policies:
  - name: workspace-client-login-trail-check
    resource: aws.workspaces-directory
    filters:
      - type: client-properties
        key: LoginTrailEnabled
        value: DISABLED
```

🔹 **What Happens?**  
📌 Cloud Custodian **checks whether `LoginTrailEnabled` is set to `DISABLED`**.  
📌 Flags directories **that do not meet security auditing requirements**.  

---

## 🎯 **Why Use Client-Properties Filtering?**  
✅ **Improves Security & Compliance:** Ensures WorkSpaces meet organizational security standards.  
✅ **Prevents Misconfigurations:** Detects incorrect client settings before they cause security issues.  
✅ **Automates Configuration Audits:** Regularly checks WorkSpaces directories for compliance.  

---

## ⚠ **Key Considerations**  
⚠ **Understand Reconnect Settings:** Some organizations may require session reconnection, while others may block it for security reasons.  
⚠ **Audit Login Tracking Regularly:** Ensure login trails are enabled for **audit logging and security visibility**.  
⚠ **Use Regex for Flexible Matching:** Use `value_regex` to **match multiple client properties dynamically**.  

---

## 🛠 **Supported Client-Properties Filter Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The client property to filter by (e.g., `ReconnectEnabled`, `LoginTrailEnabled`). |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value for the filter. |
| `value_regex` | `string`   | Regular expression pattern for matching values. |
| `value_type` | `enum`     | Data type (`integer`, `boolean`, `date`, etc.). |

---

## ✅ **Best Practices for WorkSpaces Client Property Audits**  
💡 **Ensure Secure Client Configurations:** Verify that WorkSpaces settings **align with security best practices**.  
💡 **Audit Login Tracking Settings:** Ensure `LoginTrailEnabled` is configured correctly for compliance.  
💡 **Automate Regular Checks:** Use Cloud Custodian to **scan and enforce security settings periodically**.  

---
## 🔹 **Config-Compliance: Filter AWS Resources Based on AWS Config Compliance Rules**  

### ✨ **What is Config-Compliance?**  
The `config-compliance` filter in Cloud Custodian **identifies AWS resources based on their compliance with AWS Config rules**. This allows organizations to **automate compliance audits, enforce security policies, and track misconfigured resources**.  

**Common Use Cases:**  
✅ **Detect Non-Compliant Resources** – Identify EC2 instances, S3 buckets, and other resources that fail AWS Config rules.  
✅ **Monitor Compliance Trends** – Track compliance violations over time.  
✅ **Automate Remediation** – Pair with `mark-for-op` or `notify` actions to enforce compliance.  

---

## 🔍 **How It Works**  
1️⃣ **Queries AWS Config for resource compliance data**.  
2️⃣ **Filters resources based on compliance state (`COMPLIANT`, `NON_COMPLIANT`, etc.)**.  
3️⃣ **Optionally applies evaluation filters** (e.g., find resources flagged non-compliant in the last 30 days).  
4️⃣ **Returns matching resources** for further action or remediation.  

---

## 📝 **Example: Find EC2 Instances That Failed Compliance in the Last 30 Days**  
This policy **identifies EC2 instances that are non-compliant with encryption and tagging rules** in the last 30 days.  

```yaml
policies:
  - name: non-compliant-ec2
    resource: ec2
    filters:
      - type: config-compliance
        eval_filters:
          - type: value
            key: ResultRecordedTime
            value_type: age
            value: 30
            op: less-than
        rules:
          - custodian-ec2-encryption-required
          - custodian-ec2-tags-required
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves AWS Config compliance evaluations** for EC2 instances.  
📌 It **filters instances that failed compliance checks (`NON_COMPLIANT`) in the last 30 days**.  
📌 Ensures **encryption and required tags are enforced across EC2 instances**.  

---

## 📝 **Example: Find All Non-Compliant S3 Buckets**  
This policy **identifies S3 buckets that are flagged as `NON_COMPLIANT` by AWS Config**.  

```yaml
policies:
  - name: s3-non-compliant-buckets
    resource: s3
    filters:
      - type: config-compliance
        states:
          - NON_COMPLIANT
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves S3 bucket compliance evaluations from AWS Config**.  
📌 It **filters out buckets that are non-compliant**, helping **security teams enforce data protection policies**.  

---

## 🎯 **Why Use Config-Compliance Filtering?**  
✅ **Automates Compliance Checks:** Detects resources violating AWS security best practices.  
✅ **Enhances Governance & Auditing:** Enables continuous monitoring for security and compliance teams.  
✅ **Works Across All AWS Services:** Applies to **EC2, S3, IAM, RDS, and more**.  

---

## ⚠ **Key Considerations**  
⚠ **Ensure AWS Config is Enabled:** AWS Config must be active and tracking required resources.  
⚠ **Combine with Remediation Actions:** Use `mark-for-op`, `notify`, or `tag` to take action on non-compliant resources.  
⚠ **Use Evaluation Filters for Time-Based Compliance Checks:** Track recent compliance violations effectively.  

---

## 🛠 **Supported Config-Compliance Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `rules`       | `array`    | List of AWS Config rules to check. **(Required)** |
| `states`      | `array`    | Compliance states (`COMPLIANT`, `NON_COMPLIANT`, etc.). |
| `eval_filters` | `array`   | Additional filters (e.g., compliance age, severity). |
| `op`         | `enum`     | Logical operator (`and`, `or`). Default: `and`. |
| `type`        | `enum`     | Must be `config-compliance`. **(Required)** |

---

## ✅ **Best Practices for AWS Config Compliance**  
💡 **Use AWS Config Rules to Define Security Standards:** Ensure AWS Config monitors **key compliance controls**.  
💡 **Track Compliance Over Time:** Use `eval_filters` to identify **recent compliance violations**.  
💡 **Automate Remediation for Non-Compliant Resources:** Apply `notify`, `tag`, or `mark-for-op` actions for governance.  

---

## 🔹 **Config-Compliance: Filter AWS Resources Based on AWS Config Compliance Rules**  

### ✨ **What is Config-Compliance?**  
The `config-compliance` filter in Cloud Custodian **identifies AWS resources based on their compliance with AWS Config rules**. This allows organizations to **automate compliance audits, enforce security policies, and track misconfigured resources**.  

**Common Use Cases:**  
✅ **Detect Non-Compliant Resources** – Identify EC2 instances, S3 buckets, and other resources that fail AWS Config rules.  
✅ **Monitor Compliance Trends** – Track compliance violations over time.  
✅ **Automate Remediation** – Pair with `mark-for-op` or `notify` actions to enforce compliance.  

---

## 🔍 **How It Works**  
1️⃣ **Queries AWS Config for resource compliance data**.  
2️⃣ **Filters resources based on compliance state (`COMPLIANT`, `NON_COMPLIANT`, etc.)**.  
3️⃣ **Optionally applies evaluation filters** (e.g., find resources flagged non-compliant in the last 30 days).  
4️⃣ **Returns matching resources** for further action or remediation.  

---

## 📝 **Example: Find EC2 Instances That Failed Compliance in the Last 30 Days**  
This policy **identifies EC2 instances that are non-compliant with encryption and tagging rules** in the last 30 days.  

```yaml
policies:
  - name: non-compliant-ec2
    resource: ec2
    filters:
      - type: config-compliance
        eval_filters:
          - type: value
            key: ResultRecordedTime
            value_type: age
            value: 30
            op: less-than
        rules:
          - custodian-ec2-encryption-required
          - custodian-ec2-tags-required
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves AWS Config compliance evaluations** for EC2 instances.  
📌 It **filters instances that failed compliance checks (`NON_COMPLIANT`) in the last 30 days**.  
📌 Ensures **encryption and required tags are enforced across EC2 instances**.  

---

## 📝 **Example: Find All Non-Compliant S3 Buckets**  
This policy **identifies S3 buckets that are flagged as `NON_COMPLIANT` by AWS Config**.  

```yaml
policies:
  - name: s3-non-compliant-buckets
    resource: s3
    filters:
      - type: config-compliance
        states:
          - NON_COMPLIANT
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves S3 bucket compliance evaluations from AWS Config**.  
📌 It **filters out buckets that are non-compliant**, helping **security teams enforce data protection policies**.  

---

## 🎯 **Why Use Config-Compliance Filtering?**  
✅ **Automates Compliance Checks:** Detects resources violating AWS security best practices.  
✅ **Enhances Governance & Auditing:** Enables continuous monitoring for security and compliance teams.  
✅ **Works Across All AWS Services:** Applies to **EC2, S3, IAM, RDS, and more**.  

---

## ⚠ **Key Considerations**  
⚠ **Ensure AWS Config is Enabled:** AWS Config must be active and tracking required resources.  
⚠ **Combine with Remediation Actions:** Use `mark-for-op`, `notify`, or `tag` to take action on non-compliant resources.  
⚠ **Use Evaluation Filters for Time-Based Compliance Checks:** Track recent compliance violations effectively.  

---

## 🛠 **Supported Config-Compliance Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `rules`       | `array`    | List of AWS Config rules to check. **(Required)** |
| `states`      | `array`    | Compliance states (`COMPLIANT`, `NON_COMPLIANT`, etc.). |
| `eval_filters` | `array`   | Additional filters (e.g., compliance age, severity). |
| `op`         | `enum`     | Logical operator (`and`, `or`). Default: `and`. |
| `type`        | `enum`     | Must be `config-compliance`. **(Required)** |

---

## ✅ **Best Practices for AWS Config Compliance**  
💡 **Use AWS Config Rules to Define Security Standards:** Ensure AWS Config monitors **key compliance controls**.  
💡 **Track Compliance Over Time:** Use `eval_filters` to identify **recent compliance violations**.  
💡 **Automate Remediation for Non-Compliant Resources:** Apply `notify`, `tag`, or `mark-for-op` actions for governance.  

---

## 🔹 **Configuration: Filter AWS Resources Based on Configuration Attributes**  

### ✨ **What is Configuration?**  
The `configuration` filter in Cloud Custodian **examines specific configuration attributes of AWS resources**, allowing organizations to **enforce best practices, detect misconfigurations, and maintain compliance**.  

**Common Use Cases:**  
✅ **Ensure Security & Compliance** – Validate that critical configurations meet organizational policies.  
✅ **Detect Configuration Drift** – Identify resources that deviate from expected settings.  
✅ **Audit Resource Settings** – Check for specific values, patterns, or missing attributes.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves configuration details** for AWS resources.  
2️⃣ **Applies filters based on key-value conditions** (e.g., `InstanceType`, `VpcId`, `EncryptionEnabled`).  
3️⃣ **Supports regex matching, numerical comparisons, and logical operators** for advanced filtering.  
4️⃣ **Returns resources that match or violate the defined criteria**.  

---

## 📝 **Example: Find EC2 Instances Without Encryption Enabled**  
This policy **identifies EC2 instances where encryption is not enabled for root EBS volumes**.  

```yaml
policies:
  - name: unencrypted-ec2
    resource: ec2
    filters:
      - type: configuration
        key: BlockDeviceMappings[0].Ebs.Encrypted
        value: false
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves EC2 instance configurations**.  
📌 **Checks if encryption is disabled (`false`) for the root EBS volume**.  
📌 **Flags non-compliant instances**, ensuring encryption best practices are followed.  

---

## 📝 **Example: Find S3 Buckets Without Logging Enabled**  
This policy **detects S3 buckets that do not have logging configured**, which is critical for security monitoring.  

```yaml
policies:
  - name: s3-bucket-no-logging
    resource: s3
    filters:
      - type: configuration
        key: LoggingEnabled
        value: absent
```

🔹 **What Happens?**  
📌 Cloud Custodian **checks the `LoggingEnabled` attribute for each S3 bucket**.  
📌 **Flags buckets where logging is not configured**, helping **enhance security and visibility**.  

---

## 🎯 **Why Use Configuration Filtering?**  
✅ **Ensures AWS Resources Follow Best Practices:** Automates configuration enforcement.  
✅ **Detects Misconfigurations Before They Cause Issues:** Identifies non-compliant resources proactively.  
✅ **Flexible & Powerful Filtering Options:** Supports regex, numerical comparisons, and logical conditions.  

---

## ⚠ **Key Considerations**  
⚠ **Configuration Keys Must Be Valid:** Ensure the `key` matches the resource's API attributes.  
⚠ **Use Regex & Operators for Advanced Filtering:** `value_regex`, `op`, and `value_type` allow complex queries.  
⚠ **Monitor Configurations Regularly:** Combine with `notify` or `mark-for-op` to track and remediate misconfigurations.  

---

## 🛠 **Supported Configuration Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The configuration attribute to filter by (e.g., `VpcId`, `InstanceType`). |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value for the filter. |
| `value_regex` | `string`   | Regular expression pattern for matching values. |
| `value_type` | `enum`     | Data type (`integer`, `boolean`, `date`, etc.). |

---

## ✅ **Best Practices for Configuration Auditing**  
💡 **Regularly Audit Resource Configurations:** Use Cloud Custodian to **detect unwanted changes automatically**.  
💡 **Enforce Encryption & Security Settings:** Ensure **critical resources like EC2, RDS, and S3** meet security standards.  
💡 **Use Logical Operators for Complex Checks:** Combine `and`, `or`, and `not` filters for **advanced policy enforcement**.  

---

## 🔹 **Connection-Aliases: Filter AWS WorkSpaces Directories by Connection Aliases**  

### ✨ **What is Connection-Aliases?**  
The `connection-aliases` filter in Cloud Custodian **evaluates AWS WorkSpaces directories based on their connection alias configurations**. This helps organizations **manage remote access, ensure secure configurations, and maintain directory consistency**.  

**Common Use Cases:**  
✅ **Identify WorkSpaces Without Connection Aliases** – Detect WorkSpaces that lack assigned aliases.  
✅ **Verify Alias Configuration** – Ensure correct aliases are in place for routing and security.  
✅ **Audit and Enforce Network Access Policies** – Validate alias assignments for compliance.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves AWS WorkSpaces directory configurations**.  
2️⃣ **Filters based on assigned connection aliases** (`ConnectionAliases`).  
3️⃣ **Supports regex matching, numerical comparisons, and logical operators** for advanced filtering.  
4️⃣ **Returns directories that match or violate the defined criteria**.  

---

## 📝 **Example: Find WorkSpaces Without Connection Aliases**  
This policy **identifies WorkSpaces directories where no connection alias is assigned**.  

```yaml
policies:
  - name: workspace-connection-alias
    resource: aws.workspaces-directory
    filters:
      - type: connection-aliases
        key: 'ConnectionAliases'
        value: 'empty'
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves the `ConnectionAliases` attribute for WorkSpaces directories**.  
📌 If **no connection alias is set (`empty`)**, the directory is **included in the results**.  
📌 Ensures **proper alias configurations for remote access and compliance**.  

---

## 📝 **Example: Find WorkSpaces with Specific Connection Aliases**  
This policy **filters WorkSpaces directories that use specific connection aliases** for access control.  

```yaml
policies:
  - name: workspace-connection-alias-check
    resource: aws.workspaces-directory
    filters:
      - type: connection-aliases
        key: 'ConnectionAliases'
        value_regex: '^secure-access-*'
```

🔹 **What Happens?**  
📌 Cloud Custodian **matches directories with connection aliases starting with `secure-access-`**.  
📌 Helps ensure **only approved aliases are used for remote access**.  

---

## 🎯 **Why Use Connection-Aliases Filtering?**  
✅ **Ensures Secure & Consistent WorkSpaces Access:** Detects missing or misconfigured connection aliases.  
✅ **Automates Compliance Audits:** Identifies directories that do not meet network policies.  
✅ **Flexible Filtering Options:** Supports regex, logical conditions, and direct value matching.  

---

## ⚠ **Key Considerations**  
⚠ **Verify Alias Usage Before Removing Entries:** Ensure aliases are not required for critical access before enforcing changes.  
⚠ **Monitor for Unauthorized Alias Usage:** Regularly check for **unauthorized alias assignments**.  
⚠ **Use Regex for Dynamic Checks:** Apply **pattern-based filtering** to match multiple alias formats.  

---

## 🛠 **Supported Connection-Aliases Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The attribute to filter by (e.g., `ConnectionAliases`). |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value for the filter. |
| `value_regex` | `string`   | Regular expression pattern for matching values. |
| `value_type` | `enum`     | Data type (`integer`, `boolean`, `date`, etc.). |

---

## ✅ **Best Practices for WorkSpaces Connection Management**  
💡 **Ensure All WorkSpaces Have Valid Aliases:** Helps enforce **consistent network access policies**.  
💡 **Use Pattern-Based Filtering for Dynamic Checks:** Ensure aliases **match expected naming conventions**.  
💡 **Regularly Audit Connection Aliases:** Use Cloud Custodian to **identify and correct alias misconfigurations**.  

---

## 🔹 **Cost-Optimization: Identify AWS Cost Optimization Opportunities**  

### ✨ **What is Cost-Optimization?**  
The `cost-optimization` filter in Cloud Custodian **analyzes AWS resources based on AWS Cost Optimization Hub recommendations**, helping organizations **reduce cloud expenses** while maintaining efficiency.  

**Common Use Cases:**  
✅ **Identify Underutilized Resources** – Detect idle EC2 instances, RDS databases, or other services.  
✅ **Recommend Rightsizing & Upgrades** – Suggest moving workloads to more cost-effective options.  
✅ **Highlight Savings Plan & Reserved Instance Opportunities** – Identify resources that could benefit from long-term savings commitments.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves AWS Cost Optimization Hub recommendations**.  
2️⃣ **Filters recommendations based on action types** (`Rightsize`, `Stop`, `Upgrade`, etc.).  
3️⃣ **Applies additional filters** for estimated savings, lookback periods, and effort levels.  
4️⃣ **Returns AWS resources that can be optimized for cost savings**.  

---

## 📝 **Example: Identify EC2 Instances That Should Be Rightsized**  
This policy **finds EC2 instances with rightsizing recommendations, where potential monthly savings exceed $30, and the recommendation is at least 10 days old**.  

```yaml
policies:
  - name: cost-ec2-optimize
    resource: aws.ec2
    filters:
      - type: cost-optimization
        attrs:
          - actionType: Rightsize
          - key: recommendationLookbackPeriodInDays
            op: gte
            value: 10
          - key: estimatedMonthlySavings
            value: 30
            op: gte
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves AWS Cost Optimization Hub recommendations** for EC2 instances.  
📌 Filters results to **only include instances where**:  
   - **AWS recommends rightsizing (`actionType: Rightsize`)**.  
   - **The recommendation has been available for at least 10 days**.  
   - **The estimated monthly savings is at least $30**.  

---

## 📝 **Example: Identify Workloads That Should Be Migrated to Graviton**  
This policy **flags workloads that AWS recommends migrating to Graviton-based instances for cost savings**.  

```yaml
policies:
  - name: migrate-to-graviton
    resource: aws.ec2
    filters:
      - type: cost-optimization
        attrs:
          - actionType: MigrateToGraviton
          - key: estimatedMonthlySavings
            value: 50
            op: gte
```

🔹 **What Happens?**  
📌 Cloud Custodian **finds EC2 instances where AWS suggests moving to Graviton-based instances**.  
📌 **Only instances with at least $50 in monthly savings are included**.  

---

## 🎯 **Why Use Cost-Optimization Filtering?**  
✅ **Reduces AWS Costs:** Helps organizations **identify waste and optimize resources**.  
✅ **Automates Cost Recommendations:** Leverages **AWS Cost Optimization Hub insights**.  
✅ **Supports Various Optimization Strategies:** Rightsizing, stopping unused resources, upgrading, and purchasing savings plans.  

---

## ⚠ **Key Considerations**  
⚠ **Review Recommendations Before Taking Action:** Not all recommendations may be suitable for immediate execution.  
⚠ **Effort Levels Matter:** AWS assigns an **effort rating (`VeryLow` to `VeryHigh`)** to indicate how complex a recommendation is.  
⚠ **Combine with Lifecycle Actions:** Use **`mark-for-op` or `notify`** to plan or schedule cost-saving changes.  

---

## 🛠 **Supported Cost-Optimization Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `action`      | `enum`     | Cost optimization action (`Rightsize`, `Stop`, `Upgrade`, `MigrateToGraviton`, etc.). |
| `attrs`       | `array`    | Filters based on attributes like `estimatedMonthlySavings`, `recommendationLookbackPeriodInDays`. |
| `efforts`     | `array`    | Effort level required to apply the recommendation (`VeryLow`, `Low`, `Medium`, etc.). |
| `type`        | `enum`     | Must be `cost-optimization`. **(Required)** |

---

## ✅ **Best Practices for Cost Optimization**  
💡 **Regularly Review Optimization Recommendations:** Run policies **monthly or weekly** to identify savings opportunities.  
💡 **Prioritize High-Impact Savings:** Focus on **rightsizing, stopping unused resources, and committing to savings plans**.  
💡 **Automate Cost Remediation:** Use `notify` or `mark-for-op` to **plan and execute cost-saving changes**.  

---

## 🔹 **Domain-Options: Filter AWS CloudSearch Domains Based on Configuration Options**  

### ✨ **What is Domain-Options?**  
The `domain-options` filter in Cloud Custodian **checks configuration settings of AWS CloudSearch domains**, allowing organizations to **enforce security, performance, and compliance policies**.  

**Common Use Cases:**  
✅ **Ensure Secure HTTPS Access** – Verify that CloudSearch domains enforce HTTPS.  
✅ **Detect Misconfigurations** – Identify domains that do not meet operational policies.  
✅ **Audit Performance & Scalability Settings** – Ensure domains use optimal configurations.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves AWS CloudSearch domain configurations**.  
2️⃣ **Filters domains based on specific attributes** (e.g., `EnforceHTTPS`, `MultiAZ`).  
3️⃣ **Supports advanced filtering options** (e.g., regex, numerical comparisons).  
4️⃣ **Returns CloudSearch domains that match or violate the defined settings**.  

---

## 📝 **Example: Detect CloudSearch Domains Without HTTPS Enforcement**  
This policy **identifies CloudSearch domains where HTTPS is not enforced**, helping enforce **secure connections**.  

```yaml
policies:
  - name: cloudsearch-detect-https
    resource: cloudsearch
    filters:
      - type: domain-options
        key: Options.EnforceHTTPS
        value: false
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves CloudSearch domain configurations**.  
📌 Domains **without HTTPS enforcement (`EnforceHTTPS: false`) are flagged**.  
📌 Helps ensure **secure data transmission** for CloudSearch services.  

---

## 📝 **Example: Find CloudSearch Domains Not Using Multi-AZ**  
This policy **flags CloudSearch domains that are not configured for Multi-AZ** availability.  

```yaml
policies:
  - name: cloudsearch-multi-az-check
    resource: cloudsearch
    filters:
      - type: domain-options
        key: Options.MultiAZ
        value: false
```

🔹 **What Happens?**  
📌 Cloud Custodian **identifies CloudSearch domains where Multi-AZ support is disabled**.  
📌 Helps ensure **high availability and fault tolerance** for CloudSearch deployments.  

---

## 🎯 **Why Use Domain-Options Filtering?**  
✅ **Enhances Security & Compliance:** Ensures **HTTPS enforcement, IAM policies, and encryption settings** are configured correctly.  
✅ **Optimizes Performance & Availability:** Validates **Multi-AZ configurations and indexing options**.  
✅ **Automates CloudSearch Audits:** Reduces manual checks for misconfigurations.  

---

## ⚠ **Key Considerations**  
⚠ **Verify Default AWS CloudSearch Settings:** Some settings may be disabled by default—ensure policies account for expected configurations.  
⚠ **Use Regex for Pattern-Based Checks:** If multiple settings have common attributes, **use `value_regex` for dynamic filtering**.  
⚠ **Monitor Compliance Over Time:** Combine this filter with **`notify` or `mark-for-op`** for automated remediation workflows.  

---

## 🛠 **Supported Domain-Options Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The CloudSearch configuration attribute to filter by (e.g., `EnforceHTTPS`, `MultiAZ`). |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value for the filter. |
| `value_regex` | `string`   | Regular expression pattern for matching values. |
| `value_type` | `enum`     | Data type (`integer`, `boolean`, `date`, etc.). |

---

## ✅ **Best Practices for CloudSearch Configuration Management**  
💡 **Ensure HTTPS is Enforced:** Prevent unencrypted data transmission **by enforcing `EnforceHTTPS: true`**.  
💡 **Enable Multi-AZ for High Availability:** Ensure **critical workloads remain resilient** in case of failures.  
💡 **Regularly Audit CloudSearch Configurations:** Use Cloud Custodian to **detect and remediate misconfigurations** proactively.  

---

## 🔹 **EC2-Metadata-Defaults: Audit Default IMDS Settings in AWS Accounts**  

### ✨ **What is EC2-Metadata-Defaults?**  
The `ec2-metadata-defaults` filter in Cloud Custodian **checks the default EC2 Instance Metadata Service (IMDS) settings** at the AWS account and region level. This helps organizations **ensure secure default configurations for new EC2 instances**.  

**Common Use Cases:**  
✅ **Ensure IMDSv2 is Enforced** – Detect accounts where `HttpTokens` is set to `optional` instead of `required`.  
✅ **Audit Security Configurations** – Verify that default metadata settings align with security best practices.  
✅ **Prevent Misconfigurations** – Ensure new EC2 instances follow secure defaults at the account level.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves AWS account-level default EC2 metadata settings**.  
2️⃣ **Filters based on attributes such as `HttpTokens` (IMDS version enforcement)**.  
3️⃣ **Returns accounts where settings do not meet security policies**.  

---

## 📝 **Example: Identify Accounts with Weak IMDS Settings**  
This policy **identifies AWS accounts where `HttpTokens` is set to `optional` or is absent**, meaning that **IMDSv2 is not enforced** by default for new EC2 instances.  

```yaml
policies:
  - name: ec2-imds-defaults
    resource: account
    filters:
      - or:
          - type: ec2-metadata-defaults
            key: HttpTokens
            value: optional
          - type: ec2-metadata-defaults
            key: HttpTokens
            value: absent
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves the default EC2 metadata settings for the account**.  
📌 Flags accounts where **IMDSv2 is not enforced (`HttpTokens: optional`)** or where the setting **has never been configured (`absent`)**.  

---

## 📝 **Example: Enforce IMDSv2 Across All AWS Accounts**  
This policy **ensures that all accounts enforce `HttpTokens: required` to mandate IMDSv2**.  

```yaml
policies:
  - name: enforce-imds-v2
    resource: account
    filters:
      - type: ec2-metadata-defaults
        key: HttpTokens
        value: required
```

🔹 **What Happens?**  
📌 Only accounts where `HttpTokens` is **already set to `required`** are returned.  
📌 Helps **track compliance with AWS security best practices**.  

---

## 🎯 **Why Use EC2-Metadata-Defaults Filtering?**  
✅ **Prevents Metadata Service Exploits:** IMDSv2 **mitigates SSRF (Server-Side Request Forgery) attacks**.  
✅ **Enforces Security Standards at Scale:** Ensures **all new EC2 instances** in an AWS account use secure defaults.  
✅ **Simplifies Compliance Audits:** Easily **identify accounts that need metadata security improvements**.  

---

## ⚠ **Key Considerations**  
⚠ **Defaults Apply Only to New Instances:** This policy **does not affect existing EC2 instances**—use separate policies to audit running instances.  
⚠ **Settings May Be Absent:** If `HttpTokens` was **never explicitly set**, it **does not appear in the AWS response**.  
⚠ **Pair with Instance-Level Checks:** Combine with **EC2 instance metadata settings audits** to **ensure full compliance**.  

---

## 🛠 **Supported EC2-Metadata-Defaults Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The IMDS configuration attribute to check (e.g., `HttpTokens`). |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value for the filter (e.g., `required`, `optional`). |
| `value_regex` | `string`   | Regular expression pattern for matching values. |
| `value_type` | `enum`     | Data type (`integer`, `boolean`, `date`, etc.). |

---

## ✅ **Best Practices for AWS EC2 Metadata Security**  
💡 **Enforce IMDSv2 by Default:** Ensure **all new EC2 instances use IMDSv2 (`HttpTokens: required`)**.  
💡 **Monitor Metadata Settings Across All Accounts:** Regularly **audit AWS account settings** to detect changes.  
💡 **Combine with Instance-Level Audits:** Use Cloud Custodian to check **IMDS settings on running instances**.  

---

## 🔹 **Engine: Filter RDS Instances Based on Engine Metadata**  

### ✨ **What is Engine?**  
The `engine` filter in Cloud Custodian **analyzes the engine metadata of AWS RDS instances**, allowing organizations to **detect outdated versions, enforce best practices, and ensure database compliance**.  

**Common Use Cases:**  
✅ **Identify Deprecated Database Versions** – Detect RDS instances running outdated or unsupported database engines.  
✅ **Audit Database Engine Status** – Ensure all RDS instances meet security and performance guidelines.  
✅ **Track Database Lifecycle Changes** – Monitor instances that require upgrades or migrations.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves AWS RDS instance engine metadata**.  
2️⃣ **Filters based on attributes such as `Status`, `Engine`, `EngineVersion`**.  
3️⃣ **Supports regex, numerical comparisons, and logical operators** for advanced filtering.  
4️⃣ **Returns RDS instances that match or violate defined engine requirements**.  

---

## 📝 **Example: Find RDS Instances Running Deprecated Database Versions**  
This policy **identifies RDS instances running database engines marked as `deprecated`**.  

```yaml
policies:
  - name: find-deprecated-versions
    resource: aws.rds
    filters:
      - type: engine
        key: Status
        value: deprecated
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves the engine metadata for all RDS instances**.  
📌 Instances **with `Status: deprecated` are flagged**, ensuring teams are aware of outdated versions.  

---

## 📝 **Example: Identify RDS Instances Running MySQL 5.7 or Older**  
This policy **flags RDS instances running MySQL versions older than 8.0**.  

```yaml
policies:
  - name: detect-old-mysql-instances
    resource: aws.rds
    filters:
      - type: engine
        key: Engine
        value: mysql
      - type: engine
        key: EngineVersion
        value_regex: "^(5\\.7|5\\..*)"
```

🔹 **What Happens?**  
📌 Cloud Custodian **identifies RDS instances running MySQL**.  
📌 It **flags instances running MySQL 5.7 or earlier**, ensuring teams prioritize upgrades.  

---

## 🎯 **Why Use Engine Filtering?**  
✅ **Ensures Database Security & Compliance:** Detects outdated or insecure database versions.  
✅ **Automates Database Lifecycle Audits:** Identifies instances that require upgrades or maintenance.  
✅ **Optimizes Performance & Cost:** Ensures all RDS instances **run on supported and optimized versions**.  

---

## ⚠ **Key Considerations**  
⚠ **AWS Regularly Deprecates Older RDS Versions:** Keep track of **AWS announcements for version deprecations**.  
⚠ **Use Regex for Dynamic Version Checks:** Regular expressions **simplify matching multiple outdated versions**.  
⚠ **Combine with Remediation Actions:** Pair this filter with **`notify` or `mark-for-op`** to plan version upgrades.  

---

## 🛠 **Supported Engine Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The RDS engine attribute to check (e.g., `Engine`, `EngineVersion`, `Status`). |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value for the filter (e.g., `mysql`, `deprecated`). |
| `value_regex` | `string`   | Regular expression pattern for matching values. |
| `value_type` | `enum`     | Data type (`integer`, `boolean`, `date`, etc.). |

---

## ✅ **Best Practices for RDS Engine Auditing**  
💡 **Regularly Audit RDS Engine Versions:** Prevent **running unsupported or vulnerable database versions**.  
💡 **Use AWS RDS Upgrade Paths:** Plan **version upgrades proactively** to avoid disruptions.  
💡 **Monitor Engine Deprecation Notices:** AWS **periodically discontinues support for older versions**—stay updated.  

---

## 🔹 **Event: Filter AWS Resources Based on Events**  

### ✨ **What is Event Filtering?**  
The `event` filter in Cloud Custodian **triggers policies based on specific AWS events**, allowing organizations to **detect, respond, and automate actions for key operational changes** in real-time.  

**Common Use Cases:**  
✅ **Detect Changes in Resource State** – Identify newly created, modified, or deleted resources.  
✅ **Automate Incident Response** – Trigger actions based on security-related events (e.g., IAM changes).  
✅ **Monitor Compliance & Governance** – Ensure resources adhere to predefined configurations upon modification.  

---

## 🔍 **How It Works**  
1️⃣ **Monitors AWS event logs (CloudTrail, EventBridge, or other sources).**  
2️⃣ **Filters events based on attributes** (e.g., `eventName`, `eventSource`).  
3️⃣ **Applies logic to match specific events** (regex, numerical comparisons, etc.).  
4️⃣ **Returns resources that match defined event conditions** for further processing.  

---

## 📝 **Example: Detect EC2 Instance Creation Events**  
This policy **detects newly created EC2 instances by filtering on `RunInstances` events**.  

```yaml
policies:
  - name: detect-ec2-creation
    resource: ec2
    filters:
      - type: event
        key: eventName
        value: RunInstances
```

🔹 **What Happens?**  
📌 Cloud Custodian **monitors AWS events** and filters for **EC2 instance creation (`RunInstances`)**.  
📌 Only instances **created via this event are included in the results**.  

---

## 📝 **Example: Track IAM Policy Changes**  
This policy **flags changes to IAM policies to detect unauthorized modifications**.  

```yaml
policies:
  - name: detect-iam-policy-changes
    resource: aws.iam-policy
    filters:
      - type: event
        key: eventName
        value: PutRolePolicy
```

🔹 **What Happens?**  
📌 Cloud Custodian **detects IAM policy updates (`PutRolePolicy`)** in AWS logs.  
📌 Helps security teams **identify unauthorized role policy modifications**.  

---

## 🎯 **Why Use Event Filtering?**  
✅ **Enhances Security Monitoring:** Detects unauthorized access or configuration changes.  
✅ **Automates Cloud Operations:** Allows **event-driven automation** for resource lifecycle management.  
✅ **Provides Real-Time Compliance Enforcement:** Ensures **newly created or modified resources meet security standards**.  

---

## ⚠ **Key Considerations**  
⚠ **Events Must Be Logged in CloudTrail or EventBridge:** Ensure relevant AWS services are capturing required events.  
⚠ **Use Regex for Flexible Matching:** If multiple events need filtering, **use `value_regex` for pattern-based matching**.  
⚠ **Pair with Action Policies for Automation:** Use event detection alongside **tagging, notifications, or remediation actions**.  

---

## 🛠 **Supported Event Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The event attribute to filter by (e.g., `eventName`, `eventSource`). |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value for the filter (e.g., `RunInstances`, `PutRolePolicy`). |
| `value_regex` | `string`   | Regular expression pattern for matching event values. |
| `value_type` | `enum`     | Data type (`integer`, `boolean`, `date`, etc.). |

---

## ✅ **Best Practices for Event Monitoring**  
💡 **Track Critical AWS Events:** Monitor key services like **EC2, IAM, RDS, and S3** for changes.  
💡 **Integrate with Security Tools:** Combine with **AWS GuardDuty, AWS Security Hub, or SIEM tools**.  
💡 **Automate Responses:** Use **event filtering with actions like `notify`, `mark-for-op`, or `tag`** to automate remediation.  

---

## 🔹 **Finding: Identify Security Hub Findings Related to AWS Resources**  

### ✨ **What is Finding?**  
The `finding` filter in Cloud Custodian **checks AWS Security Hub for security-related findings** related to specific resources. This allows organizations to **identify risks, enforce compliance, and automate security audits**.  

**Common Use Cases:**  
✅ **Detect Security Vulnerabilities** – Identify misconfigurations flagged by AWS Security Hub.  
✅ **Automate Compliance Monitoring** – Track failed checks from **AWS Foundational Security Best Practices, CIS Benchmark, and PCI DSS**.  
✅ **Prioritize Incident Response** – Find resources with **active security findings** and take immediate action.  

---

## 🔍 **How It Works**  
1️⃣ **Queries AWS Security Hub for findings related to a resource**.  
2️⃣ **Filters based on specific security findings** (e.g., finding ID, compliance status, severity).  
3️⃣ **Returns matching resources with security issues** for further action or remediation.  

---

## 📝 **Example: Identify IAM Roles with Security Findings**  
This policy **flags IAM roles that have any active findings in AWS Security Hub**.  

```yaml
policies:
  - name: iam-roles-with-findings
    resource: aws.iam-role
    filters:
      - finding
```

🔹 **What Happens?**  
📌 Cloud Custodian **checks AWS Security Hub** for findings related to IAM roles.  
📌 **Any IAM role with an active security finding** is flagged.  
📌 Helps **security teams investigate and remediate misconfigurations**.  

---

## 📝 **Example: Detect IAM Roles with Risky KMS Decryption Permissions**  
This policy **identifies IAM roles with inline policies allowing unrestricted KMS decryption (`KMS.2` security check in AWS Security Hub)**.  

```yaml
policies:
  - name: iam-roles-with-global-kms-decrypt
    resource: aws.iam-role
    filters:
      - type: finding
        query:
          Id:
            - Comparison: PREFIX
              Value: 'arn:aws:securityhub:{region}:{account_id}:subscription/aws-foundational-security-best-practices/v/1.0.0/KMS.2'
          Title:
            - Comparison: EQUALS
              Value: >-
                KMS.2 IAM principals should not have IAM inline policies
                that allow decryption actions on all KMS keys
          ComplianceStatus:
            - Comparison: EQUALS
              Value: 'FAILED'
          RecordState:
            - Comparison: EQUALS
              Value: 'ACTIVE'
```

🔹 **What Happens?**  
📌 Cloud Custodian **checks Security Hub for IAM roles violating KMS decryption security best practices (`KMS.2`)**.  
📌 Filters only for findings that are **`FAILED` (non-compliant) and `ACTIVE` (not remediated)**.  
📌 Helps **detect and mitigate risky IAM policies** that allow unrestricted KMS decryption.  

---

## 🎯 **Why Use Finding Filtering?**  
✅ **Automates Security Audits:** Continuously checks for AWS Security Hub findings on cloud resources.  
✅ **Prioritizes High-Risk Issues:** Filters findings based on severity, compliance status, and record state.  
✅ **Supports Customizable Queries:** Allows flexible searching for **specific security checks, policies, and compliance failures**.  

---

## ⚠ **Key Considerations**  
⚠ **AWS Security Hub Must Be Enabled:** Findings will only be available if Security Hub is enabled in your AWS account.  
⚠ **Finding IDs Change Over Time:** Regularly update queries to **match current security best practices and AWS recommendations**.  
⚠ **Use PREFIX Matching for Finding IDs:** AWS generates different finding IDs per region and account—**use `PREFIX` to match all accounts/regions**.  

---

## 🛠 **Supported Finding Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `query`       | `object`   | Defines conditions to match Security Hub findings (e.g., `Id`, `Title`, `ComplianceStatus`). |
| `region`      | `string`   | Specifies the AWS region for filtering Security Hub findings. |
| `type`        | `enum`     | Must be `finding`. **(Required)** |

---

## ✅ **Best Practices for Security & Compliance Monitoring**  
💡 **Track Critical Security Findings:** Focus on findings **related to IAM, S3, RDS, and network security**.  
💡 **Combine with Remediation Actions:** Use `notify`, `mark-for-op`, or `tag` to **automate security responses**.  
💡 **Monitor Compliance Frameworks:** Regularly audit **AWS Foundational Security Best Practices, CIS Benchmarks, and PCI DSS**.  

---

## 🔹 **Flow-Logs: Verify and Audit AWS VPC Flow Logs Configuration**  

### ✨ **What is Flow-Logs?**  
The `flow-logs` filter in Cloud Custodian **checks whether VPC Flow Logs are enabled for AWS resources**. It allows organizations to **enforce network monitoring, detect misconfigurations, and ensure compliance with security best practices**.  

**Common Use Cases:**  
✅ **Ensure Flow Logs Are Enabled on All VPCs** – Detect VPCs that do not have flow logs enabled.  
✅ **Audit Flow Log Configuration** – Ensure logs capture all traffic and are stored in the correct location.  
✅ **Monitor Compliance for Security & Incident Response** – Verify that flow logs are correctly set up for monitoring.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves Flow Log settings for AWS VPCs, Subnets, or Network Interfaces**.  
2️⃣ **Filters resources based on Flow Log attributes** (e.g., `TrafficType`, `LogGroupName`, `FlowLogStatus`).  
3️⃣ **Supports advanced filtering** (e.g., checking if logs are sent to CloudWatch, verifying status).  
4️⃣ **Returns VPCs or other network resources with missing or misconfigured Flow Logs**.  

---

## 📝 **Example: Detect VPCs Without Flow Logs Enabled**  
This policy **identifies VPCs that do not have Flow Logs enabled**, helping ensure **network activity is being recorded**.  

```yaml
policies:
  - name: flow-logs-enabled
    resource: vpc
    filters:
      - flow-logs
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves VPC Flow Log configurations**.  
📌 **Only VPCs with Flow Logs enabled are returned** (use `not` for missing logs).  
📌 Helps organizations **ensure compliance with security policies**.  

---

## 📝 **Example: Identify VPCs Without Active Flow Logs or Incorrect Configurations**  
This policy **flags VPCs that have Flow Logs enabled but are not logging all traffic or are inactive**.  

```yaml
policies:
  - name: flow-mis-configured
    resource: vpc
    filters:
      - not:
          - type: flow-logs
            attrs:
              - TrafficType: ALL
              - FlowLogStatus: ACTIVE
              - LogGroupName: vpc-logs
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves VPC Flow Log settings**.  
📌 **Filters VPCs where**:  
   - Flow logs are not capturing **all traffic** (`TrafficType: ALL`).  
   - Logs are not in an **active state** (`FlowLogStatus: ACTIVE`).  
   - Logs are not being sent to the **correct CloudWatch log group** (`LogGroupName: vpc-logs`).  

---

## 🎯 **Why Use Flow-Logs Filtering?**  
✅ **Ensures Network Visibility & Security:** Helps security teams monitor VPC traffic logs.  
✅ **Improves Incident Response:** Ensures logs are available for forensic analysis.  
✅ **Supports Compliance Frameworks:** Meets regulatory requirements for **AWS security best practices, PCI DSS, and SOC 2**.  

---

## ⚠ **Key Considerations**  
⚠ **Flow Logs May Be Disabled by Default:** Ensure logs are **explicitly enabled** for new VPCs and resources.  
⚠ **Check Log Destination (`destination-type`) Carefully:** Logs can be stored in **CloudWatch Logs or S3**—validate the correct destination.  
⚠ **Ensure Correct Log Retention Policy:** Ensure logs are **retained for an appropriate duration** based on compliance requirements.  

---

## 🛠 **Supported Flow-Logs Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `attrs`       | `array`    | List of attributes to filter by (e.g., `TrafficType`, `FlowLogStatus`). |
| `traffic-type` | `enum`     | Type of traffic to log (`accept`, `reject`, `all`). |
| `destination-type` | `enum`  | Where logs are stored (`s3`, `cloud-watch-logs`). |
| `log-group`    | `string`   | CloudWatch Log Group where logs are stored. |
| `status`      | `enum`     | Flow log status (`active`). |
| `enabled`     | `boolean`  | Whether Flow Logs are enabled (`true` or `false`). |
| `deliver-status` | `enum`  | Log delivery status (`success`, `failure`). |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |

---

## ✅ **Best Practices for VPC Flow Log Monitoring**  
💡 **Ensure Flow Logs Are Enabled Across All VPCs:** Monitor **all traffic (accept & reject)** for security and compliance.  
💡 **Verify Log Storage & Retention Policies:** Store logs in **secure locations (CloudWatch or S3) with appropriate retention settings**.  
💡 **Regularly Audit Flow Log Configurations:** Use Cloud Custodian to **detect misconfigurations or disabled logs**.  

---

## 🔹 **Gateway-Route: Filter AWS App Mesh Gateway Routes**  

### ✨ **What is Gateway-Route?**  
The `gateway-route` filter in Cloud Custodian **analyzes AWS App Mesh Gateway Routes**, allowing organizations to **enforce security policies, validate configurations, and monitor service mesh ownership**.  

**Common Use Cases:**  
✅ **Ensure Gateway Routes Are Properly Configured** – Detect misconfigured App Mesh gateway routes.  
✅ **Verify Mesh Ownership** – Identify gateway routes that are owned by external accounts.  
✅ **Enforce Service Mesh Policies** – Validate routing configurations across virtual gateways.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves AWS App Mesh Gateway Route configurations**.  
2️⃣ **Filters resources based on attributes like `meshOwner`, `routeType`, and `virtualService`**.  
3️⃣ **Supports regex, numerical comparisons, and logical operators** for advanced filtering.  
4️⃣ **Returns AWS App Mesh Virtual Gateways with matching or non-compliant gateway routes**.  

---

## 📝 **Example: Identify App Mesh Gateway Routes Owned by External Accounts**  
This policy **detects App Mesh gateway routes where the mesh owner is different from the resource owner**.  

```yaml
policies:
  - name: appmesh-gateway-route-policy
    resource: aws.appmesh-virtualgateway
    filters:
      - type: gateway-route
        attrs:
          - type: value
            key: meshOwner
            op: ne
            value: resourceOwner
            value_type: expr
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves AWS App Mesh Gateway Route configurations**.  
📌 Flags gateway routes where **the mesh is owned by an external AWS account (`meshOwner ≠ resourceOwner`)**.  
📌 Ensures **service mesh configurations are controlled by internal teams**.  

---

## 📝 **Example: Detect Gateway Routes Without TLS Enforcement**  
This policy **flags App Mesh gateway routes that do not enforce TLS encryption**.  

```yaml
policies:
  - name: appmesh-insecure-gateway-routes
    resource: aws.appmesh-virtualgateway
    filters:
      - type: gateway-route
        attrs:
          - key: route.httpRoute.match.headers[].match.exact
            op: ne
            value: "TLS"
```

🔹 **What Happens?**  
📌 Cloud Custodian **checks AWS App Mesh Gateway Routes for TLS encryption enforcement**.  
📌 Flags routes where **TLS is not required**, ensuring secure communication between services.  

---

## 🎯 **Why Use Gateway-Route Filtering?**  
✅ **Enhances Security & Access Control:** Prevents unauthorized ownership or misconfigured routes.  
✅ **Improves Observability & Governance:** Ensures gateway routes follow service mesh policies.  
✅ **Supports Compliance & Best Practices:** Helps enforce **TLS encryption, access control, and route validation**.  

---

## ⚠ **Key Considerations**  
⚠ **Mesh Ownership May Vary by Region & Account:** Use `meshOwner` to **validate multi-account mesh setups**.  
⚠ **Ensure TLS is Enforced for Secure Routing:** Validate that gateway routes use **TLS encryption** for traffic security.  
⚠ **Use Regex for Flexible Matching:** Use `value_regex` to **match multiple route patterns dynamically**.  

---

## 🛠 **Supported Gateway-Route Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `attrs`       | `array`    | List of attributes to filter by (e.g., `meshOwner`, `routeType`). |
| `count`       | `number`   | Number of matching attributes required. |
| `count_op`    | `enum`     | Comparison operator (`eq`, `lt`, `gt`, etc.). |
| `type`        | `enum`     | Must be `gateway-route`. **(Required)** |

---

## ✅ **Best Practices for AWS App Mesh Gateway Route Audits**  
💡 **Verify Route Ownership Regularly:** Ensure all **gateway routes belong to trusted AWS accounts**.  
💡 **Enforce TLS for Secure Communication:** Require TLS in **all App Mesh gateway routes** to **encrypt service traffic**.  
💡 **Monitor for Unauthorized Configuration Changes:** Use Cloud Custodian to **track gateway route modifications**.  

---

## 🔹 **Health-Event: Monitor AWS Personal Health Dashboard (PHD) Events for Resources**  

### ✨ **What is Health-Event?**  
The `health-event` filter in Cloud Custodian **checks for AWS Personal Health Dashboard (PHD) events related to AWS resources**. This helps organizations **track service disruptions, scheduled changes, and account notifications** for proactive cloud management.  

**Common Use Cases:**  
✅ **Detect AWS Service Issues Affecting Resources** – Identify AWS outages or infrastructure failures.  
✅ **Monitor Scheduled Maintenance Events** – Track AWS-initiated resource updates (e.g., RDS maintenance, EC2 retirements).  
✅ **Respond to Account Notifications** – Detect AWS security advisories, policy updates, or billing alerts.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves AWS PHD events linked to a resource**.  
2️⃣ **Filters events based on categories (`issue`, `scheduledChange`, `accountNotification`)**.  
3️⃣ **Matches event status (`open`, `upcoming`, `closed`)** to focus on active or past incidents.  
4️⃣ **Returns AWS resources affected by health events** for further analysis or action.  

---

## 📝 **Example: Identify Resources Impacted by Open AWS Health Events**  
This policy **flags AWS resources affected by open AWS Health events** in the `issue` category.  

```yaml
policies:
  - name: detect-open-health-events
    resource: ec2
    filters:
      - type: health-event
        category:
          - issue
        statuses:
          - open
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves AWS Health events** related to EC2 instances.  
📌 Filters only **open issues**, helping teams **identify active incidents affecting EC2 workloads**.  

---

## 📝 **Example: Monitor Upcoming AWS Maintenance for RDS Instances**  
This policy **tracks scheduled AWS maintenance events for RDS instances**.  

```yaml
policies:
  - name: rds-upcoming-maintenance
    resource: rds
    filters:
      - type: health-event
        category:
          - scheduledChange
        statuses:
          - upcoming
```

🔹 **What Happens?**  
📌 Cloud Custodian **checks AWS PHD for scheduled maintenance events** affecting RDS.  
📌 Flags **upcoming changes**, helping **teams prepare for maintenance windows**.  

---

## 🎯 **Why Use Health-Event Filtering?**  
✅ **Detects Critical AWS Incidents:** Helps teams respond **proactively to AWS outages or failures**.  
✅ **Tracks Scheduled AWS Maintenance:** Ensures **proper planning for infrastructure updates**.  
✅ **Enhances Cloud Monitoring & Automation:** Enables **automated responses to AWS health events**.  

---

## ⚠ **Key Considerations**  
⚠ **AWS Health Events Are Account-Specific:** PHD events **only show incidents relevant to your AWS account**.  
⚠ **Use Lambda Execution Mode for Automated Responses:** Combine with **notifications, tagging, or remediation actions**.  
⚠ **Monitor All AWS Resources for Better Coverage:** Use `health-event` on **EC2, RDS, S3, and IAM** for **full-stack visibility**.  

---

## 🛠 **Supported Health-Event Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `category`     | `array`    | Type of AWS Health event (`issue`, `scheduledChange`, `accountNotification`). |
| `statuses`     | `array`    | Event status (`open`, `upcoming`, `closed`). |
| `types`        | `array`    | Specific event types to filter. |
| `type`         | `enum`     | Must be `health-event`. **(Required)** |

---

## ✅ **Best Practices for AWS Health Monitoring**  
💡 **Track Open & Upcoming Events for Mission-Critical Resources:** Focus on **EC2, RDS, and networking components**.  
💡 **Use AWS Lambda Mode for Event-Driven Automation:** **Automatically remediate** or **notify teams** when health events occur.  
💡 **Monitor Security & Compliance Alerts:** Stay ahead of AWS advisories on **IAM, encryption, and compliance updates**.  

---

## 🔹 **IAM-Analyzer: Analyze AWS Resource Policies for Public or External Access**  

### ✨ **What is IAM-Analyzer?**  
The `iam-analyzer` filter in Cloud Custodian **uses AWS IAM Access Analyzer to evaluate resource IAM policies**, helping organizations **identify security risks, public access, and external permissions**.  

**Common Use Cases:**  
✅ **Detect Publicly Accessible AWS Resources** – Identify S3 buckets, IAM roles, or Lambda functions with open access.  
✅ **Analyze External Access Risks** – Check for permissions that grant access outside of an AWS account.  
✅ **Enforce Security Best Practices** – Ensure IAM policies comply with least privilege principles.  

---

## 🔍 **How It Works**  
1️⃣ **Uses AWS IAM Access Analyzer** to evaluate resource policies.  
2️⃣ **Filters based on key attributes** (e.g., `isPublic`, `principalOrgId`, `grantedActions`).  
3️⃣ **Returns AWS resources that match the defined security criteria**.  

---

## 📝 **Example: Identify Publicly Accessible S3 Buckets**  
This policy **flags S3 buckets that are publicly accessible (`isPublic: true`)**.  

```yaml
policies:
  - name: s3-check
    resource: aws.s3
    filters:
      - type: iam-analyzer
        key: isPublic
        value: true
```

🔹 **What Happens?**  
📌 Cloud Custodian **analyzes S3 bucket policies using IAM Access Analyzer**.  
📌 If a bucket is **publicly accessible (`isPublic: true`)**, it is **included in the results**.  
📌 Helps **detect and remediate S3 buckets that expose data to unauthorized users**.  

---

## 📝 **Example: Detect IAM Roles Granting Cross-Account Access**  
This policy **identifies IAM roles that grant access outside the AWS account**.  

```yaml
policies:
  - name: cross-account-iam-role
    resource: aws.iam-role
    filters:
      - type: iam-analyzer
        key: principalOrgId
        value: null
```

🔹 **What Happens?**  
📌 Cloud Custodian **analyzes IAM roles using AWS IAM Access Analyzer**.  
📌 Flags roles where **`principalOrgId` is `null`**, indicating **permissions are granted outside the AWS organization**.  
📌 Helps **detect cross-account IAM role misconfigurations**.  

---

## 🎯 **Why Use IAM-Analyzer Filtering?**  
✅ **Identifies Security Risks in IAM Policies:** Detects public access, cross-account permissions, and other security misconfigurations.  
✅ **Enhances AWS Compliance & Governance:** Ensures AWS resource policies follow security best practices.  
✅ **Automates Security Audits:** Continuously scans for **policy violations and external access risks**.  

---

## ⚠ **Key Considerations**  
⚠ **IAM Access Analyzer Must Be Enabled:** Ensure AWS IAM Access Analyzer **is active in your AWS account**.  
⚠ **Use Logical Operators for Advanced Filtering:** Combine conditions to **detect multiple access risks simultaneously**.  
⚠ **Pair with Remediation Actions:** Use `notify`, `mark-for-op`, or `remove-policy` to **automate security fixes**.  

---

## 🛠 **Supported IAM-Analyzer Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `analyzer`    | `string`   | Specifies which IAM Access Analyzer to use. |
| `key`         | `string`   | Attribute to filter (e.g., `isPublic`, `principalOrgId`). |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, etc.). |
| `value`      | `string/boolean/number` | Expected value (e.g., `true`, `null`). |
| `value_regex` | `string`   | Regular expression pattern for matching values. |
| `value_type` | `enum`     | Data type (`integer`, `boolean`, `date`, etc.). |

---

## ✅ **Best Practices for IAM Policy Auditing**  
💡 **Monitor All Publicly Accessible AWS Resources:** Use IAM Analyzer to track **S3, IAM roles, Lambda, and more**.  
💡 **Check Cross-Account Permissions:** Ensure **IAM roles and policies do not unintentionally grant external access**.  
💡 **Automate Security Fixes:** Combine with **remediation actions like `remove-statements` or `tag`**.  

---

## 🔹 **Image: Filter AWS Auto Scaling Groups (ASG) Based on AMI Attributes**  

### ✨ **What is Image Filtering?**  
The `image` filter in Cloud Custodian **evaluates AWS Auto Scaling Groups (ASG) based on the Amazon Machine Images (AMI) they use**, enabling organizations to **enforce OS policies, detect outdated images, and ensure compliance with security best practices**.  

**Common Use Cases:**  
✅ **Ensure ASGs Use Approved Operating Systems** – Detect unauthorized OS types or outdated AMIs.  
✅ **Audit AMI Versions in Use** – Identify ASGs running older or unpatched AMIs.  
✅ **Enforce Compliance with Security Policies** – Ensure ASGs are using hardened images or approved AMIs.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves the AMI (Amazon Machine Image) used by an ASG**.  
2️⃣ **Filters based on AMI attributes** (e.g., `Platform`, `ImageId`, `CreationDate`).  
3️⃣ **Supports regex, numerical comparisons, and logical operators** for advanced filtering.  
4️⃣ **Returns ASGs running images that match or violate the defined criteria**.  

---

## 📝 **Example: Detect Auto Scaling Groups Running Non-Windows AMIs**  
This policy **identifies ASGs that are not using Windows-based AMIs**.  

```yaml
policies:
  - name: non-windows-asg
    resource: asg
    filters:
      - type: image
        key: Platform
        value: Windows
        op: ne
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves the AMI information for each ASG**.  
📌 If an ASG **does not use a Windows-based AMI (`Platform: Windows`)**, it **is flagged**.  
📌 Helps **enforce OS policies for workload segmentation**.  

---

## 📝 **Example: Identify ASGs Running Older AMIs**  
This policy **flags ASGs using AMIs that were created more than 90 days ago**.  

```yaml
policies:
  - name: outdated-amis
    resource: asg
    filters:
      - type: image
        key: CreationDate
        value_type: age
        value: 90
        op: greater-than
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves the AMI creation date for each ASG**.  
📌 ASGs running **images older than 90 days are flagged**, helping **enforce security patching policies**.  

---

## 🎯 **Why Use Image Filtering?**  
✅ **Ensures ASGs Use Approved AMIs:** Prevents **unauthorized or outdated images from being used**.  
✅ **Improves Security & Compliance:** Helps **enforce security patching and OS restrictions**.  
✅ **Optimizes Cloud Governance:** Provides **visibility into AMI usage across Auto Scaling Groups**.  

---

## ⚠ **Key Considerations**  
⚠ **Ensure AMI IDs Are Updated Regularly:** If enforcing a specific AMI, ensure **your policies account for rolling updates**.  
⚠ **Filter by More Than Just Platform:** Consider filtering by **CreationDate, Owner, or Image Lifecycle State** for better control.  
⚠ **Use Regex for Dynamic AMI Pattern Matching:** Use `value_regex` to **match multiple AMI naming conventions**.  

---

## 🛠 **Supported Image Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The AMI attribute to filter by (e.g., `Platform`, `CreationDate`, `ImageId`). |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value (e.g., `Windows`, `Amazon Linux`). |
| `value_regex` | `string`   | Regular expression pattern for matching values. |
| `value_type` | `enum`     | Data type (`integer`, `boolean`, `date`, etc.). |

---

## ✅ **Best Practices for ASG Image Auditing**  
💡 **Ensure ASGs Are Running the Latest AMIs:** Regularly **audit AMI creation dates** to ensure patching compliance.  
💡 **Use Named AMI Owners for Governance:** Restrict AMI usage to those **created by trusted AWS accounts**.  
💡 **Combine with Auto Remediation Actions:** Use `mark-for-op` or `notify` **to schedule ASG image updates**.  

---

## 🔹 **Instance-Attribute: Filter AWS Connect Instances Based on Attributes**  

### ✨ **What is Instance-Attribute?**  
The `instance-attribute` filter in Cloud Custodian **checks attributes of AWS Connect instances**, allowing organizations to **enforce compliance, detect misconfigurations, and ensure optimal setup for contact centers**.  

**Common Use Cases:**  
✅ **Verify Contact Lens Is Enabled** – Ensure real-time transcription and sentiment analysis is activated.  
✅ **Check Amazon Connect Instance Settings** – Audit attributes like encryption, logging, or telephony settings.  
✅ **Detect Misconfigured Contact Centers** – Identify instances missing required configurations.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves AWS Connect instance attributes** (e.g., `CONTACT_LENS`, `ENCRYPTION`).  
2️⃣ **Filters resources based on attributes using conditions** (e.g., `true`, `false`, regex).  
3️⃣ **Returns Connect instances that match or violate the defined settings**.  

---

## 📝 **Example: Identify AWS Connect Instances with Contact Lens Disabled**  
This policy **detects Amazon Connect instances where Contact Lens is not enabled**.  

```yaml
policies:
  - name: connect-instance-attribute
    resource: connect-instance
    filters:
      - type: instance-attribute
        key: Attribute.Value
        value: true
        attribute_type: CONTACT_LENS
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves the `CONTACT_LENS` attribute for all Amazon Connect instances**.  
📌 Flags instances where **Contact Lens is not enabled**, ensuring **real-time analytics and compliance**.  

---

## 📝 **Example: Detect Connect Instances Without Encryption**  
This policy **identifies AWS Connect instances where encryption is not enabled**.  

```yaml
policies:
  - name: connect-encryption-check
    resource: connect-instance
    filters:
      - type: instance-attribute
        key: Attribute.Value
        value: false
        attribute_type: ENCRYPTION
```

🔹 **What Happens?**  
📌 Cloud Custodian **checks if encryption is enabled for Amazon Connect instances**.  
📌 Flags **instances without encryption**, ensuring **compliance with data protection policies**.  

---

## 🎯 **Why Use Instance-Attribute Filtering?**  
✅ **Ensures AWS Connect Configurations Meet Security Standards** – Detect misconfigurations that could expose customer data.  
✅ **Automates Amazon Connect Audits** – Monitor compliance for **logging, encryption, Contact Lens, and other settings**.  
✅ **Enhances Contact Center Resilience** – Ensure best practices are followed for high availability and security.  

---

## ⚠ **Key Considerations**  
⚠ **Check AWS Region Availability for Features:** Some Amazon Connect features may not be **enabled in all AWS regions**.  
⚠ **Ensure Attribute Names Are Correct:** The attribute key **must match the API response format** (e.g., `CONTACT_LENS`).  
⚠ **Use Logical Operators for Advanced Filtering:** Combine with **`or` and `not`** to detect multiple misconfigurations.  

---

## 🛠 **Supported Instance-Attribute Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `attribute_type` | `string`  | The type of AWS Connect instance attribute (e.g., `CONTACT_LENS`, `ENCRYPTION`). **(Required)** |
| `key`         | `string`   | The specific attribute key to check. |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value for the filter (e.g., `true`, `false`). |
| `value_regex` | `string`   | Regular expression pattern for matching values. |

---

## ✅ **Best Practices for Amazon Connect Auditing**  
💡 **Ensure Contact Lens Is Enabled Where Required:** Improve **customer interaction insights and compliance**.  
💡 **Monitor Encryption Settings:** Enforce **data protection policies** across all Amazon Connect instances.  
💡 **Regularly Audit Configuration Settings:** Use Cloud Custodian **to detect misconfigurations automatically**.  

---

## 🔹 **Intelligent-Tiering: Audit S3 Intelligent Tiering Configurations**  

### ✨ **What is Intelligent-Tiering?**  
The `intelligent-tiering` filter in Cloud Custodian **checks S3 bucket Intelligent-Tiering storage configurations**, allowing organizations to **optimize costs, enforce best practices, and ensure compliance with storage lifecycle policies**.  

**Common Use Cases:**  
✅ **Ensure Intelligent-Tiering Is Enabled for Cost Savings** – Detect S3 buckets that are not using tiering for cost optimization.  
✅ **Verify Tiering Rules for Compliance** – Ensure data is transitioning correctly to `ARCHIVE_ACCESS` or `DEEP_ARCHIVE_ACCESS`.  
✅ **Optimize Storage Costs** – Identify buckets with misconfigured or missing Intelligent-Tiering policies.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves Intelligent-Tiering configurations for S3 buckets**.  
2️⃣ **Filters based on attributes such as `Status`, `Filter`, and `Tierings`**.  
3️⃣ **Supports regex, numerical comparisons, and logical operators** for advanced filtering.  
4️⃣ **Returns S3 buckets that match or violate the defined criteria**.  

---

## 📝 **Example: Identify S3 Buckets Using Intelligent-Tiering**  
This policy **detects S3 buckets that have Intelligent-Tiering enabled** and **apply specific tiering rules**.  

```yaml
policies:
  - name: s3-intelligent-tiering-configuration
    resource: s3
    filters:
      - type: intelligent-tiering
        attrs:
          - Status: Enabled
          - Filter:
              And:
                Prefix: test
                Tags:
                  - Key: Owner
                    Value: c7n
          - Tierings:
              - Days: 100
              - AccessTier: ARCHIVE_ACCESS
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves S3 bucket Intelligent-Tiering configurations**.  
📌 Filters for buckets where:  
   - **Intelligent-Tiering is enabled (`Status: Enabled`)**.  
   - **Objects with the prefix `test` and tag `Owner: c7n` are included in the tiering policy**.  
   - **Objects are moved to `ARCHIVE_ACCESS` after 100 days**.  

---

## 📝 **Example: Detect S3 Buckets Without Intelligent-Tiering Enabled**  
This policy **flags S3 buckets that do not have Intelligent-Tiering enabled**.  

```yaml
policies:
  - name: detect-no-intelligent-tiering
    resource: s3
    filters:
      - not:
          - type: intelligent-tiering
            attrs:
              - Status: Enabled
```

🔹 **What Happens?**  
📌 Cloud Custodian **identifies S3 buckets that lack Intelligent-Tiering policies**.  
📌 Helps organizations **enforce automated storage cost optimizations**.  

---

## 🎯 **Why Use Intelligent-Tiering Filtering?**  
✅ **Reduces AWS S3 Storage Costs:** Identifies **buckets that should transition objects to lower-cost storage tiers**.  
✅ **Enhances Storage Lifecycle Management:** Ensures **data moves to the correct storage class** over time.  
✅ **Supports Cost-Effective Data Retention Policies:** Helps enforce **intelligent data archiving**.  

---

## ⚠ **Key Considerations**  
⚠ **Intelligent-Tiering May Not Be Suitable for All Data:** Evaluate **access patterns before enabling Intelligent-Tiering**.  
⚠ **AWS Charges a Monitoring Fee for Intelligent-Tiering:** Ensure **it is cost-effective for your workload**.  
⚠ **Use Logical Operators for Advanced Filtering:** Combine conditions to **detect multiple misconfigurations simultaneously**.  

---

## 🛠 **Supported Intelligent-Tiering Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `attrs`       | `array`    | List of attributes to filter by (e.g., `Status`, `Filter`, `Tierings`). |
| `count`       | `number`   | Number of matching attributes required. |
| `count_op`    | `enum`     | Comparison operator (`eq`, `lt`, `gt`, etc.). |
| `type`        | `enum`     | Must be `intelligent-tiering`. **(Required)** |

---

## ✅ **Best Practices for S3 Intelligent-Tiering Audits**  
💡 **Ensure Tiering Policies Align with Data Access Patterns:** Use **Intelligent-Tiering only for infrequently accessed data**.  
💡 **Regularly Review Tiering Rules for Cost Optimization:** Ensure data is **transitioning to ARCHIVE_ACCESS efficiently**.  
💡 **Monitor AWS Storage Costs:** Track storage expenses **to validate the impact of Intelligent-Tiering policies**.  

---

## 🔹 **List-Item: Multi-Attribute Filtering on List-Based Resources**  

### ✨ **What is List-Item?**  
The `list-item` filter in Cloud Custodian **enables multi-attribute filtering within list-based resource attributes**, allowing users to **identify misconfigurations, security risks, and compliance violations** efficiently.  

**Common Use Cases:**  
✅ **Detect Open Security Group Rules** – Identify security groups allowing unrestricted access (e.g., `0.0.0.0/0` on port 22).  
✅ **Validate ECS Task Definitions** – Ensure containers are using approved Amazon ECR registries.  
✅ **Enforce Policies on Nested Attributes** – Perform complex filtering on attributes stored within lists.  

---

## 🔍 **How It Works**  
1️⃣ **Extracts list-based attributes from AWS resources** (e.g., `IpPermissions` in security groups, `containerDefinitions` in ECS).  
2️⃣ **Filters list items based on multiple attribute conditions** (e.g., `CidrIp`, `FromPort`, `image`).  
3️⃣ **Supports `or`, `and`, `not` logic**, regex patterns, and numerical comparisons.  
4️⃣ **Returns resources that match the filtering conditions**.  

---

## 📝 **Example: Identify Security Groups with Port 22 Open to the World**  
This policy **flags security groups that allow unrestricted SSH access (`0.0.0.0/0` on port 22)**.  

```yaml
policies:
  - name: security-group-with-22-open-to-world
    resource: aws.security-group
    filters:
      - type: list-item
        key: IpPermissions
        attrs:
          - type: value
            key: IpRanges[].CidrIp
            value: '0.0.0.0/0'
            op: in
            value_type: swap
          - type: value
            key: FromPort
            value: 22
          - type: value
            key: ToPort
            value: 22
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves all inbound security group rules (`IpPermissions`)**.  
📌 It **flags rules where**:  
   - **CidrIp is `0.0.0.0/0`** (allowing public access).  
   - **Port range includes `22`** (allowing SSH access).  
📌 Helps **detect and prevent public SSH exposure**.  

---

## 📝 **Example: Find ECS Task Definitions Not Using ECR for Container Images**  
This policy **detects ECS task definitions that are using non-ECR container images**.  

```yaml
policies:
  - name: find-task-def-not-using-registry
    resource: aws.ecs-task-definition
    filters:
      - not:
          - type: list-item
            key: containerDefinitions
            attrs:
              - not:
                  - type: value
                    key: image
                    value: "${account_id}.dkr.ecr.us-east-2.amazonaws.com.*"
                    op: regex
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves all container image definitions for ECS tasks**.  
📌 Flags tasks where **container images are NOT hosted in Amazon ECR**.  
📌 Helps **enforce security policies requiring container images to be stored in a trusted registry**.  

---

## 🎯 **Why Use List-Item Filtering?**  
✅ **Allows Multi-Attribute Filtering on List-Based Properties** – Enables complex filtering in **security groups, ECS, IAM, and more**.  
✅ **Enhances AWS Security & Compliance Audits** – Helps **detect risky configurations** and **enforce best practices**.  
✅ **Supports Advanced Filtering Logic** – Uses **`and`, `or`, `not` conditions**, regex, and numerical comparisons.  

---

## ⚠ **Key Considerations**  
⚠ **Ensure Key Paths Are Correct:** List-based attributes **vary by AWS resource** (e.g., `IpPermissions`, `containerDefinitions`).  
⚠ **Use `not` for Exclusion-Based Filters:** If filtering for **violations**, wrap the filter in `not:` to **find non-compliant resources**.  
⚠ **Optimize with `or` or `and` for Logical Matching:** Use logical operators **for filtering multiple conditions efficiently**.  

---

## 🛠 **Supported List-Item Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The list-based attribute to filter (e.g., `IpPermissions`, `containerDefinitions`). |
| `attrs`       | `array`    | List of conditions applied to the filtered list items. |
| `count`       | `number`   | Number of matching attributes required. |
| `count_op`    | `enum`     | Comparison operator (`eq`, `lt`, `gt`, etc.). |
| `type`        | `enum`     | Must be `list-item`. **(Required)** |

---

## ✅ **Best Practices for List-Based Filtering**  
💡 **Filter on Nested List Attributes in Security Groups & ECS:** Ensure **correct access controls and registry usage**.  
💡 **Use `not` for Exclusion Checks:** Detect **policy violations** by filtering out **approved configurations**.  
💡 **Regularly Audit Security Rules & Container Images:** Use Cloud Custodian **to enforce security best practices automatically**.  

---

## 🔹 **Lock-Configuration: Audit S3 Bucket Object Lock Settings**  

### ✨ **What is Lock-Configuration?**  
The `lock-configuration` filter in Cloud Custodian **checks the object lock configuration of S3 buckets**, helping organizations **enforce compliance, data retention policies, and prevent accidental deletions**.  

**Common Use Cases:**  
✅ **Ensure Compliance Mode is Enabled** – Detect buckets with weak or missing object lock settings.  
✅ **Verify Retention Periods** – Ensure data is protected for required durations.  
✅ **Prevent Accidental Data Deletion** – Confirm that immutable storage policies are enforced.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves S3 bucket object lock configurations**.  
2️⃣ **Filters based on attributes such as `Mode` and `Retention Period`**.  
3️⃣ **Supports regex, numerical comparisons, and logical operators** for advanced filtering.  
4️⃣ **Returns S3 buckets that match or violate the defined object lock policies**.  

---

## 📝 **Example: Identify S3 Buckets in Compliance Mode**  
This policy **detects S3 buckets where object lock is set to `COMPLIANCE` mode**.  

```yaml
policies:
  - name: lock-configuration-compliance
    resource: aws.s3
    filters:
      - type: lock-configuration
        key: Rule.DefaultRetention.Mode
        value: COMPLIANCE
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves object lock configurations for S3 buckets**.  
📌 Flags **buckets where `DefaultRetention.Mode` is `COMPLIANCE`**, ensuring **strong immutability policies**.  

---

## 📝 **Example: Detect S3 Buckets Without Object Lock Enabled**  
This policy **flags S3 buckets that do not have an object lock policy configured**.  

```yaml
policies:
  - name: detect-missing-object-lock
    resource: aws.s3
    filters:
      - not:
          - type: lock-configuration
            key: Rule
            value: present
```

🔹 **What Happens?**  
📌 Cloud Custodian **checks for buckets without an object lock configuration**.  
📌 Helps **prevent accidental data loss by enforcing retention policies**.  

---

## 🎯 **Why Use Lock-Configuration Filtering?**  
✅ **Ensures Data Retention Compliance:** Helps meet **regulatory requirements (e.g., SEC, GDPR, HIPAA)**.  
✅ **Prevents Accidental or Malicious Deletion:** Ensures **data is protected against deletion or modification**.  
✅ **Automates Storage Policy Audits:** Detects **misconfigured or missing object lock settings**.  

---

## ⚠ **Key Considerations**  
⚠ **Object Lock Must Be Enabled at Bucket Creation:** S3 buckets **must have object lock enabled during creation** to configure retention settings.  
⚠ **Compliance Mode Prevents All Deletions:** Ensure `COMPLIANCE` mode is **aligned with organizational retention policies**.  
⚠ **Use `not` for Exclusion-Based Checks:** Detect buckets **without proper lock settings** by negating filters.  

---

## 🛠 **Supported Lock-Configuration Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The S3 object lock attribute to filter by (e.g., `Rule.DefaultRetention.Mode`). |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value (e.g., `COMPLIANCE`, `GOVERNANCE`). |
| `value_regex` | `string`   | Regular expression pattern for matching values. |

---

## ✅ **Best Practices for S3 Object Lock Auditing**  
💡 **Ensure Compliance Mode Is Used for Regulatory Data:** Enforce `COMPLIANCE` mode **for legally required data retention**.  
💡 **Regularly Audit Retention Policies:** Ensure object lock settings **match organizational retention policies**.  
💡 **Use Governance Mode for Less Restrictive Policies:** Allows authorized users **to delete objects with special permissions**.  

---

## 🔹 **Logging: Audit AWS WAFv2 Logging Configurations**  

### ✨ **What is Logging Filtering?**  
The `logging` filter in Cloud Custodian **checks AWS WAFv2 logging configurations**, helping organizations **ensure compliance, monitor security policies, and detect misconfigurations in web access logging**.  

**Common Use Cases:**  
✅ **Detect WAFv2 Configurations Without Logging Enabled** – Ensure that web ACLs are logging to an AWS destination.  
✅ **Verify Redacted Fields in WAF Logging** – Ensure that sensitive headers (e.g., `user-agent`, `cookie`) are redacted in logs.  
✅ **Audit WAFv2 Log Destination & Settings** – Ensure logs are sent to **CloudWatch Logs, S3, or Kinesis Data Firehose**.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves AWS WAFv2 logging configurations**.  
2️⃣ **Filters resources based on attributes such as `ResourceArn`, `RedactedFields`, and `LoggingDestination`**.  
3️⃣ **Supports regex, numerical comparisons, and logical operators** for advanced filtering.  
4️⃣ **Returns WAFv2 configurations that match or violate defined logging policies**.  

---

## 📝 **Example: Identify WAFv2 Configurations Without Logging Enabled**  
This policy **detects WAFv2 web ACLs that do not have logging enabled**.  

```yaml
policies:
  - name: wafv2-logging-enabled
    resource: aws.wafv2
    filters:
      - not:
          - type: logging
            key: ResourceArn
            value: present
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves WAFv2 logging settings** for web ACLs.  
📌 Flags ACLs where **`ResourceArn` is absent**, meaning **no logging destination is configured**.  
📌 Helps ensure **WAF logs are collected for security analysis**.  

---

## 📝 **Example: Verify That User-Agent Header is Redacted in WAFv2 Logs**  
This policy **ensures that the `user-agent` field is redacted in WAFv2 logging** to prevent exposure of sensitive user information.  

```yaml
policies:
  - name: check-redacted-fields
    resource: aws.wafv2
    filters:
      - type: logging
        key: RedactedFields[].SingleHeader.Name
        value: user-agent
        op: in
        value_type: swap
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves WAFv2 logging configurations**.  
📌 Flags ACLs **where `user-agent` is NOT included in `RedactedFields`**, ensuring **sensitive headers are properly masked in logs**.  

---

## 🎯 **Why Use Logging Filtering?**  
✅ **Ensures WAFv2 Logs Are Collected for Compliance & Security** – Helps security teams **analyze and detect threats**.  
✅ **Prevents Data Leakage in Logging** – Enforces **sensitive field redaction policies**.  
✅ **Automates AWS Security Audits** – Monitors **WAFv2 logging configurations for compliance violations**.  

---

## ⚠ **Key Considerations**  
⚠ **AWS WAFv2 Logging is Not Enabled by Default:** Ensure web ACLs **explicitly configure a logging destination**.  
⚠ **Use `not` for Detecting Missing Log Configurations:** If checking for missing logs, **wrap the filter in `not:`**.  
⚠ **Ensure Logs Are Sent to the Correct Destination:** Verify logging is enabled for **CloudWatch Logs, S3, or Kinesis Firehose**.  

---

## 🛠 **Supported Logging Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The logging attribute to filter by (e.g., `ResourceArn`, `RedactedFields`). |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value for the filter (e.g., `present`, `user-agent`). |
| `value_regex` | `string`   | Regular expression pattern for matching values. |

---

## ✅ **Best Practices for WAFv2 Logging Audits**  
💡 **Ensure All WAFv2 ACLs Have Logging Enabled:** Avoid security blind spots by **enforcing mandatory logging**.  
💡 **Redact Sensitive Fields in Logs:** Prevent **exposure of sensitive data in logs** (e.g., `Authorization`, `Cookie`).  
💡 **Regularly Audit Log Storage & Retention:** Ensure logs are stored in **secure AWS destinations with appropriate retention policies**.  

---

## 🔹 **Logging-Config: Audit AWS Network Firewall Logging Configurations**  

### ✨ **What is Logging-Config?**  
The `logging-config` filter in Cloud Custodian **checks AWS Network Firewall logging configurations**, helping organizations **ensure compliance, monitor security policies, and detect misconfigurations**.  

**Common Use Cases:**  
✅ **Ensure Network Firewalls Have Logging Enabled** – Detect firewalls without active logging.  
✅ **Audit Log Types for Compliance** – Verify that `FLOW`, `ALERT`, or both log types are configured.  
✅ **Enforce Centralized Logging Practices** – Ensure logs are sent to **CloudWatch Logs, S3, or Kinesis Data Firehose**.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves AWS Network Firewall logging configurations**.  
2️⃣ **Filters resources based on attributes such as `LogType`, `LogDestinationConfig`, and `Status`**.  
3️⃣ **Supports regex, numerical comparisons, and logical operators** for advanced filtering.  
4️⃣ **Returns AWS Network Firewalls that match or violate logging requirements**.  

---

## 📝 **Example: Identify Firewalls Logging Only Flow Logs**  
This policy **detects AWS Network Firewalls configured to log only `FLOW` logs**.  

```yaml
policies:
  - name: network-firewall-logging-configuration
    resource: firewall
    filters:
      - type: logging-config
        attrs:
          - LogType: FLOW
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves logging configurations for AWS Network Firewalls**.  
📌 Flags firewalls where **only `FLOW` logs are enabled**, helping ensure **adequate security monitoring**.  

---

## 📝 **Example: Detect Firewalls Without Any Logging Enabled**  
This policy **flags AWS Network Firewalls with missing or disabled logging configurations**.  

```yaml
policies:
  - name: detect-missing-network-firewall-logs
    resource: firewall
    filters:
      - not:
          - type: logging-config
            attrs:
              - LogDestinationConfigs
                value: present
```

🔹 **What Happens?**  
📌 Cloud Custodian **checks whether logging destinations are configured**.  
📌 Flags **firewalls without logging enabled**, ensuring security events are captured.  

---

## 🎯 **Why Use Logging-Config Filtering?**  
✅ **Enhances Network Visibility & Security:** Ensures firewall logs are collected for **threat detection and auditing**.  
✅ **Prevents Misconfigurations in Logging Destinations:** Ensures logs are sent to the correct **CloudWatch, S3, or Kinesis destinations**.  
✅ **Automates AWS Network Firewall Audits:** Detects **logging gaps before they impact security monitoring**.  

---

## ⚠ **Key Considerations**  
⚠ **AWS Network Firewall Logging Is Not Enabled by Default:** Ensure firewalls **explicitly configure a logging destination**.  
⚠ **Use `not` for Detecting Missing Log Configurations:** If checking for missing logs, **wrap the filter in `not:`**.  
⚠ **Ensure Logs Are Sent to the Correct Destination:** Validate logging is enabled for **CloudWatch Logs, S3, or Kinesis Firehose**.  

---

## 🛠 **Supported Logging-Config Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `attrs`       | `array`    | List of attributes to filter by (e.g., `LogType`, `LogDestinationConfigs`). |
| `count`       | `number`   | Number of matching attributes required. |
| `count_op`    | `enum`     | Comparison operator (`eq`, `lt`, `gt`, etc.). |
| `type`        | `enum`     | Must be `logging-config`. **(Required)** |

---

## ✅ **Best Practices for AWS Network Firewall Logging Audits**  
💡 **Ensure All Firewalls Have Logging Enabled:** Avoid security blind spots by **enforcing mandatory logging**.  
💡 **Use Both `FLOW` and `ALERT` Logs for Visibility:** Ensure **comprehensive monitoring of firewall traffic**.  
💡 **Regularly Audit Log Storage & Retention:** Ensure logs are stored in **secure AWS destinations with appropriate retention policies**.  

---

## 🔹 **Login-Profile: Identify IAM Users with Console Login Access**  

### ✨ **What is Login-Profile Filtering?**  
The `login-profile` filter in Cloud Custodian **identifies IAM users who have an associated AWS Management Console login**. This allows organizations to **enforce least privilege access, detect unused credentials, and strengthen security posture**.  

**Common Use Cases:**  
✅ **Identify IAM Users with Console Access** – Detect users who can log in via the AWS Management Console.  
✅ **Detect Unused IAM Credentials** – Audit IAM users with login profiles but no recent activity.  
✅ **Improve AWS Security & Compliance** – Enforce security best practices by restricting unnecessary console access.  

---

## 🔍 **How It Works**  
1️⃣ **Checks IAM users for an associated login profile** (which means they have console access).  
2️⃣ **Filters based on attributes such as `exists`, `password_age`, and regex-based conditions**.  
3️⃣ **Supports advanced filtering options** (e.g., `password_enabled`, `password_last_used`).  
4️⃣ **Returns IAM users that match or violate the defined login profile criteria**.  

---

## 📝 **Example: Identify IAM Users with Console Login Access**  
This policy **flags IAM users who have a login profile (i.e., they can log into the AWS Management Console)**.  

```yaml
policies:
  - name: detect-console-users
    resource: aws.iam-user
    filters:
      - type: login-profile
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves IAM user login profiles**.  
📌 Flags **IAM users who have an AWS console login**.  
📌 Helps **enforce least privilege by identifying users who do not need console access**.  

---

## 📝 **Example: Detect IAM Users with Console Login But No Recent Use**  
This policy **identifies IAM users who have console access but haven't logged in within the last 90 days**.  

```yaml
policies:
  - name: detect-unused-console-users
    resource: aws.iam-user
    filters:
      - type: login-profile
      - type: credential
        key: password_last_used
        value_type: age
        value: 90
        op: greater-than
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves IAM users with an active login profile**.  
📌 Filters users who **haven't logged in within the last 90 days**, helping **identify inactive accounts**.  
📌 Helps **enforce AWS security best practices by disabling unused accounts**.  

---

## 🎯 **Why Use Login-Profile Filtering?**  
✅ **Identifies IAM Users with Console Access:** Ensures AWS access policies **follow least privilege principles**.  
✅ **Detects Unused IAM Credentials:** Helps **reduce the attack surface by identifying inactive accounts**.  
✅ **Automates AWS Security Audits:** Continuously scans for **misconfigured IAM user access settings**.  

---

## ⚠ **Key Considerations**  
⚠ **Use `credential` Filter for Credential Age:** The `credential` filter provides **more efficient evaluation** when detecting unused passwords.  
⚠ **Restrict IAM Console Access for Service Accounts:** Ensure only **human users have console login profiles**.  
⚠ **Combine with MFA & Password Policies:** Ensure **console users meet multi-factor authentication (MFA) and strong password policies**.  

---

## 🛠 **Supported Login-Profile Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The IAM login profile attribute to filter by. |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value for the filter (e.g., `true`, `false`). |
| `value_regex` | `string`   | Regular expression pattern for matching values. |

---

## ✅ **Best Practices for IAM Login Profile Auditing**  
💡 **Minimize AWS Console Access:** Ensure only necessary users **have console login profiles**.  
💡 **Detect & Disable Unused IAM Accounts:** Audit **inactive console users regularly**.  
💡 **Require MFA for IAM Users:** Enforce **multi-factor authentication for all users with console access**.  

---

## 🔹 **Marked-for-Op: Automate Future Actions Based on Tags**  

### ✨ **What is Marked-for-Op?**  
The `marked-for-op` filter in Cloud Custodian **identifies resources tagged for future actions** (e.g., stopping an EC2 instance or deleting a volume). This enables **scheduled resource management, cost optimization, and automated cleanup**.  

**Common Use Cases:**  
✅ **Stop EC2 Instances at a Scheduled Date** – Automatically stop instances based on a `stop@YYYY-MM-DD` tag.  
✅ **Delete Unused Resources After a Grace Period** – Ensure **volumes, snapshots, or databases are deleted after a retention period**.  
✅ **Send Warnings Before Termination** – Notify users **days or hours before a scheduled action**.  

---

## 🔍 **How It Works**  
1️⃣ **Checks for a specific tag (default: `maid_status`) on AWS resources**.  
2️⃣ **Parses the tag value in the format `op@YYYY-MM-DD`** (e.g., `stop@2024-07-15`).  
3️⃣ **Compares the date with today’s date** (or applies a `skew` value for warnings).  
4️⃣ **Filters resources where today’s date is equal to or later than the target date**.  

---

## 📝 **Example: Stop EC2 Instances Marked for Shutdown**  
This policy **stops EC2 instances that have been tagged for termination on or before today’s date**.  

```yaml
policies:
  - name: ec2-stop-marked
    resource: ec2
    filters:
      - type: marked-for-op
        tag: custodian_status
        op: stop
        tz: utc
    actions:
      - type: stop
```

🔹 **What Happens?**  
📌 Cloud Custodian **checks for the `custodian_status` tag** with a value like `stop@2024-07-15`.  
📌 If today’s date **is on or after July 15, 2024**, the instance is **stopped automatically**.  

---

## 📝 **Example: Notify Users 3 Days Before Resource Deletion**  
This policy **sends a final warning 3 days before an S3 bucket is scheduled for deletion**.  

```yaml
policies:
  - name: s3-delete-warning
    resource: aws.s3
    filters:
      - type: marked-for-op
        tag: custodian_status
        op: delete
        skew: 3  # Look 3 days ahead
    actions:
      - type: notify
        to:
          - email@example.com
        subject: "S3 Bucket Scheduled for Deletion"
        message: "This S3 bucket is marked for deletion in 3 days. Please take action if needed."
```

🔹 **What Happens?**  
📌 Cloud Custodian **checks for the `custodian_status` tag** with values like `delete@2024-07-18`.  
📌 If today is **July 15, 2024**, the bucket is **scheduled for deletion in 3 days**—and a **warning email is sent**.  

---

## 🎯 **Why Use Marked-for-Op Filtering?**  
✅ **Automates Resource Lifecycle Management:** Stops, deletes, or snapshots resources **based on tags**.  
✅ **Optimizes AWS Cost Management:** Automatically shuts down **unused instances or storage** after a retention period.  
✅ **Prevents Accidental Data Loss:** Sends **warnings before deleting critical resources**.  

---

## ⚠ **Key Considerations**  
⚠ **Ensure Tags Are Applied Consistently:** Cloud Custodian only acts **on correctly formatted `op@YYYY-MM-DD` tags**.  
⚠ **Use `skew` for Pre-Action Notifications:** Helps **send alerts before an action is executed**.  
⚠ **Time Zones Matter (`tz`):** The default time zone is **UTC**—set `tz` to your region if needed.  

---

## 🛠 **Supported Marked-for-Op Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `tag`         | `string`   | The tag name that contains the operation date (default: `maid_status`). |
| `op`         | `string`   | The action to check (e.g., `stop`, `delete`). |
| `skew`       | `number`   | Number of days to look ahead (e.g., send warnings before deletion). |
| `skew_hours` | `number`   | Number of hours to look ahead. |
| `tz`         | `string`   | Time zone for date comparison (default: `utc`). |
| `type`       | `enum`     | Must be `marked-for-op`. **(Required)** |

---

## ✅ **Best Practices for Scheduled Resource Management**  
💡 **Use `notify` Before Deletion:** Send emails **days before resource termination**.  
💡 **Combine with Lifecycle Policies:** Automate cleanup for **S3 buckets, RDS snapshots, and unused EC2 instances**.  
💡 **Regularly Audit Marked Resources:** Run **Cloud Custodian policies to track upcoming resource actions**.  

---

## 🔹 **Metrics: Analyze AWS CloudWatch Metrics for Resource Monitoring**  

### ✨ **What is Metrics Filtering?**  
The `metrics` filter in Cloud Custodian **retrieves CloudWatch metrics for AWS resources**, allowing organizations to **monitor utilization, detect underused resources, and enforce performance standards**.  

**Common Use Cases:**  
✅ **Detect Underutilized EC2 Instances** – Identify instances with low CPU utilization over a period.  
✅ **Monitor Load Balancer Traffic** – Flag ELBs with low request counts.  
✅ **Analyze Storage Utilization** – Check EBS volume throughput and optimize costs.  

---

## 🔍 **How It Works**  
1️⃣ **Fetches CloudWatch metric data for supported AWS resources**.  
2️⃣ **Applies filtering based on metric name, time period, and thresholds**.  
3️⃣ **Supports missing-value handling** (e.g., assume `0` if no data is reported).  
4️⃣ **Returns resources that meet or violate the metric criteria**.  

---

## 📝 **Example: Identify EC2 Instances with Low CPU Utilization**  
This policy **detects EC2 instances with an average CPU utilization below 30% over the last 4 days**.  

```yaml
policies:
  - name: ec2-underutilized
    resource: ec2
    filters:
      - type: metrics
        name: CPUUtilization
        days: 4
        period: 86400
        value: 30
        op: less-than
```

🔹 **What Happens?**  
📌 Cloud Custodian **fetches CPU utilization data from CloudWatch** for the last 4 days.  
📌 Flags instances where **average CPU utilization is below 30%**, helping **identify cost-saving opportunities**.  

---

## 📝 **Example: Identify Load Balancers With Low Traffic**  
This policy **flags ELBs with fewer than 7 requests in the last 7 days, treating missing data as zero**.  

```yaml
policies:
  - name: elb-low-request-count
    resource: elb
    filters:
      - type: metrics
        name: RequestCount
        statistics: Sum
        days: 7
        value: 7
        missing-value: 0
        op: less-than
```

🔹 **What Happens?**  
📌 Cloud Custodian **fetches ELB request counts from CloudWatch for the past 7 days**.  
📌 Flags ELBs **with fewer than 7 total requests**, including those **with no data (missing-value: 0)**.  
📌 Helps **identify unused or low-traffic ELBs for cost optimization**.  

---

## 🎯 **Why Use Metrics Filtering?**  
✅ **Optimizes AWS Costs:** Identifies **underutilized EC2, ELB, and other AWS resources**.  
✅ **Enhances Performance Monitoring:** Enables **proactive detection of inefficient resource usage**.  
✅ **Automates Cloud Governance:** Helps enforce **utilization-based resource policies**.  

---

## ⚠ **Key Considerations**  
⚠ **CloudWatch Metrics May Have Gaps:** If an instance is **stopped**, it **does not report metrics** during that period.  
⚠ **Use `missing-value` for Unreported Metrics:** Ensures resources **without metrics are still included in evaluations**.  
⚠ **Customize Metric Statistics:** The default statistic is `Average`, but **can be changed to `Sum`, `Min`, or `Max`**.  

---

## 🛠 **Supported Metrics Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `name`        | `string`   | CloudWatch metric name (e.g., `CPUUtilization`, `RequestCount`). **(Required)** |
| `days`        | `number`   | Number of days to retrieve metric data. |
| `period`      | `number`   | CloudWatch metric period in seconds (e.g., `86400` for daily data). |
| `value`       | `number`   | Threshold for comparison (e.g., `30` for CPU utilization). **(Required)** |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `lt`, `gt`, etc.). |
| `statistics`  | `string`   | CloudWatch statistic type (`Average`, `Sum`, `Min`, `Max`). Default: `Average`. |
| `missing-value` | `number` | Default value to use when CloudWatch has no data. |

---

## ✅ **Best Practices for CloudWatch Metrics Auditing**  
💡 **Monitor Resource Utilization Regularly:** Identify **cost-saving opportunities by analyzing usage trends**.  
💡 **Ensure Key Services Are Logging Metrics:** Verify **critical AWS services are sending data to CloudWatch**.  
💡 **Use Metrics with Auto-Scaling Policies:** Optimize **resource scaling by defining CPU, memory, or traffic thresholds**.  

---

## 🔹 **Network-Location: Validate Network Configuration Consistency**  

### ✨ **What is Network-Location Filtering?**  
The `network-location` filter in Cloud Custodian **checks the consistency of security groups, subnets, and resource attributes**, ensuring that resources are aligned with **network segmentation policies**.  

**Common Use Cases:**  
✅ **Ensure EC2 Instances Are Using Correctly Tagged Security Groups and Subnets** – Prevent misconfigurations in network segmentation.  
✅ **Detect Network Resource Mismatches** – Identify EC2 instances with **security groups or subnets that do not match a specific tag**.  
✅ **Enforce Team-Based Network Isolation** – Ensure resources are attached **only to subnets and security groups assigned to the same team**.  

---

## 🔍 **How It Works**  
1️⃣ **Compares network attributes across EC2 instances, security groups, and subnets**.  
2️⃣ **Filters based on a shared key** (e.g., `tag:TEAM_NAME`) across these network components.  
3️⃣ **Returns instances where the security group and subnet values differ from the expected resource value**.  
4️⃣ **Supports exclusions for specific values using `ignore`**, allowing flexibility in compliance checks.  

---

## 📝 **Example: Remove Security Groups That Don't Match the Instance's Team Tag**  
This policy **identifies EC2 instances where security groups have a different `TEAM_NAME` tag than the instance itself** and removes the mismatched security groups.  

```yaml
policies:
  - name: ec2-mismatched-sg-remove
    resource: ec2
    filters:
      - type: network-location
        compare: ["resource", "security-group"]
        key: "tag:TEAM_NAME"
        ignore:
          - "tag:TEAM_NAME": Enterprise
    actions:
      - type: modify-security-groups
        remove: network-location
        isolation-group: sg-xxxxxxxx
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves the `TEAM_NAME` tag from the EC2 instance and its security groups**.  
📌 If the security group **has a different `TEAM_NAME` than the instance**, it **is removed** (unless the value is `Enterprise`, as defined in `ignore`).  
📌 Helps ensure **team-based network isolation**, where **each EC2 instance is only assigned security groups belonging to its team**.  

---

## 🎯 **Why Use Network-Location Filtering?**  
✅ **Prevents Network Misconfigurations:** Ensures **instances, subnets, and security groups follow a unified tagging structure**.  
✅ **Enhances Security by Enforcing Network Isolation:** Helps **segment AWS environments by teams or applications**.  
✅ **Automates Governance for Networking Policies:** Ensures network compliance **without manual intervention**.  

---

## ⚠ **Key Considerations**  
⚠ **Ensure Tags Are Consistently Applied:** If tags are missing, resources **may be flagged incorrectly**.  
⚠ **Use `ignore` for Exemptions:** Exclude specific teams or departments **that follow a different segmentation strategy**.  
⚠ **Combine with Remediation Actions:** Use `modify-security-groups` or `isolate` to **fix non-compliant network configurations automatically**.  

---

## 🛠 **Supported Network-Location Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `compare`      | `array`    | Specifies what to compare (`resource`, `subnet`, `security-group`). |
| `key`         | `string`   | The attribute or tag to compare (e.g., `tag:TEAM_NAME`). |
| `match`       | `enum`     | Match type (`equal`, `not-equal`, `in`). Default: `not-equal`. |
| `ignore`      | `array`    | List of values to exclude from filtering. |
| `missing-ok`  | `boolean`  | Defines behavior when keys are missing (`false` treats missing keys as mismatches). |
| `max-cardinality` | `integer` | Defines the maximum number of allowed matches. |

---

## ✅ **Best Practices for Network Segmentation Compliance**  
💡 **Standardize Tagging Across Network Components:** Ensure **EC2, security groups, and subnets share common attributes** for accurate filtering.  
💡 **Regularly Audit Network Configurations:** Detect **misconfigured network locations before they cause security or access issues**.  
💡 **Use Automated Remediation for Policy Enforcement:** Implement **tag-based security group removal or isolation actions**.  

---

## 🔹 **Offhour: Automate Resource Shutdown During Off-Peak Hours**  

### ✨ **What is Offhour Filtering?**  
The `offhour` filter in Cloud Custodian **schedules AWS resources to shut down or scale down during off-peak hours**, helping organizations **reduce costs, enforce energy efficiency, and automate cloud governance**.  

**Common Use Cases:**  
✅ **Automatically Shut Down EC2 & RDS Instances at Night** – Save costs by stopping instances outside business hours.  
✅ **Skip Shutdowns on Specific Days** – Avoid turning off resources on holidays or maintenance periods.  
✅ **Customize Scheduling Based on Tags** – Allow **per-resource scheduling** using tags like `custodian_offhours`.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves the `offhour` schedule from policy or resource tags**.  
2️⃣ **Determines if the current time falls within an off-hour period**.  
3️⃣ **Supports additional logic for opt-outs, skipping specific days, and weekend-only schedules**.  
4️⃣ **Triggers appropriate actions (e.g., `stop`, `snapshot`, or `scale-down`) when conditions match**.  

---

## 📝 **Example: Stop EC2 Instances During Non-Business Hours**  
This policy **automatically stops EC2 instances every night at 8 PM UTC** unless they are opted out via a tag.  

```yaml
policies:
  - name: stop-instances-offhours
    resource: ec2
    filters:
      - type: offhour
        offhour: 20  # 8 PM UTC
        default_tz: UTC
        tag: custodian_offhours
        opt-out: true
    actions:
      - type: stop
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves the off-hour schedule (8 PM UTC)**.  
📌 If an EC2 instance **does not have `custodian_offhours: opt-out`**, it **is stopped automatically**.  

---

## 📝 **Example: Skip Shutdown on Specific Days (Holidays or Maintenance Windows)**  
This policy **ensures EC2 instances are not stopped on predefined skip days (e.g., `2024-12-25` for Christmas)**.  

```yaml
policies:
  - name: stop-ec2-offhours-skip-holidays
    resource: ec2
    filters:
      - type: offhour
        offhour: 22
        default_tz: America/New_York
        skip-days:
          - "2024-12-25"  # Christmas
          - "2024-01-01"  # New Year's Day
    actions:
      - type: stop
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves the off-hour schedule (10 PM ET)**.  
📌 If today is **not a skip day (Christmas, New Year's)**, the instance **is stopped as scheduled**.  

---

## 📝 **Example: Restrict Off-Hour Shutdowns to Weekends Only**  
This policy **only stops instances on Saturdays and Sundays** at 10 PM UTC.  

```yaml
policies:
  - name: stop-instances-weekends
    resource: ec2
    filters:
      - type: offhour
        offhour: 22
        default_tz: UTC
        weekends-only: true
    actions:
      - type: stop
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves the off-hour schedule (10 PM UTC)**.  
📌 If today is **Saturday or Sunday**, the instance **is stopped**.  

---

## 🎯 **Why Use Offhour Filtering?**  
✅ **Reduces AWS Costs:** Saves money by **automatically stopping resources during non-business hours**.  
✅ **Supports Flexible Scheduling:** Enables **per-resource customization using tags, weekends-only, and holiday skips**.  
✅ **Enhances Cloud Automation:** Ensures **non-essential workloads do not run outside business hours**.  

---

## ⚠ **Key Considerations**  
⚠ **Time Zones Matter (`default_tz`)** – Ensure the correct **time zone is set for accurate scheduling**.  
⚠ **Use Tags for Opt-Outs** – Allow **exceptions by tagging critical resources with an opt-out flag**.  
⚠ **Combine with `notify` Actions for Visibility** – Send **email notifications before stopping instances**.  

---

## 🛠 **Supported Offhour Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `offhour`     | `integer`  | The hour (0-23) to trigger the off-hour action. **(Required)** |
| `default_tz`  | `string`   | The default time zone for scheduling. **(Required)** |
| `tag`         | `string`   | The resource tag used for off-hour scheduling (e.g., `custodian_offhours`). |
| `opt-out`     | `boolean`  | If `true`, resources with the tag **can opt out of off-hour actions**. |
| `weekends-only` | `boolean` | If `true`, **only applies off-hour actions on weekends**. |
| `skip-days`   | `array`    | List of dates (`YYYY-MM-DD`) when off-hour actions should be skipped. |
| `fallback_schedule` | `string` | Alternative schedule if no off-hour schedule is set. |

---

## ✅ **Best Practices for Off-Hour Scheduling**  
💡 **Ensure Business-Critical Workloads Are Excluded:** Use **tags (`custodian_offhours: opt-out`) for important resources**.  
💡 **Notify Teams Before Automatic Shutdowns:** Use `notify` **to send alerts before taking action**.  
💡 **Regularly Update Skip Days for Public Holidays & Maintenance Windows:** Ensure **critical dates are accounted for**.  

---
## 🔹 **Onhour: Automate Resource Start During Business Hours**  

### ✨ **What is Onhour Filtering?**  
The `onhour` filter in Cloud Custodian **schedules AWS resources to start at predefined times**, helping organizations **optimize costs, enforce uptime policies, and ensure operational efficiency**.  

**Common Use Cases:**  
✅ **Automatically Start EC2 & RDS Instances During Business Hours** – Ensure workloads are active when needed.  
✅ **Skip Startup on Specific Days** – Avoid starting resources on public holidays or scheduled maintenance days.  
✅ **Customize Scheduling Based on Tags** – Allow per-resource scheduling via tags like `custodian_onhours`.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves the `onhour` schedule from policy or resource tags**.  
2️⃣ **Determines if the current time falls within a scheduled start period**.  
3️⃣ **Supports additional logic for opt-outs, skipping specific days, and weekend-only scheduling**.  
4️⃣ **Triggers appropriate actions (e.g., `start`, `scale-up`) when conditions match**.  

---

## 📝 **Example: Start EC2 Instances at 8 AM UTC**  
This policy **automatically starts EC2 instances at 8 AM UTC unless they have opted out**.  

```yaml
policies:
  - name: start-instances-onhours
    resource: ec2
    filters:
      - type: onhour
        onhour: 8  # 8 AM UTC
        default_tz: UTC
        tag: custodian_onhours
        opt-out: true
    actions:
      - type: start
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves the on-hour schedule (8 AM UTC)**.  
📌 If an EC2 instance **does not have `custodian_onhours: opt-out`**, it **is started automatically**.  

---

## 📝 **Example: Skip Startup on Specific Days (Holidays or Maintenance Windows)**  
This policy **ensures EC2 instances are not started on predefined skip days (e.g., `2024-12-25` for Christmas)**.  

```yaml
policies:
  - name: start-ec2-onhours-skip-holidays
    resource: ec2
    filters:
      - type: onhour
        onhour: 7
        default_tz: America/New_York
        skip-days:
          - "2024-12-25"  # Christmas
          - "2024-01-01"  # New Year's Day
    actions:
      - type: start
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves the on-hour schedule (7 AM ET)**.  
📌 If today is **not a skip day (Christmas, New Year's)**, the instance **is started as scheduled**.  

---

## 📝 **Example: Restrict On-Hour Scheduling to Weekends Only**  
This policy **only starts instances on Saturdays and Sundays** at 9 AM UTC.  

```yaml
policies:
  - name: start-instances-weekends
    resource: ec2
    filters:
      - type: onhour
        onhour: 9
        default_tz: UTC
        weekends-only: true
    actions:
      - type: start
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves the on-hour schedule (9 AM UTC)**.  
📌 If today is **Saturday or Sunday**, the instance **is started**.  

---

## 🎯 **Why Use Onhour Filtering?**  
✅ **Reduces AWS Costs by Starting Only When Needed:** Ensures resources **are not running unnecessarily outside working hours**.  
✅ **Supports Flexible Scheduling:** Enables **per-resource customization using tags, weekends-only, and holiday skips**.  
✅ **Enhances Cloud Automation:** Ensures **business-critical workloads are online when required**.  

---

## ⚠ **Key Considerations**  
⚠ **Time Zones Matter (`default_tz`)** – Ensure the correct **time zone is set for accurate scheduling**.  
⚠ **Use Tags for Opt-Outs** – Allow **exceptions by tagging critical resources with an opt-out flag**.  
⚠ **Combine with `notify` Actions for Visibility** – Send **email notifications before starting instances**.  

---

## 🛠 **Supported Onhour Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `onhour`      | `integer`  | The hour (0-23) to trigger the on-hour action. **(Required)** |
| `default_tz`  | `string`   | The default time zone for scheduling. **(Required)** |
| `tag`         | `string`   | The resource tag used for on-hour scheduling (e.g., `custodian_onhours`). |
| `opt-out`     | `boolean`  | If `true`, resources with the tag **can opt out of on-hour actions**. |
| `weekends-only` | `boolean` | If `true`, **only applies on-hour actions on weekends**. |
| `skip-days`   | `array`    | List of dates (`YYYY-MM-DD`) when on-hour actions should be skipped. |
| `fallback_schedule` | `string` | Alternative schedule if no on-hour schedule is set. |

---

## ✅ **Best Practices for On-Hour Scheduling**  
💡 **Ensure Business-Critical Workloads Are Started as Needed:** Prevent **delays in launching essential resources**.  
💡 **Notify Teams Before Automatic Startups:** Use `notify` **to send alerts before taking action**.  
💡 **Regularly Update Skip Days for Public Holidays & Maintenance Windows:** Ensure **critical dates are accounted for**.  

---

## 🔹 **Ops-Item: Identify AWS Resources with Open OpsCenter Items**  

### ✨ **What is Ops-Item Filtering?**  
The `ops-item` filter in Cloud Custodian **identifies AWS resources that are linked to active AWS Systems Manager OpsCenter items**, enabling organizations to **track issues, automate incident response, and enforce remediation workflows**.  

**Common Use Cases:**  
✅ **Identify AWS Resources with Open Incidents** – Detect EC2 instances, RDS databases, or other resources with unresolved issues.  
✅ **Prioritize Critical Operational Items** – Filter by priority levels (`1-5`) to focus on **high-priority incidents**.  
✅ **Track OpsCenter Status** – Find resources with **Ops items that are `Open`, `In Progress`, or `Resolved`**.  

---

## 🔍 **How It Works**  
1️⃣ **Queries AWS Systems Manager OpsCenter** for active operational issues.  
2️⃣ **Filters resources based on priority, source, and status** (e.g., `Open`, `In Progress`).  
3️⃣ **Returns AWS resources associated with matching OpsCenter items**.  

---

## 📝 **Example: Identify EC2 Instances with High-Priority Open Ops Items**  
This policy **flags EC2 instances with open Ops items of priority 1 or 2**.  

```yaml
policies:
  - name: ec2-instances-ops-items
    resource: ec2
    filters:
      - type: ops-item
        priority: [1, 2]
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves all open Ops items linked to EC2 instances**.  
📌 Flags **instances with Ops items of priority 1 or 2**, helping teams focus on **critical issues**.  

---

## 📝 **Example: Find RDS Databases with Open Ops Items from a Specific Source**  
This policy **identifies RDS databases with operational issues sourced from AWS Security Hub**.  

```yaml
policies:
  - name: rds-security-ops-items
    resource: rds
    filters:
      - type: ops-item
        source: AWS/SecurityHub
        status: ["Open"]
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves all open Ops items related to RDS databases**.  
📌 Filters for **Ops items created by AWS Security Hub**, helping **track security-related issues**.  

---

## 🎯 **Why Use Ops-Item Filtering?**  
✅ **Enhances Incident Response Automation:** Helps **track and remediate AWS resource issues proactively**.  
✅ **Prioritizes Business-Critical Issues:** Focus on **high-priority operational incidents**.  
✅ **Automates AWS OpsCenter Monitoring:** Continuously audits **Ops items linked to AWS resources**.  

---

## ⚠ **Key Considerations**  
⚠ **Ensure OpsCenter Is Enabled:** AWS Systems Manager OpsCenter **must be active for filtering to work**.  
⚠ **Use `priority` to Focus on Critical Issues:** Lower values (1-2) indicate **higher-priority items**.  
⚠ **Combine with `notify` or `remediation` Actions:** Automate incident resolution **using `notify`, `tag`, or `mark-for-op` actions**.  

---

## 🛠 **Supported Ops-Item Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `priority`    | `array`    | List of priority levels (1-5, where 1 is highest). |
| `source`      | `string`   | Source of the Ops item (e.g., `AWS/SecurityHub`). |
| `status`      | `array`    | Status of the Ops item (`Open`, `In Progress`, `Resolved`). Default: `Open`. |
| `title`       | `string`   | Ops item title for filtering by name. |
| `type`        | `enum`     | Must be `ops-item`. **(Required)** |

---

## ✅ **Best Practices for AWS OpsCenter Audits**  
💡 **Monitor High-Priority Ops Items First:** Prioritize **critical issues (`priority: [1, 2]`) for faster resolution**.  
💡 **Track Security-Related Ops Items Separately:** Use **`source: AWS/SecurityHub`** to filter security findings.  
💡 **Automate Response with `mark-for-op`:** Tag non-compliant resources **for remediation workflows**.  

---

## 🔹 **Org-Unit: Filter AWS Resources by Organizational Unit (OU)**  

### ✨ **What is Org-Unit Filtering?**  
The `org-unit` filter in Cloud Custodian **identifies AWS resources that belong to a specific AWS Organizations Organizational Unit (OU)**, enabling organizations to **enforce policies, manage cost allocation, and automate governance at the OU level**.  

**Common Use Cases:**  
✅ **Filter AWS Organizational Units by Name** – Identify OUs based on naming conventions (e.g., `dev`, `prod`).  
✅ **Find AWS Accounts Within a Specific OU** – Ensure accounts are **correctly assigned within AWS Organizations**.  
✅ **Audit Organizational Hierarchy & Compliance** – Validate that resources **are placed in the appropriate OUs for governance**.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves AWS Organizational Units (OUs) and accounts from AWS Organizations**.  
2️⃣ **Filters resources based on OU attributes** (e.g., `Name`, `ParentId`).  
3️⃣ **Supports regex, numerical comparisons, and logical operators** for advanced filtering.  
4️⃣ **Returns OUs or accounts that match or violate the defined criteria**.  

---

## 📝 **Example: Find Organizational Units Named `dev`**  
This policy **identifies AWS OUs where the `Name` is `dev`**.  

```yaml
policies:
  - name: org-units-by-parent-ou
    resource: aws.org-unit
    filters:
      - type: org-unit
        key: Name
        value: dev
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves all AWS Organizational Units**.  
📌 Filters **OUs where the `Name` is `dev`**, ensuring proper organizational structure.  

---

## 📝 **Example: Find AWS Accounts Belonging to a Specific OU**  
This policy **flags AWS accounts that belong to the `dev` OU**.  

```yaml
policies:
  - name: org-accounts-by-parent-ou
    resource: aws.org-account
    filters:
      - type: org-unit
        key: Name
        value: dev
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves all AWS accounts and their associated OUs**.  
📌 Flags accounts **belonging to the `dev` OU**, helping with **cost tracking and policy enforcement**.  

---

## 🎯 **Why Use Org-Unit Filtering?**  
✅ **Improves AWS Governance & Security:** Ensures **AWS accounts and OUs are structured correctly**.  
✅ **Automates Organizational Policy Enforcement:** Helps **track resource placement across OUs**.  
✅ **Enhances Cost Management & Budgeting:** Filters **accounts by OU for better billing analysis**.  

---

## ⚠ **Key Considerations**  
⚠ **Ensure AWS Organizations Is Enabled:** AWS Organizations **must be active for OU filtering to work**.  
⚠ **Use Regex for Flexible OU Name Matching:** Allows filtering **multiple related OUs dynamically**.  
⚠ **Combine with Other Filters for Deep Audits:** Use alongside **`account`, `tag`, or `policy` filters** for granular control.  

---

## 🛠 **Supported Org-Unit Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The OU attribute to filter by (e.g., `Name`, `ParentId`). |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value (e.g., `dev`, `prod`). |
| `value_regex` | `string`   | Regular expression pattern for matching values. |

---

## ✅ **Best Practices for AWS Organizations Audits**  
💡 **Ensure OUs Are Used for Governance:** Place **all AWS accounts inside an OU for policy enforcement**.  
💡 **Regularly Audit AWS Account Assignments:** Ensure **new accounts are correctly assigned to OUs**.  
💡 **Use OU-Based Cost Allocation Tags:** Improve **budgeting and chargeback tracking**.  

---

## 🔹 **Ownership: Audit S3 Bucket Object Ownership Controls**  

### ✨ **What is Ownership Filtering?**  
The `ownership` filter in Cloud Custodian **checks the object ownership settings of S3 buckets**, allowing organizations to **enforce security policies, manage ACL usage, and ensure compliance with best practices**.  

**Common Use Cases:**  
✅ **Identify Buckets with ACLs Disabled** – Detect S3 buckets where ACLs are fully disabled (`BucketOwnerEnforced`).  
✅ **Ensure Buckets Use Preferred or Enforced Ownership** – Confirm that object ownership is controlled properly.  
✅ **Find Buckets with No Ownership Controls Set** – Identify buckets without explicit ownership settings.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves S3 bucket object ownership settings** (e.g., `BucketOwnerEnforced`, `BucketOwnerPreferred`, `ObjectWriter`).  
2️⃣ **Filters based on attributes such as `value` and `op`** (comparison operator).  
3️⃣ **Supports regex, list-based filtering, and logical conditions** for advanced auditing.  
4️⃣ **Returns S3 buckets that match or violate the defined ownership settings**.  

---

## 📝 **Example: Identify Buckets with ACLs Disabled (`BucketOwnerEnforced`)**  
This policy **detects S3 buckets where ACLs are completely disabled**.  

```yaml
policies:
  - name: s3-bucket-acls-disabled
    resource: aws.s3
    region: us-east-1
    filters:
      - type: ownership
        value: BucketOwnerEnforced
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves S3 bucket ownership settings**.  
📌 Flags **buckets where `BucketOwnerEnforced` is applied**, ensuring **ACLs are disabled** for stronger security.  

---

## 📝 **Example: Identify Buckets with Preferred or Enforced Ownership**  
This policy **identifies S3 buckets using either `BucketOwnerEnforced` or `BucketOwnerPreferred`**.  

```yaml
policies:
  - name: s3-bucket-ownership-preferred
    resource: aws.s3
    region: us-east-1
    filters:
      - type: ownership
        op: in
        value:
          - BucketOwnerEnforced
          - BucketOwnerPreferred
```

🔹 **What Happens?**  
📌 Cloud Custodian **checks object ownership settings on all S3 buckets**.  
📌 Flags **buckets using either `BucketOwnerEnforced` or `BucketOwnerPreferred`**, ensuring **centralized ownership**.  

---

## 📝 **Example: Detect Buckets Without Ownership Controls**  
This policy **flags S3 buckets that do not have an ownership control set**.  

```yaml
policies:
  - name: s3-bucket-no-ownership-controls
    resource: aws.s3
    region: us-east-1
    filters:
      - type: ownership
        value: empty
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves S3 bucket ownership settings**.  
📌 Flags **buckets where ownership settings are missing (`empty`)**, ensuring **all buckets have explicit ownership rules**.  

---

## 🎯 **Why Use Ownership Filtering?**  
✅ **Improves AWS Security & Compliance:** Ensures **ACLs are disabled and object ownership is enforced**.  
✅ **Automates Cloud Governance:** Detects **misconfigured S3 bucket ownership settings**.  
✅ **Supports AWS Best Practices:** Aligns with **AWS recommendations for disabling ACLs in favor of IAM-based permissions**.  

---

## ⚠ **Key Considerations**  
⚠ **`BucketOwnerEnforced` Disables ACLs Completely:** This is the **most secure option** for **preventing object-level ACL permissions**.  
⚠ **Use `not` for Detecting Misconfigured Buckets:** If checking for missing settings, **wrap the filter in `not:`**.  
⚠ **Regularly Audit Object Ownership Settings:** AWS **recommends using IAM policies instead of bucket ACLs**.  

---

## 🛠 **Supported Ownership Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The S3 bucket ownership attribute to filter by. |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value (`BucketOwnerEnforced`, `BucketOwnerPreferred`, `ObjectWriter`). |
| `value_regex` | `string`   | Regular expression pattern for matching values. |

---

## ✅ **Best Practices for S3 Bucket Ownership Auditing**  
💡 **Ensure All Buckets Use `BucketOwnerEnforced`:** Enforce IAM-based access control **instead of ACLs**.  
💡 **Monitor Buckets Without Ownership Controls:** Identify buckets **missing explicit settings**.  
💡 **Regularly Audit Ownership Policies for Compliance:** Ensure **all new buckets follow ownership best practices**.  

---

## 🔹 **Policy: Filter AWS Policies Based on Attributes**  

### ✨ **What is Policy Filtering?**  
The `policy` filter in Cloud Custodian **analyzes AWS policies, including Service Control Policies (SCPs), Tag Policies, Backup Policies, and AI Service Opt-Out Policies**, enabling organizations to **enforce compliance, detect misconfigurations, and audit policy adherence**.  

**Common Use Cases:**  
✅ **Audit Service Control Policies (SCPs)** – Identify AWS accounts restricted by specific SCPs.  
✅ **Ensure Proper Tag Policies** – Enforce tagging standards across AWS environments.  
✅ **Monitor Backup Policies** – Ensure critical AWS resources have backup retention rules in place.  
✅ **Track AI Service Opt-Outs** – Identify AWS accounts that have opted out of AI services.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves AWS policies of the specified type** (e.g., `SERVICE_CONTROL_POLICY`, `TAG_POLICY`).  
2️⃣ **Filters policies based on attributes like policy inheritance, applied rules, or content**.  
3️⃣ **Supports regex, list-based filtering, and logical conditions** for advanced auditing.  
4️⃣ **Returns AWS policies that match or violate the defined conditions**.  

---

## 📝 **Example: Find Service Control Policies (SCPs) Applied to AWS Accounts**  
This policy **retrieves all SCPs within an AWS Organization**.  

```yaml
policies:
  - name: list-scp-policies
    resource: aws.policy
    filters:
      - type: policy
        policy-type: SERVICE_CONTROL_POLICY
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves all SCPs in the AWS Organization**.  
📌 Helps track **which policies enforce restrictions on AWS accounts**.  

---

## 📝 **Example: Identify AWS Tag Policies**  
This policy **flags AWS accounts that have Tag Policies applied**.  

```yaml
policies:
  - name: audit-tag-policies
    resource: aws.policy
    filters:
      - type: policy
        policy-type: TAG_POLICY
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves AWS Tag Policies** applied within an organization.  
📌 Helps **ensure AWS tagging consistency across accounts**.  

---

## 📝 **Example: Detect AWS Accounts Without Backup Policies**  
This policy **flags AWS accounts missing backup enforcement policies**.  

```yaml
policies:
  - name: detect-missing-backup-policies
    resource: aws.policy
    filters:
      - type: policy
        policy-type: BACKUP_POLICY
      - not:
          - type: inherited
            value: true
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves backup policies applied to AWS accounts**.  
📌 Flags **accounts without inherited backup policies**, ensuring compliance with disaster recovery policies.  

---

## 🎯 **Why Use Policy Filtering?**  
✅ **Automates AWS Governance & Compliance:** Tracks **AWS accounts and resources for policy adherence**.  
✅ **Ensures Security Policy Enforcement:** Identifies **AWS accounts not following SCPs or Tag Policies**.  
✅ **Enhances Backup & Disaster Recovery Readiness:** Verifies that **backup policies are consistently applied**.  

---

## ⚠ **Key Considerations**  
⚠ **Ensure AWS Organizations Is Enabled:** AWS policy filtering **requires AWS Organizations for SCPs and Tag Policies**.  
⚠ **Use `not` for Detecting Missing Policies:** If checking for missing policies, **wrap the filter in `not:`**.  
⚠ **Regularly Audit Policy Inheritance:** Ensure **all child AWS accounts comply with inherited policies**.  

---

## 🛠 **Supported Policy Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `policy-type` | `enum`     | Type of AWS policy (`SERVICE_CONTROL_POLICY`, `TAG_POLICY`, `BACKUP_POLICY`, `AISERVICES_OPT_OUT_POLICY`). **(Required)** |
| `inherited`   | `boolean`  | Whether the policy is inherited from a parent OU or account. |
| `key`         | `string`   | Policy attribute to filter by. |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value (e.g., policy name, ID). |

---

## ✅ **Best Practices for AWS Policy Auditing**  
💡 **Regularly Audit AWS SCPs to Prevent Overly Permissive Access:** Restrict AWS actions **only to approved services**.  
💡 **Ensure All AWS Accounts Have Backup Policies Applied:** Prevent **accidental data loss by enforcing backup retention**.  
💡 **Enforce Tagging Policies for Cost & Compliance:** Ensure **consistent AWS resource tagging for cost tracking and governance**.  

---

## 🔹 **Reduce: Group, Sort, and Limit AWS Resources for Custom Selection**  

### ✨ **What is Reduce Filtering?**  
The `reduce` filter in Cloud Custodian **groups, sorts, and limits AWS resources** based on attributes, helping organizations **prioritize resource selection, optimize workloads, and automate governance**.  

**Common Use Cases:**  
✅ **Select the Oldest or Newest Instance in an Auto Scaling Group (ASG)** – Helps **identify resources for termination or maintenance**.  
✅ **Randomly Select a Subset of AWS Resources** – Useful for **gradual policy enforcement or testing**.  
✅ **Enforce Maximum Limits on Filtered Resources** – Avoid processing **too many resources at once**.  

---

## 🔍 **How It Works**  
1️⃣ **Groups AWS resources based on a shared attribute** (e.g., `tag:aws:autoscaling:groupName`).  
2️⃣ **Sorts resources by a specific field** (e.g., `LaunchTime`, `InstanceId`).  
3️⃣ **Limits the number of resources selected** (e.g., max 15, top 10%).  
4️⃣ **Returns only the subset of resources that match the defined criteria**.  

---

## 📝 **Example: Select the Oldest EC2 Instance from Each Auto Scaling Group**  
This policy **groups EC2 instances by ASG name, sorts them by launch time, and selects the oldest instance from each group**.  

```yaml
policies:
  - name: oldest-instance-by-asg
    resource: ec2
    filters:
      - "tag:aws:autoscaling:groupName": present
      - type: reduce
        group-by: "tag:aws:autoscaling:groupName"
        sort-by: "LaunchTime"
        order: asc
        limit: 1
```

🔹 **What Happens?**  
📌 Cloud Custodian **groups EC2 instances by their ASG tag (`tag:aws:autoscaling:groupName`)**.  
📌 Sorts **instances by `LaunchTime` in ascending order**, selecting **the oldest instance from each ASG**.  
📌 Helps **identify instances that have been running the longest for lifecycle actions**.  

---

## 📝 **Example: Randomly Select 10% of Resources, Capping at 15 Instances**  
This policy **randomly selects 10% of EC2 instances but ensures no more than 15 are chosen**.  

```yaml
policies:
  - name: random-selection
    resource: ec2
    filters:
      - type: reduce
        order: randomize
        limit: 15
        limit-percent: 10
```

🔹 **What Happens?**  
📌 Cloud Custodian **randomly selects 10% of the total EC2 instances**.  
📌 Ensures that **no more than 15 instances are selected, even if 10% is greater than 15**.  
📌 Useful for **testing policies or gradual enforcement**.  

---

## 🎯 **Why Use Reduce Filtering?**  
✅ **Optimizes AWS Resource Selection:** Selects **only the most relevant resources for policy actions**.  
✅ **Improves Performance & Efficiency:** Reduces **unnecessary processing by limiting filtered resources**.  
✅ **Supports Randomized Selection for Load Balancing:** Useful for **gradual enforcement of governance policies**.  

---

## ⚠ **Key Considerations**  
⚠ **Ensure Grouping Attributes Exist (`group-by`)** – Ensure **grouping keys (e.g., ASG names) are present** in all resources.  
⚠ **Use `randomize` for Load Distribution:** When **testing policies across a sample of resources**, use `randomize`.  
⚠ **Set `limit-percent` Carefully:** **10% of thousands of resources can still be a large number**—set **hard limits (`limit`) when needed**.  

---

## 🛠 **Supported Reduce Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `group-by`    | `string`   | Attribute to group resources by (e.g., `tag:aws:autoscaling:groupName`). |
| `sort-by`     | `string`   | Attribute to sort resources by (e.g., `LaunchTime`). |
| `order`       | `enum`     | Sorting order (`asc`, `desc`, `randomize`). |
| `limit`       | `number`   | Maximum number of resources to return. |
| `limit-percent` | `number` | Percentage of total resources to select (e.g., `10%`). |
| `discard`     | `number`   | Number of resources to remove from selection. |

---

## ✅ **Best Practices for Using Reduce Filters**  
💡 **Use `group-by` for Resource-Level Granularity:** Ensure **policy actions are applied to the correct group of resources**.  
💡 **Limit Large Query Results for Efficiency:** Use `limit` and `limit-percent` **to prevent excessive resource filtering**.  
💡 **Randomize When Testing Policies:** If gradually applying a policy, **use `randomize` to spread enforcement across resources**.  

---

## 🔹 **Route: Filter AWS App Mesh Routes from Virtual Routers**  

### ✨ **What is Route Filtering?**  
The `route` filter in Cloud Custodian **analyzes AWS App Mesh routes attached to virtual routers**, allowing organizations to **enforce service mesh governance, detect misconfigurations, and optimize traffic routing**.  

**Common Use Cases:**  
✅ **Ensure App Mesh Routes Belong to the Correct Owner** – Verify that routes are **not configured with an external `meshOwner`**.  
✅ **Audit Route Configurations for Compliance** – Identify **misconfigured routing rules** across services.  
✅ **Detect Unauthorized Route Modifications** – Track **changes in virtual router configurations**.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves AWS App Mesh route configurations from virtual routers**.  
2️⃣ **Filters resources based on attributes like `meshOwner`, `routeType`, and `virtualService`**.  
3️⃣ **Supports regex, list-based filtering, and logical conditions** for advanced auditing.  
4️⃣ **Returns App Mesh configurations that match or violate routing rules**.  

---

## 📝 **Example: Identify App Mesh Routes Owned by External Accounts**  
This policy **detects AWS App Mesh routes where the `meshOwner` is different from the `resourceOwner`**.  

```yaml
policies:
  - name: appmesh-route-policy
    resource: aws.appmesh-mesh
    filters:
      - type: route
        key: virtualRouters[].routes[]
        attrs:
          - type: value
            key: meshOwner
            op: ne
            value: resourceOwner
            value_type: "expr"
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves App Mesh routes from virtual routers**.  
📌 Flags **routes where `meshOwner` is different from `resourceOwner`**, ensuring that all routes **belong to the correct AWS account**.  

---

## 🎯 **Why Use Route Filtering?**  
✅ **Enhances App Mesh Security & Governance:** Prevents **misconfigured routing rules in service mesh architectures**.  
✅ **Improves Observability & Control:** Ensures **routing configurations follow organizational policies**.  
✅ **Detects Unauthorized Modifications:** Helps **identify unauthorized route ownership changes**.  

---

## ⚠ **Key Considerations**  
⚠ **Mesh Ownership May Vary by Region & Account:** Use `meshOwner` **to validate multi-account mesh setups**.  
⚠ **Ensure TLS is Enforced for Secure Routing:** Validate that **App Mesh routes use TLS encryption for traffic security**.  
⚠ **Use Regex for Dynamic Matching:** Apply **pattern-based filtering to match multiple route patterns dynamically**.  

---

## 🛠 **Supported Route Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `attrs`       | `array`    | List of attributes to filter by (e.g., `meshOwner`, `routeType`). |
| `count`       | `number`   | Number of matching attributes required. |
| `count_op`    | `enum`     | Comparison operator (`eq`, `lt`, `gt`, etc.). |
| `type`        | `enum`     | Must be `route`. **(Required)** |

---

## ✅ **Best Practices for AWS App Mesh Route Audits**  
💡 **Verify Route Ownership Regularly:** Ensure all **routes belong to trusted AWS accounts**.  
💡 **Enforce TLS for Secure Communication:** Require **TLS in all App Mesh routes** to encrypt service traffic.  
💡 **Monitor for Unauthorized Configuration Changes:** Use Cloud Custodian to **track route modifications**.  

---

## 🔹 **Security-Group: Filter Resources by Associated Security Groups**  

### ✨ **What is Security-Group Filtering?**  
The `security-group` filter in Cloud Custodian **evaluates AWS resources based on their associated security groups**, helping organizations **enforce security policies, detect misconfigurations, and optimize access control**.  

**Common Use Cases:**  
✅ **Identify EC2 Instances Using Specific Security Groups** – Track instances based on security group attributes.  
✅ **Find Misconfigured Security Group Associations** – Detect resources attached to unauthorized security groups.  
✅ **Ensure Compliance with Security Best Practices** – Enforce rules restricting access to specific ports or CIDR ranges.  

---

## 🔍 **How It Works**  
1️⃣ **Retrieves security group associations for AWS resources** (e.g., EC2 instances, RDS databases, ENIs).  
2️⃣ **Filters based on attributes such as `GroupId`, `GroupName`, or `Description`**.  
3️⃣ **Supports regex, list-based filtering, and logical conditions (`and`, `or`)**.  
4️⃣ **Returns AWS resources that match or violate security group rules**.  

---

## 📝 **Example: Identify EC2 Instances with a Specific Security Group**  
This policy **detects EC2 instances using security group `sg-12345678`**.  

```yaml
policies:
  - name: ec2-with-specific-security-group
    resource: ec2
    filters:
      - type: security-group
        key: GroupId
        value: sg-12345678
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves EC2 instances and their attached security groups**.  
📌 Flags **instances using `sg-12345678`**, helping **track resources using a specific security group**.  

---

## 📝 **Example: Detect Resources Using an Unapproved Security Group Name**  
This policy **flags EC2 instances using security groups that do not match the `approved-sg-*` naming convention**.  

```yaml
policies:
  - name: ec2-with-unapproved-security-group
    resource: ec2
    filters:
      - type: security-group
        key: GroupName
        op: regex
        value: "^approved-sg-.*$"
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves EC2 instances and their security group names**.  
📌 Flags **instances using security groups that do not match `approved-sg-*`**, enforcing security standards.  

---

## 📝 **Example: Find Security Groups Associated with EC2 but Not Attached to Any ENI**  
This policy **detects security groups that are associated with EC2 instances but not linked to any network interface (ENI)**.  

```yaml
policies:
  - name: security-groups-without-eni
    resource: security-group
    filters:
      - type: security-group
        key: GroupId
        match-resource: false
```

🔹 **What Happens?**  
📌 Cloud Custodian **retrieves security groups and their ENI associations**.  
📌 Flags **security groups not associated with any network interface**, identifying **unused security groups**.  

---

## 🎯 **Why Use Security-Group Filtering?**  
✅ **Enhances AWS Security & Access Control:** Ensures **only authorized resources are attached to specific security groups**.  
✅ **Automates AWS Security Audits:** Tracks **misconfigured security group associations across AWS services**.  
✅ **Supports Compliance & Governance Policies:** Ensures **security groups follow naming conventions and best practices**.  

---

## ⚠ **Key Considerations**  
⚠ **Security Groups Can Be Attached to Multiple Resources:** Ensure **your policies account for multi-resource usage**.  
⚠ **Use `match-resource: false` for Unused Security Groups:** Helps identify **security groups no longer in use**.  
⚠ **Combine with `network-location` for Deep Audits:** Validate **security group configurations along with subnet rules**.  

---

## 🛠 **Supported Security-Group Properties**  

| 🔖 **Property**       | 🏷 **Type**    | 🔍 **Description** |
|----------------|------------|----------------|
| `key`         | `string`   | The security group attribute to filter by (`GroupId`, `GroupName`, `Description`). |
| `op`         | `enum`     | Comparison operator (`eq`, `ne`, `contains`, `regex`, etc.). |
| `value`      | `string/boolean/number` | Expected value for the filter (e.g., `sg-12345678`). |
| `operator`   | `enum`     | Logical operator (`and`, `or`). |
| `match-resource` | `boolean`  | If `false`, filters for security groups **not associated with any resource**. |

---

## ✅ **Best Practices for AWS Security Group Auditing**  
💡 **Ensure Only Approved Security Groups Are Used:** Prevent **unauthorized access by enforcing security group policies**.  
💡 **Detect Unused Security Groups:** Regularly **audit and remove security groups that are no longer in use**.  
💡 **Monitor Security Group Changes Continuously:** Use Cloud Custodian **to track changes in security group assignments**.  

---

