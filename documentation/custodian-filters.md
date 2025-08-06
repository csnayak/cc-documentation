## **Cloud Custodian Generic Filters**

### **🔹 What is a Value Filter?**  
A **Value Filter** in Cloud Custodian is used to filter cloud resources based on specific attributes. It allows for granular selection by defining conditions on resource properties.

📌 **Key Use Cases:**  
- Identify **EC2 instances** older than 30 days.  
- Find **untagged resources** in the environment.  
- Detect **security groups** allowing unrestricted access.  
- Filter **S3 buckets** with public access enabled.  

---

### **🔹 How to Use a Value Filter?**  
Value filters are defined in **YAML** and follow this structure:

```yaml
filters:
  - type: value
    key: "<attribute>"
    op: "<operator>"
    value: "<expected_value>"
```

📌 **Breakdown of Components:**  
- **`type: value`** → Specifies the filter type.  
- **`key`** → The resource attribute to evaluate.  
- **`op`** → The comparison operation (e.g., `equal`, `greater-than`).  
- **`value`** → The expected value.  
- **`value_type`** *(optional)* → Used for data type conversion (e.g., `age`, `cidr`).  

---

### **🔹 Supported Comparison Operators**
| **Operator**     | **Meaning**                           | **Example**                        |
|-----------------|---------------------------------|----------------------------------|
| `equal`         | Exact match                     | `State.Name: running`           |
| `not-equal`     | Not equal to a value           | `State.Name: stopped`           |
| `greater-than`  | Value is greater than          | `age > 30`                      |
| `less-than`     | Value is less than             | `size < 100`                    |
| `contains`      | Checks if a string contains    | `"tag:Owner" contains "admin"`  |
| `regex`         | Matches a pattern using regex  | `"tag:Owner" matches "^(admin).*$"` |
| `in`           | Checks if value exists in a list  | `InstanceType in ["t2.micro", "t3.small"]` |
| `not-in`       | Checks if value is not in a list | `Region not in ["us-east-1", "us-west-2"]` |
| `intersect`    | Finds overlapping values in lists | `CIDR intersects ["10.0.0.0/8"]` |

---

### **🔹 Common Use Cases & Examples**

#### ✅ **Filter EC2 Instances Older Than 30 Days**
```yaml
filters:
  - type: value
    key: LaunchTime
    value_type: age
    op: greater-than
    value: 30
```
🔹 **Finds all EC2 instances that have been running for more than 30 days.**  

---

#### ✅ **Find S3 Buckets with Public Access**
```yaml
filters:
  - type: value
    key: PublicAccessBlockConfiguration.BlockPublicAcls
    op: equal
    value: false
```
🔹 **Identifies S3 buckets that allow public ACLs.**  

---

#### ✅ **Detect Security Groups Allowing SSH from Any IP**
```yaml
filters:
  - type: ingress
    key: Cidr
    op: equal
    value: "0.0.0.0/0"
    Ports: [22]
```
🔹 **Finds security groups that expose SSH (port 22) to the internet.**  

---

#### ✅ **Identify IAM Users Without MFA**
```yaml
filters:
  - type: value
    key: MFAEnabled
    op: equal
    value: false
```
🔹 **Lists IAM users who do not have Multi-Factor Authentication (MFA) enabled.**  

---

### **🔹 Advanced Use Cases**

#### ✅ **Use Regular Expressions to Match Values**
```yaml
filters:
  - type: value
    key: "tag:Owner"
    op: regex
    value: "^(admin|manager).*$"
```
🔹 **Finds resources where the `Owner` tag starts with `admin` or `manager`.**  

---

#### ✅ **Filter EC2 Instances by Multiple Instance Types**
```yaml
filters:
  - type: value
    key: InstanceType
    op: in
    value: ["t2.micro", "t3.micro", "t3.small"]
```
🔹 **Finds instances of any specified instance types.**  

---

#### ✅ **Detect Security Groups Allowing Traffic in a Specific Network Range**
```yaml
filters:
  - type: value
    key: IpPermissions[*].IpRanges
    op: intersect
    value: ["10.0.0.0/8", "192.168.1.0/24"]
```
🔹 **Finds security groups allowing access within the specified CIDR blocks.**  

---


### **🔹 What Are Special Values?**  
Special values in Cloud Custodian are **meta-values** that help check whether a resource contains a specific key or value. These values make it easier to test for **existence, emptiness, or missing attributes** in cloud resources.

---

### **🔹 Available Special Values**  

| **Special Value** | **Description** |
|------------------|-------------------------------------------------|
| **`absent`**      | Matches when a key **does not exist**. |
| **`present`**     | Matches when a key **exists**. |
| **`empty`**       | Matches when a value is **false, empty, or missing**. |
| **`not-null`**    | Matches when a value **exists and is not false or empty**. |

---

### **🔹 Example: Understanding Special Values**  
Consider an **S3 bucket** with the following attributes:  

