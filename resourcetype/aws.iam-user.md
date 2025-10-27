---
Title: Aws.Iam User
Category: Cloud Custodian
Last Updated: 2025-10-27
Version: 0.9.47
Resource Type: aws.iam-user
---

# AWS.IAM-USER

AWS Resource Type: `aws.iam-user`


## Table of Contents
- [Available Actions](#available-actions)
- [Available Filters](#available-filters)
- [Action Details](#action-details)
- [Filter Details](#filter-details)

## Available Actions
- [auto-tag-user](#action-auto-tag-user)
- [copy-related-tag](#action-copy-related-tag)
- [delete](#action-delete)
- [delete-ssh-keys](#action-delete-ssh-keys)
- [invoke-lambda](#action-invoke-lambda)
- [invoke-sfn](#action-invoke-sfn)
- [mark-for-op](#action-mark-for-op)
- [notify](#action-notify)
- [post-finding](#action-post-finding)
- [post-item](#action-post-item)
- [put-metric](#action-put-metric)
- [remove-keys](#action-remove-keys)
- [remove-tag](#action-remove-tag)
- [set-boundary](#action-set-boundary)
- [set-groups](#action-set-groups)
- [set-policy](#action-set-policy)
- [tag](#action-tag)
- [webhook](#action-webhook)

## Available Filters
- [access-key](#filter-access-key)
- [check-permissions](#filter-check-permissions)
- [config-compliance](#filter-config-compliance)
- [credential](#filter-credential)
- [event](#filter-event)
- [finding](#filter-finding)
- [group](#filter-group)
- [has-inline-policy](#filter-has-inline-policy)
- [list-item](#filter-list-item)
- [login-profile](#filter-login-profile)
- [marked-for-op](#filter-marked-for-op)
- [mfa-device](#filter-mfa-device)
- [ops-item](#filter-ops-item)
- [policy](#filter-policy)
- [reduce](#filter-reduce)
- [ssh-key](#filter-ssh-key)
- [usage](#filter-usage)
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

Delete a user or properties of a user.

For example if you want to have a whitelist of valid (machine-)users
and want to ensure that no users have been clicked without documentation.

You can use both the 'credential' or the 'username'
filter. 'credential' will have an SLA of 4h,
(http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_getting-report.html),
but the added benefit of performing less API calls, whereas
'username' will make more API calls, but have a SLA of your cache.

📌 **Example Usage:**

<!-- # using a 'credential' filter'
- name: iam-only-whitelisted-users-credential
  resource: iam-user
  filters:
    - type: credential
      key: user
      op: not-in
      value:
        - valid-user-1
        - valid-user-2
  actions:
    - delete -->

<!-- # using a 'username' filter with 'UserName'
- name: iam-only-whitelisted-users-username
  resource: iam-user
  filters:
    - type: value
      key: UserName
      op: not-in
      value:
        - valid-user-1
        - valid-user-2
  actions:
    - delete -->

<!-- # using a 'username' filter with 'Arn'
- name: iam-only-whitelisted-users-arn
  resource: iam-user
  filters:
    - type: value
      key: Arn
      op: not-in
      value:
        - arn:aws:iam:123456789012:user/valid-user-1
        - arn:aws:iam:123456789012:user/valid-user-2
  actions:
    - delete -->

<!-- Additionally, you can specify the options to delete properties of an iam-user,
including console-access, access-keys, attached-user-policies,
inline-user-policies, mfa-devices, groups,
ssh-keys, signing-certificates, and service-specific-credentials. -->

<!-- Note: using options will _not_ delete the user itself, only the items specified
by ``options`` that are attached to the respective iam-user. To delete a user
completely, use the ``delete`` action without specifying ``options``. -->

<!-- - name: delete-console-access-unless-valid
      comment: |
        finds iam-users with console access and deletes console access unless
        the username is included in whitelist
      resource: iam-user
      filters:
        - type: value
          key: UserName
          op: not-in
          value:
            - valid-user-1
            - valid-user-2
        - type: credential
          key: password_enabled
          value: true
      actions:
        - type: delete
          options:
            - console-access -->

<!-- - name: delete-misc-access-for-iam-user
      comment: |
        deletes multiple options from test_user
      resource: iam-user
      filters:
        - UserName: test_user
      actions:
        - type: delete
          options:
            - mfa-devices
            - access-keys
            - ssh-keys -->

📌 **Schema:**

```yaml
------

properties:
options:
items:
enum:
- console-access
- access-keys
- attached-user-policies
- inline-user-policies
- mfa-devices
- groups
- ssh-keys
- signing-certificates
- service-specific-credentials
- user-policies
type: string
type: array
type:
enum:
- delete
required:
- type
```


### Action: delete-ssh-keys
<a name="action-delete-ssh-keys"></a>
📌 **Description:**

----

Delete or disable a user's SSH keys.

For example to delete keys after 90 days:

📌 **Example Usage:**

<!-- - name: iam-user-delete-ssh-keys
   resource: iam-user
   actions:
     - type: delete-ssh-keys -->

📌 **Schema:**

```yaml
------

properties:
disable:
type: boolean
matched:
type: boolean
type:
enum:
- delete-ssh-keys
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


### Action: remove-keys
<a name="action-remove-keys"></a>
📌 **Description:**

----

Delete or disable user's access keys.

For example if we wanted to disable keys 90 days after creation and
delete them 180 days after creation:

📌 **Example Usage:**

<!-- - name: iam-mfa-active-key-no-login
   resource: iam-user
   actions:
     - type: remove-keys
       disable: true
       age: 90
     - type: remove-keys
       age: 180 -->

📌 **Schema:**

```yaml
------

properties:
age:
type: number
disable:
type: boolean
matched:
type: boolean
type:
enum:
- remove-keys
required:
- type
```


### Action: remove-tag
<a name="action-remove-tag"></a>
📌 **Description:**

----

Remove tags from an iam user.

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


### Action: set-boundary
<a name="action-set-boundary"></a>
📌 **Description:**

----

Set IAM Permission boundary on an IAM Role or User.

A role or user can only have a single permission boundary set.

📌 **Example Usage:**

```yaml
actions:
  - type: set-boundary
```

📌 **Schema:**

```yaml
------

properties:
policy:
type: string
state:
enum:
- present
- absent
type:
enum:
- set-boundary
required:
- type
```


### Action: set-groups
<a name="action-set-groups"></a>
📌 **Description:**

----

Set a specific IAM user as added/removed from a group

📌 **Example Usage:**

<!-- - name: iam-user-add-remove
  resource: iam-user
  filters:
    - type: value
      key: UserName
      value: Bob
  actions:
    - type: set-groups
      state: remove
      group: Admin -->

📌 **Schema:**

```yaml
------

properties:
group:
type: string
state:
enum:
- add
- remove
type:
enum:
- set-groups
required:
- state
- group
- type
```


### Action: set-policy
<a name="action-set-policy"></a>
📌 **Description:**

----

Set a specific IAM policy as attached or detached on a user.

You will identify the policy by its arn.

Returns a list of roles modified by the action.

For example, if you want to automatically attach a single policy while
detaching all exisitng policies:

📌 **Example Usage:**

<!-- - name: iam-attach-user-policy
  resource: iam-user
  filters:
    - type: value
      key: UserName
      op: not-in
      value:
        - AdminUser1
        - AdminUser2
  actions:
    - type: set-policy
      state: detached
      arn: arn:aws:iam::aws:policy/AdministratorAccess -->

📌 **Schema:**

```yaml
------

properties:
arn:
type: string
state:
enum:
- attached
- detached
type:
enum:
- set-policy
required:
- state
- arn
- type
```


### Action: tag
<a name="action-tag"></a>
📌 **Description:**

----

Tag an iam user.

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

### Filter: access-key
<a name="filter-access-key"></a>
📌 **Description:**

----

Filter IAM users based on access-key values

By default multiple uses of this filter will match
on any user key satisfying either filter. To find
specific keys that match multiple access-key filters,
use `match-operator: and`

📌 **Example Usage:**

```yaml
policies:
  - name: iam-users-with-active-keys
    resource: iam-user
    filters:
      - type: access-key
        key: Status
        value: Active
      - type: access-key
        match-operator: and
        key: CreateDate
        value_type: age
        value: 90
```

📌 **Schema:**

```yaml
------

properties:
default:
type: object
key:
type: string
match-operator:
enum:
- and
- or
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
- access-key
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


### Filter: group
<a name="filter-group"></a>
📌 **Description:**

----

Filter IAM users based on attached group values

📌 **Example Usage:**

```yaml
policies:
  - name: iam-users-in-admin-group
    resource: iam-user
    filters:
      - type: group
        key: GroupName
        value: Admins
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
- group
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


### Filter: has-inline-policy
<a name="filter-has-inline-policy"></a>
📌 **Description:**

----

Filter IAM users that have an inline-policy attached

True: Filter users that have an inline-policy
False: Filter users that do not have an inline-policy

📌 **Example Usage:**

```yaml
filters:
  - type: has-inline-policy
```

📌 **Schema:**

```yaml
------

properties:
type:
enum:
- has-inline-policy
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


### Filter: login-profile
<a name="filter-login-profile"></a>
📌 **Description:**

----

Filter IAM users that have an associated login-profile

For quicker evaluation and reduced API traffic, it is recommended to
instead use the 'credential' filter with 'password_enabled': true when
a delay of up to four hours for credential report syncing is acceptable.

(https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_getting-report.html)

📌 **Example Usage:**

<!-- .. code-block: yaml -->

```yaml
policies:
  - name: iam-users-with-console-access
    resource: iam-user
    filters:
      - type: login-profile
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
- login-profile
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


### Filter: mfa-device
<a name="filter-mfa-device"></a>
📌 **Description:**

----

Filter iam-users based on mfa-device status

📌 **Example Usage:**

```yaml
policies:
  - name: mfa-enabled-users
    resource: iam-user
    filters:
      - type: mfa-device
        key: UserName
        value: not-null
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
- mfa-device
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


### Filter: policy
<a name="filter-policy"></a>
📌 **Description:**

----

Filter IAM users based on attached policy values

📌 **Example Usage:**

```yaml
policies:
  - name: iam-users-with-admin-access
    resource: iam-user
    filters:
      - type: policy
        key: PolicyName
        value: AdministratorAccess
        include-via: true
```

📌 **Schema:**

```yaml
------

properties:
default:
type: object
include-via:
type: boolean
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
- policy
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


### Filter: ssh-key
<a name="filter-ssh-key"></a>
📌 **Description:**

----

Filter IAM users based on uploaded SSH public keys

📌 **Example Usage:**

```yaml
policies:
  - name: iam-users-with-old-ssh-keys
    resource: iam-user
    filters:
      - type: ssh-key
        key: Status
        value: Active
      - type: ssh-key
        key: UploadDate
        value_type: age
        value: 90
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
- ssh-key
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


### Filter: usage
<a name="filter-usage"></a>
📌 **Description:**

----

Filter iam resources by their api/service usage.

Note recent activity (last 4hrs) may not be shown, evaluation
is against the last 365 days of data.

Each service access record is evaluated against all specified
attributes.  Attribute filters can be specified in short form k:v
pairs or in long form as a value type filter.

match-operator allows to specify how a resource is treated across
service access record matches. 'any' means a single matching
service record will return the policy resource as matching. 'all'
means all service access records have to match.


Find iam users that have not used any services in the last year

📌 **Example Usage:**

<!-- - name: usage-unused-users
resource: iam-user
filters:
  - type: usage
    match-operator: all
    LastAuthenticated: null -->

<!-- Find iam users that have used dynamodb in last 30 days -->

<!-- - name: unused-users
resource: iam-user
filters:
  - type: usage
    ServiceNamespace: dynamodb
    TotalAuthenticatedEntities: 1
    LastAuthenticated:
      type: value
      value_type: age
      op: less-than
      value: 30
    match-operator: any -->

<!-- https://aws.amazon.com/blogs/security/automate-analyzing-permissions-using-iam-access-advisor/ -->

📌 **Schema:**

```yaml
------

properties:
LastAuthenticated:
oneOf:
- type: string
- type: boolean
- type: number
- type: 'null'
- $ref: '#/definitions/filters/value'
LastAuthenticatedEntity:
oneOf:
- type: string
- type: boolean
- type: number
- type: 'null'
- $ref: '#/definitions/filters/value'
ServiceName:
oneOf:
- type: string
- type: boolean
- type: number
- type: 'null'
- $ref: '#/definitions/filters/value'
ServiceNamespace:
oneOf:
- type: string
- type: boolean
- type: number
- type: 'null'
- $ref: '#/definitions/filters/value'
TotalAuthenticatedEntities:
oneOf:
- type: string
- type: boolean
- type: number
- type: 'null'
- $ref: '#/definitions/filters/value'
match-operator:
enum:
- all
- any
poll-delay:
type: number
type:
enum:
- usage
required:
- match-operator
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

