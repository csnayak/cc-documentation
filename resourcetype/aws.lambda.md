---
Title: Aws.Lambda
Category: Cloud Custodian
Last Updated: 2025-10-27
Version: 0.9.47
Resource Type: aws.lambda
---

# AWS.LAMBDA

AWS Resource Type: `aws.lambda`


## Table of Contents
- [Available Actions](#available-actions)
- [Available Filters](#available-filters)
- [Action Details](#action-details)
- [Filter Details](#filter-details)

## Available Actions
- [auto-tag-user](#action-auto-tag-user)
- [copy-related-tag](#action-copy-related-tag)
- [delete](#action-delete)
- [invoke-lambda](#action-invoke-lambda)
- [invoke-sfn](#action-invoke-sfn)
- [mark-for-op](#action-mark-for-op)
- [modify-security-groups](#action-modify-security-groups)
- [notify](#action-notify)
- [post-finding](#action-post-finding)
- [post-item](#action-post-item)
- [put-metric](#action-put-metric)
- [remove-statements](#action-remove-statements)
- [remove-tag](#action-remove-tag)
- [rename-tag](#action-rename-tag)
- [set-concurrency](#action-set-concurrency)
- [set-xray-tracing](#action-set-xray-tracing)
- [tag](#action-tag)
- [trim-versions](#action-trim-versions)
- [update](#action-update)
- [webhook](#action-webhook)

## Available Filters
- [check-permissions](#filter-check-permissions)
- [config-compliance](#filter-config-compliance)
- [cost-optimization](#filter-cost-optimization)
- [cross-account](#filter-cross-account)
- [event](#filter-event)
- [event-source](#filter-event-source)
- [finding](#filter-finding)
- [has-specific-managed-policy](#filter-has-specific-managed-policy)
- [iam-analyzer](#filter-iam-analyzer)
- [kms-key](#filter-kms-key)
- [lambda-edge](#filter-lambda-edge)
- [list-item](#filter-list-item)
- [marked-for-op](#filter-marked-for-op)
- [metrics](#filter-metrics)
- [network-location](#filter-network-location)
- [ops-item](#filter-ops-item)
- [reduce](#filter-reduce)
- [reserved-concurrency](#filter-reserved-concurrency)
- [security-group](#filter-security-group)
- [subnet](#filter-subnet)
- [url-config](#filter-url-config)
- [value](#filter-value)
- [vpc](#filter-vpc)

## Action Details

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

Delete a lambda function (including aliases and older versions).

📌 **Example Usage:**

```yaml
policies:
      - name: lambda-delete-dotnet-functions
        resource: lambda
        filters:
          - Runtime: dotnetcore1.0
        actions:
          - delete
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

Tag resources for future action.

📌 **Example Usage:**

<!-- .. code-block :: yaml -->

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


### Action: modify-security-groups
<a name="action-modify-security-groups"></a>
📌 **Description:**

----

Common action for modifying security groups on a vpc attached resources.

Security groups for add or remove can be specified via group id or
name. Group removal also supports symbolic names such as
'matched', 'network-location' or 'all'. 'matched' uses the
annotations/output of the 'security-group' filter
filter. 'network-location' uses the annotations of the
'network-location' interface filter for `SecurityGroupMismatch`.

Note a vpc attached resource requires at least one security group,
this action will use the sg specified in `isolation-group` to ensure
resources always have at least one security-group.

type: modify-security-groups
    add: []
    remove: [] | matched | network-location
    isolation-group: sg-xyz
    add-by-tag: {}

📌 **Example Usage:**

```yaml
policies:
      - name: set-prod-security-groups
        resource: ec2
        filters:
          - type: value
            key: 'tag:env'
            value: 'prod'
        actions:
          - type: modify-security-groups
            add: prod-default-sg
            remove:
              - launch-wizard-1
              - launch-wizard-2
            add-by-tag:
              key: environment
              values:
                - production
```

📌 **Schema:**

```yaml
------

anyOf:
- required:
- isolation-group
- remove
- type
- required:
- add
- remove
- type
- required:
- add
- type
- required:
- add-by-tag
- type
properties:
add:
oneOf:
- type: string
- items:
type: string
type: array
add-by-tag:
additionalProperties: false
properties:
key:
type: string
values:
items:
type: string
type: array
required:
- key
- values
type: object
isolation-group:
oneOf:
- type: string
- items:
type: string
type: array
remove:
oneOf:
- items:
type: string
type: array
- enum:
- matched
- network-location
- all
- type: string
type:
enum:
- modify-security-groups
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

Action to remove policy/permission statements from lambda functions.

📌 **Example Usage:**

```yaml
policies:
      - name: lambda-remove-cross-accounts
        resource: lambda
        filters:
          - type: cross-account
        actions:
          - type: remove-statements
            statement_ids: matched
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
- remove-statements
required:
- statement_ids
- type
```


### Action: remove-tag
<a name="action-remove-tag"></a>
📌 **Description:**

----

Removes the specified tags from the specified resources.

📌 **Example Usage:**

```yaml
actions:
  - type: remove-tag
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


### Action: rename-tag
<a name="action-rename-tag"></a>
📌 **Description:**

----

Rename an existing tag key to a new value.

📌 **Example Usage:**

<!-- rename Application, and Bap to App, if a resource has both of the old keys
then we'll use the value specified by Application, which is based on the
order of values of old_keys. -->

<!-- .. code-block :: yaml -->

```yaml
policies:
    - name: rename-tags-example
      resource: aws.log-group
      filters:
        - or:
          - "tag:Bap": present
          - "tag:Application": present
      actions:
        - type: rename-tag
          old_keys: [Application, Bap]
          new_key: App
```

📌 **Schema:**

```yaml
------

properties:
new_key:
type: string
old_key:
type: string
old_keys:
items:
type: string
type: array
type:
enum:
- rename-tag
required:
- type
```


### Action: set-concurrency
<a name="action-set-concurrency"></a>
📌 **Description:**

----

Set lambda function concurrency to the desired level.

Can be used to set the reserved function concurrency to an exact value,
to delete reserved concurrency, or to set the value to an attribute of
the resource.

📌 **Example Usage:**

```yaml
actions:
  - type: set-concurrency
```

📌 **Schema:**

```yaml
------

properties:
expr:
type: boolean
type:
enum:
- set-concurrency
value:
oneOf:
- type: string
- type: integer
- type: 'null'
required:
- value
```


### Action: set-xray-tracing
<a name="action-set-xray-tracing"></a>
📌 **Description:**

----

This action allows for enable Xray tracing to Active

📌 **Example Usage:**

<!-- actions:
- type: enable-xray-tracing -->

📌 **Schema:**

```yaml
------

properties:
state:
default: true
type: boolean
type:
enum:
- set-xray-tracing
required:
- type
```


### Action: tag
<a name="action-tag"></a>
📌 **Description:**

----

Applies one or more tags to the specified resources.

📌 **Example Usage:**

<!-- .. code-block :: yaml -->

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


### Action: trim-versions
<a name="action-trim-versions"></a>
📌 **Description:**

----

Delete old versions of a function.

By default this will only remove the non $LATEST
version of a function that are not referenced by
an alias. Optionally it can delete only versions
older than a given age.

📌 **Example Usage:**

```yaml
policies:
   - name: lambda-gc
     resource: aws.lambda
     actions:
       - type: trim-versions
         exclude-aliases: true  # default true
         older-than: 60 # default not-set
         retain-latest: true # default false
```

<!-- retain-latest refers to whether the latest numeric
version will be retained, the $LATEST alias will
still point to the last revision even without this set,
so this is safe wrt to the function availability, its more
about desire to retain an explicit version of the current
code, rather than just the $LATEST alias pointer which will
be automatically updated. -->

📌 **Schema:**

```yaml
------

properties:
exclude-aliases:
default: true
type: boolean
older-than:
type: number
retain-latest:
default: true
type: boolean
type:
enum:
- trim-versions
required:
- type
```


### Action: update
<a name="action-update"></a>
📌 **Description:**

----

Update a lambda's configuration.

This action also has specific support for enacting recommendations
from the AWS Cost Optimization Hub for resizing.

📌 **Example Usage:**

```yaml
policies:
   - name: lambda-rightsize
     resource: aws.lambda
     filters:
       - type: cost-optimization
         attrs:
           - actionType: Rightsize
     actions:
       - update
```

📌 **Schema:**

```yaml
------

properties:
properties:
type: object
type:
enum:
- update
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


## Filter Details

### Filter: check-permissions
<a name="filter-check-permissions"></a>
📌 **Description:**

----

Check IAM permissions associated with a resource.

📌 **Example Usage:**

<!-- Find users that can create other users -->

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

<!-- Find users with access to all services and actions -->

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

<!-- By default permission boundaries are checked. -->

📌 **Schema:**

```yaml
------

properties:
actions:
items:
type: string
type: array
boundaries:
type: boolean
match:
oneOf:
- enum:
- allowed
- denied
- $ref: '#/definitions/filters/valuekv'
- $ref: '#/definitions/filters/value'
match-operator:
enum:
- and
- or
type:
enum:
- check-permissions
required:
- actions
- match
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


### Filter: cross-account
<a name="filter-cross-account"></a>
📌 **Description:**

----

Filters lambda functions with cross-account permissions

The whitelist parameter can be used to prevent certain accounts
from being included in the results (essentially stating that these
accounts permissions are allowed to exist)

This can be useful when combining this filter with the delete action.

📌 **Example Usage:**

```yaml
policies:
      - name: lambda-cross-account
        resource: lambda
        filters:
          - type: cross-account
            whitelist:
              - 'IAM-Policy-Cross-Account-Access'
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
return_allowed:
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


### Filter: event-source
<a name="filter-event-source"></a>
📌 **Description:**

----

No help is available for this item.

📌 **Example Usage:**

```yaml
filters:
  - type: event-source
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
- event-source
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


### Filter: has-specific-managed-policy
<a name="filter-has-specific-managed-policy"></a>
📌 **Description:**

----

Filter an lambda function that has an IAM execution role that has a
specific managed IAM policy.

📌 **Example Usage:**

```yaml
policies:
  - name: lambda-has-admin-policy
    resource: aws.lambda
    filters:
      - type: has-specific-managed-policy
        value: admin-policy
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
- has-specific-managed-policy
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


### Filter: kms-key
<a name="filter-kms-key"></a>
📌 **Description:**

----

Filter a resource by its associated kms key and optionally the aliasname
of the kms key by using 'c7n:AliasName'

📌 **Example Usage:**

<!-- Match a specific key alias: -->

```yaml
policies:
        - name: dms-encrypt-key-check
          resource: dms-instance
          filters:
            - type: kms-key
              key: "c7n:AliasName"
              value: alias/aws/dms
```

<!-- Or match against native key attributes such as ``KeyManager``, which
more explicitly distinguishes between ``AWS`` and ``CUSTOMER``-managed
keys. The above policy can also be written as: -->

```yaml
policies:
        - name: dms-aws-managed-key
          resource: dms-instance
          filters:
            - type: kms-key
              key: KeyManager
              value: AWS
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
- kms-key
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


### Filter: lambda-edge
<a name="filter-lambda-edge"></a>
📌 **Description:**

----

Filter for lambda@edge functions. Lambda@edge only exists in us-east-1

📌 **Example Usage:**

```yaml
policies:
        - name: lambda-edge-filter
          resource: lambda
          region: us-east-1
          filters:
            - type: lambda-edge
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
- lambda-edge
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


### Filter: reserved-concurrency
<a name="filter-reserved-concurrency"></a>
📌 **Description:**

----

No help is available for this item.

📌 **Example Usage:**

```yaml
filters:
  - type: reserved-concurrency
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
- reserved-concurrency
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
associated to an internet gateway or a nat gateway. -->

```yaml
policies:
 - name: public-ec2
   resource: aws.ec2
   filters:
     - type: subnet
       operator: or
       igw: True
       nat: True
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
nat:
enum:
- true
- false
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


### Filter: url-config
<a name="filter-url-config"></a>
📌 **Description:**

----

No help is available for this item.

📌 **Example Usage:**

```yaml
filters:
  - type: url-config
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
- url-config
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


### Filter: vpc
<a name="filter-vpc"></a>
📌 **Description:**

----

Filter a resource by its associated vpc.

📌 **Example Usage:**

```yaml
filters:
  - type: vpc
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
- vpc
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

