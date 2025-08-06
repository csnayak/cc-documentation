### **📌 Conditional Policy Execution in Cloud Custodian**

---

### **🔹 What is Conditional Policy Execution?**  
Cloud Custodian allows policies to **execute only under specific conditions**, preventing unnecessary evaluations and actions. Policies can be skipped based on **region, date, account ID, provider, or other environment factors**.

📌 **Common Use Cases:**  
- **Shut down EC2 instances during a holiday break** and start them later.  
- **Deploy policies only in specific AWS regions**.  
- **Skip execution for automated service accounts** in event-driven policies.  

---

### **🔹 Available Environment Keys for Conditions**
| **Key**        | **Description** |
|---------------|----------------|
| `name`        | Name of the policy. |
| `region`      | AWS region where the policy is evaluated. |
| `resource`    | The resource type the policy applies to. |
| `account_id`  | AWS account ID (or subscription/project ID in other clouds). |
| `provider`    | Cloud provider (`aws`, `azure`, `gcp`, etc.). |
| `policy`      | The policy data structure. |
| `now`         | The current date and time. |
| `account`     | The account information when running in **c7n-org**. |

---

## **🔹 Example 1: Stop EC2 Instances During Holiday Break**
This policy **automatically stops EC2 instances** between **December 15 and December 31, 2018**.

```yaml
policies:
  - name: holiday-break-stop
    description: |
      Stop all EC2 instances during the holiday break (Dec 15 - Dec 31, 2018).
    resource: ec2
    conditions:
      - type: value
        key: now
        op: greater-than
        value_type: date
        value: "2018-12-15"
      - type: value
        key: now
        op: less-than
        value_type: date
        value: "2018-12-31"
    filters:
      - "tag:holiday-off-hours": present
    actions:
      - stop
```
✔ **Prevents unnecessary costs by stopping instances during inactive periods.**  

---

## **🔹 Example 2: Start EC2 Instances on January 1, 2019**
This policy **starts EC2 instances** on **January 1, 2019** if they have the `holiday-off-hours` tag.

```yaml
policies:
  - name: holiday-break-start
    description: |
      Start EC2 instances after the holiday break on January 1, 2019.
    resource: ec2
    conditions:
      - type: value
        key: now
        value_type: date
        op: greater-than
        value: "2019-01-01"
      - type: value
        key: now
        value_type: date
        op: less-than
        value: "2019-01-01 23:59:59"
    filters:
      - "tag:holiday-off-hours": present
    actions:
      - start
```
✔ **Ensures instances are automatically restarted after the break.**  

---

## **🔹 Example 3: Restrict Policy Execution to Specific AWS Regions**
This policy **only executes in `us-east-2` and `us-west-2` regions**.

```yaml
policies:
  - name: ec2-auto-tag-creator
    description: Auto-tag Creator on EC2 if not set.
    resource: aws.ec2
    mode:
      type: cloudtrail
      events:
        - RunInstances
    conditions:
      - type: value
        key: region
        op: in
        value:
          - us-east-2
          - us-west-2
```
✔ **Prevents execution in other regions, ensuring policy runs only where needed.**  

---

## **🔹 Example 4: Prevent Execution for Automated Service Accounts**
This policy **skips execution if the event is triggered by a service account** (e.g., Cloud Custodian, Jenkins, AWS Service Roles).

```yaml
policies:
  - name: ec2-auto-tag-creator
    resource: aws.ec2
    mode:
      type: cloudtrail
      events:
        - RunInstances
    conditions:
      - not:
          - type: event
            key: "detail.userIdentity.arn"
            op: regex-case
            value: '.*(CloudCustodian|Jenkins|AWS.*ServiceRole|LambdaFunction|\/sfr-|\/i-|\d{8,}$)'
    filters:
      - "tag:Creator": empty
    actions:
      - type: auto-tag-user
        tag: Creator
```
✔ **Ensures that the policy only applies to manually created EC2 instances, ignoring automation triggers.**  

---

### **📌 Limiting How Many Resources Cloud Custodian Affects**

---

### **🔹 Why Limit Resource Actions?**  
By default, Cloud Custodian **acts on all resources that match a policy's filters**. However, to **prevent unintended large-scale modifications**, policy authors can set **limits on how many resources** a policy can affect.

📌 **Common Use Cases:**  
- **Prevent mass deletions** of AWS log groups, EC2 instances, or S3 buckets.  
- **Set safety limits** on large-scale policy execution.  
- **Ensure compliance** by enforcing controlled changes.  

---

### **🔹 Methods for Limiting Resources**
| **Method**             | **Description** |
|-----------------------|----------------|
| `max-resources-percent` | Stops execution if **more than a set percentage** of total resources would be affected. |
| `max-resources`       | Stops execution if **more than a set number** of resources would be affected. |
| `max-resources` with `or`/`and` | Combines **percentage and absolute limits** for fine-grained control. |

---

## **🔹 Example 1: Limit Policy Execution to 5% of Log Groups**
This policy **deletes AWS log groups** that haven't been written to in **5 days**, but **stops execution if more than 5% of total log groups** would be deleted.

```yaml
policies:
  - name: log-delete
    description: |
      Delete log groups inactive for 5 days,
      but stop if more than 5% of total log groups would be deleted.
    resource: aws.log-group
    max-resources-percent: 5
    filters:
      - type: last-write
        days: 5
```
✔ **Ensures that only a small percentage of log groups are affected at a time.**  

---

## **🔹 Example 2: Limit Execution Based on Absolute Number (`max-resources`)**
This policy **stops execution if more than 20 log groups** would be affected.

```yaml
policies:
  - name: log-delete
    description: |
      Delete log groups inactive for 5 days,
      but stop execution if more than 20 log groups match.
    resource: aws.log-group
    max-resources: 20
    filters:
      - type: last-write
        days: 5
```
✔ **Prevents accidental deletion of too many log groups at once.**  

---

## **🔹 Example 3: Enforce Both Percentage & Count Limits (`max-resources` with `and`)**
This policy **stops execution if**:
- **More than 50%** of total log groups would be affected **AND**
- **More than 20** log groups would be affected.

```yaml
policies:
  - name: log-delete
    description: |
      Stop execution if affected resources exceed 50% of total log groups,
      and the absolute count is over 20.
    resource: aws.log-group
    max-resources:
      percent: 50
      amount: 20
      op: and
    filters:
      - type: last-write
        days: 5
    actions:
      - delete
```
✔ **Ensures both percentage and absolute safety limits are met before execution.**  

---

### **🔹 What Happens When Limits Are Exceeded?**
If a policy tries to affect more resources than the defined limit, Custodian **stops execution** and logs an error:

```plaintext
custodian.commands:ERROR policy: log-delete exceeded resource limit: 2.5% found: 1 total: 1
```
✔ **No resources are modified when limits are breached.**  

---

### **🔹 Metrics for Resource Limits**
If **metrics collection (`-m` or `--metrics`)** is enabled, Custodian will publish:
- **ResourceCount** → The number of resources matched by the policy.  
✔ **Useful for tracking how many resources would be affected before taking action.**  

---