```json
{
  "Name": "my_bucket",
  "Versioning": {},
  "Tags": [{
    "Environment": "dev",
    "Owner": ""
  }]
}
```

📌 **What This Means:**  
- The `Environment` tag has a value of `"dev"`.  
- The `Owner` tag **exists** but is empty.  
- The `Team` tag **does not exist**.  
- `Versioning` is present but has **no `Status` value**.

---

### **🔹 Special Value Filters in Action**  

✅ **Find Buckets with an `Environment` Tag Set to "dev"**  
```yaml
filters:
  - "tag:Environment": "dev"
```
✔ **Matches because** the `"Environment"` tag is `"dev"`.

---

✅ **Find Buckets Where `Environment` Tag Exists (Regardless of Value)**  
```yaml
filters:
  - "tag:Environment": "present"
```
✔ **Matches because** the `"Environment"` tag exists.  

---

✅ **Find Buckets Where `Environment` Tag Has Any Value**  
```yaml
filters:
  - "tag:Environment": "not-null"
```
✔ **Matches because** `"Environment"` tag exists and is not empty.  

---

✅ **Find Buckets Where `Owner` Tag Is Empty**  
```yaml
filters:
  - "tag:Owner": "empty"
```
✔ **Matches because** the `"Owner"` tag exists but has no value.  

---

✅ **Find Buckets Where `Owner` Tag Exists (Even If Empty)**  
```yaml
filters:
  - "tag:Owner": "present"
```
✔ **Matches because** the `"Owner"` tag exists, even though it's empty.  

---

✅ **Find Buckets Where `Team` Tag Is Empty or Missing**  
```yaml
filters:
  - "tag:Team": "empty"
```
✔ **Matches because** the `"Team"` tag is missing, which counts as empty.  

---

✅ **Find Buckets Where `Team` Tag Does Not Exist**  
```yaml
filters:
  - "tag:Team": "absent"
```
✔ **Matches because** `"Team"` tag does not exist.  

---

✅ **Find Buckets Where `Versioning` Is Present But Empty**  
```yaml
filters:
  - "Versioning": "empty"
```
✔ **Matches because** `"Versioning"` exists but contains no `Status` field.  

---

✅ **Find Buckets Where `Versioning` Exists**  
```yaml
filters:
  - "Versioning": "present"
```
✔ **Matches because** `"Versioning"` exists, even though it is empty.  

---

✅ **Find Buckets Where `Versioning.Status` Is Empty**  
```yaml
filters:
  - "Versioning.Status": "empty"
```
✔ **Matches because** `"Versioning.Status"` does not exist (empty field).  

---

✅ **Find Buckets Where `Versioning.Status` Is Missing**  
```yaml
filters:
  - "Versioning.Status": "absent"
```
✔ **Matches because** `"Versioning.Status"` does not exist at all.  

---

### **🔹 What Are Comparison Operators?**  
Comparison operators in Cloud Custodian allow policies to **evaluate resource attributes** based on numerical, string, or list-based conditions. These operators enable precise filtering to identify cloud resources that match specific criteria.

📌 **Common Use Cases:**  
- Find **EC2 instances** with more than 4 CPU cores.  
- Identify **S3 buckets** without encryption enabled.  
- Detect **IAM users** without Multi-Factor Authentication (MFA).  
- Filter **security groups** allowing unrestricted access.  

---

### **🔹 Available Comparison Operators**  

| **Operator**       | **Alias**      | **Description** |
|-------------------|---------------|----------------|
| `equal`          | `eq`           | Matches exact values |
| `not-equal`      | `ne`           | Matches values that are not equal |
| `greater-than`   | `gt`           | Matches values greater than the given number |
| `greater-than-or-equal` | `gte` or `ge` | Matches values greater than or equal to the given number |
| `less-than`      | `lt`           | Matches values less than the given number |
| `less-than-or-equal` | `lte` or `le` | Matches values less than or equal to the given number |
| `in`            | -             | Matches if the value exists in a predefined list |
| `not-in`        | `ni`          | Matches if the value is **not** in a predefined list |
| `contains`      | -             | Matches if a string or list contains a specific value |

---

### **🔹 Example: Using Comparison Operators**  

#### ✅ **Find EC2 Instances With More Than 36 CPU Cores**
```yaml
filters:
  - type: value
    key: CpuOptions.CoreCount   # Attribute to compare
    value: 36                   # Value being compared
    op: greater-than            # Comparison operator
```
✔ **Matches instances with more than 36 CPU cores.**  

---

#### ✅ **Find S3 Buckets Without Encryption**
```yaml
filters:
  - type: value
    key: ServerSideEncryptionConfiguration
    op: absent
```
✔ **Matches S3 buckets that do not have encryption enabled.**  

---

#### ✅ **Find RDS Databases with Storage Less Than 100 GB**
```yaml
filters:
  - type: value
    key: AllocatedStorage
    value: 100
    op: lt
```
✔ **Matches RDS databases with less than 100 GB storage.**  

