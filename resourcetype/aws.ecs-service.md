---
Title: Aws.Ecs Service
Category: Cloud Custodian
Last Updated: 2025-03-22
Version: 1.0
---

# AWS Resources Covered
- [aws.ecs-service](#aws-ecs-service)

## Table of Contents
- [AWS.ECS-SERVICE](#aws-ecs-service)

## AWS.ECS-SERVICE

### Available Actions
- [auto-tag-user](#action-auto-tag-user)
- [copy-related-tag](#action-copy-related-tag)
- [delete](#action-delete)
- [invoke-lambda](#action-invoke-lambda)
- [invoke-sfn](#action-invoke-sfn)
- [mark-for-op](#action-mark-for-op)
- [modify](#action-modify)
- [modify-definition](#action-modify-definition)
- [notify](#action-notify)
- [post-finding](#action-post-finding)
- [post-item](#action-post-item)
- [put-metric](#action-put-metric)
- [remove-tag](#action-remove-tag)
- [resize](#action-resize)
- [tag](#action-tag)
- [webhook](#action-webhook)

### Available Filters
- [config-compliance](#filter-config-compliance)
- [cost-optimization](#filter-cost-optimization)
- [event](#filter-event)
- [finding](#filter-finding)
- [list-item](#filter-list-item)
- [marked-for-op](#filter-marked-for-op)
- [metrics](#filter-metrics)
- [network-location](#filter-network-location)
- [offhour](#filter-offhour)
- [onhour](#filter-onhour)
- [ops-item](#filter-ops-item)
- [reduce](#filter-reduce)
- [security-group](#filter-security-group)
- [subnet](#filter-subnet)
- [taggable](#filter-taggable)
- [task-definition](#filter-task-definition)
- [value](#filter-value)

### Action Details

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

Delete service(s).

📌 **Example Usage:**

```yaml
actions:
  - type: delete
```

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- delete
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

Mark ECS resources for deferred action
(ecs, ecs-task-definition, ecs-service, ecs-task, ecs-container-instance)

Requires arns in new format for tasks, services, and container-instances.
https://docs.aws.amazon.com/AmazonECS/latest/userguide/ecs-resource-ids.html

📌 **Example Usage:**

```yaml
policies:
  - name: ecs-service-invalid-tag-stop
    resource: ecs-service
    filters:
      - "tag:InvalidTag": present
      - type: taggable
        state: true
    actions:
      - type: mark-for-op
        op: delete
        days: 1
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

### Action: modify
<a name="action-modify"></a>
📌 **Description:**

----

Action to update service

📌 **Example Usage:**

```yaml
policies:
      - name: no-public-ips-services
        resource: ecs-service
        filters:
          - 'networkConfiguration.awsvpcConfiguration.assignPublicIp': 'ENABLED'
        actions:
          - type: modify
            update:
              networkConfiguration:
                awsvpcConfiguration:
                  assignPublicIp: DISABLED
```

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- modify
update:
deploymentConfiguration:
properties:
maximumPercent:
type: integer
minimumHealthyPercent:
type: integer
type: object
desiredCount:
type: integer
forceNewDeployment:
default: false
type: boolean
healthCheckGracePeriodSeconds:
type: integer
networkConfiguration:
properties:
awsvpcConfiguration:
properties:
assignPublicIp:
enum:
- ENABLED
- DISABLED
type: string
securityGroups:
items:
type: string
subnets:
items:
type: string
minItems: 1
type: array
type: object
type: object
platformVersion:
type: string
taskDefinition:
type: string
required:
- type
```

### Action: modify-definition
<a name="action-modify-definition"></a>
📌 **Description:**

----

Parent base class for filters and actions.

📌 **Example Usage:**

```yaml
actions:
  - type: modify-definition
```

📌 **Schema:**

```yaml
------

properties:
properties:
type: object
type:
enum:
- modify-definition
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

### Action: remove-tag
<a name="action-remove-tag"></a>
📌 **Description:**

----

Remove tag(s) from ECS resources
(ecs, ecs-task-definition, ecs-service, ecs-task, ecs-container-instance)

📌 **Example Usage:**

```yaml
policies:
      - name: ecs-service-remove-tag
        resource: ecs-service
        filters:
          - type: taggable
            state: true
        actions:
          - type: remove-tag
            tags: ["BadTag"]
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

### Action: resize
<a name="action-resize"></a>
📌 **Description:**

----

Action to resize the min/max/desired count in an application autoscaling target

There are several ways to use this action:

1. apply a fixed resize of min, max or desired, optionally saving the
   previous values to a named tag (for restoring later):

📌 **Example Usage:**

```yaml
policies:
      - name: offhours-ecs-off
        resource: ecs-service
        filters:
          - type: offhour
            offhour: 19
            default_tz: bst
        actions:
          - type: resize
            min-capacity: 0
            desired: 0
            save-options-tag: OffHoursPrevious
            suspend-scaling: true
```

<!-- 2. restore previous values for min/max/desired from a tag: -->

```yaml
policies:
      - name: offhours-ecs-on
        resource: ecs-service
        filters:
          - type: onhour
            onhour: 8
            default_tz: bst
        actions:
          - type: resize
            restore-options-tag: OffHoursPrevious
            restore-scaling: true
```

📌 **Schema:**

```yaml
------

properties:
desired:
anyOf:
- enum:
- current
- minimum: 0
type: integer
max-capacity:
minimum: 0
type: integer
min-capacity:
minimum: 0
type: integer
restore-options-tag:
type: string
restore-scaling:
type: boolean
save-options-tag:
type: string
suspend-scaling:
type: boolean
type:
enum:
- resize
required:
- type
```

### Action: tag
<a name="action-tag"></a>
📌 **Description:**

----

Action to create tag(s) on an ECS resource
(ecs, ecs-task-definition, ecs-service, ecs-task, ecs-container-instance)

Requires arns in new format for tasks, services, and container-instances.
https://docs.aws.amazon.com/AmazonECS/latest/userguide/ecs-resource-ids.html

📌 **Example Usage:**

```yaml
policies:
      - name: tag-ecs-service
        resource: ecs-service
        filters:
          - "tag:target-tag": absent
          - type: taggable
            state: true
        actions:
          - type: tag
            key: target-tag
            value: target-value
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

### Filter: cost-optimization
<a name="filter-cost-optimization"></a>
📌 **Description:**

----

Cost optimization hub recommendations.

📌 **Example Usage:**

<!-- - name: cost-ec2-optimize
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
       op: gte -->

📌 **Schema:**

```yaml
------

properties:
action:
enum:
- Rightsize
- Stop
- Upgrade
- PurchaseSavingsPlans
- PurchaseReservedInstances
- MigrateToGraviton
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
efforts:
items:
enum:
- VeryLow
- Low
- Medium
- High
- VeryHigh
type: array
type:
enum:
- cost-optimization
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

Supports cloud watch metrics filters on resources.

All resources that have cloud watch metrics are supported.

Docs on cloud watch metrics

- GetMetricStatistics
  https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_GetMetricStatistics.html

- Supported Metrics
  https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html

📌 **Example Usage:**

<!-- - name: ec2-underutilized
resource: ec2
filters:
  - type: metrics
    name: CPUUtilization
    days: 4
    period: 86400
    value: 30
    op: less-than -->

<!-- Note periods when a resource is not sending metrics are not part
of calculated statistics as in the case of a stopped ec2 instance,
nor for resources to new to have existed the entire
period. ie. being stopped for an ec2 instance wouldn't lower the
average cpu utilization. -->

<!-- The "missing-value" key allows a policy to specify a default
value when CloudWatch has no data to report: -->

<!-- - name: elb-low-request-count
resource: elb
filters:
  - type: metrics
    name: RequestCount
    statistics: Sum
    days: 7
    value: 7
    missing-value: 0
    op: less-than -->

<!-- This policy matches any ELB with fewer than 7 requests for the past week.
ELBs with no requests during that time will have an empty set of metrics.
Rather than skipping those resources, "missing-value: 0" causes the
policy to treat their request counts as 0. -->

<!-- Note the default statistic for metrics is Average. -->

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

### Filter: network-location
<a name="filter-network-location"></a>
📌 **Description:**

----

On a network attached resource, determine intersection of
security-group attributes, subnet attributes, and resource attributes.

The use case is a bit specialized, for most use cases using `subnet`
and `security-group` filters suffice. but say for example you wanted to
verify that an ec2 instance was only using subnets and security groups
with a given tag value, and that tag was not present on the resource.

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-mismatched-sg-remove
    resource: ec2
    filters:
      - type: network-location
        compare: ["resource","security-group"]
        key: "tag:TEAM_NAME"
        ignore:
          - "tag:TEAM_NAME": Enterprise
    actions:
      - type: modify-security-groups
        remove: network-location
        isolation-group: sg-xxxxxxxx
```

📌 **Schema:**

```yaml
------

properties:
compare:
default:
- resource
- subnet
- security-group
description: Which elements of network location should be considered when matching.
items:
enum:
- resource
- subnet
- security-group
type: array
ignore:
items:
type: object
type: array
key:
description: The attribute expression that should be matched on
type: string
match:
default: non-equal
enum:
- equal
- not-equal
- in
type: string
max-cardinality:
default: 1
title: ''
type: integer
missing-ok:
default: false
description: How to handle missing keys on elements, by default this causesresources
to be considered not-equal
type: boolean
type:
enum:
- network-location
value:
items:
type: string
type: array
required:
- key
- type
```

### Filter: offhour
<a name="filter-offhour"></a>
📌 **Description:**

----

Schedule offhours for resources see :ref:`offhours <offhours>`
for features and configuration.

📌 **Example Usage:**

```yaml
filters:
  - type: offhour
```

📌 **Schema:**

```yaml
------

properties:
default_tz:
type: string
fallback-schedule:
type: string
fallback_schedule:
type: string
offhour:
maximum: 23
minimum: 0
type: integer
opt-out:
type: boolean
skip-days:
items:
pattern: ^[0-9]{4}-[0-9]{2}-[0-9]{2}
type: string
type: array
skip-days-from:
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
tag:
type: string
type:
enum:
- offhour
weekends:
type: boolean
weekends-only:
type: boolean
required:
- offhour
- default_tz
- type
```

### Filter: onhour
<a name="filter-onhour"></a>
📌 **Description:**

----

Schedule offhours for resources see :ref:`offhours <offhours>`
for features and configuration.

📌 **Example Usage:**

```yaml
filters:
  - type: onhour
```

📌 **Schema:**

```yaml
------

properties:
default_tz:
type: string
fallback-schedule:
type: string
fallback_schedule:
type: string
onhour:
maximum: 23
minimum: 0
type: integer
opt-out:
type: boolean
skip-days:
items:
pattern: ^[0-9]{4}-[0-9]{2}-[0-9]{2}
type: string
type: array
skip-days-from:
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
tag:
type: string
type:
enum:
- onhour
weekends:
type: boolean
weekends-only:
type: boolean
required:
- onhour
- default_tz
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

### Filter: security-group
<a name="filter-security-group"></a>
📌 **Description:**

----

Filter a resource by its associated security groups.

📌 **Example Usage:**

```yaml
filters:
  - type: security-group
```

📌 **Schema:**

```yaml
------

properties:
default:
type: object
key:
type: string
match-resource:
type: boolean
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
operator:
enum:
- and
- or
type:
enum:
- security-group
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

### Filter: subnet
<a name="filter-subnet"></a>
📌 **Description:**

----

Filter a resource by its associated subnets attributes.

This filter is generally available for network attached resources.

ie. to find lambda functions that are vpc attached to subnets with
a tag key Location and value Database.

📌 **Example Usage:**

```yaml
policies:
- name: lambda
  resource: aws.lambda
  filters:
    - type: subnet
      key: tag:Location
      value: Database
```

<!-- It also supports finding resources on public or private subnets
via route table introspection to determine if the subnet is
associated to an internet gateway. -->

```yaml
policies:
 - name: public-ec2
   resource: aws.ec2
   filters:
     - type: subnet
       igw: True
       key: SubnetId
       value: present
```

📌 **Schema:**

```yaml
------

properties:
default:
type: object
igw:
enum:
- true
- false
key:
type: string
match-resource:
type: boolean
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
operator:
enum:
- and
- or
type:
enum:
- subnet
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

### Filter: taggable
<a name="filter-taggable"></a>
📌 **Description:**

----

Filter ECS resources on arn-format
https://docs.aws.amazon.com/AmazonECS/latest/userguide/ecs-resource-ids.html

📌 **Example Usage:**

```yaml
policies:
        - name: taggable
          resource: ecs-service
          filters:
            - type: taggable
              state: True
```

📌 **Schema:**

```yaml
------

properties:
state:
type: boolean
type:
enum:
- taggable
required:
- type
```

### Filter: task-definition
<a name="filter-task-definition"></a>
📌 **Description:**

----

Filter services by their task definitions.

:Example:

 Find any fargate services that are running with a particular
 image in the task and stop them.

📌 **Example Usage:**

```yaml
policies:
 - name: fargate-find-stop-image
   resource: ecs-task
   filters:
     - launchType: FARGATE
     - type: task-definition
       key: "containerDefinitions[].image"
       value: "elasticsearch/elasticsearch:6.4.3"
       value_type: swap
       op: contains
   actions:
     - type: stop
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
- task-definition
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
