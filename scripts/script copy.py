import subprocess
import re
import json

def run_custodian_schema(command):
    """Runs a Cloud Custodian schema command and returns its output."""
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return None

def get_schema_details(resource_type, category, name):
    """Fetch details for a specific filter or action."""
    command = ["/vagrant/custodian-env/bin/custodian", "schema", f"{resource_type}.{category}.{name}"]
    output = run_custodian_schema(command)

    if not output:
        return None

    # Extract Help Section
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

def generate_markdown(resource_type, actions, filters):
    """Formats extracted Cloud Custodian schema into Markdown."""
    markdown_content = f"# Cloud Custodian Documentation - {resource_type.upper()}\n\n"
    
    markdown_content += f"## Overview\n\n"
    markdown_content += f"Cloud Custodian policies for `{resource_type}` allow managing resources with various filters and actions.\n\n"

    markdown_content += "## Available Actions\n\n"
    for action in actions:
        markdown_content += f"- **{action}**\n"

    markdown_content += "\n## Available Filters\n\n"
    for filter_name in filters:
        markdown_content += f"- **{filter_name}**\n"

    # Fetch individual filter details
    markdown_content += "\n## Filter Details\n\n"
    for filter_name in filters:
        help_text, schema_text = get_schema_details(resource_type, "filters", filter_name)
        markdown_content += f"### **{filter_name}**\n\n"
        markdown_content += f"**Description:**\n```\n{help_text}\n```\n\n"
        markdown_content += f"**Schema:**\n```\n{schema_text}\n```\n\n"

    # Fetch individual action details
    markdown_content += "\n## Action Details\n\n"
    for action in actions:
        help_text, schema_text = get_schema_details(resource_type, "actions", action)
        markdown_content += f"### **{action}**\n\n"
        markdown_content += f"**Description:**\n```\n{help_text}\n```\n\n"
        markdown_content += f"**Schema:**\n```\n{schema_text}\n```\n\n"

    return markdown_content

# Run the script
resource_type = "aws.ec2"
schema_text = run_custodian_schema(["/vagrant/custodian-env/bin/custodian", "schema", resource_type])

if schema_text:
    # Extract filters and actions
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

    # Generate full markdown documentation
    markdown_doc = generate_markdown(resource_type, actions, filters)

    # Save to Markdown file
    with open(f"{resource_type}_custodian.md", "w") as f:
        f.write(markdown_doc)

    print(f"✅ Markdown documentation generated: {resource_type}_custodian.md")
