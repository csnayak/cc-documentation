---
Title: Aws.S3
Category: Cloud Custodian
Last Updated: 2025-03-22
Version: 1.0
---

# AWS Resources Covered
- [aws.s3](#aws-s3)

## Table of Contents
- [AWS.S3](#aws-s3)

## AWS.S3

### Available Actions
- [attach-encrypt](#action-attach-encrypt)
- [auto-tag-user](#action-auto-tag-user)
- [configure-lifecycle](#action-configure-lifecycle)
- [copy-related-tag](#action-copy-related-tag)
- [delete](#action-delete)
- [delete-bucket-notification](#action-delete-bucket-notification)
- [delete-global-grants](#action-delete-global-grants)
- [encrypt-keys](#action-encrypt-keys)
- [encryption-policy](#action-encryption-policy)
- [invoke-lambda](#action-invoke-lambda)
- [invoke-sfn](#action-invoke-sfn)
- [mark-for-op](#action-mark-for-op)
- [no-op](#action-no-op)
- [notify](#action-notify)
- [post-finding](#action-post-finding)
- [post-item](#action-post-item)
- [put-metric](#action-put-metric)
- [remove-statements](#action-remove-statements)
- [remove-tag](#action-remove-tag)
- [remove-website-hosting](#action-remove-website-hosting)
- [set-bucket-encryption](#action-set-bucket-encryption)
- [set-intelligent-tiering](#action-set-intelligent-tiering)
- [set-inventory](#action-set-inventory)
- [set-public-block](#action-set-public-block)
- [set-replication](#action-set-replication)
- [set-statements](#action-set-statements)
- [tag](#action-tag)
- [toggle-logging](#action-toggle-logging)
- [toggle-versioning](#action-toggle-versioning)
- [webhook](#action-webhook)

### Available Filters
- [bucket-encryption](#filter-bucket-encryption)
- [bucket-logging](#filter-bucket-logging)
- [bucket-notification](#filter-bucket-notification)
- [bucket-replication](#filter-bucket-replication)
- [check-public-block](#filter-check-public-block)
- [config-compliance](#filter-config-compliance)
- [cross-account](#filter-cross-account)
- [data-events](#filter-data-events)
- [event](#filter-event)
- [finding](#filter-finding)
- [global-grants](#filter-global-grants)
- [has-statement](#filter-has-statement)
- [iam-analyzer](#filter-iam-analyzer)
- [intelligent-tiering](#filter-intelligent-tiering)
- [inventory](#filter-inventory)
- [is-log-target](#filter-is-log-target)
- [list-item](#filter-list-item)
- [lock-configuration](#filter-lock-configuration)
- [marked-for-op](#filter-marked-for-op)
- [metrics](#filter-metrics)
- [missing-policy-statement](#filter-missing-policy-statement)
- [no-encryption-statement](#filter-no-encryption-statement)
- [ops-item](#filter-ops-item)
- [ownership](#filter-ownership)
- [reduce](#filter-reduce)
- [value](#filter-value)

### Action Details

### Action: attach-encrypt
<a name="action-attach-encrypt"></a>
📌 **Description:**

----

Action attaches lambda encryption policy to S3 bucket
   supports attachment via lambda bucket notification or sns notification
   to invoke lambda. a special topic value of `default` will utilize an
   extant notification or create one matching the bucket name.

📌 **Example Usage:**

```yaml
policies:
          - name: attach-lambda-encrypt
            resource: s3
            filters:
              - type: missing-policy-statement
            actions:
              - type: attach-encrypt
                role: arn:aws:iam::123456789012:role/my-role
```

📌 **Schema:**

```yaml
------

properties:
role:
type: string
tags:
type: object
topic:
type: string
type:
enum:
- attach-encrypt
required:
- type
```

### Action: auto-tag-user
<a name="action-auto-tag-user"></a>
📌 **Description:**

----

Tag a resource with the user who created/modified it.

📌 **Example Usage:**

```yaml
policies:
- name: ec2-auto-tag-ownercontact
  resource: ec2
  description: |
    Triggered when a new EC2 Instance is launched. Checks to see if
    it's missing the OwnerContact tag. If missing it gets created
    with the value of the ID of whomever called the RunInstances API
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

<!-- There's a number of caveats to usage. Resources which don't
include tagging as part of their api may have some delay before
automation kicks in to create a tag. Real world delay may be several
minutes, with worst case into hours[0]. This creates a race condition
between auto tagging and automation. -->

<!-- In practice this window is on the order of a fraction of a second, as
we fetch the resource and evaluate the presence of the tag before
attempting to tag it. -->

<!-- References -->

<!-- CloudTrail User
 https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html -->

📌 **Schema:**

```yaml
------

properties:
principal_id_tag:
type: string
tag:
type: string
type:
enum:
- auto-tag-user
update:
type: boolean
user-type:
items:
enum:
- IAMUser
- AssumedRole
- FederatedUser
type: string
type: array
value:
enum:
- userName
- arn
- sourceIPAddress
- principalId
type: string
required:
- tag
- type
```

### Action: configure-lifecycle
<a name="action-configure-lifecycle"></a>
📌 **Description:**

----

Action applies a lifecycle policy to versioned S3 buckets

The schema to supply to the rule follows the schema here:
 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_lifecycle_configuration

To delete a lifecycle rule, supply Status=absent

📌 **Example Usage:**

```yaml
policies:
      - name: s3-apply-lifecycle
        resource: s3
        actions:
          - type: configure-lifecycle
            rules:
              - ID: my-lifecycle-id
                Status: Enabled
                Prefix: foo/
                Transitions:
                  - Days: 60
                    StorageClass: GLACIER
```

📌 **Schema:**

```yaml
------

properties:
rules:
items:
additionalProperties: false
properties:
AbortIncompleteMultipartUpload:
additionalProperties: false
properties:
DaysAfterInitiation:
type: integer
type: object
Expiration:
additionalProperties: false
properties:
Date:
type: string
Days:
type: integer
ExpiredObjectDeleteMarker:
type: boolean
type: object
Filter:
additionalProperties: false
maxProperties: 1
minProperties: 1
properties:
And:
additionalProperties: false
properties:
ObjectSizeGreaterThan:
type: integer
ObjectSizeLessThan:
type: integer
Prefix:
type: string
Tags:
items:
additionalProperties: false
properties:
Key:
type: string
Value:
type: string
required:
- Key
- Value
type: object
type: array
type: object
ObjectSizeGreaterThan:
type: integer
ObjectSizeLessThan:
type: integer
Prefix:
type: string
Tag:
additionalProperties: false
properties:
Key:
type: string
Value:
type: string
required:
- Key
- Value
type: object
type: object
ID:
type: string
NoncurrentVersionExpiration:
additionalProperties: false
properties:
NewerNoncurrentVersions:
type: integer
NoncurrentDays:
type: integer
type: object
NoncurrentVersionTransitions:
items:
additionalProperties: false
properties:
NewerNoncurrentVersions:
type: integer
NoncurrentDays:
type: integer
StorageClass:
type: string
type: object
type: array
Prefix:
type: string
Status:
enum:
- Enabled
- Disabled
- absent
Transitions:
items:
additionalProperties: false
properties:
Date:
type: string
Days:
type: integer
StorageClass:
type: string
type: object
type: array
required:
- ID
- Status
type: object
type: array
type:
enum:
- configure-lifecycle
required:
- type
```

### Action: copy-related-tag
<a name="action-copy-related-tag"></a>
📌 **Description:**

----

Copy a related resource tag to its associated resource

In some scenarios, resource tags from a related resource should be applied
to its child resource. For example, EBS Volume tags propogating to their
snapshots. To use this action, specify the resource type that contains the
tags that are to be copied, which can be found by using the
`custodian schema` command.

Then, specify the key on the resource that references the related resource.
In the case of ebs-snapshot, the VolumeId attribute would be the key that
identifies the related resource, ebs.

Finally, specify a list of tag keys to copy from the related resource onto
the original resource. The special character "*" can be used to signify that
all tags from the related resource should be copied to the original resource.

To raise an error when related resources cannot be found, use the
`skip_missing` option. By default, this is set to True.

📌 **Example Usage:**

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

<!-- In the event that the resource type is not supported in Cloud Custodian but
is supported in the resources groups tagging api, use the resourcegroupstaggingapi
resource type to reference the resource. The value should be an ARN for the
related resource. -->

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

📌 **Schema:**

```yaml
------

properties:
key:
type: string
resource:
type: string
skip_missing:
type: boolean
tags:
oneOf:
- enum:
- '*'
- type: array
type:
enum:
- copy-related-tag
required:
- tags
- key
- resource
- type
```

### Action: delete
<a name="action-delete"></a>
📌 **Description:**

----

Action deletes a S3 bucket

📌 **Example Usage:**

```yaml
policies:
      - name: delete-unencrypted-buckets
        resource: s3
        filters:
          - type: missing-statement
            statement_ids:
              - RequiredEncryptedPutObject
        actions:
          - type: delete
            remove-contents: true
```

📌 **Schema:**

```yaml
------

properties:
remove-contents:
type: boolean
type:
enum:
- delete
required:
- type
```

### Action: delete-bucket-notification
<a name="action-delete-bucket-notification"></a>
📌 **Description:**

----

Action to delete S3 bucket notification configurations

📌 **Example Usage:**

```yaml
actions:
  - type: delete-bucket-notification
```

📌 **Schema:**

```yaml
------

properties:
statement_ids:
oneOf:
- enum:
- matched
- items:
type: string
type: array
type:
enum:
- delete-bucket-notification
required:
- statement_ids
- type
```

### Action: delete-global-grants
<a name="action-delete-global-grants"></a>
📌 **Description:**

----

Deletes global grants associated to a S3 bucket

📌 **Example Usage:**

```yaml
policies:
      - name: s3-delete-global-grants
        resource: s3
        filters:
          - type: global-grants
        actions:
          - delete-global-grants
```

📌 **Schema:**

```yaml
------

properties:
grantees:
items:
type: string
type: array
type:
enum:
- delete-global-grants
required:
- type
```

### Action: encrypt-keys
<a name="action-encrypt-keys"></a>
📌 **Description:**

----

Action to encrypt unencrypted S3 objects

📌 **Example Usage:**

```yaml
policies:
      - name: s3-encrypt-objects
        resource: s3
        actions:
          - type: encrypt-keys
            crypto: aws:kms
            key-id: 9c3983be-c6cf-11e6-9d9d-cec0c932ce01
```

📌 **Schema:**

```yaml
------

dependencies:
key-id:
properties:
crypto:
pattern: aws:kms
required:
- crypto
properties:
crypto:
enum:
- AES256
- aws:kms
glacier:
type: boolean
key-id:
type: string
large:
type: boolean
report-only:
type: boolean
type:
enum:
- encrypt-keys
```

### Action: encryption-policy
<a name="action-encryption-policy"></a>
📌 **Description:**

----

Action to apply an encryption policy to S3 buckets

📌 **Example Usage:**

```yaml
policies:
      - name: s3-enforce-encryption
        resource: s3
        mode:
          type: cloudtrail
          events:
            - CreateBucket
        actions:
          - encryption-policy
```

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- encryption-policy
required:
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

### Action: mark-for-op
<a name="action-mark-for-op"></a>
📌 **Description:**

----

Action schedules custodian to perform an action at a certain date

📌 **Example Usage:**

```yaml
policies:
      - name: s3-encrypt
        resource: s3
        filters:
          - type: missing-statement
            statement_ids:
              - RequiredEncryptedPutObject
        actions:
          - type: mark-for-op
            op: attach-encrypt
            days: 7
```

📌 **Schema:**

```yaml
------

properties:
days:
minimum: 0
type: number
hours:
minimum: 0
type: number
msg:
type: string
op:
type: string
tag:
type: string
type:
enum:
- mark-for-op
tz:
type: string
required:
- type
```

### Action: no-op
<a name="action-no-op"></a>
📌 **Description:**

----

Parent base class for filters and actions.

📌 **Example Usage:**

```yaml
actions:
  - type: no-op
```

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- no-op
required:
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

### Action: remove-statements
<a name="action-remove-statements"></a>
📌 **Description:**

----

Action to remove policy statements from S3 buckets

📌 **Example Usage:**

```yaml
policies:
      - name: s3-remove-encrypt-put
        resource: s3
        filters:
          - type: has-statement
            statement_ids:
              - RequireEncryptedPutObject
        actions:
          - type: remove-statements
            statement_ids:
              - RequiredEncryptedPutObject
```

📌 **Schema:**

```yaml
------

properties:
statement_ids:
oneOf:
- enum:
- matched
- '*'
- items:
type: string
type: array
type:
enum:
- remove-statements
required:
- statement_ids
- type
```

### Action: remove-tag
<a name="action-remove-tag"></a>
📌 **Description:**

----

Removes tag/tags from a S3 object

📌 **Example Usage:**

```yaml
policies:
      - name: s3-remove-owner-tag
        resource: s3
        filters:
          - "tag:BucketOwner": present
        actions:
          - type: remove-tag
            tags: ['BucketOwner']
```

📌 **Schema:**

```yaml
------

properties:
tags:
items:
type: string
type: array
type:
enum:
- remove-tag
- unmark
- untag
- remove-tag
required:
- type
```

### Action: remove-website-hosting
<a name="action-remove-website-hosting"></a>
📌 **Description:**

----

Action that removes website hosting configuration.

📌 **Example Usage:**

```yaml
actions:
  - type: remove-website-hosting
```

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- remove-website-hosting
required:
- type
```

### Action: set-bucket-encryption
<a name="action-set-bucket-encryption"></a>
📌 **Description:**

----

Action enables default encryption on S3 buckets

`enabled`: boolean Optional: Defaults to True

`crypto`: aws:kms | AES256` Optional: Defaults to AES256

`key`: arn, alias, or kms id key

`bucket-key`: boolean Optional:
Defaults to True.
Reduces amount of API traffic from Amazon S3 to KMS and can reduce KMS request
costsby up to 99 percent. Requires kms:Decrypt permissions for copy and upload
on the AWS KMS Key Policy.

Bucket Key Docs: https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-key.html

📌 **Example Usage:**

```yaml
policies:
      - name: s3-enable-default-encryption-kms
        resource: s3
        actions:
          - type: set-bucket-encryption
          # enabled: true <------ optional (true by default)
            crypto: aws:kms
            key: 1234abcd-12ab-34cd-56ef-1234567890ab
            bucket-key: true
```

<!-- - name: s3-enable-default-encryption-kms-alias
        resource: s3
        actions:
          - type: set-bucket-encryption
          # enabled: true <------ optional (true by default)
            crypto: aws:kms
            key: alias/some/alias/key
            bucket-key: true -->

<!-- - name: s3-enable-default-encryption-aes256
        resource: s3
        actions:
          - type: set-bucket-encryption
          # bucket-key: true <--- optional (true by default for AWS SSE)
          # crypto: AES256 <----- optional (AES256 by default)
          # enabled: true <------ optional (true by default) -->

<!-- - name: s3-disable-default-encryption
        resource: s3
        actions:
          - type: set-bucket-encryption
            enabled: false -->

📌 **Schema:**

```yaml
------

dependencies:
key:
properties:
crypto:
pattern: aws:kms
required:
- crypto
properties:
bucket-key:
type: boolean
crypto:
enum:
- aws:kms
- AES256
enabled:
type: boolean
key:
type: string
type:
enum:
- set-bucket-encryption
```

### Action: set-intelligent-tiering
<a name="action-set-intelligent-tiering"></a>
📌 **Description:**

----

Action applies an intelligent tiering configuration to a S3 bucket

The schema to supply to the configuration follows the schema here:
 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/put_bucket_intelligent_tiering_configuration.html

To delete a configuration, supply Status=delete with the either the Id or Id: matched

📌 **Example Usage:**

```yaml
policies:
      - name: s3-apply-intelligent-tiering-config
        resource: aws.s3
        filters:
          - not:
            - type: intelligent-tiering
              attrs:
                - Status: Enabled
                - Filter:
                    And:
                      Prefix: helloworld
                      Tags:
                        - Key: Hello
                          Value: World
                - Tierings:
                  - Days: 123
                    AccessTier: ARCHIVE_ACCESS
        actions:
          - type: set-intelligent-tiering
            Id: c7n-default
            IntelligentTieringConfiguration:
              Id: c7n-default
              Status: Enabled
              Tierings:
                - Days: 149
                  AccessTier: ARCHIVE_ACCESS
```

<!-- - name: s3-delete-intelligent-tiering-configuration
        resource: aws.s3
        filters:
          - type: intelligent-tiering
            attrs:
              - Status: Enabled
              - Id: test-config
        actions:
          - type: set-intelligent-tiering
            Id: test-config
            State: delete -->

<!-- - name: s3-delete-intelligent-tiering-matched-configs
        resource: aws.s3
        filters:
          - type: intelligent-tiering
            attrs:
              - Status: Enabled
              - Id: test-config
        actions:
          - type: set-intelligent-tiering
            Id: matched
            State: delete -->

📌 **Schema:**

```yaml
------

oneOf:
- required:
- type
- Id
- IntelligentTieringConfiguration
- required:
- type
- Id
- State
properties:
Id:
type: string
IntelligentTieringConfiguration:
type: object
State:
enum:
- delete
type: string
type:
enum:
- set-intelligent-tiering
```

### Action: set-inventory
<a name="action-set-inventory"></a>
📌 **Description:**

----

Configure bucket inventories for an s3 bucket.

📌 **Example Usage:**

```yaml
actions:
  - type: set-inventory
```

📌 **Schema:**

```yaml
------

properties:
destination:
description: Name of destination bucket
type: string
encryption:
enum:
- SSES3
- SSEKMS
fields:
items:
enum:
- Size
- LastModifiedDate
- StorageClass
- ETag
- IsMultipartUploaded
- ReplicationStatus
- EncryptionStatus
- ObjectLockRetainUntilDate
- ObjectLockMode
- ObjectLockLegalHoldStatus
- IntelligentTieringAccessTier
- BucketKeyStatus
- ChecksumAlgorithm
type: array
format:
enum:
- CSV
- ORC
- Parquet
key_id:
description: Optional Customer KMS KeyId for SSE-KMS
type: string
name:
description: Name of inventory
type: string
prefix:
description: Destination prefix
type: string
schedule:
enum:
- Daily
- Weekly
state:
enum:
- enabled
- disabled
- absent
type:
enum:
- set-inventory
versions:
enum:
- All
- Current
required:
- name
- destination
- type
```

### Action: set-public-block
<a name="action-set-public-block"></a>
📌 **Description:**

----

Action to update Public Access blocks on S3 buckets

If no action parameters are provided all settings will be set to the `state`, which defaults

If action parameters are provided, those will be set and other extant values preserved.

📌 **Example Usage:**

```yaml
policies:
      - name: s3-public-block-enable-all
        resource: s3
        filters:
          - type: check-public-block
        actions:
          - type: set-public-block
```

```yaml
policies:
      - name: s3-public-block-disable-all
        resource: s3
        filters:
          - type: check-public-block
        actions:
          - type: set-public-block
            state: false
```

```yaml
policies:
      - name: s3-public-block-enable-some
        resource: s3
        filters:
          - or:
            - type: check-public-block
              BlockPublicAcls: false
            - type: check-public-block
              BlockPublicPolicy: false
        actions:
          - type: set-public-block
            BlockPublicAcls: true
            BlockPublicPolicy: true
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
- set-public-block
required:
- type
```

### Action: set-replication
<a name="action-set-replication"></a>
📌 **Description:**

----

Action to add or remove replication configuration statement from S3 buckets

📌 **Example Usage:**

```yaml
policies:
      - name: s3-unapproved-account-replication
        resource: s3
        filters:
          - type: value
            key: Replication.ReplicationConfiguration.Rules[].Destination.Account
            value: present
          - type: value
            key: Replication.ReplicationConfiguration.Rules[].Destination.Account
            value_from:
              url: 's3:///path/to/file.json'
              format: json
              expr: "approved_accounts.*"
            op: ni
        actions:
          - type: set-replication
            state: enable
```

📌 **Schema:**

```yaml
------

properties:
state:
enum:
- enable
- disable
- remove
type: string
type:
enum:
- set-replication
required:
- type
```

### Action: set-statements
<a name="action-set-statements"></a>
📌 **Description:**

----

Action to add or update policy statements to S3 buckets

📌 **Example Usage:**

```yaml
policies:
      - name: force-s3-https
        resource: s3
        actions:
          - type: set-statements
            statements:
              - Sid: "DenyHttp"
                Effect: "Deny"
                Action: "s3:GetObject"
                Principal:
                  AWS: "*"
                Resource: "arn:aws:s3:::{bucket_name}/*"
                Condition:
                  Bool:
                    "aws:SecureTransport": false
```

📌 **Schema:**

```yaml
------

properties:
statements:
items:
oneOf:
- required:
- Principal
- Action
- Resource
- required:
- NotPrincipal
- Action
- Resource
- required:
- Principal
- NotAction
- Resource
- required:
- NotPrincipal
- NotAction
- Resource
- required:
- Principal
- Action
- NotResource
- required:
- NotPrincipal
- Action
- NotResource
- required:
- Principal
- NotAction
- NotResource
- required:
- NotPrincipal
- NotAction
- NotResource
properties:
Action:
anyOf:
- type: string
- type: array
Condition:
type: object
Effect:
enum:
- Allow
- Deny
type: string
NotAction:
anyOf:
- type: string
- type: array
NotPrincipal:
anyOf:
- type: object
- type: array
NotResource:
anyOf:
- type: string
- type: array
Principal:
anyOf:
- type: string
- type: object
- type: array
Resource:
anyOf:
- type: string
- type: array
Sid:
type: string
required:
- Sid
- Effect
type: object
type: array
type:
enum:
- set-statements
required:
- type
```

### Action: tag
<a name="action-tag"></a>
📌 **Description:**

----

Action to create tags on a S3 bucket

📌 **Example Usage:**

```yaml
policies:
      - name: s3-tag-region
        resource: s3
        region: us-east-1
        filters:
          - "tag:RegionName": absent
        actions:
          - type: tag
            key: RegionName
            value: us-east-1
```

📌 **Schema:**

```yaml
------

properties:
key:
type: string
tag:
type: string
tags:
type: object
type:
enum:
- tag
- mark
value:
type: string
required:
- type
```

### Action: toggle-logging
<a name="action-toggle-logging"></a>
📌 **Description:**

----

Action to enable/disable logging on a S3 bucket.

Target bucket ACL must allow for WRITE and READ_ACP Permissions
Not specifying a target_prefix will default to the current bucket name.
https://docs.aws.amazon.com/AmazonS3/latest/dev/enable-logging-programming.html

📌 **Example Usage:**

```yaml
policies:
      - name: s3-enable-logging
        resource: s3
        filters:
          - "tag:Testing": present
        actions:
          - type: toggle-logging
            target_bucket: log-bucket
            target_prefix: logs123/
```

```yaml
policies:
      - name: s3-force-standard-logging
        resource: s3
        filters:
          - type: bucket-logging
            op: not-equal
            target_bucket: "{account_id}-{region}-s3-logs"
            target_prefix: "{account}/{source_bucket_name}/"
        actions:
          - type: toggle-logging
            target_bucket: "{account_id}-{region}-s3-logs"
            target_prefix: "{account}/{source_bucket_name}/"
```

📌 **Schema:**

```yaml
------

properties:
enabled:
type: boolean
target_bucket:
type: string
target_prefix:
type: string
type:
enum:
- toggle-logging
required:
- type
```

### Action: toggle-versioning
<a name="action-toggle-versioning"></a>
📌 **Description:**

----

Action to enable/suspend versioning on a S3 bucket

Note versioning can never be disabled only suspended.

📌 **Example Usage:**

```yaml
policies:
      - name: s3-enable-versioning
        resource: s3
        filters:
          - or:
            - type: value
              key: Versioning.Status
              value: Suspended
            - type: value
              key: Versioning.Status
              value: absent
        actions:
          - type: toggle-versioning
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
- toggle-versioning
required:
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

### Filter: bucket-encryption
<a name="filter-bucket-encryption"></a>
📌 **Description:**

----

Filters for S3 buckets that have bucket-encryption

:example

📌 **Example Usage:**

```yaml
policies:
      - name: s3-bucket-encryption-AES256
        resource: s3
        region: us-east-1
        filters:
          - type: bucket-encryption
            state: True
            crypto: AES256
      - name: s3-bucket-encryption-KMS
        resource: s3
        region: us-east-1
        filters:
          - type: bucket-encryption
            state: True
            crypto: aws:kms
            key: alias/some/alias/key
      - name: s3-bucket-encryption-off
        resource: s3
        region: us-east-1
        filters:
          - type: bucket-encryption
            state: False
      - name: s3-bucket-test-bucket-key-enabled
        resource: s3
        region: us-east-1
        filters:
          - type: bucket-encryption
            bucket_key_enabled: True
```

📌 **Schema:**

```yaml
------

properties:
bucket_key_enabled:
type: boolean
crypto:
enum:
- AES256
- aws:kms
type: string
key:
type: string
state:
type: boolean
type:
enum:
- bucket-encryption
required:
- type
```

### Filter: bucket-logging
<a name="filter-bucket-logging"></a>
📌 **Description:**

----

Filter based on bucket logging configuration.

📌 **Example Usage:**

```yaml
policies:
      - name: add-bucket-logging-if-missing
        resource: s3
        filters:
          - type: bucket-logging
            op: disabled
        actions:
          - type: toggle-logging
            target_bucket: "{account_id}-{region}-s3-logs"
            target_prefix: "{source_bucket_name}/"
```

```yaml
policies:
      - name: update-incorrect-or-missing-logging
        resource: s3
        filters:
          - type: bucket-logging
            op: not-equal
            target_bucket: "{account_id}-{region}-s3-logs"
            target_prefix: "{account}/{source_bucket_name}/"
        actions:
          - type: toggle-logging
            target_bucket: "{account_id}-{region}-s3-logs"
            target_prefix: "{account}/{source_bucket_name}/"
```

📌 **Schema:**

```yaml
------

properties:
op:
enum:
- enabled
- disabled
- equal
- not-equal
- eq
- ne
target_bucket:
type: string
target_prefix:
type: string
type:
enum:
- bucket-logging
required:
- op
- type
```

### Filter: bucket-notification
<a name="filter-bucket-notification"></a>
📌 **Description:**

----

Filter based on bucket notification configuration.

📌 **Example Usage:**

```yaml
policies:
      - name: delete-incorrect-notification
        resource: s3
        filters:
          - type: bucket-notification
            kind: lambda
            key: Id
            value: "IncorrectLambda"
            op: eq
        actions:
          - type: delete-bucket-notification
            statement_ids: matched
```

📌 **Schema:**

```yaml
------

properties:
default:
type: object
key:
type: string
kind:
enum:
- lambda
- sns
- sqs
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
- bucket-notification
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
- kind
- type
```

### Filter: bucket-replication
<a name="filter-bucket-replication"></a>
📌 **Description:**

----

Filter for S3 buckets to look at bucket replication configurations

The schema to supply to the attrs follows the schema here:
 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/get_bucket_replication.html

📌 **Example Usage:**

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
- bucket-replication
required:
- type
```

### Filter: check-public-block
<a name="filter-check-public-block"></a>
📌 **Description:**

----

Filter for s3 bucket public blocks

If no filter paramaters are provided it checks to see if any are unset or False.

If parameters are provided only the provided ones are checked.

📌 **Example Usage:**

```yaml
policies:
      - name: CheckForPublicAclBlock-Off
        resource: s3
        region: us-east-1
        filters:
          - type: check-public-block
            BlockPublicAcls: true
            BlockPublicPolicy: true
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
type:
enum:
- check-public-block
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

### Filter: cross-account
<a name="filter-cross-account"></a>
📌 **Description:**

----

Filters cross-account access to S3 buckets

📌 **Example Usage:**

```yaml
policies:
      - name: s3-acl
        resource: s3
        region: us-east-1
        filters:
          - type: cross-account
```

📌 **Schema:**

```yaml
------

properties:
actions:
items:
type: string
type: array
everyone_only:
type: boolean
type:
enum:
- cross-account
whitelist:
items:
type: string
type: array
whitelist_conditions:
items:
type: string
type: array
whitelist_from:
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
whitelist_orgids:
items:
type: string
type: array
whitelist_orgids_from:
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
whitelist_vpc:
items:
type: string
type: array
whitelist_vpc_from:
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
whitelist_vpce:
items:
type: string
type: array
whitelist_vpce_from:
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
required:
- type
```

### Filter: data-events
<a name="filter-data-events"></a>
📌 **Description:**

----

Find buckets for which CloudTrail is logging data events.

Note that this filter only examines trails that are defined in the
current account.

📌 **Example Usage:**

```yaml
filters:
  - type: data-events
```

📌 **Schema:**

```yaml
------

properties:
state:
enum:
- present
- absent
type:
enum:
- data-events
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

### Filter: global-grants
<a name="filter-global-grants"></a>
📌 **Description:**

----

Filters for all S3 buckets that have global-grants

*Note* by default this filter allows for read access
if the bucket has been configured as a website. This
can be disabled per the example below.

📌 **Example Usage:**

```yaml
policies:
 - name: remove-global-grants
   resource: s3
   filters:
    - type: global-grants
      allow_website: false
   actions:
    - delete-global-grants
```

📌 **Schema:**

```yaml
------

properties:
allow_website:
type: boolean
operator:
enum:
- or
- and
type: string
permissions:
items:
enum:
- READ
- WRITE
- WRITE_ACP
- READ_ACP
- FULL_CONTROL
type: string
type: array
type:
enum:
- global-grants
required:
- type
```

### Filter: has-statement
<a name="filter-has-statement"></a>
📌 **Description:**

----

Find resources with matching access policy statements.

If you want to return resource statements that include the listed Action or
NotAction, you can use PartialMatch instead of an exact match.

📌 **Example Usage:**

```yaml
policies:
      - name: sns-check-statement-id
        resource: sns
        filters:
          - type: has-statement
            statement_ids:
              - BlockNonSSL
    policies:
      - name: sns-check-block-non-ssl
        resource: sns
        filters:
          - type: has-statement
            statements:
              - Effect: Deny
                Action: 'SNS:Publish'
                Principal: '*'
                Condition:
                    Bool:
                        "aws:SecureTransport": "false"
                PartialMatch: 'Action'
```

📌 **Schema:**

```yaml
------

properties:
statement_ids:
items:
type: string
type: array
statements:
items:
properties:
Action:
anyOf:
- type: string
- type: array
Condition:
type: object
Effect:
enum:
- Allow
- Deny
type: string
NotAction:
anyOf:
- type: string
- type: array
NotPrincipal:
anyOf:
- type: object
- type: array
NotResource:
anyOf:
- type: string
- type: array
PartialMatch:
anyOf:
- enum:
- Action
- NotAction
type: string
- items:
- enum:
- Action
- NotAction
type: string
type: array
Principal:
anyOf:
- type: string
- type: object
- type: array
Resource:
anyOf:
- type: string
- type: array
Sid:
type: string
required:
- Effect
type: object
type: array
type:
enum:
- has-statement
required:
- type
```

### Filter: iam-analyzer
<a name="filter-iam-analyzer"></a>
📌 **Description:**

----

Analyze resource access policies using AWS IAM Access Analyzer.

Access analyzer uses logic based reasoning to analyze embedded resource
iam access policies to determine access outside of a zone of trust.

📌 **Example Usage:**

```yaml
policies:
 - name: s3-check
   resource: aws.s3
   filters:
     - type: iam-analyzer
       key: isPublic
       value: true
```

📌 **Schema:**

```yaml
------

properties:
analyzer:
type: string
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
- iam-analyzer
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

### Filter: intelligent-tiering
<a name="filter-intelligent-tiering"></a>
📌 **Description:**

----

Filter for S3 buckets to look at intelligent tiering configurations

The schema to supply to the attrs follows the schema here:
 https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_bucket_intelligent_tiering_configurations.html

📌 **Example Usage:**

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
- intelligent-tiering
required:
- type
```

### Filter: inventory
<a name="filter-inventory"></a>
📌 **Description:**

----

Filter inventories for a bucket

📌 **Example Usage:**

```yaml
filters:
  - type: inventory
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
- inventory
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

### Filter: is-log-target
<a name="filter-is-log-target"></a>
📌 **Description:**

----

Filter and return buckets are log destinations.

Not suitable for use in lambda on large accounts, This is a api
heavy process to detect scan all possible log sources.

Sources:
  - elb (Access Log)
  - s3 (Access Log)
  - cfn (Template writes)
  - cloudtrail

📌 **Example Usage:**

```yaml
policies:
      - name: s3-log-bucket
        resource: s3
        filters:
          - type: is-log-target
```

📌 **Schema:**

```yaml
------

properties:
self:
type: boolean
services:
items:
enum:
- s3
- elb
- cloudtrail
type: array
type:
enum:
- is-log-target
value:
type: boolean
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

### Filter: lock-configuration
<a name="filter-lock-configuration"></a>
📌 **Description:**

----

Filter S3 buckets based on their object lock configurations

📌 **Example Usage:**

<!-- Get all buckets where lock configuration mode is COMPLIANCE -->

```yaml
policies:
          - name: lock-configuration-compliance
            resource: aws.s3
            filters:
              - type: lock-configuration
                key: Rule.DefaultRetention.Mode
                value: COMPLIANCE
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
- lock-configuration
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

### Filter: marked-for-op
<a name="filter-marked-for-op"></a>
📌 **Description:**

----

Filter resources for tag specified future action

Filters resources by a 'maid_status' tag which specifies a future
date for an action.

The filter parses the tag values looking for an 'op@date'
string. The date is parsed and compared to do today's date, the
filter succeeds if today's date is gte to the target date.

The optional 'skew' parameter provides for incrementing today's
date a number of days into the future. An example use case might
be sending a final notice email a few days before terminating an
instance, or snapshotting a volume prior to deletion.

The optional 'skew_hours' parameter provides for incrementing the current
time a number of hours into the future.

Optionally, the 'tz' parameter can get used to specify the timezone
in which to interpret the clock (default value is 'utc')

.. code-block :: yaml

  policies:
    - name: ec2-stop-marked
      resource: ec2
      filters:
        - type: marked-for-op
          # The default tag used is maid_status
          # but that is configurable
          tag: custodian_status
          op: stop
          # Another optional tag is skew
          tz: utc
      actions:
        - type: stop

📌 **Example Usage:**

```yaml
filters:
  - type: marked-for-op
```

📌 **Schema:**

```yaml
------

properties:
op:
type: string
skew:
minimum: 0
type: number
skew_hours:
minimum: 0
type: number
tag:
type: string
type:
enum:
- marked-for-op
tz:
type: string
required:
- type
```

### Filter: metrics
<a name="filter-metrics"></a>
📌 **Description:**

----

S3 CW Metrics need special handling for attribute/dimension
mismatch, and additional required dimension.

📌 **Example Usage:**

```yaml
filters:
  - type: metrics
```

📌 **Schema:**

```yaml
------

properties:
attr-multiplier:
type: number
days:
type: number
dimensions:
patternProperties:
^.*$:
type: string
type: object
missing-value:
type: number
name:
type: string
namespace:
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
type: string
percent-attr:
type: string
period:
type: number
statistics:
type: string
type:
enum:
- metrics
value:
type: number
required:
- value
- name
```

### Filter: missing-policy-statement
<a name="filter-missing-policy-statement"></a>
📌 **Description:**

----

Find buckets missing a set of named policy statements.

📌 **Example Usage:**

```yaml
policies:
      - name: s3-bucket-missing-statement
        resource: s3
        filters:
          - type: missing-statement
            statement_ids:
              - RequiredEncryptedPutObject
```

📌 **Schema:**

```yaml
------

properties:
statement_ids:
items:
type: string
type: array
type:
enum:
- missing-policy-statement
- missing-statement
required:
- type
```

### Filter: no-encryption-statement
<a name="filter-no-encryption-statement"></a>
📌 **Description:**

----

Find buckets with missing encryption policy statements.

📌 **Example Usage:**

```yaml
policies:
      - name: s3-bucket-not-encrypted
        resource: s3
        filters:
          - type: no-encryption-statement
```

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- no-encryption-statement
required:
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

### Filter: ownership
<a name="filter-ownership"></a>
📌 **Description:**

----

Filter for object ownership controls

Reference: https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html

:example

Find buckets with ACLs disabled

📌 **Example Usage:**

```yaml
policies:
      - name: s3-bucket-acls-disabled
        resource: aws.s3
        region: us-east-1
        filters:
          - type: ownership
            value: BucketOwnerEnforced
```

<!-- :example -->

<!-- Find buckets with object ownership preferred or enforced -->

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

<!-- :example -->

<!-- Find buckets with no object ownership controls -->

```yaml
policies:
      - name: s3-bucket-no-ownership-controls
        resource: aws.s3
        region: us-east-1
        filters:
          - type: ownership
            value: empty
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
- ownership
value:
oneOf:
- enum:
- BucketOwnerEnforced
- BucketOwnerPreferred
- ObjectWriter
- absent
- present
- not-null
- empty
type: string
- items:
enum:
- BucketOwnerEnforced
- BucketOwnerPreferred
- ObjectWriter
- absent
- present
- not-null
- empty
type: string
type: array
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