---

#### ✅ **Find Security Groups Allowing SSH from the Internet**
```yaml
filters:
  - type: ingress
    key: Cidr
    value: "0.0.0.0/0"
    op: equal
    Ports: [22]
```
✔ **Matches security groups that allow SSH (port 22) from any IP.**  

---

#### ✅ **Find EC2 Instances Running Specific Instance Types**
```yaml
filters:
  - type: value
    key: InstanceType
    op: in
    value: ["t2.micro", "t3.micro", "t3.small"]
```
✔ **Matches instances with instance types `t2.micro`, `t3.micro`, or `t3.small`.**  

---

#### ✅ **Find IAM Users Without MFA Enabled**
```yaml
filters:
  - type: value
    key: MFAEnabled
    op: equal
    value: false
```
✔ **Matches IAM users who do not have MFA enabled.**  

---

#### ✅ **Find EC2 Instances in Specific Regions**
```yaml
filters:
  - type: value
    key: Placement.AvailabilityZone
    op: in
    value: ["us-east-1a", "us-west-2b"]
```
✔ **Matches EC2 instances running in `us-east-1a` or `us-west-2b`.**  

---


### **🔹 What Are Logical Operators?**  
Logical operators in Cloud Custodian allow **combining multiple conditions** within a filter. These operators help refine policies by applying **AND**, **OR**, and **NOT** logic to resource attributes.

📌 **Common Use Cases:**  
- Find **EC2 instances** with either 36 or 42 CPU cores.  
- Identify **RDS databases** that are either unencrypted or have storage below 100 GB.  
- Detect **S3 buckets** that are both public and missing encryption.  

---

### **🔹 Available Logical Operators**  

| **Operator**  | **Description** |
|--------------|----------------|
| `or`        | Matches **if any** condition is `True`. |
| `and`       | Matches **only if all** conditions are `True`. |
| `not`       | Matches **if the condition is `False`**. |

---

### **🔹 Example: Using Logical Operators**  

#### ✅ **Find EC2 Instances with 36 or 42 CPU Cores**  
```yaml
filters:
  - or:  
      - type: value
        key: CpuOptions.CoreCount  
        value: 36  
      - type: value
        key: CpuOptions.CoreCount  
        value: 42  
```
✔ **Matches instances with either 36 or 42 CPU cores.**  

---

#### ✅ **Find RDS Databases That Are Either Unencrypted or Have Less Than 100 GB Storage**  
```yaml
filters:
  - or:
      - type: value
        key: StorageEncrypted
        value: false
      - type: value
        key: AllocatedStorage
        value: 100
        op: lt
```
✔ **Matches RDS databases that are either unencrypted or have storage less than 100 GB.**  

---

#### ✅ **Find Security Groups That Allow SSH (Port 22) or RDP (Port 3389) from Any IP**  
```yaml
filters:
  - or:
      - type: ingress
        key: Cidr
        value: "0.0.0.0/0"
        Ports: [22]
      - type: ingress
        key: Cidr
        value: "0.0.0.0/0"
        Ports: [3389]
```
✔ **Matches security groups allowing unrestricted SSH or RDP access.**  

---

#### ✅ **Find S3 Buckets That Are Both Public and Missing Encryption**  
```yaml
filters:
  - and:
      - type: value
        key: PublicAccessBlockConfiguration.BlockPublicAcls
        value: false
      - type: value
        key: ServerSideEncryptionConfiguration
        op: absent
```
✔ **Matches S3 buckets that are both public and do not have encryption enabled.**  

---

#### ✅ **Find IAM Users Without MFA (Using `not`)**  
```yaml
filters:
  - not:
      - type: value
        key: MFAEnabled
        value: true
```
✔ **Matches IAM users who do not have MFA enabled.**  

---


### **🔹 What Are List Operators?**  
List operators in Cloud Custodian allow policies to compare **resource attributes against lists of values**. These operators help filter resources that match, contain, or differ from predefined lists.

📌 **Common Use Cases:**  
- Find **EC2 instances** using specific AMIs.  
- Identify **resources assigned to specific security groups**.  
- Detect **IAM roles missing required policies**.  
- Filter **VPCs missing expected subnets**.  

---

### **🔹 Available List Operators**  

| **Operator**    | **Description** |
|---------------|----------------|
| `in`          | Matches **if the resource value exists in the list**. |
| `not-in` or `ni` | Matches **if the resource value is not in the list**. |
| `contains`    | Matches **if the resource list contains the specified value**. |
| `intersect`   | Matches **if two lists share any elements**. |
| `difference`  | Matches **if the first list contains values not in the second list**. |

---

### **🔹 Example: Using List Operators**  

#### ✅ **Find EC2 Instances Using a Specific AMI**  
```yaml
filters:
  - type: value
    key: ImageId  
    op: in  
    value: ["ami-123456", "ami-654321"]
```
✔ **Matches EC2 instances that use AMI `ami-123456` or `ami-654321`.**  

