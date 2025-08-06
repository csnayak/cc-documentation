import subprocess
import logging
from collections import defaultdict

# Configure logging
logging.basicConfig(
    filename="custodian_schema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Logical grouping of AWS resources
# resource_groups = {
#     "aws-compute.md": ["aws.ec2", "aws.lambda", "aws.batch-compute", "aws.eks", "aws.elasticbeanstalk"],
#     "aws-storage.md": ["aws.s3", "aws.ebs", "aws.efs", "aws.glacier", "aws.fsx", "aws.backup-plan"],
#     "aws-database.md": ["aws.rds", "aws.dynamodb-table", "aws.redshift", "aws.timestream-database", "aws.qldb"],
#     "aws-networking.md": ["aws.vpc", "aws.route-table", "aws.nat-gateway", "aws.elb", "aws.transit-gateway"],
#     "aws-security.md": ["aws.iam-role", "aws.iam-user", "aws.guardduty-finding", "aws.security-group", "aws.waf"],
#     "aws-monitoring.md": ["aws.cloudwatch-dashboard", "aws.event-rule", "aws.config-rule", "aws.cloudtrail", "aws.health-event"],
# }

resource_groups = {
    "aws-compute.md": [
        "aws.ec2", "aws.ec2-capacity-reservation", "aws.ec2-host", "aws.ec2-reserved",
        "aws.ec2-spot-fleet-request", "aws.batch-compute", "aws.batch-definition",
        "aws.batch-queue", "aws.lambda", "aws.lambda-layer", "aws.eks",
        "aws.eks-nodegroup", "aws.elasticbeanstalk", "aws.elasticbeanstalk-environment",
        "aws.lightsail-instance", "aws.appstream-fleet", "aws.appstream-stack", "aws.asg"
    ],
    "aws-storage.md": [
        "aws.s3", "aws.s3-access-point", "aws.s3-access-point-multi", "aws.s3-directory",
        "aws.s3-storage-lens", "aws.ebs", "aws.ebs-snapshot", "aws.efs", "aws.efs-mount-target",
        "aws.glacier", "aws.fsx", "aws.fsx-backup", "aws.backup-plan", "aws.backup-vault"
    ],
    "aws-database.md": [
        "aws.rds", "aws.rds-cluster", "aws.rds-cluster-param-group", "aws.rds-cluster-snapshot",
        "aws.rds-param-group", "aws.rds-proxy", "aws.rds-reserved", "aws.rds-snapshot",
        "aws.rds-subnet-group", "aws.rds-subscription", "aws.dynamodb-table", "aws.dynamodb-stream",
        "aws.dynamodb-backup", "aws.redshift", "aws.redshift-reserved", "aws.redshift-snapshot",
        "aws.redshift-subnet-group", "aws.timestream-database", "aws.timestream-influxdb",
        "aws.timestream-table", "aws.qldb", "aws.memorydb", "aws.memorydb-acl",
        "aws.memorydb-snapshot", "aws.memorydb-subnet-group", "aws.memorydb-user"
    ],
    "aws-networking.md": [
        "aws.vpc", "aws.vpc-endpoint", "aws.route-table", "aws.nat-gateway", "aws.subnet",
        "aws.transit-gateway", "aws.transit-attachment", "aws.vpn-connection", "aws.vpn-gateway",
        "aws.internet-gateway", "aws.directconnect", "aws.globalaccelerator", "aws.elb",
        "aws.app-elb", "aws.app-elb-target-group", "aws.cloudfront", "aws.streaming-distribution",
        "aws.hostedzone", "aws.rrset", "aws.firewall", "aws.network-acl", "aws.network-addr",
        "aws.networkmanager-core", "aws.networkmanager-device", "aws.networkmanager-global",
        "aws.networkmanager-link", "aws.networkmanager-site", "aws.prefix-list",
        "aws.origin-access-control"
    ]
}


def run_custodian_schema(command):
    """Runs a Cloud Custodian schema command and returns its output."""
    try:
        logging.info(f"Running command: {' '.join(command)}")
        result = subprocess.run(
            command, capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running command: {e}")
        return None

def get_filters_and_actions(resource):
    """Fetch available filters and actions for a resource."""
    schema_output = run_custodian_schema(["/vagrant/custodian-env/bin/custodian", "schema", resource])

    if not schema_output:
        logging.error(f"Failed to fetch filters/actions for {resource}")
        return [], []

    actions, filters = [], []
    current_section = None

    for line in schema_output.split("\n"):
        line = line.strip()
        if line.startswith("actions:"):
            current_section = "actions"
            continue
        elif line.startswith("filters:"):
            current_section = "filters"
            continue

        if current_section == "actions" and line.startswith("- "):
            actions.append(line[2:])
        elif current_section == "filters" and line.startswith("- "):
            filters.append(line[2:])

    logging.info(f"Extracted {len(actions)} actions and {len(filters)} filters for {resource}")
    return actions, filters

def get_schema_details(resource, category, name):
    """Fetch details for a specific filter or action."""
    command = ["/vagrant/custodian-env/bin/custodian", "schema", f"{resource}.{category}.{name}"]
    output = run_custodian_schema(command)

    if not output:
        logging.error(f"Failed to fetch details for {resource}.{category}.{name}")
        return None, None

    help_text, schema_text = "", ""
    capturing_help, capturing_schema = False, False

    for line in output.split("\n"):
        line = line.strip()

        if line.startswith("Help"):
            capturing_help = True
            capturing_schema = False
            continue
        elif line.startswith("Schema"):
            capturing_schema = True
            capturing_help = False
            continue

        if capturing_help:
            help_text += line + "\n"
        elif capturing_schema:
            schema_text += line + "\n"

    return help_text.strip(), schema_text.strip()

def generate_markdown(file_name, resources):
    """Generates structured Markdown documentation with filters and actions."""
    logging.info(f"Generating Markdown file: {file_name}")
    markdown_content = f"# Cloud Custodian Documentation - {file_name.replace('.md', '').replace('-', ' ').title()}\n\n"

    # Table of Contents
    markdown_content += "## Table of Contents\n\n"
    for resource in resources:
        resource_link = resource.replace(".", "-")
        markdown_content += f"- [{resource}](#{resource_link})\n"

    # Process each resource
    for resource in resources:
        logging.info(f"Processing resource: {resource}")
        markdown_content += f"\n# {resource.upper()}\n\n"
        markdown_content += f"## Overview\n\nCloud Custodian policies for `{resource}` allow managing cloud resources using various filters and actions.\n\n"

        # Get available filters and actions
        actions, filters = get_filters_and_actions(resource)

        # Adding actions
        markdown_content += "## Available Actions\n\n"
        if actions:
            for action in actions:
                action_link = f"{resource}-actions-{action}"
                markdown_content += f"- [{action}](#{action_link})\n"
        else:
            markdown_content += "No actions available.\n"

        # Adding filters
        markdown_content += "\n## Available Filters\n\n"
        if filters:
            for filter_name in filters:
                filter_link = f"{resource}-filters-{filter_name}"
                markdown_content += f"- [{filter_name}](#{filter_link})\n"
        else:
            markdown_content += "No filters available.\n"

        # Individual Filter Details
        markdown_content += "\n## Filter Details\n\n"
        for filter_name in filters:
            filter_link = f"{resource}-filters-{filter_name}"
            help_text, schema_text = get_schema_details(resource, "filters", filter_name)
            markdown_content += f"### <a name='{filter_link}'></a> {filter_name}\n\n"
            markdown_content += f"**Description:**\n```\n{help_text}\n```\n\n"
            markdown_content += f"**Schema:**\n```\n{schema_text}\n```\n\n"

        # Individual Action Details
        markdown_content += "\n## Action Details\n\n"
        for action in actions:
            action_link = f"{resource}-actions-{action}"
            help_text, schema_text = get_schema_details(resource, "actions", action)
            markdown_content += f"### <a name='{action_link}'></a> {action}\n\n"
            markdown_content += f"**Description:**\n```\n{help_text}\n```\n\n"
            markdown_content += f"**Schema:**\n```\n{schema_text}\n```\n\n"

    return markdown_content

# Run the script
logging.info("Starting script execution...")

for file_name, resources in resource_groups.items():
    markdown_doc = generate_markdown(file_name, resources)

    # Save to Markdown file
    with open(file_name, "w") as f:
        f.write(markdown_doc)

    logging.info(f"✅ Markdown file generated: {file_name}")
    print(f"✅ Markdown file generated: {file_name}")
