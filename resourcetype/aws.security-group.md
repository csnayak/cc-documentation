---
Title: Aws.Security Group
Category: Cloud Custodian
Last Updated: 2025-10-27
Version: 0.9.47
Resource Type: aws.security-group
---

# AWS.SECURITY-GROUP

AWS Resource Type: `aws.security-group`


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
- [normalize-tag](#action-normalize-tag)
- [notify](#action-notify)
- [patch](#action-patch)
- [post-finding](#action-post-finding)
- [post-item](#action-post-item)
- [put-metric](#action-put-metric)
- [remove-permissions](#action-remove-permissions)
- [remove-tag](#action-remove-tag)
- [rename-tag](#action-rename-tag)
- [set-permissions](#action-set-permissions)
- [tag](#action-tag)
- [tag-trim](#action-tag-trim)
- [webhook](#action-webhook)

## Available Filters
- [config-compliance](#filter-config-compliance)
- [default-vpc](#filter-default-vpc)
- [diff](#filter-diff)
- [egress](#filter-egress)
- [event](#filter-event)
- [finding](#filter-finding)
- [ingress](#filter-ingress)
- [list-item](#filter-list-item)
- [marked-for-op](#filter-marked-for-op)
- [ops-item](#filter-ops-item)
- [reduce](#filter-reduce)
- [stale](#filter-stale)
- [tag-count](#filter-tag-count)
- [unused](#filter-unused)
- [used](#filter-used)
- [value](#filter-value)

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

Action to delete security group(s)

It is recommended to apply a filter to the delete policy to avoid the
deletion of all security groups returned.

📌 **Example Usage:**

```yaml
policies:
      - name: security-groups-unused-delete
        resource: security-group
        filters:
          - type: unused
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

The optional 'tz' parameter can be used to adjust the clock to align
with a given timezone. The default value is 'utc'.

If neither 'days' nor 'hours' is specified, Cloud Custodian will default
to marking the resource for action 4 days in the future.

.. code-block :: yaml

  policies:
    - name: ec2-mark-for-stop-in-future
      resource: ec2
      filters:
        - type: value
          key: Name
          value: instance-to-stop-in-four-days
      actions:
        - type: mark-for-op
          op: stop

📌 **Example Usage:**

```yaml
actions:
  - type: mark-for-op
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


### Action: normalize-tag
<a name="action-normalize-tag"></a>
📌 **Description:**

----

Transform the value of a tag.

Set the tag value to uppercase, title, lowercase, or strip text
from a tag key.

.. code-block :: yaml

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

📌 **Example Usage:**

```yaml
actions:
  - type: normalize-tag
```

📌 **Schema:**

```yaml
------

properties:
action:
items:
enum:
- upper
- lower
- titlestrip
- replace
type: string
key:
type: string
type:
enum:
- normalize-tag
value:
type: string
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


### Action: patch
<a name="action-patch"></a>
📌 **Description:**

----

Modify a resource via application of a reverse delta.

📌 **Example Usage:**

```yaml
actions:
  - type: patch
```

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- patch
required:
- type
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


### Action: remove-permissions
<a name="action-remove-permissions"></a>
📌 **Description:**

----

Action to remove ingress/egress rule(s) from a security group

📌 **Example Usage:**

```yaml
policies:
      - name: security-group-revoke-8080
        resource: security-group
        filters:
          - type: ingress
            IpProtocol: tcp
            Ports: [8080]
        actions:
          - type: remove-permissions
            ingress: matched
```

📌 **Schema:**

```yaml
------

properties:
egress:
enum:
- matched
- all
type: string
ingress:
enum:
- matched
- all
type: string
type:
enum:
- remove-permissions
required:
- type
```


### Action: remove-tag
<a name="action-remove-tag"></a>
📌 **Description:**

----

Remove tags from ec2 resources.

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

Create a new tag with identical value & remove old tag

📌 **Example Usage:**

```yaml
actions:
  - type: rename-tag
```

📌 **Schema:**

```yaml
------

properties:
new_key:
type: string
old_key:
type: string
type:
enum:
- rename-tag
required:
- type
```


### Action: set-permissions
<a name="action-set-permissions"></a>
📌 **Description:**

----

Action to add/remove ingress/egress rule(s) to a security group

📌 **Example Usage:**

```yaml
policies:
 - name: ops-access-via
   resource: aws.security-group
   filters:
     - type: ingress
       IpProtocol: "-1"
       Ports: [22, 3389]
       Cidr: "0.0.0.0/0"
   actions:
    - type: set-permissions
      # remove the permission matched by a previous ingress filter.
      remove-ingress: matched
      # remove permissions by specifying them fully, ie remove default outbound
      # access.
      remove-egress:
         - IpProtocol: "-1"
           Cidr: "0.0.0.0/0"
```

<!-- # add a list of permissions to the group.
      add-ingress:
        # full syntax/parameters to authorize can be used.
        - IpPermissions:
           - IpProtocol: TCP
             FromPort: 22
             ToPort: 22
             IpRanges:
               - Description: Ops SSH Access
                 CidrIp: "1.1.1.1/32"
               - Description: Security SSH Access
                 CidrIp: "2.2.2.2/32"
      # add a list of egress permissions to a security group
      add-egress:
         - IpProtocol: "TCP"
           FromPort: 5044
           ToPort: 5044
           CidrIp: "192.168.1.2/32" -->

📌 **Schema:**

```yaml
------

properties:
add-egress:
items:
minProperties: 1
type: object
type: array
add-ingress:
items:
minProperties: 1
type: object
type: array
remove-egress:
oneOf:
- enum:
- all
- matched
- items:
minProperties: 2
type: object
type: array
remove-ingress:
oneOf:
- enum:
- all
- matched
- items:
minProperties: 2
type: object
type: array
type:
enum:
- set-permissions
required:
- type
```


### Action: tag
<a name="action-tag"></a>
📌 **Description:**

----

Tag an ec2 resource.

📌 **Example Usage:**

```yaml
actions:
  - type: tag
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


### Action: tag-trim
<a name="action-tag-trim"></a>
📌 **Description:**

----

Automatically remove tags from an ec2 resource.

EC2 Resources have a limit of 50 tags, in order to make
additional tags space on a set of resources, this action can
be used to remove enough tags to make the desired amount of
space while preserving a given set of tags.

.. code-block :: yaml

   policies:
     - name: ec2-tag-trim
       comment: |
         Any instances with 48 or more tags get tags removed until
         they match the target tag count, in this case 47 so we
         that we free up a tag slot for another usage.
       resource: ec2
       filters:
             # Filter down to resources which already have 8 tags
             # as we need space for 3 more, this also ensures that
             # metrics reporting is correct for the policy.
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

📌 **Example Usage:**

```yaml
actions:
  - type: tag-trim
```

📌 **Schema:**

```yaml
------

properties:
preserve:
items:
type: string
type: array
space:
type: integer
type:
enum:
- tag-trim
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


### Filter: default-vpc
<a name="filter-default-vpc"></a>
📌 **Description:**

----

Filter that returns any security group that exists within the default vpc

📌 **Example Usage:**

```yaml
policies:
      - name: security-group-default-vpc
        resource: security-group
        filters:
          - default-vpc
```

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- default-vpc
required:
- type
```


### Filter: diff
<a name="filter-diff"></a>
📌 **Description:**

----

Compute the diff from the current resource to a previous version.

A resource matches the filter if a diff exists between the current
resource and the selected revision.

Utilizes config as a resource revision database.

Revisions can be selected by date, against the previous version, and
against a locked version (requires use of is-locked filter).

📌 **Example Usage:**

```yaml
filters:
  - type: diff
```

📌 **Schema:**

```yaml
------

properties:
selector:
enum:
- previous
- date
- locked
selector_value:
type: string
type:
enum:
- diff
required:
- type
```


### Filter: egress
<a name="filter-egress"></a>
📌 **Description:**

----

Filter for verifying security group ingress and egress permissions

All attributes of a security group permission are available as
value filters.

If multiple attributes are specified the permission must satisfy
all of them. Note that within an attribute match against a list value
of a permission we default to or.

If a group has any permissions that match all conditions, then it
matches the filter.

Permissions that match on the group are annotated onto the group and
can subsequently be used by the remove-permission action.

We have specialized handling for matching `Ports` in ingress/egress
permission From/To range. The following example matches on ingress
rules which allow for a range that includes all of the given ports.

📌 **Example Usage:**

<!-- - type: ingress
Ports: [22, 443, 80] -->

<!-- As well for verifying that a rule only allows for a specific set of ports
as in the following example. The delta between this and the previous
example is that if the permission allows for any ports not specified here,
then the rule will match. ie. OnlyPorts is a negative assertion match,
it matches when a permission includes ports outside of the specified set. -->

<!-- - type: ingress
OnlyPorts: [22] -->

<!-- For simplifying ipranges handling which is specified as a list on a rule
we provide a `Cidr` key which can be used as a value type filter evaluated
against each of the rules. If any iprange cidr match then the permission
matches. -->

<!-- - type: ingress
IpProtocol: -1
FromPort: 445 -->

<!-- We also have specialized handling for matching self-references in
ingress/egress permissions. The following example matches on ingress
rules which allow traffic its own same security group. -->

<!-- - type: ingress
SelfReference: True -->

<!-- As well for assertions that a ingress/egress permission only matches
a given set of ports, *note* OnlyPorts is an inverse match. -->

<!-- - type: egress
OnlyPorts: [22, 443, 80] -->

<!-- - type: egress
Cidr:
  value_type: cidr
  op: in
  value: x.y.z -->

<!-- `value_type: cidr` can also filter if cidr is a subset of cidr
value range. In this example we are allowing any smaller cidrs within
allowed_cidrs.csv. -->

<!-- - type: ingress
Cidr:
  value_type: cidr
  op: not-in
  value_from:
    url: s3://a-policy-data-us-west-2/allowed_cidrs.csv
    format: csv -->

<!-- or value can be specified as a list. -->

<!-- - type: ingress
Cidr:
  value_type: cidr
  op: not-in
  value: ["10.0.0.0/8", "192.168.0.0/16"] -->

<!-- `Cidr` can match ipv4 rules and `CidrV6` can match ipv6 rules.  In
this example we are blocking global inbound connections to SSH or
RDP. -->

<!-- - or:
- type: ingress
  Ports: [22, 3389]
  Cidr:
    value: "0.0.0.0/0"
- type: ingress
  Ports: [22, 3389]
  CidrV6:
    value: "::/0" -->

<!-- `SGReferences` can be used to filter out SG references in rules.
In this example we want to block ingress rules that reference a SG
that is tagged with `Access: Public`. -->

<!-- - type: ingress
SGReferences:
  key: "tag:Access"
  value: "Public"
  op: equal -->

<!-- We can also filter SG references based on the VPC that they are
within. In this example we want to ensure that our outbound rules
that reference SGs are only referencing security groups within a
specified VPC. -->

<!-- - type: egress
SGReferences:
  key: 'VpcId'
  value: 'vpc-11a1a1aa'
  op: equal -->

<!-- Likewise, we can also filter SG references by their description.
For example, we can prevent egress rules from referencing any
SGs that have a description of "default - DO NOT USE". -->

<!-- - type: egress
SGReferences:
  key: 'Description'
  value: 'default - DO NOT USE'
  op: equal -->

<!-- By default, this filter matches a security group rule if
_all_ of its keys match. Using `match-operator: or` causes a match
if _any_ key matches. This can help consolidate some simple
cases that would otherwise require multiple filters. To find
security groups that allow all inbound traffic over IPv4 or IPv6,
for example, we can use two filters inside an `or` block: -->

<!-- - or:
- type: ingress
  Cidr: "0.0.0.0/0"
- type: ingress
  CidrV6: "::/0" -->

<!-- or combine them into a single filter: -->

<!-- - type: ingress
match-operator: or
  Cidr: "0.0.0.0/0"
  CidrV6: "::/0" -->

<!-- Note that evaluating _combinations_ of factors (e.g. traffic over
port 22 from 0.0.0.0/0) still requires separate filters. -->

📌 **Schema:**

```yaml
------

properties:
Cidr: {}
CidrV6: {}
Description: {}
FromPort:
oneOf:
- $ref: '#/definitions/filters/value'
- type: integer
IpProtocol:
oneOf:
- enum:
- '-1'
- -1
- tcp
- udp
- icmp
- icmpv6
- $ref: '#/definitions/filters/value'
IpRanges: {}
OnlyPorts:
items:
type: integer
type: array
Ports:
items:
type: integer
type: array
PrefixListIds: {}
SGReferences: {}
SelfReference:
type: boolean
ToPort:
oneOf:
- $ref: '#/definitions/filters/value'
- type: integer
UserIdGroupPairs: {}
match-operator:
enum:
- or
- and
type: string
type:
enum:
- egress
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


### Filter: ingress
<a name="filter-ingress"></a>
📌 **Description:**

----

Filter for verifying security group ingress and egress permissions

All attributes of a security group permission are available as
value filters.

If multiple attributes are specified the permission must satisfy
all of them. Note that within an attribute match against a list value
of a permission we default to or.

If a group has any permissions that match all conditions, then it
matches the filter.

Permissions that match on the group are annotated onto the group and
can subsequently be used by the remove-permission action.

We have specialized handling for matching `Ports` in ingress/egress
permission From/To range. The following example matches on ingress
rules which allow for a range that includes all of the given ports.

📌 **Example Usage:**

<!-- - type: ingress
Ports: [22, 443, 80] -->

<!-- As well for verifying that a rule only allows for a specific set of ports
as in the following example. The delta between this and the previous
example is that if the permission allows for any ports not specified here,
then the rule will match. ie. OnlyPorts is a negative assertion match,
it matches when a permission includes ports outside of the specified set. -->

<!-- - type: ingress
OnlyPorts: [22] -->

<!-- For simplifying ipranges handling which is specified as a list on a rule
we provide a `Cidr` key which can be used as a value type filter evaluated
against each of the rules. If any iprange cidr match then the permission
matches. -->

<!-- - type: ingress
IpProtocol: -1
FromPort: 445 -->

<!-- We also have specialized handling for matching self-references in
ingress/egress permissions. The following example matches on ingress
rules which allow traffic its own same security group. -->

<!-- - type: ingress
SelfReference: True -->

<!-- As well for assertions that a ingress/egress permission only matches
a given set of ports, *note* OnlyPorts is an inverse match. -->

<!-- - type: egress
OnlyPorts: [22, 443, 80] -->

<!-- - type: egress
Cidr:
  value_type: cidr
  op: in
  value: x.y.z -->

<!-- `value_type: cidr` can also filter if cidr is a subset of cidr
value range. In this example we are allowing any smaller cidrs within
allowed_cidrs.csv. -->

<!-- - type: ingress
Cidr:
  value_type: cidr
  op: not-in
  value_from:
    url: s3://a-policy-data-us-west-2/allowed_cidrs.csv
    format: csv -->

<!-- or value can be specified as a list. -->

<!-- - type: ingress
Cidr:
  value_type: cidr
  op: not-in
  value: ["10.0.0.0/8", "192.168.0.0/16"] -->

<!-- `Cidr` can match ipv4 rules and `CidrV6` can match ipv6 rules.  In
this example we are blocking global inbound connections to SSH or
RDP. -->

<!-- - or:
- type: ingress
  Ports: [22, 3389]
  Cidr:
    value: "0.0.0.0/0"
- type: ingress
  Ports: [22, 3389]
  CidrV6:
    value: "::/0" -->

<!-- `SGReferences` can be used to filter out SG references in rules.
In this example we want to block ingress rules that reference a SG
that is tagged with `Access: Public`. -->

<!-- - type: ingress
SGReferences:
  key: "tag:Access"
  value: "Public"
  op: equal -->

<!-- We can also filter SG references based on the VPC that they are
within. In this example we want to ensure that our outbound rules
that reference SGs are only referencing security groups within a
specified VPC. -->

<!-- - type: egress
SGReferences:
  key: 'VpcId'
  value: 'vpc-11a1a1aa'
  op: equal -->

<!-- Likewise, we can also filter SG references by their description.
For example, we can prevent egress rules from referencing any
SGs that have a description of "default - DO NOT USE". -->

<!-- - type: egress
SGReferences:
  key: 'Description'
  value: 'default - DO NOT USE'
  op: equal -->

<!-- By default, this filter matches a security group rule if
_all_ of its keys match. Using `match-operator: or` causes a match
if _any_ key matches. This can help consolidate some simple
cases that would otherwise require multiple filters. To find
security groups that allow all inbound traffic over IPv4 or IPv6,
for example, we can use two filters inside an `or` block: -->

<!-- - or:
- type: ingress
  Cidr: "0.0.0.0/0"
- type: ingress
  CidrV6: "::/0" -->

<!-- or combine them into a single filter: -->

<!-- - type: ingress
match-operator: or
  Cidr: "0.0.0.0/0"
  CidrV6: "::/0" -->

<!-- Note that evaluating _combinations_ of factors (e.g. traffic over
port 22 from 0.0.0.0/0) still requires separate filters. -->

📌 **Schema:**

```yaml
------

properties:
Cidr: {}
CidrV6: {}
Description: {}
FromPort:
oneOf:
- $ref: '#/definitions/filters/value'
- type: integer
IpProtocol:
oneOf:
- enum:
- '-1'
- -1
- tcp
- udp
- icmp
- icmpv6
- $ref: '#/definitions/filters/value'
IpRanges: {}
OnlyPorts:
items:
type: integer
type: array
Ports:
items:
type: integer
type: array
PrefixListIds: {}
SGReferences: {}
SelfReference:
type: boolean
ToPort:
oneOf:
- $ref: '#/definitions/filters/value'
- type: integer
UserIdGroupPairs: {}
match-operator:
enum:
- or
- and
type: string
type:
enum:
- ingress
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


### Filter: stale
<a name="filter-stale"></a>
📌 **Description:**

----

Filter to find security groups that contain stale references
to other groups that are either no longer present or traverse
a broken vpc peering connection. Note this applies to VPC
Security groups only and will implicitly filter security groups.

AWS Docs:
  https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-security-groups.html

📌 **Example Usage:**

```yaml
policies:
      - name: stale-security-groups
        resource: security-group
        filters:
          - stale
```

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- stale
required:
- type
```


### Filter: tag-count
<a name="filter-tag-count"></a>
📌 **Description:**

----

Simplify tag counting..

ie. these two blocks are equivalent

.. code-block :: yaml

   - filters:
       - type: value
         op: gte
         count: 8

   - filters:
       - type: tag-count
         count: 8

📌 **Example Usage:**

```yaml
filters:
  - type: tag-count
```

📌 **Schema:**

```yaml
------

properties:
count:
minimum: 0
type: integer
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
- tag-count
required:
- type
```


### Filter: unused
<a name="filter-unused"></a>
📌 **Description:**

----

Filter to just vpc security groups that are not used.

We scan all extant enis in the vpc to get a baseline set of groups
in use. Then augment with those referenced by launch configs, and
lambdas as they may not have extant resources in the vpc at a
given moment. We also find any security group with references from
other security group either within the vpc or across peered
connections. Also checks cloud watch event targeting ecs.

Checks - enis, lambda, launch-configs, sg rule refs, and ecs cwe
targets.

Note this filter does not support classic security groups atm.

📌 **Example Usage:**

```yaml
policies:
      - name: security-groups-unused
        resource: security-group
        filters:
          - unused
```

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- unused
required:
- type
```


### Filter: used
<a name="filter-used"></a>
📌 **Description:**

----

Filter to security groups that are used.
This operates as a complement to the unused filter for multi-step
workflows.

📌 **Example Usage:**

```yaml
policies:
      - name: security-groups-in-use
        resource: security-group
        filters:
          - used
```

```yaml
policies:
      - name: security-groups-used-by-rds
        resource: security-group
        filters:
          - used
          - type: value
            key: c7n:InstanceOwnerIds
            op: intersect
            value:
              - amazon-rds
```

```yaml
policies:
      - name: security-groups-used-by-natgw
        resource: security-group
        filters:
          - used
          - type: value
            key: c7n:InterfaceTypes
            op: intersect
            value:
              - nat_gateway
```

```yaml
policies:
      - name: security-groups-used-by-alb
        resource: security-group
        filters:
          - used
          - type: value
            key: c7n:InterfaceResourceTypes
            op: intersect
            value:
              - elb-app
```

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- used
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