---

#### ✅ **Find EC2 Instances That Do Not Use a Specific AMI**  
```yaml
filters:
  - type: value
    key: ImageId  
    op: not-in  
    value: ["ami-123456", "ami-654321"]
```
✔ **Matches EC2 instances that do NOT use these AMIs.**  

---

#### ✅ **Find EC2 Instances Containing a Specific Security Group**  
```yaml
filters:
  - type: value
    key: SecurityGroups[].GroupName
    op: contains
    value: default
```
✔ **Matches instances that have the security group named `default`.**  

---

#### ✅ **Find Security Groups That Share Any Elements with a Predefined List**  
```yaml
filters:
  - type: value
    key: SecurityGroups[].GroupName
    op: intersect
    value: ["common", "custom"]
```
✔ **Matches instances where at least one security group is `common` or `custom`.**  

---

#### ✅ **Find EC2 Instances with Unexpected Security Groups**  
```yaml
filters:
  - type: value
    key: SecurityGroups[].GroupName
    op: difference
    value:
      - common
      - custom
```
✔ **Matches instances that have security groups not in `common` or `custom`.**  

---

#### ✅ **Find EC2 Instances Missing a Required Security Group**  
```yaml
filters:
  - type: value
    key: SecurityGroups[].GroupName
    op: difference
    value:
      - common
      - custom
    value_type: swap
```
✔ **Matches instances missing at least one required security group (`common`, `custom`).**  

---

### **📌 Pattern Matching & Value Transformations in Cloud Custodian**

---

## **🔹 Pattern Matching Operators**
Pattern matching operators in Cloud Custodian allow **advanced filtering of text attributes** using **glob patterns** and **regular expressions (regex)**.

📌 **Common Use Cases:**  
- Find **Lambda functions** with names starting with `custodian_` or `c7n_`.  
- Identify **resources containing specific keywords** in their names.  
- Exclude **resources that contain certain words** in their attributes.  

### **🛠 Available Pattern Matching Operators**
| **Operator**     | **Description** |
|-----------------|----------------|
| `glob`          | Uses wildcard-style matching (`*`, `?`, `[ ]`). |
| `regex`         | Uses **case-insensitive** regex matching. |
| `regex-case`    | Uses **case-sensitive** regex matching. |

---

### **🔹 Example: Using Pattern Matching Operators**  

#### ✅ **Find Lambda Functions with Names Starting with `custodian_` or `c7n_`**  
```yaml
filters:
  - type: value
    key: FunctionName  
    op: regex  
    value: '(custodian|c7n)_\w+'  
```
✔ **Matches functions like `custodian_lambda1`, `c7n_processor`, etc.**  

---

#### ✅ **Find Resources Containing `c7n` in Their Name**  
```yaml
filters:
  - type: value
    key: name  
    op: regex  
    value: '^.*c7n.*$'  
```
✔ **Matches any resource with `c7n` anywhere in its name.**  

---

#### ✅ **Find Resources That Do **NOT** Contain `c7n` in Their Name**  
```yaml
filters:
  - type: value
    key: name  
    op: regex  
    value: '^((?!c7n).)*$'  
```
✔ **Excludes all resources with `c7n` in their name.**  

---

## **🔹 Value Type Transformations**
Cloud Custodian supports **value transformations** using the `value_type` keyword. These transformations **convert data types** before applying comparisons.

📌 **Common Use Cases:**  
- Convert timestamps to **dates** or **ages**.  
- Normalize **text to lowercase** for case-insensitive comparison.  
- Parse **IP addresses and CIDR ranges**.  
- Count the **number of security groups** assigned to an instance.  

---

### **🛠 Available Value Type Transformations**
| **Value Type**    | **Description** |
|------------------|----------------|
| `age`           | Converts to a **datetime** (for past date comparisons). |
| `expiration`    | Converts to a **datetime** (for future date comparisons). |
| `integer`       | Converts the value to an **integer**. |
| `normalize`     | Converts text to **lowercase**. |
| `size`          | Gets the **length** of an element (list count). |
| `swap`          | Swaps the **value and evaluated key**. |
| `cidr`          | Parses an **IP address**. |
| `cidr_size`     | Extracts the **network prefix length** from a CIDR block. |
| `resource_count` | Compares **number of matched resources**. |
| `date`          | Parses the filter’s value as a **date**. |

---

### **🔹 Example: Using Value Type Transformations**

#### ✅ **Find EC2 Instances with Exactly Two Security Groups**  
```yaml
filters:
  - type: value
    key: SecurityGroups[].GroupId
    value_type: size
    value: 2
```
✔ **Matches instances with exactly 2 security groups.**  

---

