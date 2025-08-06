import subprocess
import re
import logging

# Configure logging
logging.basicConfig(
    filename="custodian_schema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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

def get_all_resources():
    """Fetch all resource types from Cloud Custodian schema."""
    logging.info("Fetching all resource types...")
    command = ["/vagrant/custodian-env/bin/custodian", "schema"]
    output = run_custodian_schema(command)

    if not output:
        logging.error("Failed to fetch resource types.")
        return []

    resources = []
    capturing = False
    for line in output.split("\n"):
        line = line.strip()
        if line.startswith("resources:"):
            capturing = True
            continue
        if capturing and line.startswith("- "):
            resources.append(line[2:])  # Remove '- ' prefix

    logging.info(f"Extracted {len(resources)} resources.")
    return resources

def get_schema_details(resource_type, category, name):
    """Fetch details for a specific filter or action."""
    logging.info(f"Fetching details for {category}: {name} in {resource_type}")
    command = ["/vagrant/custodian-env/bin/custodian", "schema", f"{resource_type}.{category}.{name}"]
    output = run_custodian_schema(command)

    if not output:
        logging.error(f"Failed to fetch details for {resource_type}.{category}.{name}")
        return None, None

    help_section = ""
    schema_section = ""
    capturing_help = False
    capturing_schema = False

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
            help_section += line + "\n"
        elif capturing_schema:
            schema_section += line + "\n"

    return help_section.strip(), schema_section.strip()

def generate_markdown(resources):
    """Formats extracted Cloud Custodian schema into Markdown with ToC."""
    logging.info("Generating Markdown documentation...")
    markdown_content = "# Cloud Custodian Documentation\n\n"

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

        schema_text = run_custodian_schema(["/vagrant/custodian-env/bin/custodian", "schema", resource])
        if not schema_text:
            logging.error(f"Skipping {resource} due to missing schema.")
            continue

        actions, filters = [], []
        current_section = None

        for line in schema_text.split("\n"):
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

        # Adding actions to the resource section
        markdown_content += "## Available Actions\n\n"
        for action in actions:
            action_link = f"{resource}-actions-{action}"
            markdown_content += f"- [{action}](#{action_link})\n"

        # Adding filters to the resource section
        markdown_content += "\n## Available Filters\n\n"
        for filter_name in filters:
            filter_link = f"{resource}-filters-{filter_name}"
            markdown_content += f"- [{filter_name}](#{filter_link})\n"

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
resources = get_all_resources()
if resources:
    markdown_doc = generate_markdown(resources)

    # Save to Markdown file
    with open("cloud_custodian_full.md", "w") as f:
        f.write(markdown_doc)

    logging.info("Markdown documentation generated: cloud_custodian_full.md")
    print(f"✅ Markdown documentation generated: cloud_custodian_full.md")
else:
    logging.error("No resources found. Markdown not generated.")
