import subprocess
import logging
import csv
import os
import datetime
import re
import yaml
from collections import defaultdict

# Configure logging
logging.basicConfig(
    filename="custodian_schema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def generate_resource_groups_from_csv(csv_file):
    resource_groups = defaultdict(list)
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if len(row) < 2:
                continue
            resource, markdown_file = row[0].strip(), row[1].strip()
            resource_groups[markdown_file].append(resource)
    return dict(resource_groups)

def run_custodian_schema(command):
    try:
        logging.info(f"Executing: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as error:
        logging.error(f"Command execution failed: {error}\n{error.stderr}")
        return None

def get_filters_and_actions(resource):
    schema_output = run_custodian_schema(["custodian", "schema", resource])
    if not schema_output:
        logging.error(f"Skipping resource {resource} due to failed schema retrieval.")
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
    return actions, filters

def get_schema_details(resource, category, name):
    command = ["custodian", "schema", f"{resource}.{category}.{name}"]
    output = run_custodian_schema(command)
    if not output:
        return None, None, None

    help_text, schema_text, example_text = "", "", ""
    capturing_help, capturing_schema, capturing_example = False, False, False
    example_lines = []

    for line in output.split("\n"):
        stripped = line.strip()
        if stripped.startswith("Help"):
            capturing_help = True
            capturing_schema = False
            capturing_example = False
            continue
        elif stripped.startswith("Schema"):
            capturing_schema = True
            capturing_help = False
            capturing_example = False
            continue
        elif stripped.startswith(":example:") or stripped.startswith(".. code-block:: yaml"):
            capturing_example = True
            capturing_help = False
            capturing_schema = False
            continue

        if capturing_help:
            help_text += line + "\n"
        elif capturing_schema:
            schema_text += stripped + "\n"
        elif capturing_example:
            example_lines.append(line)

    if example_lines:
        example_text = "\n".join(example_lines)
        example_text = re.sub(r"\.\. code-block:: yaml", "", example_text)
        example_text = re.sub(r"^    ", "", example_text, flags=re.MULTILINE)
        example_text = example_text.strip()

    return help_text.strip(), schema_text.strip(), example_text.strip()

def generate_markdown(file_name, resources):
    logging.info(f"Generating Markdown file: {file_name}")
    markdown_content = f"""---
Title: {file_name.replace('.md', '').replace('-', ' ').title()}
Category: Cloud Custodian
Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d')}
Version: 1.0
---

# AWS Resources Covered
"""
    toc = "\n## Table of Contents\n"

    for resource in resources:
        anchor = resource.replace('.', '-')
        markdown_content += f"- [{resource}](#{anchor})\n"
        toc += f"- [{resource.upper()}](#{anchor})\n"

    markdown_content += toc
    #markdown_content += "\n## AWS Resource Policies\n"

    for resource in resources:
        markdown_content += f"\n## {resource.upper()}\n"
        actions, filters = get_filters_and_actions(resource)

        markdown_content += "\n### Available Actions\n"
        for action in actions:
            anchor = f"action-{action.lower()}"
            markdown_content += f"- [{action}](#{anchor})\n"

        markdown_content += "\n### Available Filters\n"
        for f in filters:
            anchor = f"filter-{f.lower()}"
            markdown_content += f"- [{f}](#{anchor})\n"

        markdown_content += "\n### Action Details\n"
        for action in actions:
            anchor = f"action-{action.lower()}"
            markdown_content += f"\n### Action: {action}\n<a name=\"{anchor}\"></a>\n"
            help_text, schema_text, example_text = get_schema_details(resource, "actions", action)
            markdown_content += f"📌 **Description:**\n\n{help_text}\n"
            markdown_content += "\n📌 **Example Usage:**\n\n"
            if example_text:
                examples = [ex.strip() for ex in example_text.split("\n\n") if ex.strip()]
                for ex in examples:
                    if ex.startswith("policies:"):
                        markdown_content += f"```yaml\n{ex}\n```\n\n"
                    else:
                        markdown_content += f"<!-- {ex} -->\n\n"
            else:
                markdown_content += f"```yaml\nactions:\n  - type: {action}\n```\n\n"
            try:
                formatted_schema = yaml.safe_dump(yaml.safe_load(schema_text), sort_keys=False, indent=2)
                formatted_schema = re.sub(r'^-+\n', '', formatted_schema)
            except Exception:
                formatted_schema = schema_text
            markdown_content += f"📌 **Schema:**\n\n```yaml\n{formatted_schema}\n```\n"

        markdown_content += "\n### Filter Details\n"
        for f in filters:
            anchor = f"filter-{f.lower()}"
            markdown_content += f"\n### Filter: {f}\n<a name=\"{anchor}\"></a>\n"
            help_text, schema_text, example_text = get_schema_details(resource, "filters", f)
            markdown_content += f"📌 **Description:**\n\n{help_text or '_No additional details available._'}\n"
            markdown_content += "\n📌 **Example Usage:**\n\n"
            if example_text:
                examples = [ex.strip() for ex in example_text.split("\n\n") if ex.strip()]
                for ex in examples:
                    if ex.startswith("policies:"):
                        markdown_content += f"```yaml\n{ex}\n```\n\n"
                    else:
                        markdown_content += f"<!-- {ex} -->\n\n"
            else:
                markdown_content += f"```yaml\nfilters:\n  - type: {f}\n```\n\n"
            try:
                formatted_schema = yaml.safe_dump(yaml.safe_load(schema_text), sort_keys=False, indent=2)
                formatted_schema = re.sub(r'^-+\n', '', formatted_schema)
            except Exception:
                formatted_schema = schema_text
            markdown_content += f"📌 **Schema:**\n\n```yaml\n{formatted_schema}\n```\n"

    output_directory = "/vagrant/shared/chatbot/resourcetype/"
    os.makedirs(output_directory, exist_ok=True)
    output_file_path = os.path.join(output_directory, file_name)

    with open(output_file_path, "w") as f:
        f.write(markdown_content)

    logging.info(f"Markdown file generated: {file_name}")

csv_file_path = "/vagrant/shared/chatbot/resourcetype.csv"
resource_groups = generate_resource_groups_from_csv(csv_file_path)
RESOURCE_GROUPS = resource_groups

for file_name, resources in RESOURCE_GROUPS.items():
    generate_markdown(file_name, resources)

print("✅ Markdown files generated successfully!")