#### ✅ **Check If a Security Group Is in a Predefined List**  
```yaml
filters:
  - type: value
    key: SecurityGroups[].GroupId
    value_type: swap
    op: in
    value: sg-49b87f44
```
✔ **Matches instances if `sg-49b87f44` is in their security groups.**  

---

#### ✅ **Convert a Tag Value to an Integer Before Comparison**  
```yaml
filters:
  - type: value
    key: tag:Count
    op: greater-than
    value_type: integer
    value: 0
```
✔ **Matches resources where the `Count` tag is greater than `0`.**  

---

#### ✅ **Find RDS Instances Created After a Specific Date**  
```yaml
filters:
  - type: value
    key: InstanceCreateTime
    op: greater-than
    value_type: date
    value: "2019/05/01"
```
✔ **Matches RDS instances created after May 1, 2019.**  

---

#### ✅ **Find EC2 Instances Launched Within the Last 31 Days**  
```yaml
filters:
  - type: value
    key: LaunchTime
    op: less-than
    value_type: age
    value: 32
```
✔ **Matches instances launched in the past month.**  

---

#### ✅ **Find EC2 Instances Launched Within the Past 12 Hours**  
```yaml
filters:
  - type: value
    key: LaunchTime
    op: less-than
    value_type: age
    value: 0.5
```
✔ **Matches instances launched in the last 12 hours.**  

---

#### ✅ **Filter Resources Based on the Total Count**  
```yaml
filters:
  - type: value
    value_type: resource_count
    op: lt
    value: 2
```
✔ **Matches only if fewer than 2 resources meet the filter conditions.**  

---

## **🔹 Advanced Example: Comparing Subnets Using External Lists**

#### ✅ **Find RDS Instances in Public Subnets Using an S3 List**  
```yaml
- name: find-rds-on-public-subnets-using-s3-list
  resource: aws.rds
  filters:
      - type: value
        key: "DBSubnetGroup.Subnets[].SubnetIdentifier"
        op: intersect
        value_from:
            url: s3://cloud-custodian-bucket/PublicSubnets.txt
            format: txt
```
✔ **Matches RDS instances in subnets listed in an S3 text file.**  

---

#### ✅ **Find RDS Instances in Public Subnets Using an Inline List**  
```yaml
- name: find-rds-on-public-subnets-using-inline-list
  resource: aws.rds
  filters:
      - type: value
        key: "DBSubnetGroup.Subnets[].SubnetIdentifier"
        op: intersect
        value:
            - subnet-2a8374658
            - subnet-1b8474522
            - subnet-2d2736444
```
✔ **Matches RDS instances in specific public subnets.**  

---

### **🔹 What Are JMESPath Functions?**  
Cloud Custodian supports **custom JMESPath functions** that help **manipulate and extract data** from resource attributes dynamically. These functions allow advanced filtering and transformations within policies.

📌 **Common Use Cases:**  
- Extract **a specific part of a string** using `split()`.  
- Convert **JSON-encoded data into a structured object** using `from_json()`.  

---

## **🔹 Supported JMESPath Functions**

| **Function**         | **Description** |
|---------------------|----------------|
| `split(separator, input_string)` | Splits a string using the given **separator** and returns a list of strings. |
| `from_json(json_encoded_string)` | Converts a **JSON-encoded string** into a structured object. |

---

## **🔹 Example: Using `split()` for String Manipulation**  
The `split()` function is useful when **extracting parts of a string** from attributes like **log group names, resource paths, or tags**.

#### ✅ **Extract Lambda Function Name from Log Group Name**
```yaml
policies:
  - name: copy-related-tag-with-split
    resource: aws.log-group
    filters:
      - type: value
        key: logGroupName
        value: "/aws/lambda/"
        op: in
        value_type: swap
    actions:
      - type: copy-related-tag
        resource: aws.lambda
        # Extract the function name from the log group name
        key: "split(`/`, logGroupName)[-1]"
        tags: "*"
```
✔ **Extracts the Lambda function name from a log group name like `/aws/lambda/my-function`.**  
✔ **Returns `"my-function"`, which can be used to copy related tags.**  

---

## **🔹 Example: Using `from_json()` for Decoding JSON Data**  
The `from_json()` function **decodes JSON-encoded strings**, allowing policies to filter based on structured data.

#### ✅ **Convert JSON-Encoded Tag Value to an Object**
```yaml
filters:
  - type: value
    key: "from_json(tag:ConfigData).Settings.Encryption"
    op: equal
    value: "enabled"
```
✔ **Extracts the `Encryption` setting from a JSON-encoded tag called `ConfigData`.**  
✔ **Matches resources where `Encryption` is set to `"enabled"`.**  

---

### **🔹 What is Value Regex?**  
When using a **Value Filter**, the `value_regex` option allows extracting specific **substrings** from resource attributes before performing comparisons. This is useful when values contain **extra text** that needs to be removed for proper evaluation.

📌 **Common Use Cases:**  
- Extract **dates** from tags for expiration checks.  
- Retrieve **numeric values** from metadata fields.  
- Normalize **resource names** by stripping unnecessary parts.  

