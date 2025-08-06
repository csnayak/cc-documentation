import subprocess
import logging
import json
import re
from collections import defaultdict
import csv

# Configure logging
logging.basicConfig(
    filename="custodian_schema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



def generate_resource_groups_from_csv(csv_file):
    """
    Reads a CSV file with AWS resource types and their corresponding markdown files,
    then generates the RESOURCE_GROUPS dictionary.

    :param csv_file: Path to the CSV file
    :return: Dictionary mapping markdown files to their respective AWS resource types
    """
    resource_groups = defaultdict(list)

    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row

        for row in reader:
            if len(row) < 2:
                continue  # Skip invalid rows
            resource, markdown_file = row[0].strip(), row[1].strip()
            resource_groups[markdown_file].append(resource)

    return dict(resource_groups)


def run_custodian_schema(command):
    """Executes a Cloud Custodian schema command and returns its output."""
    try:
        logging.info(f"Executing: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as error:
        logging.error(f"Command execution failed: {error}")
        return None


def format_anchor(text):
    """Formats text into a valid Markdown anchor (GitHub-style)."""
    return re.sub(r"[^a-z0-9\-]", "", text.lower().replace(".", "-").replace("_", "-").replace(" ", "-"))


def get_filters_and_actions(resource):
    """Retrieves available filters and actions for a given AWS resource."""
    schema_output = run_custodian_schema(["custodian", "schema", resource])
    if not schema_output:
        logging.error(f"Failed to fetch filters/actions for {resource}")
        return [], []

    actions, filters = [], []
    section = None

    for line in schema_output.split("\n"):
        line = line.strip()
        if line.startswith("actions:"):
            section = "actions"
            continue
        elif line.startswith("filters:"):
            section = "filters"
            continue
        if section == "actions" and line.startswith("- "):
            actions.append(line[2:])
        elif section == "filters" and line.startswith("- "):
            filters.append(line[2:])

    logging.info(f"Extracted {len(actions)} actions and {len(filters)} filters for {resource}")
    return actions, filters


def get_schema_details(resource, category, name):
    """Fetches schema details for a specific filter or action."""
    command = ["custodian", "schema", f"{resource}.{category}.{name}"]
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
    """Generates Markdown & JSON documentation for AWS resources."""
    logging.info(f"Generating Markdown & JSON files: {file_name}")

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

    # Save Markdown
    with open(file_name, "w") as f:
        f.write(markdown_content)
    logging.info(f"✅ Markdown file generated: {file_name}")

    # Save JSON
    json_filename = file_name.replace(".md", ".json")
    with open(json_filename, "w") as f:
        json.dump(json_data, f, indent=4)
    logging.info(f"✅ JSON file generated: {json_filename}")


# Run the script
logging.info("Starting script execution...")

# dictionary of AWS resources
csv_file_path = "/vagrant/shared/chatbot/resourcetype.csv"
resource_groups = generate_resource_groups_from_csv(csv_file_path)
RESOURCE_GROUPS = resource_groups

for file_name, resources in RESOURCE_GROUPS.items():
    generate_markdown_and_json(file_name, resources)

print("✅ All Markdown & JSON files generated successfully!")
