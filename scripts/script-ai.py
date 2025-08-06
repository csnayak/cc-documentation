import subprocess
import logging
import json
import re
from collections import defaultdict

# Configure logging
logging.basicConfig(
    filename="custodian_schema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Logical grouping of AWS resources
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
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running command: {e}")
        return None

def format_anchor(text):
    """Formats text into a valid Markdown anchor (GitHub-style)."""
    return re.sub(r'[^a-z0-9\-]', '', text.lower().replace(".", "-").replace("_", "-").replace(" ", "-"))

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

def generate_markdown_and_json(file_name, resources):
    """Generates Markdown & JSON documentation with filters and actions."""
    logging.info(f"Generating Markdown & JSON files: {file_name}")
    
    # Add AI-friendly metadata
    markdown_content = f"""---
Title: {file_name.replace('.md', '').replace('-', ' ').title()}
Category: {file_name.replace('.md', '').replace('-', ' ').title()}
Last Updated: 2025-02-23
Version: 1.0
---

# Cloud Custodian Documentation - {file_name.replace('.md', '').replace('-', ' ').title()}

## 📌 Table of Contents
"""

    json_data = {}

    for resource in resources:
        resource_anchor = format_anchor(resource)
        markdown_content += f"- [{resource}](#{resource_anchor})\n"

    for resource in resources:
        logging.info(f"Processing resource: {resource}")
        resource_anchor = format_anchor(resource)
        markdown_content += f"\n<a id='{resource_anchor}'></a>\n\n"
        markdown_content += f"# {resource.upper()}\n\n"
        markdown_content += f"## Overview\n\nCloud Custodian policies for `{resource}` allow managing cloud resources using various filters and actions.\n\n"

        actions, filters = get_filters_and_actions(resource)
        json_data[resource] = {"filters": {}, "actions": {}}

        markdown_content += "## Available Actions\n\n"
        for action in actions:
            action_anchor = format_anchor(f"{resource}-actions-{action}")
            markdown_content += f"- [{action}](#{action_anchor})\n"

        markdown_content += "\n## Available Filters\n\n"
        for filter_name in filters:
            filter_anchor = format_anchor(f"{resource}-filters-{filter_name}")
            markdown_content += f"- [{filter_name}](#{filter_anchor})\n"

        markdown_content += "\n## Filter Details\n\n"
        for filter_name in filters:
            filter_anchor = format_anchor(f"{resource}-filters-{filter_name}")
            help_text, schema_text = get_schema_details(resource, "filters", filter_name)
            markdown_content += f"<a id='{filter_anchor}'></a>\n\n"
            markdown_content += f"### {filter_name}\n\n"
            markdown_content += f"**📌 Description:**\n```\n{help_text}\n```\n\n"
            markdown_content += f"**📌 Schema:**\n```yaml\n{schema_text}\n```\n\n"
            json_data[resource]["filters"][filter_name] = {"description": help_text, "schema": schema_text}

        markdown_content += "\n## Action Details\n\n"
        for action in actions:
            action_anchor = format_anchor(f"{resource}-actions-{action}")
            help_text, schema_text = get_schema_details(resource, "actions", action)
            markdown_content += f"<a id='{action_anchor}'></a>\n\n"
            markdown_content += f"### {action}\n\n"
            markdown_content += f"**📌 Description:**\n```\n{help_text}\n```\n\n"
            markdown_content += f"**📌 Schema:**\n```yaml\n{schema_text}\n```\n\n"
            json_data[resource]["actions"][action] = {"description": help_text, "schema": schema_text}

    with open(file_name, "w") as f:
        f.write(markdown_content)
    logging.info(f"✅ Markdown file generated: {file_name}")

    json_filename = file_name.replace(".md", ".json")
    with open(json_filename, "w") as f:
        json.dump(json_data, f, indent=4)
    logging.info(f"✅ JSON file generated: {json_filename}")

# Run the script
logging.info("Starting script execution...")

for file_name, resources in resource_groups.items():
    generate_markdown_and_json(file_name, resources)

print(f"✅ All Markdown & JSON files generated successfully!")