---

### **🔹 How Value Regex Works**
- The **regex pattern** is applied to the attribute specified in `key`.  
- The **first capturing group** (`(...)`) extracts the required value.  
- If **no match is found**, the filter returns `None`, and the resource is ignored.  

📌 **Capturing Groups:**  
- `(capture_this)` → Captures a specific part of the value.  
- `(?:ignore_this|or_this)` → **Non-capturing** group (used for optional text).  

---

### **🔹 Example: Extracting Expiration Date from a Tag**
Some tags **store multiple pieces of information** in a single value, like this:

```json
{
  "tag:metadata": "owner=admin; delete_after=2025-06-30; region=us-east-1"
}
```

#### ✅ **Find Resources Expiring Soon**
```yaml
filters:
  - type: value
    key: "tag:metadata"
    value_type: expiration
    value_regex: ".*delete_after=([0-9]{4}-[0-9]{2}-[0-9]{2}).*"
    op: less-than
    value: 0
```
✔ **Extracts the expiration date (`delete_after=YYYY-MM-DD`) from `tag:metadata`.**  
✔ **Matches resources with expiration dates in the past.**  

---

### **🔹 What is `value_from`?**  
The `value_from` option in Cloud Custodian allows policies to **use external data sources** for filtering resources. Instead of hardcoding values, policies can **dynamically fetch values from URLs, S3, HTTP, CSV files, or databases**.

📌 **Common Use Cases:**  
- **Fetch allowed AMI IDs** from an external JSON file.  
- **Retrieve blocked IAM roles** from a CSV file.  
- **Get exception lists** from DynamoDB.  

---

### **🔹 How `value_from` Works**
- The `url` field specifies **where** to retrieve the data from.  
- The `format` field defines **the data type** (`json`, `csv`, `txt`).  
- The `expr` field applies a **JMESPath expression** to extract values.  
- Optional **headers** can be included for authentication.  

---

### **🔹 Supported Data Sources**
| **Source Type**  | **Description** |
|-----------------|----------------|
| `json`         | Fetch structured JSON data from S3, HTTP, etc. |
| `csv`          | Read values from CSV files. |
| `csv2dict`     | Convert CSV files into **dictionaries** (key-value pairs). |
| `txt`          | Use **line-delimited** text values. |
| `dynamodb`     | Query DynamoDB using **CQL-like syntax**. |

---

### **🔹 Example: Fetch Values from JSON in S3**  
Retrieve **allowed `AppId` values** from an external JSON file stored in S3.

```yaml
filters:
  - type: value
    key: AppId
    op: in
    value_from:
       url: s3://bucket/xyz/foo.json
       expr: [].AppId
```
✔ **Matches resources if their `AppId` exists in the JSON file.**  

---

### **🔹 Example: Fetching Allowed AMI IDs from JSON (HTTP URL)**
```yaml
filters:
  - type: value
    key: ImageId
    op: in
    value_from:
       url: http://foobar.com/mydata
       format: json
       expr: Region."us-east-1"[].ImageId
       headers:
          authorization: my-token
```
✔ **Matches EC2 instances if their `ImageId` exists in the HTTP JSON response.**  

---

### **🔹 Example: Fetching Security Group IDs from a CSV File**
```yaml
filters:
  - type: value
    key: SecurityGroups[].GroupId
    op: in
    value_from:
       url: s3://bucket/abc/foo.csv
       format: csv2dict
       expr: key[1]
```
✔ **Matches EC2 instances with security group IDs from a CSV file stored in S3.**  

---

### **🔹 Example: Using DynamoDB as an Exception List**
```yaml
filters:
  - type: value
    key: resource_id
    op: not-in
    value_from:
       url: dynamodb
       query: |
         select resource_id from exceptions
         where account_id = '{account_id}' and policy = '{policy.name}'
       expr: [].resource_id
```
✔ **Matches resources that are NOT in the `exceptions` table of DynamoDB.**  

---

### **🔹 What is `value_path`?**  
The `value_path` option in Cloud Custodian allows policies to **compare multiple attributes within the same resource** using **JMESPath queries**. Instead of using a fixed value, `value_path` dynamically **extracts values** from the resource itself.

📌 **Common Use Cases:**  
- Compare **IAM roles and permissions** within the same resource.  
- Identify **resources where two attributes should match**.  
- Filter **security groups with conflicting configurations**.  

---

### **🔹 How `value_path` Works**
- The `value_path` field specifies **a JMESPath query** to extract comparison values from the resource.  
- The `op` field **compares** the extracted values against another resource attribute or fixed value.  
- **Both values must exist within the same resource**.  

---

### **🔹 Example: Find Admins with User Access Roles**
This example checks **GCP IAM policies** to find projects where users **with `roles/admin` also have `roles/user_access`**, ensuring no privilege escalation.

