---
Title: Aws.Account
Category: Cloud Custodian
Last Updated: 2025-03-21
Version: 1.0
---

# AWS Resources Covered
- [aws.account](#aws-account)

## Table of Contents
- [AWS.ACCOUNT](#aws-account)

## AWS.ACCOUNT

### Available Actions
- [enable-cloudtrail](#action-enable-cloudtrail)
- [enable-data-events](#action-enable-data-events)
- [invoke-lambda](#action-invoke-lambda)
- [invoke-sfn](#action-invoke-sfn)
- [notify](#action-notify)
- [post-finding](#action-post-finding)
- [post-item](#action-post-item)
- [put-metric](#action-put-metric)
- [request-limit-increase](#action-request-limit-increase)
- [set-bedrock-model-invocation-logging](#action-set-bedrock-model-invocation-logging)
- [set-ebs-encryption](#action-set-ebs-encryption)
- [set-ec2-metadata-defaults](#action-set-ec2-metadata-defaults)
- [set-emr-block-public-access](#action-set-emr-block-public-access)
- [set-password-policy](#action-set-password-policy)
- [set-s3-public-block](#action-set-s3-public-block)
- [set-shield-advanced](#action-set-shield-advanced)
- [set-xray-encrypt](#action-set-xray-encrypt)
- [toggle-config-managed-rule](#action-toggle-config-managed-rule)
- [webhook](#action-webhook)

### Available Filters
- [access-analyzer](#filter-access-analyzer)
- [bedrock-model-invocation-logging](#filter-bedrock-model-invocation-logging)
- [check-cloudtrail](#filter-check-cloudtrail)
- [check-config](#filter-check-config)
- [check-macie](#filter-check-macie)
- [config-compliance](#filter-config-compliance)
- [credential](#filter-credential)
- [default-ebs-encryption](#filter-default-ebs-encryption)
- [ec2-metadata-defaults](#filter-ec2-metadata-defaults)
- [emr-block-public-access](#filter-emr-block-public-access)
- [event](#filter-event)
- [finding](#filter-finding)
- [glue-security-config](#filter-glue-security-config)
- [guard-duty](#filter-guard-duty)
- [has-virtual-mfa](#filter-has-virtual-mfa)
- [iam-summary](#filter-iam-summary)
- [lakeformation-s3-cross-account](#filter-lakeformation-s3-cross-account)
- [list-item](#filter-list-item)
- [missing](#filter-missing)
- [ops-item](#filter-ops-item)
- [organization](#filter-organization)
- [password-policy](#filter-password-policy)
- [reduce](#filter-reduce)
- [s3-public-block](#filter-s3-public-block)
- [securityhub](#filter-securityhub)
- [service-limit](#filter-service-limit)
- [ses-agg-send-stats](#filter-ses-agg-send-stats)
- [ses-send-stats](#filter-ses-send-stats)
- [shield-enabled](#filter-shield-enabled)
- [value](#filter-value)
- [xray-encrypt-key](#filter-xray-encrypt-key)

### Action Details

### Action: enable-cloudtrail
<a name="action-enable-cloudtrail"></a>
📌 **Description:**

----

Enables logging on the trail(s) named in the policy

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: trail-test
    description: Ensure CloudTrail logging is enabled
    resource: account
    actions:
      - type: enable-cloudtrail
        trail: mytrail
        bucket: trails
```

📌 **Schema:**

```yaml
------

properties:
bucket:
type: string
bucket-region:
type: string
file-digest:
type: boolean
global-events:
type: boolean
kms:
type: boolean
kms-key:
type: string
multi-region:
type: boolean
notify:
type: string
trail:
type: string
type:
enum:
- enable-cloudtrail
required:
- bucket
```

### Action: enable-data-events
<a name="action-enable-data-events"></a>
📌 **Description:**

----

Ensure all buckets in account are setup to log data events.

Note this works via a single trail for data events per
https://aws.amazon.com/about-aws/whats-new/2017/09/aws-cloudtrail-enables-option-to-add-all-amazon-s3-buckets-to-data-events/

This trail should NOT be used for api management events, the
configuration here is soley for data events. If directed to create
a trail this will do so without management events.

📌 **Example Usage:**

```yaml
policies:
      - name: s3-enable-data-events-logging
        resource: account
        actions:
         - type: enable-data-events
           data-trail:
             name: s3-events
             multi-region: us-east-1
```

📌 **Schema:**

```yaml
------

properties:
data-trail:
additionalProperties: false
properties:
create:
title: Should we create trail if needed for events?
type: boolean
key-id:
title: If creating, Enable kms on the trail
type: string
multi-region:
title: If creating, use this region for all data trails
type: string
name:
title: The name of the event trail
type: string
s3-bucket:
title: If creating, the bucket to store trail event data
type: string
s3-prefix:
type: string
topic:
title: If creating, the sns topic for the trail to send updates
type: string
type:
enum:
- ReadOnly
- WriteOnly
- All
required:
- name
type: object
type:
enum:
- enable-data-events
required:
- data-trail
- type
```

### Action: invoke-lambda
<a name="action-invoke-lambda"></a>
📌 **Description:**

----

Invoke an arbitrary lambda

serialized invocation parameters

 - resources / collection of resources
 - policy / policy that is invoke the lambda
 - action / action that is invoking the lambda
 - event / cloud trail event if any
 - version / version of custodian invoking the lambda

We automatically batch into sets of 250 for invocation,
We try to utilize async invocation by default, this imposes
some greater size limits of 128kb which means we batch
invoke.

Example::

 - type: invoke-lambda
   function: my-function
   assume-role: iam-role-arn

Note, if you're synchronously invoking the lambda, you may also need
to configure the timeout to avoid multiple invocations. The default
timeout is 90s. If the lambda doesn't respond within that time, the boto
sdk will invoke the lambda again with the same
arguments. Alternatively, use `async: true`

📌 **Example Usage:**

```yaml
actions:
  - type: invoke-lambda
```

📌 **Schema:**

```yaml
------

properties:
assume-role:
type: string
async:
type: boolean
batch_size:
type: integer
function:
type: string
qualifier:
type: string
region:
type: string
timeout:
type: integer
type:
enum:
- invoke-lambda
vars:
type: object
required:
- type
- function
```

### Action: invoke-sfn
<a name="action-invoke-sfn"></a>
📌 **Description:**

----

Invoke step function on resources.

By default this will invoke a step function for each resource
providing both the `policy` and `resource` as input.

That behavior can be configured setting policy and bulk
boolean flags on the action.

If bulk action parameter is set to true, then the step
function will be invoked in bulk, with a set of resource arns
under the `resources` key.

The size of the batch can be configured via the batch-size
parameter. Note step function state (input, execution, etc)must
fit within 32k, we default to batch size 250.

📌 **Example Usage:**

```yaml
policies:
 - name: invoke-step-function
   resource: s3
   filters:
     - is-log-target
     - "tag:IngestSetup": absent
   actions:
     - type: invoke-sfn
       # This will cause the workflow to be invoked
       # with many resources arns in a single execution.
       # Note this is *not* the default.
       bulk: true
       batch-size: 10
       state-machine: LogIngestSetup
```

📌 **Schema:**

```yaml
------

properties:
batch-size:
type: integer
bulk:
type: boolean
policy:
type: boolean
state-machine:
type: string
type:
enum:
- invoke-sfn
required:
- state-machine
- type
```

### Action: notify
<a name="action-notify"></a>
📌 **Description:**

----

Flexible notifications require quite a bit of implementation support
on pluggable transports, templates, address resolution, variable
extraction, batch periods, etc.

For expedience and flexibility then, we instead send the data to
an sqs queue, for processing.

.. note::

   The ``notify`` action does not produce complete, human-readable messages
   on its own. Instead, the `c7n-mailer`_ tool renders and delivers
   messages by combining ``notify`` output with formatted templates.

   .. _c7n-mailer: ../../tools/c7n-mailer.html

Attaching additional string message attributes are supported on the SNS
transport, with the exception of the ``mtype`` attribute, which is a
reserved attribute used by Cloud Custodian.

📌 **Example Usage:**

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
             # which template for the email should we use
             template: policy-template
             transport:
               type: sqs
               region: us-east-1
               queue: xyz
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
             # which template for the email should we use
             template: policy-template
             transport:
               type: sns
               region: us-east-1
               topic: your-notify-topic
               attributes:
                  attribute_key: attribute_value
                  attribute_key_2: attribute_value_2
```

📌 **Schema:**

```yaml
------

anyOf:
- required:
- type
- transport
- to
- required:
- type
- transport
- to_from
properties:
assume_role:
type: boolean
cc:
items:
type: string
type: array
cc_from:
additionalProperties: 'False'
properties:
expr:
oneOf:
- type: integer
- type: string
format:
enum:
- csv
- json
- txt
- csv2dict
headers:
patternProperties:
'':
type: string
type: object
query:
type: string
url:
type: string
required:
- url
type: object
cc_manager:
type: boolean
from:
type: string
owner_absent_contact:
items:
type: string
type: array
subject:
type: string
template:
type: string
to:
items:
type: string
type: array
to_from:
additionalProperties: 'False'
properties:
expr:
oneOf:
- type: integer
- type: string
format:
enum:
- csv
- json
- txt
- csv2dict
headers:
patternProperties:
'':
type: string
type: object
query:
type: string
url:
type: string
required:
- url
type: object
transport:
oneOf:
- properties:
queue:
type: string
type:
enum:
- sqs
required:
- type
- queue
type: object
- properties:
attributes:
type: object
topic:
type: string
type:
enum:
- sns
required:
- type
- topic
type: object
type:
enum:
- notify
```

### Action: post-finding
<a name="action-post-finding"></a>
📌 **Description:**

----

Report a finding to AWS Security Hub.

Custodian acts as a finding provider, allowing users to craft
policies that report to the AWS SecurityHub in the AWS Security Finding Format documented at
https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-findings-format.html

For resources that are taggable, we will tag the resource with an identifier
such that further findings generate updates. The name of the tag comes from the ``title``
parameter of the ``post-finding`` action, or the policy name if ``title`` is empty. This
allows different policies to update the same finding if they specify the same ``title``.

Example generate a finding for accounts that don't have shield enabled.

Note with Cloud Custodian (0.9+) you need to enable the Custodian integration
to post-findings, see Getting Started with :ref:`Security Hub <aws-securityhub>`.

📌 **Example Usage:**

```yaml
policies:
```

<!-- - name: account-shield-enabled
 resource: account
 filters:
   - shield-enabled
 actions:
   - type: post-finding
     description: |
        Shield should be enabled on account to allow for DDOS protection (1 time 3k USD Charge).
     severity_label: LOW
     types:
       - "Software and Configuration Checks/Industry and Regulatory Standards/NIST CSF Controls (USA)"
     recommendation: "Enable shield"
     recommendation_url: "https://www.example.com/policies/AntiDDoS.html"
     title: "shield-enabled"
     confidence: 100
     compliance_status: FAILED -->

📌 **Schema:**

```yaml
------

properties:
batch_size:
default: 1
maximum: 100
minimum: 1
type: integer
compliance_status:
enum:
- PASSED
- WARNING
- FAILED
- NOT_AVAILABLE
type: string
confidence:
max: 100
min: 0
type: number
criticality:
max: 100
min: 0
type: number
description:
default: policy.description, or if not defined in policy then policy.name
type: string
fields:
type: object
recommendation:
type: string
recommendation_url:
type: string
record_state:
default: ACTIVE
enum:
- ACTIVE
- ARCHIVED
type: string
region:
description: cross-region aggregation target
type: string
severity:
default: 0
type: number
severity_label:
default: INFORMATIONAL
enum:
- INFORMATIONAL
- LOW
- MEDIUM
- HIGH
- CRITICAL
type: string
severity_normalized:
default: 0
max: 100
min: 0
type: number
title:
default: policy.name
type: string
type:
enum:
- post-finding
types:
items:
type: string
minItems: 1
type: array
required:
- types
- type
```

### Action: post-item
<a name="action-post-item"></a>
📌 **Description:**

----

Post an OpsItem to AWS Systems Manager OpsCenter Dashboard.

https://docs.aws.amazon.com/systems-manager/latest/userguide/OpsCenter.html

Each ops item supports up to a 100 associated resources. This
action supports the builtin OpsCenter dedup logic with additional
support for associating new resources to existing Open ops items.

: Example :

Create an ops item for ec2 instances with Create User permissions

📌 **Example Usage:**

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

<!-- The builtin OpsCenter dedup logic will kick in if the same
resource set (ec2 instances in this case) is posted for the same
policy. -->

<!-- : Example : -->

<!-- Create an ops item for sqs queues with cross account access as ops items. -->

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

📌 **Schema:**

```yaml
------

properties:
description:
type: string
priority:
enum:
- 1
- 2
- 3
- 4
- 5
tags:
type: object
title:
type: string
topics:
type: string
type:
enum:
- post-item
required:
- type
```

### Action: put-metric
<a name="action-put-metric"></a>
📌 **Description:**

----

Action to put metrics based on an expression into CloudWatch metrics

📌 **Example Usage:**

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

<!-- op and units are optional and will default to simple Counts. -->

📌 **Schema:**

```yaml
------

properties:
dimensions:
items:
type: object
type: array
key:
type: string
metric_name:
type: string
namespace:
type: string
op:
enum:
- count
- distinct_count
- sum
- average
type:
enum:
- put-metric
units:
enum:
- Seconds
- Microseconds
- Milliseconds
- Bytes
- Kilobytes
- Megabytes
- Gigabytes
- Terabytes
- Bits
- Kilobits
- Megabits
- Gigabits
- Terabits
- Bytes/Second
- Kilobytes/Second
- Megabytes/Second
- Gigabytes/Second
- Terabytes/Second
- Bits/Second
- Kilobits/Second
- Megabits/Second
- Gigabits/Second
- Terabits/Second
- Count/Second
- Percent
- Count
- None
required:
- type
- key
- namespace
- metric_name
```

### Action: request-limit-increase
<a name="action-request-limit-increase"></a>
📌 **Description:**

----

File support ticket to raise limit.

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: raise-account-service-limits
    resource: account
    filters:
      - type: service-limit
        services:
          - EBS
        limits:
          - Provisioned IOPS (SSD) storage (GiB)
        threshold: 60.5
    actions:
      - type: request-limit-increase
        notify: [email, email2]
        ## You can use one of either percent-increase or an amount-increase.
        percent-increase: 50
        message: "Please raise the below account limit(s); \n {limits}"
```

📌 **Schema:**

```yaml
------

oneOf:
- required:
- type
- percent-increase
- required:
- type
- amount-increase
properties:
amount-increase:
minimum: 1
type: number
message:
type: string
minimum-increase:
minimum: 1
type: number
notify:
items:
type: string
type: array
percent-increase:
minimum: 1
type: number
severity:
enum:
- urgent
- high
- normal
- low
type: string
subject:
type: string
type:
enum:
- request-limit-increase
```

### Action: set-bedrock-model-invocation-logging
<a name="action-set-bedrock-model-invocation-logging"></a>
📌 **Description:**

----

Set Bedrock Model Invocation Logging Configuration on an account.
 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/put_model_invocation_logging_configuration.html

 To delete a configuration, supply enabled to False

📌 **Example Usage:**

```yaml
policies:
      - name: set-bedrock-model-invocation-logging
        resource: account
        actions:
          - type: set-bedrock-model-invocation-logging
            enabled: True
            loggingConfig:
              textDataDeliveryEnabled: True
              s3Config:
                bucketName: test-bedrock-1
                keyPrefix:  logging/
```

<!-- - name: delete-bedrock-model-invocation-logging
        resource: account
        actions:
          - type: set-bedrock-model-invocation-logging
            enabled: False -->

📌 **Schema:**

```yaml
------

properties:
enabled:
type: boolean
loggingConfig:
type: object
type:
enum:
- set-bedrock-model-invocation-logging
```

### Action: set-ebs-encryption
<a name="action-set-ebs-encryption"></a>
📌 **Description:**

----

Set AWS EBS default encryption on an account

📌 **Example Usage:**

```yaml
policies:
 - name: set-default-ebs-encryption
   resource: aws.account
   filters:
    - type: default-ebs-encryption
      state: false
   actions:
    - type: set-ebs-encryption
      state: true
      key: alias/aws/ebs
```

📌 **Schema:**

```yaml
------

properties:
key:
type: string
state:
type: boolean
type:
enum:
- set-ebs-encryption
required:
- type
```

### Action: set-ec2-metadata-defaults
<a name="action-set-ec2-metadata-defaults"></a>
📌 **Description:**

----

Modifies the default instance metadata service (IMDS) settings at the account level.

📌 **Example Usage:**

```yaml
policies:
      - name: set-ec2-metadata-defaults
        resource: account
        filters:
          - or:
            - type: ec2-metadata-defaults
              key: HttpTokens
              op: eq
              value: optional
            - type: ec2-metadata-defaults
              key: HttpTokens
              value: absent
        actions:
          - type: set-ec2-metadata-defaults
            HttpTokens: required
```

📌 **Schema:**

```yaml
------

properties:
HttpEndpoint:
enum:
- enabled
- disabled
- no-preference
HttpPutResponseHopLimit:
type: integer
HttpTokens:
enum:
- optional
- required
- no-preference
InstanceMetadataTags:
enum:
- enabled
- disabled
- no-preference
type:
enum:
- set-ec2-metadata-defaults
required:
- type
```

### Action: set-emr-block-public-access
<a name="action-set-emr-block-public-access"></a>
📌 **Description:**

----

Action to put/update the EMR block public access configuration for your
   AWS account in the current region

📌 **Example Usage:**

```yaml
policies:
      - name: set-emr-block-public-access
        resource: account
        filters:
          - type: emr-block-public-access
            key: BlockPublicAccessConfiguration.BlockPublicSecurityGroupRules
            value: False
        actions:
          - type: set-emr-block-public-access
            config:
                BlockPublicSecurityGroupRules: True
                PermittedPublicSecurityGroupRuleRanges:
                    - MinRange: 22
                      MaxRange: 22
                    - MinRange: 23
                      MaxRange: 23
```

📌 **Schema:**

```yaml
------

properties:
config:
properties:
BlockPublicSecurityGroupRules:
type: boolean
PermittedPublicSecurityGroupRuleRanges:
items:
properties:
MaxRange:
minimum: 0
type: number
MinRange:
minimum: 0
type: number
required:
- MinRange
type: object
type: array
required:
- BlockPublicSecurityGroupRules
type: object
type:
enum:
- set-emr-block-public-access
required:
- config
```

### Action: set-password-policy
<a name="action-set-password-policy"></a>
📌 **Description:**

----

Set an account's password policy.

This only changes the policy for the items provided.
If this is the first time setting a password policy and an item is not provided it will be
set to the defaults defined in the boto docs for IAM.Client.update_account_password_policy

📌 **Example Usage:**

```yaml
policies:
      - name: set-account-password-policy
        resource: account
        filters:
          - not:
            - type: password-policy
              key: MinimumPasswordLength
              value: 10
              op: ge
        actions:
            - type: set-password-policy
              policy:
                MinimumPasswordLength: 20
```

📌 **Schema:**

```yaml
------

properties:
policy:
type: object
type:
enum:
- set-password-policy
required:
- type
```

### Action: set-s3-public-block
<a name="action-set-s3-public-block"></a>
📌 **Description:**

----

Configure S3 Public Access Block on an account.

All public access block attributes can be set. If not specified they are merged
with the extant configuration.

https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html

📌 **Example Usage:**

<!-- .. yaml: -->

```yaml
policies:
- name: restrict-public-buckets
  resource: aws.account
  filters:
    - not:
       - type: s3-public-block
         key: RestrictPublicBuckets
         value: true
  actions:
    - type: set-s3-public-block
      RestrictPublicBuckets: true
```

📌 **Schema:**

```yaml
------

properties:
BlockPublicAcls:
type: boolean
BlockPublicPolicy:
type: boolean
IgnorePublicAcls:
type: boolean
RestrictPublicBuckets:
type: boolean
state:
default: true
type: boolean
type:
enum:
- set-s3-public-block
required:
- type
```

### Action: set-shield-advanced
<a name="action-set-shield-advanced"></a>
📌 **Description:**

----

Enable/disable Shield Advanced on an account.

📌 **Example Usage:**

```yaml
actions:
  - type: set-shield-advanced
```

📌 **Schema:**

```yaml
------

properties:
state:
type: boolean
type:
enum:
- set-shield-advanced
required:
- type
```

### Action: set-xray-encrypt
<a name="action-set-xray-encrypt"></a>
📌 **Description:**

----

Enable specific xray encryption.

📌 **Example Usage:**

```yaml
policies:
      - name: xray-default-encrypt
        resource: aws.account
        actions:
          - type: set-xray-encrypt
            key: default
      - name: xray-kms-encrypt
        resource: aws.account
        actions:
          - type: set-xray-encrypt
            key: alias/some/alias/key
```

📌 **Schema:**

```yaml
------

properties:
key:
type: string
type:
enum:
- set-xray-encrypt
required:
- key
- type
```

### Action: toggle-config-managed-rule
<a name="action-toggle-config-managed-rule"></a>
📌 **Description:**

----

Enables or disables an AWS Config Managed Rule

📌 **Example Usage:**

```yaml
policies:
  - name: config-managed-s3-bucket-public-write-remediate-event
    description: |
      This policy detects if S3 bucket allows public write by the bucket policy
      or ACL and remediates.
    comment: |
      This policy detects if S3 bucket policy or ACL allows public write access.
      When the bucket is evaluated as 'NON_COMPLIANT', the action
      'AWS-DisableS3BucketPublicReadWrite' is triggered and remediates.
    resource: account
    filters:
      - type: missing
        policy:
          resource: config-rule
          filters:
            - type: remediation
              rule_name: &rule_name 'config-managed-s3-bucket-public-write-remediate-event'
              remediation: &remediation-config
                TargetId: AWS-DisableS3BucketPublicReadWrite
                Automatic: true
                MaximumAutomaticAttempts: 5
                RetryAttemptSeconds: 211
                Parameters:
                  AutomationAssumeRole:
                    StaticValue:
                      Values:
                        - 'arn:aws:iam::{account_id}:role/myrole'
                  S3BucketName:
                    ResourceValue:
                      Value: RESOURCE_ID
    actions:
      - type: toggle-config-managed-rule
        rule_name: *rule_name
        managed_rule_id: S3_BUCKET_PUBLIC_WRITE_PROHIBITED
        resource_types:
          - 'AWS::S3::Bucket'
        rule_parameters: '{}'
        remediation: *remediation-config
```

📌 **Schema:**

```yaml
------

properties:
enabled:
default: true
type: boolean
managed_rule_id:
type: string
remediation:
properties:
Automatic:
type: boolean
ExecutionControls:
type: object
MaximumAutomaticAttempts:
maximum: 25
minimum: 1
type: integer
Parameters:
type: object
RetryAttemptSeconds:
maximum: 2678000
minimum: 1
type: integer
TargetId:
type: string
TargetType:
type: string
type: object
resource_id:
type: string
resource_tag:
properties:
key:
type: string
value:
type: string
required:
- key
- value
type: object
resource_types:
items:
pattern: ^AWS::*
type: string
type: array
rule_name:
type: string
rule_parameters:
type: string
rule_prefix:
type: string
tags:
type: object
type:
enum:
- toggle-config-managed-rule
required:
- rule_name
- type
```

### Action: webhook
<a name="action-webhook"></a>
📌 **Description:**

----

Calls a webhook with optional parameters and body
populated from JMESPath queries.

📌 **Example Usage:**

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

📌 **Schema:**

```yaml
------

properties:
batch:
type: boolean
batch-size:
type: number
body:
type: string
headers:
additionalProperties:
description: header values
type: string
type: object
method:
enum:
- PUT
- POST
- GET
- PATCH
- DELETE
type: string
query-params:
additionalProperties:
description: query string values
type: string
type: object
type:
enum:
- webhook
url:
type: string
required:
- url
- type
```

### Filter Details

### Filter: access-analyzer
<a name="filter-access-analyzer"></a>
📌 **Description:**

----

Check for access analyzers in an account

📌 **Example Usage:**

```yaml
policies:
- name: account-access-analyzer
  resource: account
  filters:
    - type: access-analyzer
      key: 'status'
      value: ACTIVE
      op: eq
```

📌 **Schema:**

```yaml
------

properties:
default:
type: object
key:
type: string
op:
enum:
- eq
- equal
- ne
- not-equal
- gt
- greater-than
- ge
- gte
- le
- lte
- lt
- less-than
- glob
- regex
- regex-case
- in
- ni
- not-in
- contains
- difference
- intersect
- mod
type:
enum:
- access-analyzer
value:
oneOf:
- type: array
- type: string
- type: boolean
- type: number
- type: 'null'
value_from:
additionalProperties: 'False'
properties:
expr:
oneOf:
- type: integer
- type: string
format:
enum:
- csv
- json
- txt
- csv2dict
headers:
patternProperties:
'':
type: string
type: object
query:
type: string
url:
type: string
required:
- url
type: object
value_path:
type: string
value_regex:
type: string
value_type:
enum:
- age
- integer
- expiration
- normalize
- size
- cidr
- cidr_size
- swap
- resource_count
- expr
- unique_size
- date
- version
- float
required:
- type
```

### Filter: bedrock-model-invocation-logging
<a name="filter-bedrock-model-invocation-logging"></a>
📌 **Description:**

----

Filter for account to look at bedrock model invocation logging configuration

The schema to supply to the attrs follows the schema here:
 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_model_invocation_logging_configuration.html

📌 **Example Usage:**

```yaml
policies:
      - name: bedrock-model-invocation-logging-configuration
        resource: account
        filters:
          - type: bedrock-model-invocation-logging
            attrs:
              - imageDataDeliveryEnabled: True
```

📌 **Schema:**

```yaml
------

properties:
attrs:
items:
anyOf:
- $ref: '#/definitions/filters/value'
- $ref: '#/definitions/filters/valuekv'
- additional_properties: false
properties:
and:
items:
anyOf:
- $ref: '#/definitions/filters/value'
- $ref: '#/definitions/filters/valuekv'
type: array
type: object
- additional_properties: false
properties:
or:
items:
anyOf:
- $ref: '#/definitions/filters/value'
- $ref: '#/definitions/filters/valuekv'
type: array
type: object
- additional_properties: false
properties:
not:
items:
anyOf:
- $ref: '#/definitions/filters/value'
- $ref: '#/definitions/filters/valuekv'
type: array
type: object
type: array
count:
type: number
count_op:
enum:
- eq
- equal
- ne
- not-equal
- gt
- greater-than
- ge
- gte
- le
- lte
- lt
- less-than
- glob
- regex
- regex-case
- in
- ni
- not-in
- contains
- difference
- intersect
- mod
type:
enum:
- bedrock-model-invocation-logging
required:
- type
```

### Filter: check-cloudtrail
<a name="filter-check-cloudtrail"></a>
📌 **Description:**

----

Verify cloud trail enabled for this account per specifications.

Returns an annotated account resource if trail is not enabled.

Of particular note, the current-region option will evaluate whether cloudtrail is available
in the current region, either as a multi region trail or as a trail with it as the home region.

The log-metric-filter-pattern option checks for the existence of a cloudwatch alarm and a
corresponding SNS subscription for a specific filter pattern

📌 **Example Usage:**

```yaml
policies:
      - name: account-cloudtrail-enabled
        resource: account
        region: us-east-1
        filters:
          - type: check-cloudtrail
            global-events: true
            multi-region: true
            running: true
            include-management-events: true
            log-metric-filter-pattern: "{ ($.eventName = \"ConsoleLogin\") }"
```

<!-- Check for CloudWatch log group with a metric filter that has a filter pattern
matching a regex pattern: -->

```yaml
policies:
      - name: account-cloudtrail-with-matching-log-metric-filter
        resource: account
        region: us-east-1
        filters:
          - type: check-cloudtrail
            log-metric-filter-pattern:
                type: value
                op: regex
                value: '\{ ?(\()? ?\$\.eventName ?= ?(")?ConsoleLogin(")? ?(\))? ?\}'
```

📌 **Schema:**

```yaml
------

properties:
current-region:
type: boolean
file-digest:
type: boolean
global-events:
type: boolean
include-management-events:
type: boolean
kms:
type: boolean
kms-key:
type: string
log-metric-filter-pattern:
oneOf:
- $ref: '#/definitions/filters/value'
- type: string
multi-region:
type: boolean
notifies:
type: boolean
running:
type: boolean
type:
enum:
- check-cloudtrail
required:
- type
```

### Filter: check-config
<a name="filter-check-config"></a>
📌 **Description:**

----

Is config service enabled for this account

📌 **Example Usage:**

```yaml
policies:
      - name: account-check-config-services
        resource: account
        region: us-east-1
        filters:
          - type: check-config
            all-resources: true
            global-resources: true
            running: true
```

📌 **Schema:**

```yaml
------

properties:
all-resources:
type: boolean
global-resources:
type: boolean
running:
type: boolean
type:
enum:
- check-config
required:
- type
```

### Filter: check-macie
<a name="filter-check-macie"></a>
📌 **Description:**

----

Check status of macie v2 in the account.

Gets the macie session info for the account, and
the macie master account for the current account if
configured.

📌 **Example Usage:**

```yaml
filters:
  - type: check-macie
```

📌 **Schema:**

```yaml
------

properties:
default:
type: object
key:
type: string
op:
enum:
- eq
- equal
- ne
- not-equal
- gt
- greater-than
- ge
- gte
- le
- lte
- lt
- less-than
- glob
- regex
- regex-case
- in
- ni
- not-in
- contains
- difference
- intersect
- mod
type:
enum:
- check-macie
value:
oneOf:
- type: array
- type: string
- type: boolean
- type: number
- type: 'null'
value_from:
additionalProperties: 'False'
properties:
expr:
oneOf:
- type: integer
- type: string
format:
enum:
- csv
- json
- txt
- csv2dict
headers:
patternProperties:
'':
type: string
type: object
query:
type: string
url:
type: string
required:
- url
type: object
value_path:
type: string
value_regex:
type: string
value_type:
enum:
- age
- integer
- expiration
- normalize
- size
- cidr
- cidr_size
- swap
- resource_count
- expr
- unique_size
- date
- version
- float
required:
- type
```

### Filter: config-compliance
<a name="filter-config-compliance"></a>
📌 **Description:**

----

Filter resources by their compliance with one or more AWS config rules.

An example of using the filter to find all ec2 instances that have
been registered as non compliant in the last 30 days against two
custom AWS Config rules.

📌 **Example Usage:**

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

<!-- Also note, custodian has direct support for deploying policies as config
rules see https://cloudcustodian.io/docs/policy/lambda.html#config-rules -->

📌 **Schema:**

```yaml
------

properties:
eval_filters:
items:
oneOf:
- $ref: '#/definitions/filters/valuekv'
- $ref: '#/definitions/filters/value'
type: array
op:
enum:
- or
- and
rules:
items:
type: string
type: array
states:
items:
enum:
- COMPLIANT
- NON_COMPLIANT
- NOT_APPLICABLE
- INSUFFICIENT_DATA
type: array
type:
enum:
- config-compliance
required:
- rules
```

### Filter: credential
<a name="filter-credential"></a>
📌 **Description:**

----

Use IAM Credential report to filter users.

The IAM Credential report aggregates multiple pieces of
information on iam users. This makes it highly efficient for
querying multiple aspects of a user that would otherwise require
per user api calls.

https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_getting-report.html

For example if we wanted to retrieve all users with mfa who have
never used their password but have active access keys from the
last month

📌 **Example Usage:**

<!-- - name: iam-mfa-active-keys-no-login
   resource: iam-user
   filters:
 - type: credential
   key: mfa_active
   value: true
 - type: credential
   key: password_last_used
   value: absent
 - type: credential
   key: access_keys.last_used_date
   value_type: age
   value: 30
   op: less-than -->

<!-- Credential Report Transforms -->

<!-- We perform some default transformations from the raw
credential report. Sub-objects (access_key_1, cert_2)
are turned into array of dictionaries for matching
purposes with their common prefixes stripped.
N/A values are turned into None, TRUE/FALSE are turned
into boolean values. -->

📌 **Schema:**

```yaml
------

properties:
key:
enum:
- user
- arn
- user_creation_time
- password_enabled
- password_last_used
- password_last_changed
- password_next_rotation
- mfa_active
- access_keys
- access_keys.active
- access_keys.last_used_date
- access_keys.last_used_region
- access_keys.last_used_service
- access_keys.last_rotated
- certs
- certs.active
- certs.last_rotated
title: report key to search
type: string
op:
enum:
- eq
- equal
- ne
- not-equal
- gt
- greater-than
- ge
- gte
- le
- lte
- lt
- less-than
- glob
- regex
- regex-case
- in
- ni
- not-in
- contains
- difference
- intersect
- mod
report_delay:
default: 10
title: Number of seconds to wait for report generation.
type: number
report_generate:
default: true
title: Generate a report if none is present.
type: boolean
report_max_age:
default: 86400
title: Number of seconds to consider a report valid.
type: number
type:
enum:
- credential
value:
oneOf:
- type: array
- type: string
- type: boolean
- type: number
- type: 'null'
value_type:
enum:
- age
- integer
- expiration
- normalize
- size
- cidr
- cidr_size
- swap
- resource_count
- expr
- unique_size
- date
- version
- float
required:
- type
```

### Filter: default-ebs-encryption
<a name="filter-default-ebs-encryption"></a>
📌 **Description:**

----

Filter an account by its ebs encryption status.

By default for key we match on the alias name for a key.

📌 **Example Usage:**

```yaml
policies:
 - name: check-default-ebs-encryption
   resource: aws.account
   filters:
    - type: default-ebs-encryption
      key: "alias/aws/ebs"
      state: true
```

<!-- It is also possible to match on specific key attributes (tags, origin) -->

```yaml
policies:
 - name: check-ebs-encryption-key-origin
   resource: aws.account
   filters:
    - type: default-ebs-encryption
      key:
        type: value
        key: Origin
        value: AWS_KMS
      state: true
```

📌 **Schema:**

```yaml
------

properties:
key:
oneOf:
- $ref: '#/definitions/filters/value'
- type: string
state:
type: boolean
type:
enum:
- default-ebs-encryption
required:
- type
```

### Filter: ec2-metadata-defaults
<a name="filter-ec2-metadata-defaults"></a>
📌 **Description:**

----

Filter on the default instance metadata service (IMDS) settings for the specified account and
region.  NOTE: Any configuration that has never been set (or is set to 'No Preference'), will
not be returned in the response.

📌 **Example Usage:**

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

📌 **Schema:**

```yaml
------

properties:
default:
type: object
key:
type: string
op:
enum:
- eq
- equal
- ne
- not-equal
- gt
- greater-than
- ge
- gte
- le
- lte
- lt
- less-than
- glob
- regex
- regex-case
- in
- ni
- not-in
- contains
- difference
- intersect
- mod
type:
enum:
- ec2-metadata-defaults
value:
oneOf:
- type: array
- type: string
- type: boolean
- type: number
- type: 'null'
value_from:
additionalProperties: 'False'
properties:
expr:
oneOf:
- type: integer
- type: string
format:
enum:
- csv
- json
- txt
- csv2dict
headers:
patternProperties:
'':
type: string
type: object
query:
type: string
url:
type: string
required:
- url
type: object
value_path:
type: string
value_regex:
type: string
value_type:
enum:
- age
- integer
- expiration
- normalize
- size
- cidr
- cidr_size
- swap
- resource_count
- expr
- unique_size
- date
- version
- float
required:
- type
```

### Filter: emr-block-public-access
<a name="filter-emr-block-public-access"></a>
📌 **Description:**

----

Check for EMR block public access configuration on an account

📌 **Example Usage:**

```yaml
policies:
      - name: get-emr-block-public-access
        resource: account
        filters:
          - type: emr-block-public-access
```

📌 **Schema:**

```yaml
------

properties:
default:
type: object
key:
type: string
op:
enum:
- eq
- equal
- ne
- not-equal
- gt
- greater-than
- ge
- gte
- le
- lte
- lt
- less-than
- glob
- regex
- regex-case
- in
- ni
- not-in
- contains
- difference
- intersect
- mod
type:
enum:
- emr-block-public-access
value:
oneOf:
- type: array
- type: string
- type: boolean
- type: number
- type: 'null'
value_from:
additionalProperties: 'False'
properties:
expr:
oneOf:
- type: integer
- type: string
format:
enum:
- csv
- json
- txt
- csv2dict
headers:
patternProperties:
'':
type: string
type: object
query:
type: string
url:
type: string
required:
- url
type: object
value_path:
type: string
value_regex:
type: string
value_type:
enum:
- age
- integer
- expiration
- normalize
- size
- cidr
- cidr_size
- swap
- resource_count
- expr
- unique_size
- date
- version
- float
required:
- type
```

### Filter: event
<a name="filter-event"></a>
📌 **Description:**

----

Filter a resource based on an event.

📌 **Example Usage:**

```yaml
filters:
  - type: event
```

📌 **Schema:**

```yaml
------

properties:
default:
type: object
key:
type: string
op:
enum:
- eq
- equal
- ne
- not-equal
- gt
- greater-than
- ge
- gte
- le
- lte
- lt
- less-than
- glob
- regex
- regex-case
- in
- ni
- not-in
- contains
- difference
- intersect
- mod
type:
enum:
- event
value:
oneOf:
- type: array
- type: string
- type: boolean
- type: number
- type: 'null'
value_from:
additionalProperties: 'False'
properties:
expr:
oneOf:
- type: integer
- type: string
format:
enum:
- csv
- json
- txt
- csv2dict
headers:
patternProperties:
'':
type: string
type: object
query:
type: string
url:
type: string
required:
- url
type: object
value_path:
type: string
value_regex:
type: string
value_type:
enum:
- age
- integer
- expiration
- normalize
- size
- cidr
- cidr_size
- swap
- resource_count
- expr
- unique_size
- date
- version
- float
required:
- type
```

### Filter: finding
<a name="filter-finding"></a>
📌 **Description:**

----

Check if there are Security Hub Findings related to the resources

📌 **Example Usage:**

<!-- By default, this filter checks to see if *any* findings exist for a given
resource. -->

```yaml
policies:
  - name: iam-roles-with-findings
    resource: aws.iam-role
    filters:
      - finding
```

<!-- The ``query`` parameter can look for specific findings. Consult this
`reference <https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_AwsSecurityFindingFilters.html>`_
for more information about available filters and their structure. Note that when matching
by finding Id, it can be helpful to combine ``PREFIX`` comparisons with parameterized
account and region information. -->

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

📌 **Schema:**

```yaml
------

properties:
query:
type: object
region:
type: string
type:
enum:
- finding
required:
- type
```

### Filter: glue-security-config
<a name="filter-glue-security-config"></a>
📌 **Description:**

----

Filter aws account by its glue encryption status and KMS key

📌 **Example Usage:**

```yaml
policies:
- name: glue-security-config
  resource: aws.account
  filters:
    - type: glue-security-config
      SseAwsKmsKeyId: alias/aws/glue
```

📌 **Schema:**

```yaml
------

properties:
AwsKmsKeyId:
type: string
CatalogEncryptionMode:
enum:
- DISABLED
- SSE-KMS
ReturnConnectionPasswordEncrypted:
type: boolean
SseAwsKmsKeyId:
type: string
type:
enum:
- glue-security-config
```

### Filter: guard-duty
<a name="filter-guard-duty"></a>
📌 **Description:**

----

Check if the guard duty service is enabled.

This allows looking at account's detector and its associated
master if any.

📌 **Example Usage:**

<!-- Check to ensure guard duty is active on account and associated to a master. -->

```yaml
policies:
      - name: guardduty-enabled
        resource: account
        filters:
          - type: guard-duty
            Detector.Status: ENABLED
            Master.AccountId: "00011001"
            Master.RelationshipStatus: "Enabled"
```

📌 **Schema:**

```yaml
------

patternProperties:
^Detector:
oneOf:
- type: object
- type: string
^Master:
oneOf:
- type: object
- type: string
properties:
match-operator:
enum:
- or
- and
type:
enum:
- guard-duty
```

### Filter: has-virtual-mfa
<a name="filter-has-virtual-mfa"></a>
📌 **Description:**

----

Is the account configured with a virtual MFA device?

📌 **Example Usage:**

```yaml
policies:
        - name: account-with-virtual-mfa
          resource: account
          region: us-east-1
          filters:
            - type: has-virtual-mfa
              value: true
```

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- has-virtual-mfa
value:
type: boolean
required:
- type
```

### Filter: iam-summary
<a name="filter-iam-summary"></a>
📌 **Description:**

----

Return annotated account resource if iam summary filter matches.

Some use cases include, detecting root api keys or mfa usage.

Example iam summary wrt to matchable fields::

  {
        "AccessKeysPerUserQuota": 2,
        "AccountAccessKeysPresent": 0,
        "AccountMFAEnabled": 1,
        "AccountSigningCertificatesPresent": 0,
        "AssumeRolePolicySizeQuota": 2048,
        "AttachedPoliciesPerGroupQuota": 10,
        "AttachedPoliciesPerRoleQuota": 10,
        "AttachedPoliciesPerUserQuota": 10,
        "GroupPolicySizeQuota": 5120,
        "Groups": 1,
        "GroupsPerUserQuota": 10,
        "GroupsQuota": 100,
        "InstanceProfiles": 0,
        "InstanceProfilesQuota": 100,
        "MFADevices": 3,
        "MFADevicesInUse": 2,
        "Policies": 3,
        "PoliciesQuota": 1000,
        "PolicySizeQuota": 5120,
        "PolicyVersionsInUse": 5,
        "PolicyVersionsInUseQuota": 10000,
        "Providers": 0,
        "RolePolicySizeQuota": 10240,
        "Roles": 4,
        "RolesQuota": 250,
        "ServerCertificates": 0,
        "ServerCertificatesQuota": 20,
        "SigningCertificatesPerUserQuota": 2,
        "UserPolicySizeQuota": 2048,
        "Users": 5,
        "UsersQuota": 5000,
        "VersionsPerPolicyQuota": 5,
    }

For example to determine if an account has either not been
enabled with root mfa or has root api keys.

📌 **Example Usage:**

```yaml
policies:
- name: root-keys-or-no-mfa
  resource: account
  filters:
    - type: iam-summary
      key: AccountMFAEnabled
      value: true
      op: eq
      value_type: swap
```

📌 **Schema:**

```yaml
------

properties:
default:
type: object
key:
type: string
op:
enum:
- eq
- equal
- ne
- not-equal
- gt
- greater-than
- ge
- gte
- le
- lte
- lt
- less-than
- glob
- regex
- regex-case
- in
- ni
- not-in
- contains
- difference
- intersect
- mod
type:
enum:
- iam-summary
value:
oneOf:
- type: array
- type: string
- type: boolean
- type: number
- type: 'null'
value_from:
additionalProperties: 'False'
properties:
expr:
oneOf:
- type: integer
- type: string
format:
enum:
- csv
- json
- txt
- csv2dict
headers:
patternProperties:
'':
type: string
type: object
query:
type: string
url:
type: string
required:
- url
type: object
value_path:
type: string
value_regex:
type: string
value_type:
enum:
- age
- integer
- expiration
- normalize
- size
- cidr
- cidr_size
- swap
- resource_count
- expr
- unique_size
- date
- version
- float
required:
- type
```

### Filter: lakeformation-s3-cross-account
<a name="filter-lakeformation-s3-cross-account"></a>
📌 **Description:**

----

Flags an account if its using a lakeformation s3 bucket resource from a different account.

📌 **Example Usage:**

```yaml
policies:
 - name: lakeformation-cross-account-bucket
   resource: aws.account
   filters:
    - type: lakeformation-s3-cross-account
```

📌 **Schema:**

```yaml
------

properties:
default:
type: object
key:
type: string
op:
enum:
- eq
- equal
- ne
- not-equal
- gt
- greater-than
- ge
- gte
- le
- lte
- lt
- less-than
- glob
- regex
- regex-case
- in
- ni
- not-in
- contains
- difference
- intersect
- mod
type:
enum:
- lakeformation-s3-cross-account
value:
oneOf:
- type: array
- type: string
- type: boolean
- type: number
- type: 'null'
value_from:
additionalProperties: 'False'
properties:
expr:
oneOf:
- type: integer
- type: string
format:
enum:
- csv
- json
- txt
- csv2dict
headers:
patternProperties:
'':
type: string
type: object
query:
type: string
url:
type: string
required:
- url
type: object
value_path:
type: string
value_regex:
type: string
value_type:
enum:
- age
- integer
- expiration
- normalize
- size
- cidr
- cidr_size
- swap
- resource_count
- expr
- unique_size
- date
- version
- float
required:
- type
```

### Filter: list-item
<a name="filter-list-item"></a>
📌 **Description:**

----

Perform multi attribute filtering on items within a list,
for example looking for security groups that have rules which
include 0.0.0.0/0 and port 22 open.

📌 **Example Usage:**

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

📌 **Schema:**

```yaml
------

properties:
attrs:
items:
anyOf:
- $ref: '#/definitions/filters/value'
- $ref: '#/definitions/filters/valuekv'
- additional_properties: false
properties:
and:
items:
anyOf:
- $ref: '#/definitions/filters/value'
- $ref: '#/definitions/filters/valuekv'
type: array
type: object
- additional_properties: false
properties:
or:
items:
anyOf:
- $ref: '#/definitions/filters/value'
- $ref: '#/definitions/filters/valuekv'
type: array
type: object
- additional_properties: false
properties:
not:
items:
anyOf:
- $ref: '#/definitions/filters/value'
- $ref: '#/definitions/filters/valuekv'
type: array
type: object
type: array
count:
type: number
count_op:
enum:
- eq
- equal
- ne
- not-equal
- gt
- greater-than
- ge
- gte
- le
- lte
- lt
- less-than
- glob
- regex
- regex-case
- in
- ni
- not-in
- contains
- difference
- intersect
- mod
key:
type: string
type:
enum:
- list-item
required:
- type
```

### Filter: missing
<a name="filter-missing"></a>
📌 **Description:**

----

Assert the absence of a particular resource.

Intended for use at a logical account/subscription/project level

This works as an effectively an embedded policy thats evaluated.

📌 **Example Usage:**

<!-- Notify if an s3 bucket is missing -->

```yaml
policies:
      - name: missing-s3-bucket
        resource: account
        filters:
          - type: missing
            policy:
              resource: s3
              filters:
                - Name: my-bucket
        actions:
          - notify
```

📌 **Schema:**

```yaml
------

properties:
policy:
properties:
resource:
type: string
required:
- resource
type: object
type:
enum:
- missing
required:
- policy
- type
```

### Filter: ops-item
<a name="filter-ops-item"></a>
📌 **Description:**

----

Filter resources associated to extant OpsCenter operational items.

📌 **Example Usage:**

<!-- Find ec2 instances with open ops items. -->

```yaml
policies:
 - name: ec2-instances-ops-items
   resource: ec2
   filters:
     - type: ops-item
       # we can filter on source, title, priority
       priority: [1, 2]
```

📌 **Schema:**

```yaml
------

properties:
priority:
items:
enum:
- 1
- 2
- 3
- 4
- 5
type: array
source:
type: string
status:
default:
- Open
items:
enum:
- Open
- In progress
- Resolved
type: array
title:
type: string
type:
enum:
- ops-item
required:
- type
```

### Filter: organization
<a name="filter-organization"></a>
📌 **Description:**

----

Check organization enrollment and configuration

📌 **Example Usage:**

<!-- determine if an account is not in an organization -->

```yaml
policies:
- name: no-org
  resource: account
  filters:
    - type: organization
      key: Id
      value: absent
```

<!-- determine if an account is setup for organization policies -->

```yaml
policies:
 - name: org-policies-not-enabled
   resource: account
   filters:
     - type: organization
       key: FeatureSet
       value: ALL
       op: not-equal
```

📌 **Schema:**

```yaml
------

properties:
default:
type: object
key:
type: string
op:
enum:
- eq
- equal
- ne
- not-equal
- gt
- greater-than
- ge
- gte
- le
- lte
- lt
- less-than
- glob
- regex
- regex-case
- in
- ni
- not-in
- contains
- difference
- intersect
- mod
type:
enum:
- organization
value:
oneOf:
- type: array
- type: string
- type: boolean
- type: number
- type: 'null'
value_from:
additionalProperties: 'False'
properties:
expr:
oneOf:
- type: integer
- type: string
format:
enum:
- csv
- json
- txt
- csv2dict
headers:
patternProperties:
'':
type: string
type: object
query:
type: string
url:
type: string
required:
- url
type: object
value_path:
type: string
value_regex:
type: string
value_type:
enum:
- age
- integer
- expiration
- normalize
- size
- cidr
- cidr_size
- swap
- resource_count
- expr
- unique_size
- date
- version
- float
required:
- type
```

### Filter: password-policy
<a name="filter-password-policy"></a>
📌 **Description:**

----

Check an account's password policy.

Note that on top of the default password policy fields, we also add an extra key,
PasswordPolicyConfigured which will be set to true or false to signify if the given
account has attempted to set a policy at all.

📌 **Example Usage:**

```yaml
policies:
      - name: password-policy-check
        resource: account
        region: us-east-1
        filters:
          - type: password-policy
            key: MinimumPasswordLength
            value: 10
            op: ge
          - type: password-policy
            key: RequireSymbols
            value: true
```

📌 **Schema:**

```yaml
------

properties:
default:
type: object
key:
type: string
op:
enum:
- eq
- equal
- ne
- not-equal
- gt
- greater-than
- ge
- gte
- le
- lte
- lt
- less-than
- glob
- regex
- regex-case
- in
- ni
- not-in
- contains
- difference
- intersect
- mod
type:
enum:
- password-policy
value:
oneOf:
- type: array
- type: string
- type: boolean
- type: number
- type: 'null'
value_from:
additionalProperties: 'False'
properties:
expr:
oneOf:
- type: integer
- type: string
format:
enum:
- csv
- json
- txt
- csv2dict
headers:
patternProperties:
'':
type: string
type: object
query:
type: string
url:
type: string
required:
- url
type: object
value_path:
type: string
value_regex:
type: string
value_type:
enum:
- age
- integer
- expiration
- normalize
- size
- cidr
- cidr_size
- swap
- resource_count
- expr
- unique_size
- date
- version
- float
required:
- type
```

### Filter: reduce
<a name="filter-reduce"></a>
📌 **Description:**

----

Generic reduce filter to group, sort, and limit your resources.

This example will select the longest running instance from each ASG,
then randomly choose 10% of those, maxing at 15 total instances.

📌 **Example Usage:**

<!-- - name: oldest-instance-by-asg
resource: ec2
filters:
  - "tag:aws:autoscaling:groupName": present
  - type: reduce
    group-by: "tag:aws:autoscaling:groupName"
    sort-by: "LaunchTime"
    order: asc
    limit: 1 -->

<!-- Or you might want to randomly select a 10 percent of your resources,
but no more than 15. -->

<!-- - name: random-selection
resource: ec2
filters:
  - type: reduce
    order: randomize
    limit: 15
    limit-percent: 10 -->

📌 **Schema:**

```yaml
------

properties:
discard:
minimum: 0
type: number
discard-percent:
maximum: 100
minimum: 0
type: number
group-by:
oneOf:
- type: string
- key:
type: string
type: object
value_regex: string
value_type:
enum:
- string
- number
- date
limit:
minimum: 0
type: number
limit-percent:
maximum: 100
minimum: 0
type: number
null-order:
enum:
- first
- last
order:
enum:
- asc
- desc
- reverse
- randomize
sort-by:
oneOf:
- type: string
- key:
type: string
type: object
value_regex: string
value_type:
enum:
- string
- number
- date
type:
enum:
- reduce
required:
- type
```

### Filter: s3-public-block
<a name="filter-s3-public-block"></a>
📌 **Description:**

----

Check for s3 public blocks on an account.

https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html

📌 **Example Usage:**

```yaml
filters:
  - type: s3-public-block
```

📌 **Schema:**

```yaml
------

properties:
default:
type: object
key:
type: string
op:
enum:
- eq
- equal
- ne
- not-equal
- gt
- greater-than
- ge
- gte
- le
- lte
- lt
- less-than
- glob
- regex
- regex-case
- in
- ni
- not-in
- contains
- difference
- intersect
- mod
type:
enum:
- s3-public-block
value:
oneOf:
- type: array
- type: string
- type: boolean
- type: number
- type: 'null'
value_from:
additionalProperties: 'False'
properties:
expr:
oneOf:
- type: integer
- type: string
format:
enum:
- csv
- json
- txt
- csv2dict
headers:
patternProperties:
'':
type: string
type: object
query:
type: string
url:
type: string
required:
- url
type: object
value_path:
type: string
value_regex:
type: string
value_type:
enum:
- age
- integer
- expiration
- normalize
- size
- cidr
- cidr_size
- swap
- resource_count
- expr
- unique_size
- date
- version
- float
required:
- type
```

### Filter: securityhub
<a name="filter-securityhub"></a>
📌 **Description:**

----

Filter an account depending on whether security hub is enabled or not.

📌 **Example Usage:**

```yaml
policies:
 - name: check-securityhub-status
   resource: aws.account
   filters:
    - type: securityhub
      enabled: true
```

📌 **Schema:**

```yaml
------

properties:
enabled:
type: boolean
type:
enum:
- securityhub
required:
- type
```

### Filter: service-limit
<a name="filter-service-limit"></a>
📌 **Description:**

----

Check if account's service limits are past a given threshold.

Supported limits are per trusted advisor, which is variable based
on usage in the account and support level enabled on the account.

The `names` attribute lets you filter which checks to query limits
about.  This is a case-insensitive globbing match on a check name.
You can specify a name exactly or use globbing wildcards like `VPC*`.

The names are exactly what's shown on the trusted advisor page:

    https://console.aws.amazon.com/trustedadvisor/home#/category/service-limits

or via the awscli:

    aws --region us-east-1 support describe-trusted-advisor-checks --language en             --query 'checks[?category==`service_limits`].[name]' --output text

While you can target individual checks via the `names` attribute, and
that should be the preferred method, the following are provided for
backward compatibility with the old style of checks:

- `services`

    The resulting limit's `service` field must match one of these.
    These are case-insensitive globbing matches.

    Note: If you haven't specified any `names` to filter, then
    these service names are used as a case-insensitive prefix match on
    the check name.  This helps limit the number of API calls we need
    to make.

- `limits`

    The resulting limit's `Limit Name` field must match one of these.
    These are case-insensitive globbing matches.

Some example names and their corresponding service and limit names:

Check Name                          Service         Limit Name
----------------------------------  --------------  ---------------------------------
Auto Scaling Groups                 AutoScaling     Auto Scaling groups
Auto Scaling Launch Configurations  AutoScaling     Launch configurations
CloudFormation Stacks               CloudFormation  Stacks
ELB Application Load Balancers      ELB             Active Application Load Balancers
ELB Classic Load Balancers          ELB             Active load balancers
ELB Network Load Balancers          ELB             Active Network Load Balancers
VPC                                 VPC             VPCs
VPC Elastic IP Address              VPC             VPC Elastic IP addresses (EIPs)
VPC Internet Gateways               VPC             Internet gateways

Note: Some service limits checks are being migrated to service quotas,
which is expected to largely replace service limit checks in trusted
advisor.  In this case, some of these checks have no results.

📌 **Example Usage:**

```yaml
policies:
      - name: specific-account-service-limits
        resource: account
        filters:
          - type: service-limit
            names:
              - IAM Policies
              - IAM Roles
              - "VPC*"
            threshold: 1.0
```

<!-- - name: increase-account-service-limits
        resource: account
        filters:
          - type: service-limit
            services:
              - EC2
            threshold: 1.0 -->

<!-- - name: specify-region-for-global-service
        region: us-east-1
        resource: account
        filters:
          - type: service-limit
            services:
              - IAM
            limits:
              - Roles -->

📌 **Schema:**

```yaml
------

properties:
limits:
items:
type: string
type: array
names:
items:
type: string
type: array
refresh_period:
title: how long should a check result be considered fresh
type: integer
services:
items:
enum:
- AutoScaling
- CloudFormation
- DynamoDB
- EBS
- EC2
- ELB
- IAM
- RDS
- Route53
- SES
- VPC
type: array
threshold:
type: number
type:
enum:
- service-limit
required:
- type
```

### Filter: ses-agg-send-stats
<a name="filter-ses-agg-send-stats"></a>
📌 **Description:**

----

This filter queries SES send statistics and aggregates all
the data points into a single report.

📌 **Example Usage:**

```yaml
policies:
      - name: ses-aggregated-send-stats-policy
        resource: account
        filters:
          - type: ses-agg-send-stats
```

📌 **Schema:**

```yaml
------

properties:
default:
type: object
key:
type: string
op:
enum:
- eq
- equal
- ne
- not-equal
- gt
- greater-than
- ge
- gte
- le
- lte
- lt
- less-than
- glob
- regex
- regex-case
- in
- ni
- not-in
- contains
- difference
- intersect
- mod
type:
enum:
- ses-agg-send-stats
value:
oneOf:
- type: array
- type: string
- type: boolean
- type: number
- type: 'null'
value_from:
additionalProperties: 'False'
properties:
expr:
oneOf:
- type: integer
- type: string
format:
enum:
- csv
- json
- txt
- csv2dict
headers:
patternProperties:
'':
type: string
type: object
query:
type: string
url:
type: string
required:
- url
type: object
value_path:
type: string
value_regex:
type: string
value_type:
enum:
- age
- integer
- expiration
- normalize
- size
- cidr
- cidr_size
- swap
- resource_count
- expr
- unique_size
- date
- version
- float
required:
- type
```

### Filter: ses-send-stats
<a name="filter-ses-send-stats"></a>
📌 **Description:**

----

This filter annotates the account resource with SES send statistics for the
last n number of days, not including the current date.

The stats are aggregated into daily metrics. Additionally, the filter also
calculates and annotates the max daily bounce rate (percentage). Using this filter,
users can alert when the bounce rate for a particular day is higher than the limit.

📌 **Example Usage:**

```yaml
policies:
      - name: ses-send-stats
        resource: account
        filters:
          - type: ses-send-stats
            days: 5
          - type: value
            key: '"c7n:ses-max-bounce-rate"'
            op: ge
            value: 10
```

📌 **Schema:**

```yaml
------

properties:
days:
minimum: 2
type: number
type:
enum:
- ses-send-stats
required:
- days
- type
```

### Filter: shield-enabled
<a name="filter-shield-enabled"></a>
📌 **Description:**

----

Parent base class for filters and actions.

📌 **Example Usage:**

```yaml
filters:
  - type: shield-enabled
```

📌 **Schema:**

```yaml
------

properties:
state:
type: boolean
type:
enum:
- shield-enabled
required:
- type
```

### Filter: value
<a name="filter-value"></a>
📌 **Description:**

----

Generic value filter using jmespath

📌 **Example Usage:**

```yaml
filters:
  - type: value
```

📌 **Schema:**

```yaml
------

properties:
default:
type: object
key:
type: string
op:
enum:
- eq
- equal
- ne
- not-equal
- gt
- greater-than
- ge
- gte
- le
- lte
- lt
- less-than
- glob
- regex
- regex-case
- in
- ni
- not-in
- contains
- difference
- intersect
- mod
type:
enum:
- value
value:
oneOf:
- type: array
- type: string
- type: boolean
- type: number
- type: 'null'
value_from:
additionalProperties: 'False'
properties:
expr:
oneOf:
- type: integer
- type: string
format:
enum:
- csv
- json
- txt
- csv2dict
headers:
patternProperties:
'':
type: string
type: object
query:
type: string
url:
type: string
required:
- url
type: object
value_path:
type: string
value_regex:
type: string
value_type:
enum:
- age
- integer
- expiration
- normalize
- size
- cidr
- cidr_size
- swap
- resource_count
- expr
- unique_size
- date
- version
- float
required:
- type
```

### Filter: xray-encrypt-key
<a name="filter-xray-encrypt-key"></a>
📌 **Description:**

----

Determine if xray is encrypted.

📌 **Example Usage:**

```yaml
policies:
      - name: xray-encrypt-with-default
        resource: aws.account
        filters:
           - type: xray-encrypt-key
             key: default
      - name: xray-encrypt-with-kms
        resource: aws.account
        filters:
           - type: xray-encrypt-key
             key: kms
      - name: xray-encrypt-with-specific-key
        resource: aws.account
        filters:
           - type: xray-encrypt-key
             key: alias/my-alias or arn or keyid
```

📌 **Schema:**

```yaml
------

properties:
key:
type: string
type:
enum:
- xray-encrypt-key
required:
- key
- type
```
