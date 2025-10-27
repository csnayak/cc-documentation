---
Title: Aws.Ec2
Category: Cloud Custodian
Last Updated: 2025-10-27
Version: 0.9.47
Resource Type: aws.ec2
---

# AWS.EC2

AWS Resource Type: `aws.ec2`


## Table of Contents
- [Available Actions](#available-actions)
- [Available Filters](#available-filters)
- [Action Details](#action-details)
- [Filter Details](#filter-details)

## Available Actions
- [auto-tag-user](#action-auto-tag-user)
- [autorecover-alarm](#action-autorecover-alarm)
- [copy-related-tag](#action-copy-related-tag)
- [invoke-lambda](#action-invoke-lambda)
- [invoke-sfn](#action-invoke-sfn)
- [mark-for-op](#action-mark-for-op)
- [modify-security-groups](#action-modify-security-groups)
- [normalize-tag](#action-normalize-tag)
- [notify](#action-notify)
- [post-finding](#action-post-finding)
- [post-item](#action-post-item)
- [propagate-spot-tags](#action-propagate-spot-tags)
- [put-metric](#action-put-metric)
- [reboot](#action-reboot)
- [remove-tag](#action-remove-tag)
- [rename-tag](#action-rename-tag)
- [resize](#action-resize)
- [send-command](#action-send-command)
- [set-instance-profile](#action-set-instance-profile)
- [set-metadata-access](#action-set-metadata-access)
- [set-monitoring](#action-set-monitoring)
- [snapshot](#action-snapshot)
- [start](#action-start)
- [stop](#action-stop)
- [tag](#action-tag)
- [tag-trim](#action-tag-trim)
- [terminate](#action-terminate)
- [webhook](#action-webhook)

## Available Filters
- [check-permissions](#filter-check-permissions)
- [config-compliance](#filter-config-compliance)
- [cost-optimization](#filter-cost-optimization)
- [default-vpc](#filter-default-vpc)
- [ebs](#filter-ebs)
- [ephemeral](#filter-ephemeral)
- [event](#filter-event)
- [finding](#filter-finding)
- [has-specific-managed-policy](#filter-has-specific-managed-policy)
- [health-event](#filter-health-event)
- [image](#filter-image)
- [image-age](#filter-image-age)
- [instance-age](#filter-instance-age)
- [instance-attribute](#filter-instance-attribute)
- [instance-uptime](#filter-instance-uptime)
- [list-item](#filter-list-item)
- [marked-for-op](#filter-marked-for-op)
- [metrics](#filter-metrics)
- [network-location](#filter-network-location)
- [offhour](#filter-offhour)
- [onhour](#filter-onhour)
- [ops-item](#filter-ops-item)
- [reduce](#filter-reduce)
- [security-group](#filter-security-group)
- [singleton](#filter-singleton)
- [ssm](#filter-ssm)
- [ssm-compliance](#filter-ssm-compliance)
- [ssm-inventory](#filter-ssm-inventory)
- [state-age](#filter-state-age)
- [stop-protected](#filter-stop-protected)
- [subnet](#filter-subnet)
- [tag-count](#filter-tag-count)
- [termination-protected](#filter-termination-protected)
- [user-data](#filter-user-data)
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


### Action: autorecover-alarm
<a name="action-autorecover-alarm"></a>
📌 **Description:**

----

Adds a cloudwatch metric alarm to recover an EC2 instance.

This action takes effect on instances that are NOT part
of an ASG.

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-autorecover-alarm
    resource: ec2
    filters:
      - singleton
    actions:
      - autorecover-alarm
```

<!-- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-recover.html -->

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- autorecover-alarm
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


### Action: modify-security-groups
<a name="action-modify-security-groups"></a>
📌 **Description:**

----

Modify security groups on an instance.

📌 **Example Usage:**

```yaml
actions:
  - type: modify-security-groups
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


### Action: propagate-spot-tags
<a name="action-propagate-spot-tags"></a>
📌 **Description:**

----

Propagate Tags that are set at Spot Request level to EC2 instances.

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-spot-instances
    resource: ec2
    filters:
      - State.Name: pending
      - instanceLifecycle: spot
    actions:
      - type: propagate-spot-tags
        only_tags:
          - Name
          - BillingTag
```

📌 **Schema:**

```yaml
------

properties:
only_tags:
items:
type: string
type: array
type:
enum:
- propagate-spot-tags
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


### Action: reboot
<a name="action-reboot"></a>
📌 **Description:**

----

Reboots a previously running EC2 instance.

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-reboot-instances
    resource: ec2
    query:
      - instance-state-name: running
    actions:
      - reboot
```

<!-- http://docs.aws.amazon.com/cli/latest/reference/ec2/reboot-instances.html -->

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- reboot
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


### Action: resize
<a name="action-resize"></a>
📌 **Description:**

----

Change an instance's size.

An instance can only be resized when its stopped, this action
can optionally stop/start an instance if needed to effect the instance
type change. Instances are always left in the run state they were
found in.

There are a few caveats to be aware of, instance resizing
needs to maintain compatibility for architecture, virtualization type
hvm/pv, and ebs optimization at minimum.

http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-resize.html

This action also has specific support for enacting recommendations
from the AWS Cost Optimization Hub for resizing.

📌 **Example Usage:**

```yaml
policies:
   - name: ec2-rightsize
     resource: aws.ec2
     filters:
       - type: cost-optimization
         attrs:
          - actionType: Rightsize
     actions:
       - resize
```

📌 **Schema:**

```yaml
------

properties:
default:
type: string
restart:
type: boolean
type:
enum:
- resize
type-map:
type: object
required:
- type
```


### Action: send-command
<a name="action-send-command"></a>
📌 **Description:**

----

Run an SSM Automation Document on an instance.

:Example:

Find ubuntu 18.04 instances are active with ssm.

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-osquery-install
    resource: ec2
    filters:
      - type: ssm
        key: PingStatus
        value: Online
      - type: ssm
        key: PlatformName
        value: Ubuntu
      - type: ssm
        key: PlatformVersion
        value: 18.04
    actions:
      - type: send-command
        command:
          DocumentName: AWS-RunShellScript
          Parameters:
            commands:
              - wget https://pkg.osquery.io/deb/osquery_3.3.0_1.linux.amd64.deb
              - dpkg -i osquery_3.3.0_1.linux.amd64.deb
```

📌 **Schema:**

```yaml
------

properties:
command:
type: object
type:
enum:
- send-command
required:
- command
```


### Action: set-instance-profile
<a name="action-set-instance-profile"></a>
📌 **Description:**

----

Sets (add, modify, remove) the instance profile for a running EC2 instance.

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: set-default-instance-profile
    resource: ec2
    filters:
      - IamInstanceProfile: absent
    actions:
      - type: set-instance-profile
        name: default
```

<!-- https://docs.aws.amazon.com/cli/latest/reference/ec2/associate-iam-instance-profile.html
https://docs.aws.amazon.com/cli/latest/reference/ec2/disassociate-iam-instance-profile.html -->

📌 **Schema:**

```yaml
------

properties:
name:
type: string
type:
enum:
- set-instance-profile
required:
- type
```


### Action: set-metadata-access
<a name="action-set-metadata-access"></a>
📌 **Description:**

----

Set instance metadata server access for an instance.

📌 **Example Usage:**

<!-- Require instances to use IMDSv2 -->

```yaml
policies:
 - name: ec2-require-imdsv2
   resource: ec2
   filters:
     - MetadataOptions.HttpTokens: optional
   actions:
     - type: set-metadata-access
       tokens: required
```

<!-- Disable metadata server access -->

<!-- .. code-block: yaml -->

```yaml
policies:
 - name: ec2-disable-imds
   resource: ec2
   filters:
     - MetadataOptions.HttpEndpoint: enabled
   actions:
     - type: set-metadata-access
       endpoint: disabled
```

```yaml
policies:
 - name: ec2-enable-metadata-tags
   resource: ec2
   filters:
     - MetadataOptions.InstanceMetadataTags: disabled
   actions:
     - type: set-metadata-access
       metadata-tags: enabled
```

<!-- Reference: https://amzn.to/2XOuxpQ -->

📌 **Schema:**

```yaml
------

properties:
anyOf:
- required:
- endpoint
- required:
- tokens
- required:
- metadatatags
- required:
- hop-limit
endpoint:
enum:
- enabled
- disabled
hop-limit:
maximum: 64
minimum: 1
type: integer
metadata-tags:
enum:
- enabled
- disabled
tokens:
enum:
- required
- optional
type:
enum:
- set-metadata-access
required:
- type
```


### Action: set-monitoring
<a name="action-set-monitoring"></a>
📌 **Description:**

----

Action on EC2 Instances to enable/disable detailed monitoring

The different states of detailed monitoring status are :
'disabled'|'disabling'|'enabled'|'pending'
(https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances)

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-detailed-monitoring-activation
    resource: ec2
    filters:
      - Monitoring.State: disabled
    actions:
      - type: set-monitoring
        state: enable
```

<!-- References -->

<!-- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-cloudwatch-new.html -->

📌 **Schema:**

```yaml
------

properties:
state:
enum:
- enable
- disable
type:
enum:
- set-monitoring
required:
- type
```


### Action: snapshot
<a name="action-snapshot"></a>
📌 **Description:**

----

Snapshot the volumes attached to an EC2 instance.

Tags may be optionally added to the snapshot during creation.

- `copy-volume-tags` copies all the tags from the specified
  volume to the corresponding snapshot.
- `copy-tags` copies the listed tags from each volume
  to the snapshot.  This is mutually exclusive with
  `copy-volume-tags`.
- `tags` allows new tags to be added to each snapshot when using
  'copy-tags`.  If no tags are specified, then the tag
  `custodian_snapshot` is added.

The default behavior is `copy-volume-tags: true`.

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-snapshots
    resource: ec2
    actions:
      - type: snapshot
        copy-tags:
          - Name
        tags:
            custodian_snapshot: True
```

📌 **Schema:**

```yaml
------

properties:
copy-tags:
items:
type: string
type: array
copy-volume-tags:
type: boolean
exclude-boot:
default: false
type: boolean
tags:
type: object
type:
enum:
- snapshot
required:
- type
```


### Action: start
<a name="action-start"></a>
📌 **Description:**

----

Starts a previously stopped EC2 instance.

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-start-stopped-instances
    resource: ec2
    query:
      - instance-state-name: stopped
    actions:
      - start
```

<!-- http://docs.aws.amazon.com/cli/latest/reference/ec2/start-instances.html -->

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- start
required:
- type
```


### Action: stop
<a name="action-stop"></a>
📌 **Description:**

----

Stops or hibernates a running EC2 instances

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-stop-running-instances
    resource: ec2
    query:
      - instance-state-name: running
    actions:
      - stop
```

<!-- - name: ec2-hibernate-instances
    resources: ec2
    query:
      - instance-state-name: running
    actions:
      - type: stop
        hibernate: true -->

<!-- Note when using hiberate, instances not configured for hiberation
will just be stopped. -->

📌 **Schema:**

```yaml
------

properties:
force:
type: boolean
hibernate:
type: boolean
terminate-ephemeral:
type: boolean
type:
enum:
- stop
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


### Action: terminate
<a name="action-terminate"></a>
📌 **Description:**

----

Terminate a set of instances.

While ec2 offers a bulk delete api, any given instance can be configured
with api deletion termination protection, so we can't use the bulk call
reliabily, we need to process the instances individually. Additionally
If we're configured with 'force' then we'll turn off instance termination
and stop protection.

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-process-termination
    resource: ec2
    filters:
      - type: marked-for-op
        op: terminate
    actions:
      - terminate
```

📌 **Schema:**

```yaml
------

properties:
force:
type: boolean
type:
enum:
- terminate
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


### Filter: default-vpc
<a name="filter-default-vpc"></a>
📌 **Description:**

----

Matches if an ec2 database is in the default vpc

📌 **Example Usage:**

```yaml
filters:
  - type: default-vpc
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


### Filter: ebs
<a name="filter-ebs"></a>
📌 **Description:**

----

EC2 instances with EBS backed volume

Filters EC2 instances with EBS backed storage devices (non ephemeral)

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-encrypted-ebs-volumes
    resource: ec2
    filters:
      - type: ebs
        key: Encrypted
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
operator:
enum:
- and
- or
skip-devices:
items:
type: string
type: array
type:
enum:
- ebs
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


### Filter: ephemeral
<a name="filter-ephemeral"></a>
📌 **Description:**

----

EC2 instances with ephemeral storage

Filters EC2 instances that have ephemeral storage (an instance-store backed
root device)

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-ephemeral-instances
    resource: ec2
    filters:
      - type: ephemeral
```

<!-- http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html -->

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- ephemeral
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


### Filter: has-specific-managed-policy
<a name="filter-has-specific-managed-policy"></a>
📌 **Description:**

----

Filter an EC2 instance that has an IAM instance profile that contains an IAM role that has
   a specific managed IAM policy. If an EC2 instance does not have a profile or the profile
   does not contain an IAM role, then it will be treated as not having the policy.

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-instance-has-admin-policy
    resource: aws.ec2
    filters:
      - type: has-specific-managed-policy
        value: admin-policy
```

<!-- Check for EC2 instances with instance profile roles that have an
attached policy matching a given list: -->

```yaml
policies:
  - name: ec2-instance-with-selected-policies
    resource: aws.ec2
    filters:
      - type: has-specific-managed-policy
        op: in
        value:
          - AmazonS3FullAccess
          - AWSOrganizationsFullAccess
```

<!-- Check for EC2 instances with instance profile roles that have
attached policy names matching a pattern: -->

```yaml
policies:
  - name: ec2-instance-with-full-access-policies
    resource: aws.ec2
    filters:
      - type: has-specific-managed-policy
        op: glob
        value: "*FullAccess"
```

<!-- Check for EC2 instances with instance profile roles that have
attached policy ARNs matching a pattern: -->

```yaml
policies:
  - name: ec2-instance-with-aws-full-access-policies
    resource: aws.ec2
    filters:
      - type: has-specific-managed-policy
        key: PolicyArn
        op: regex
        value: "arn:aws:iam::aws:policy/.*FullAccess"
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


### Filter: health-event
<a name="filter-health-event"></a>
📌 **Description:**

----

Check if there are operations health events (phd) related to the resources

https://aws.amazon.com/premiumsupport/technology/personal-health-dashboard/

Health events are stored as annotation on a resource.

Custodian also supports responding to phd events via a lambda execution mode.

📌 **Example Usage:**

```yaml
filters:
  - type: health-event
```

📌 **Schema:**

```yaml
------

properties:
category:
items:
enum:
- issue
- accountNotification
- scheduledChange
type: array
statuses:
items:
enum:
- open
- upcoming
- closed
type: string
type: array
type:
enum:
- health-event
types:
items:
type: string
type: array
required:
- type
```


### Filter: image
<a name="filter-image"></a>
📌 **Description:**

----

No help is available for this item.

📌 **Example Usage:**

```yaml
filters:
  - type: image
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
- image
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


### Filter: image-age
<a name="filter-image-age"></a>
📌 **Description:**

----

EC2 AMI age filter

Filters EC2 instances based on the age of their AMI image (in days)

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-ancient-ami
    resource: ec2
    filters:
      - type: image-age
        op: ge
        days: 90
```

📌 **Schema:**

```yaml
------

properties:
days:
type: number
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
- image-age
required:
- type
```


### Filter: instance-age
<a name="filter-instance-age"></a>
📌 **Description:**

----

Filters instances based on their age (in days)

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-30-days-plus
    resource: ec2
    filters:
      - type: instance-age
        op: ge
        days: 30
```

📌 **Schema:**

```yaml
------

properties:
days:
type: number
hours:
type: number
minutes:
type: number
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
- instance-age
required:
- type
```


### Filter: instance-attribute
<a name="filter-instance-attribute"></a>
📌 **Description:**

----

EC2 Instance Value Filter on a given instance attribute.

Filters EC2 Instances with the given instance attribute

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-unoptimized-ebs
    resource: ec2
    filters:
      - type: instance-attribute
        attribute: ebsOptimized
        key: "Value"
        value: false
```

📌 **Schema:**

```yaml
------

properties:
attribute:
enum:
- instanceType
- kernel
- ramdisk
- userData
- disableApiTermination
- instanceInitiatedShutdownBehavior
- rootDeviceName
- blockDeviceMapping
- productCodes
- sourceDestCheck
- groupSet
- ebsOptimized
- sriovNetSupport
- enaSupport
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
- instance-attribute
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
- attribute
```


### Filter: instance-uptime
<a name="filter-instance-uptime"></a>
📌 **Description:**

----

Automatically filter resources older than a given date.

**Deprecated** use a value filter with `value_type: age` which can be
done on any attribute.

📌 **Example Usage:**

```yaml
filters:
  - type: instance-uptime
```

📌 **Schema:**

```yaml
------

properties:
days:
type: number
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
- instance-uptime
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

Custodian OffHour filter

Filters running EC2 instances with the intent to stop at a given hour of
the day. A list of days to excluded can be included as a list of strings
with the format YYYY-MM-DD. Alternatively, the list (using the same syntax)
can be taken from a specified url.

Note: You can disable filtering of only running instances by setting
`state-filter: false`

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: offhour-evening-stop
    resource: ec2
    filters:
      - type: offhour
        tag: custodian_downtime
        default_tz: et
        offhour: 20
    actions:
      - stop
```

<!-- - name: offhour-evening-stop-skip-holidays
    resource: ec2
    filters:
      - type: offhour
        tag: custodian_downtime
        default_tz: et
        offhour: 20
        skip-days: ['2017-12-25']
    actions:
      - stop -->

<!-- - name: offhour-evening-stop-skip-holidays-from
    resource: ec2
    filters:
      - type: offhour
        tag: custodian_downtime
        default_tz: et
        offhour: 20
        skip-days-from:
          expr: 0
          format: csv
          url: 's3://location/holidays.csv'
    actions:
      - stop -->

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
state-filter:
type: boolean
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
- type
```


### Filter: onhour
<a name="filter-onhour"></a>
📌 **Description:**

----

Custodian OnHour filter

Filters stopped EC2 instances with the intent to start at a given hour of
the day. A list of days to excluded can be included as a list of strings
with the format YYYY-MM-DD. Alternatively, the list (using the same syntax)
can be taken from a specified url.

Note: You can disable filtering of only stopped instances by setting
`state-filter: false`

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: onhour-morning-start
    resource: ec2
    filters:
      - type: onhour
        tag: custodian_downtime
        default_tz: et
        onhour: 6
    actions:
      - start
```

<!-- - name: onhour-morning-start-skip-holidays
    resource: ec2
    filters:
      - type: onhour
        tag: custodian_downtime
        default_tz: et
        onhour: 6
        skip-days: ['2017-12-25']
    actions:
      - start -->

<!-- - name: onhour-morning-start-skip-holidays-from
    resource: ec2
    filters:
      - type: onhour
        tag: custodian_downtime
        default_tz: et
        onhour: 6
        skip-days-from:
          expr: 0
          format: csv
          url: 's3://location/holidays.csv'
    actions:
      - start -->

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
state-filter:
type: boolean
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


### Filter: singleton
<a name="filter-singleton"></a>
📌 **Description:**

----

EC2 instances without autoscaling or a recover alarm

Filters EC2 instances that are not members of an autoscaling group
and do not have Cloudwatch recover alarms.

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-recover-instances
    resource: ec2
    filters:
      - singleton
    actions:
      - type: tag
        key: problem
        value: instance is not resilient
```

<!-- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-recover.html -->

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- singleton
required:
- type
```


### Filter: ssm
<a name="filter-ssm"></a>
📌 **Description:**

----

Filter ec2 instances by their ssm status information.

:Example:

Find ubuntu 18.04 instances are active with ssm.

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-ssm-check
    resource: ec2
    filters:
      - type: ssm
        key: PingStatus
        value: Online
      - type: ssm
        key: PlatformName
        value: Ubuntu
      - type: ssm
        key: PlatformVersion
        value: 18.04
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
- ssm
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


### Filter: ssm-compliance
<a name="filter-ssm-compliance"></a>
📌 **Description:**

----

Filter ec2 instances by their ssm compliance status.

:Example:

Find non-compliant ec2 instances.

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-ssm-compliance
    resource: ec2
    filters:
      - type: ssm-compliance
        compliance_types:
          - Association
          - Patch
        severity:
          - CRITICAL
          - HIGH
          - MEDIUM
          - LOW
          - UNSPECIFIED
        states:
          - NON_COMPLIANT
        eval_filters:
         - type: value
           key: ExecutionSummary.ExecutionTime
           value_type: age
           value: 30
           op: less-than
```

📌 **Schema:**

```yaml
------

properties:
compliance_types:
items:
type: string
type: array
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
severity:
items:
type: string
type: array
states:
default:
- NON_COMPLIANT
items:
enum:
- COMPLIANT
- NON_COMPLIANT
type: array
type:
enum:
- ssm-compliance
required:
- compliance_types
- type
```


### Filter: ssm-inventory
<a name="filter-ssm-inventory"></a>
📌 **Description:**

----

Filter EC2 instances by their SSM software inventory.

:Example:

Find instances that have a specific package installed.

📌 **Example Usage:**

```yaml
policies:
- name: ec2-find-specific-package
  resource: ec2
  filters:
  - type: ssm-inventory
    query:
    - Key: Name
      Values:
      - "docker"
      Type: Equal
```

<!-- - name: ec2-get-all-packages
  resource: ec2
  filters:
  - type: ssm-inventory -->

📌 **Schema:**

```yaml
------

properties:
query:
items:
properties:
Key:
type: string
Type:
enum:
- Equal
- NotEqual
- BeginWith
- LessThan
- GreaterThan
- Exists
Values:
items:
type: string
type: array
required:
- Key
- Values
type: object
type: array
type:
enum:
- ssm-inventory
required:
- type
```


### Filter: state-age
<a name="filter-state-age"></a>
📌 **Description:**

----

Age an instance has been in the given state.

📌 **Example Usage:**

```yaml
policies:
  - name: ec2-state-running-7-days
    resource: ec2
    filters:
      - type: state-age
        op: ge
        days: 7
```

📌 **Schema:**

```yaml
------

properties:
days:
type: number
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
- state-age
required:
- type
```


### Filter: stop-protected
<a name="filter-stop-protected"></a>
📌 **Description:**

----

EC2 instances with ``disableApiStop`` attribute set

Filters EC2 instances with ``disableApiStop`` attribute set to true.

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: stop-protection-enabled
    resource: ec2
    filters:
      - type: stop-protected
```

<!-- :Example: -->

```yaml
policies:
  - name: stop-protection-NOT-enabled
    resource: ec2
    filters:
      - not:
        - type: stop-protected
```

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- stop-protected
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


### Filter: termination-protected
<a name="filter-termination-protected"></a>
📌 **Description:**

----

EC2 instances with ``disableApiTermination`` attribute set

Filters EC2 instances with ``disableApiTermination`` attribute set to true.

:Example:

📌 **Example Usage:**

```yaml
policies:
  - name: termination-protection-enabled
    resource: ec2
    filters:
      - type: termination-protected
```

<!-- :Example: -->

```yaml
policies:
  - name: termination-protection-NOT-enabled
    resource: ec2
    filters:
      - not:
        - type: termination-protected
```

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- termination-protected
required:
- type
```


### Filter: user-data
<a name="filter-user-data"></a>
📌 **Description:**

----

Filter on EC2 instances which have matching userdata.
Note: It is highly recommended to use regexes with the ?sm flags, since Custodian
uses re.match() and userdata spans multiple lines.

📌 **Example Usage:**

```yaml
policies:
      - name: ec2_userdata_stop
        resource: ec2
        filters:
          - type: user-data
            op: regex
            value: (?smi).*password=
        actions:
          - stop
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
- user-data
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