```yaml
policies:
  - name: find-admins-with-user-roles
    resource: gcp.project
    filters:
      - type: iam-policy
        doc:
          key: bindings[?(role=='roles/admin')].members[]
          op: intersect
          value_path: bindings[?(role=='roles/user_access')].members[]
```
✔ **Matches projects where at least one IAM user has both `roles/admin` and `roles/user_access`.**  

---

### **🔹 How `value_path` Helps**
✅ **Avoids hardcoded values** by dynamically pulling data.  
✅ **Works across different attributes** within the same resource.  
✅ **Supports complex filtering** with JMESPath expressions.  
✅ **Improves policy flexibility** for IAM, networking, and compliance checks.  

---

### **🔹 What is the `list-item` Filter?**  
The `list-item` filter in Cloud Custodian allows **evaluating resource properties that contain lists**. This filter is useful when dealing with attributes that **store multiple values**, such as container definitions in ECS, security group rules, or lifecycle policies in S3.

📌 **Common Use Cases:**  
- Detect **ECS task definitions** using unauthorized container images.  
- Check **S3 lifecycle rules** to ensure proper cleanup configurations.  
- Validate **IAM policies** that contain multiple permission statements.  

---

### **🔹 Why Use `list-item` Instead of `value`?**  
✅ **Operates on lists directly**, allowing per-item checks.  
✅ **Supports nested filtering**, applying multiple conditions on list elements.  
✅ **Works with `not`, `regex`, and other operators** for complex evaluations.  

---

### **🔹 Example 1: Find ECS Task Definitions Using External Images**
AWS **ECS Task Definitions** include a list of **container definitions**, each with an associated **image**. This policy **identifies task definitions using container images that are not from the organization’s AWS ECR registry**.

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
✔ **Matches task definitions where at least one container uses an external image.**  
✔ **Uses `regex` to check if the image is from AWS ECR for the given account and region.**  

---

### **🔹 Example 2: Find S3 Buckets Missing Multipart Upload Cleanup Rules**
S3 **lifecycle policies** include multiple **rules**. This policy ensures that **S3 buckets have a rule to clean up incomplete multipart uploads**.

```yaml
policies:
  - name: s3-mpu-cleanup-not-configured
    resource: aws.s3
    filters:
      - not:
          - type: list-item
            key: Lifecycle.Rules[]
            attrs:
              - Status: Enabled
              - AbortIncompleteMultipartUpload.DaysAfterInitiation: not-null
```
✔ **Matches S3 buckets that do NOT have an active cleanup rule for multipart uploads.**  
✔ **Ensures the rule is `Enabled` and contains `DaysAfterInitiation`.**  

---



### **🔹 What is the `event` Filter?**  
The `event` filter in Cloud Custodian allows **filtering resources based on CloudWatch event data**, rather than resource attributes from a describe API call. This enables real-time enforcement of policies based on **CloudTrail events**.

📌 **Common Use Cases:**  
- Detect **EC2 instances launching with public IPs** and terminate them.  
- Identify **S3 buckets created without encryption enabled**.  
- Monitor **IAM role changes** and ensure compliance.  

---

### **🔹 How `event` Works**
- The `mode` must be set to **`cloudtrail`** to trigger the policy based on AWS CloudTrail events.  
- The `key` is a **JMESPath query** to extract event details.  
- The `op` field specifies **how the extracted value is compared**.  
- The `value` field defines the **expected value**.  

---

### **🔹 Example: Auto-Terminate EC2 Instances with Public IPs**
This policy **monitors EC2 instance launches (`RunInstances` event)** and terminates instances that **request a public IP**.

```yaml
policies:
  - name: no-ec2-public-ips
    resource: aws.ec2
    mode:
      type: cloudtrail
      events:
        - RunInstances
    filters:
      - type: event
        # Extract network interface details from the CloudTrail event JSON
        key: "detail.requestParameters.networkInterfaceSet.items[].associatePublicIpAddress"
        op: contains
        value: true
    actions:
      - type: terminate
        force: true
```
✔ **Monitors EC2 launch events and terminates instances with public IPs.**  
✔ **Uses `op: contains` to check if any network interface requests a public IP.**  

---

### **🔹 How `event` Differs from `value` Filter**
| **Feature** | **`event` Filter** | **`value` Filter** |
|------------|----------------|----------------|
| **Source of Data** | CloudWatch Event (CloudTrail logs) | AWS Describe API (Live resource state) |
| **Use Case** | Real-time event-based filtering | Attribute-based filtering |
| **Example** | Monitor instance launches | Filter running instances |

---

### **🔹 What is the `reduce` Filter?**  
The `reduce` filter in Cloud Custodian **groups, sorts, and limits** resources before applying actions. This allows **batch processing, random selection, and prioritization** of resources based on defined criteria.

📌 **Common Use Cases:**  
- **Select and terminate EC2 instances** for **chaos engineering**, ensuring no more than **one instance per ASG** is affected.  
- **Limit AMI deletions** to **only the 10 oldest images**.  
- **Sort resources by expiration date** before **deregistering AMIs**.  

---

### **🔹 How the `reduce` Filter Works**
1. **Group Resources** → Resources are categorized based on a key (`group-by`).  
2. **Sort Within Groups** → Sorting is applied using `sort-by` and `order`.  
3. **Discard Unwanted Items** → Remove initial elements using `discard` or `discard-percent`.  
4. **Limit the Selection** → Restrict the number of resources using `limit` or `limit-percent`.  
5. **Combine Groups** → Sorted groups are merged back into a single resource list.

---

### **🔹 Step 1: Grouping Resources (`group-by`)**  
Resources are grouped based on the value extracted using `group-by`.  
- If `group-by` is **not specified**, all resources are placed in a single group.  
- If a resource **does not have the `group-by` key**, it is placed in its own group.

---

### **🔹 Step 2: Sorting Resources (`sort-by` and `order`)**  
Sorting determines how resources **within each group** are ordered.  

📌 **Sorting Attributes**  
| **Attribute** | **Description** |
|--------------|----------------|
| `sort-by`    | JMESPath expression used to sort resources. |
| `order`      | Sorting order: `asc` (default), `desc`, `reverse`, `randomize`. |
| `null-order` | Sorts `null` values: `last` (default) or `first`. |

📌 **Example Sorting by Launch Time (Ascending Order)**  
```yaml
filters:
  - type: reduce
    group-by: "tag:aws:autoscaling:groupName"
    sort-by: "LaunchTime"
    order: asc
    limit: 1
```
✔ **Finds the **longest-running** EC2 instance per ASG.**  

---

### **🔹 Step 3: Discarding Resources (`discard`, `discard-percent`)**  
Resources can be **filtered out before applying limits**.

📌 **Example: Discard 20% of the Oldest Resources**  
```yaml
filters:
  - type: reduce
    sort-by: "CreationDate"
    order: asc
    discard-percent: 20
```
✔ **Removes the oldest 20% of resources before applying limits.**  

---

### **🔹 Step 4: Limiting Resources (`limit`, `limit-percent`)**  
After discarding, the **remaining resources** can be **restricted further**.

📌 **Example: Keep the Oldest 10 Resources**  
```yaml
filters:
  - type: reduce
    sort-by: "CreationDate"
    order: asc
    limit: 10
```
✔ **Selects the 10 oldest resources after sorting.**  

---

### **🔹 Step 5: Combining Groups**  
Once groups are processed, they are merged back into a single resource list.

📌 **Example: Merge Sorted Groups and Apply Global Limit**  
```yaml
filters:
  - type: reduce
    sort-by: "tag:expire-after"
    value_type: date
    order: asc
    limit: 10
```
✔ **Ensures only 10 resources with the closest expiration dates are selected.**  

---

## **🔹 Examples of `reduce` in Action**

### ✅ **Example 1: Chaos Engineering on EC2 Instances**
- **Select the longest-running EC2 instance per ASG.**  
- **Randomly choose 10% of these instances (max 15).**  
- **Terminate the selected instances.**

```yaml
policies:
  - name: chaos-engineering
    resource: aws.ec2
    filters:
      - "State.Name": "running"
      - "tag:aws:autoscaling:groupName": present
      - type: reduce
        group-by: "tag:aws:autoscaling:groupName"
        sort-by: "LaunchTime"
        order: asc
        limit: 1
      - type: reduce
        order: randomize
        limit: 15
        limit-percent: 10
    actions:
      - terminate
```
✔ **Prevents disrupting multiple instances from the same ASG.**  

---

### ✅ **Example 2: Limit AMI Deletions to 10 Oldest Images**
- **Find AMIs older than 180 days.**  
- **Sort by `CreationDate`.**  
- **Delete only the 10 oldest AMIs.**

```yaml
policies:
  - name: limited-ami-expiration
    resource: aws.ami
    filters:
      - type: image-age
        days: 180
        op: ge
      - type: reduce
        sort-by: "CreationDate"
        order: asc
        limit: 10
    actions:
      - deregister
```
✔ **Ensures controlled deletion instead of removing all old AMIs at once.**  

---

### ✅ **Example 3: Sort AMIs by Expiration Date Before Deregistering**
- **Sort AMIs based on `expire-after` tag.**  
- **Ensure date format is standardized.**  
- **Keep only the top 10 for processing.**

```yaml
policies:
  - name: ami-expiration-by-expire-date
    resource: aws.ami
    filters:
      - type: value
        key: "tag:expire-after"
        value_type: age
        op: gt
        value: 0
      - type: reduce
        sort-by:
          key: "tag:expire-after"
          value_type: date
        order: asc
        limit: 10
    actions:
      - deregister
```
✔ **Handles date formats correctly and ensures the oldest AMIs are deregistered first.**  

---

