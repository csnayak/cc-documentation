import subprocess
import logging
import os
import datetime
import re
import yaml
from collections import defaultdict
from multiprocessing import Pool, cpu_count
from functools import partial
import time

# Configure logging
logging.basicConfig(
    filename="custodian_schema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_aws_resource_types_from_schema():
    """Get AWS resource types from custodian schema aws command"""
    try:
        logging.info("Getting AWS resource types from custodian schema")
        result = subprocess.run(["custodian", "schema", "aws"], capture_output=True, text=True, check=True)
        schema_output = result.stdout
        
        resource_types = []
        in_resources_section = False
        
        for line in schema_output.split("\n"):
            line = line.strip()
            
            # Look for the resources section
            if line.startswith("resources:") or line.startswith("Resources:"):
                in_resources_section = True
                continue
            
            # If we're in resources section and find a resource (starts with aws.)
            if in_resources_section and line.startswith("- aws."):
                resource_name = line.replace("- ", "").strip()
                resource_types.append(resource_name)
            
            # Stop if we hit another section (like filters, actions, etc.)
            elif in_resources_section and line.startswith("- ") and not line.startswith("- aws."):
                break
            elif in_resources_section and line and not line.startswith("- ") and not line.startswith(" "):
                # Hit another section
                if line.endswith(":"):
                    break
        
        logging.info(f"Found {len(resource_types)} AWS resource types")
        return resource_types
        
    except subprocess.CalledProcessError as error:
        logging.error(f"Failed to get AWS resource types: {error}\n{error.stderr}")
        return []

def generate_resource_groups_from_schema():
    """Generate resource groups from custodian schema instead of CSV"""
    resource_types = get_aws_resource_types_from_schema()
    
    if not resource_types:
        logging.error("No resource types found from schema")
        return {}
    
    # Create one-to-one mapping: resource type -> filename.md
    resource_groups = {}
    
    for resource in resource_types:
        # Direct mapping: aws.access-analyzer-finding -> aws.access-analyzer-finding.md
        filename = f"{resource}.md"
        resource_groups[filename] = [resource]
    
    return resource_groups

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

def generate_markdown_for_resource(args):
    """Generate markdown for a single resource (multiprocessing-friendly)"""
    resource, process_id, total_resources = args
    
    start_time = time.time()
    file_name = f"{resource}.md"
    
    # Setup process-specific logging (avoid conflicts)
    process_logger = logging.getLogger(f"worker_{process_id}")
    process_logger.info(f"[Process {process_id}] Generating Markdown file: {file_name}")
    
    try:
        markdown_content = f"""---
Title: {resource.replace('-', ' ').title()}
Category: Cloud Custodian
Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d')}
Version: 1.0
Resource Type: {resource}
---

# {resource.upper()}

AWS Resource Type: `{resource}`

"""

        # Get filters and actions for this resource
        actions, filters = get_filters_and_actions(resource)

        # Table of Contents
        markdown_content += "\n## Table of Contents\n"
        markdown_content += "- [Available Actions](#available-actions)\n"
        markdown_content += "- [Available Filters](#available-filters)\n"
        markdown_content += "- [Action Details](#action-details)\n"
        markdown_content += "- [Filter Details](#filter-details)\n"

        # Available Actions Section
        markdown_content += "\n## Available Actions\n"
        if actions:
            for action in actions:
                anchor = f"action-{action.lower().replace('_', '-')}"
                markdown_content += f"- [{action}](#{anchor})\n"
        else:
            markdown_content += "_No actions available for this resource._\n"

        # Available Filters Section
        markdown_content += "\n## Available Filters\n"
        if filters:
            for f in filters:
                anchor = f"filter-{f.lower().replace('_', '-')}"
                markdown_content += f"- [{f}](#{anchor})\n"
        else:
            markdown_content += "_No filters available for this resource._\n"

        # Action Details Section
        markdown_content += "\n## Action Details\n"
        if actions:
            for action in actions:
                anchor = f"action-{action.lower().replace('_', '-')}"
                markdown_content += f"\n### Action: {action}\n<a name=\"{anchor}\"></a>\n"
                help_text, schema_text, example_text = get_schema_details(resource, "actions", action)
                
                markdown_content += f"📌 **Description:**\n\n{help_text or '_No description available._'}\n"
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
                
                if schema_text:
                    try:
                        formatted_schema = yaml.safe_dump(yaml.safe_load(schema_text), sort_keys=False, indent=2)
                        formatted_schema = re.sub(r'^-+\n', '', formatted_schema)
                    except Exception:
                        formatted_schema = schema_text
                    markdown_content += f"📌 **Schema:**\n\n```yaml\n{formatted_schema}\n```\n\n"
        else:
            markdown_content += "_No action details available._\n"

        # Filter Details Section
        markdown_content += "\n## Filter Details\n"
        if filters:
            for f in filters:
                anchor = f"filter-{f.lower().replace('_', '-')}"
                markdown_content += f"\n### Filter: {f}\n<a name=\"{anchor}\"></a>\n"
                help_text, schema_text, example_text = get_schema_details(resource, "filters", f)
                
                markdown_content += f"📌 **Description:**\n\n{help_text or '_No description available._'}\n"
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
                
                if schema_text:
                    try:
                        formatted_schema = yaml.safe_dump(yaml.safe_load(schema_text), sort_keys=False, indent=2)
                        formatted_schema = re.sub(r'^-+\n', '', formatted_schema)
                    except Exception:
                        formatted_schema = schema_text
                    markdown_content += f"📌 **Schema:**\n\n```yaml\n{formatted_schema}\n```\n\n"
        else:
            markdown_content += "_No filter details available._\n"

        # Write the file
        output_directory = "./resourcetype/"
        os.makedirs(output_directory, exist_ok=True)
        output_file_path = os.path.join(output_directory, file_name)

        with open(output_file_path, "w", encoding='utf-8') as f:
            f.write(markdown_content)

        elapsed_time = time.time() - start_time
        process_logger.info(f"[Process {process_id}] Completed {file_name} in {elapsed_time:.2f}s")
        
        return {
            'resource': resource,
            'file_name': file_name,
            'status': 'success',
            'actions_count': len(actions),
            'filters_count': len(filters),
            'process_time': elapsed_time,
            'process_id': process_id
        }
        
    except Exception as e:
        error_msg = f"[Process {process_id}] Error generating {file_name}: {str(e)}"
        process_logger.error(error_msg)
        return {
            'resource': resource,
            'file_name': file_name,
            'status': 'error',
            'error': str(e),
            'process_id': process_id
        }

def generate_markdown(file_name, resources):
    """Legacy function - kept for compatibility"""
    # This is now handled by generate_markdown_for_resource
    pass

def main():
    """Main function with multiprocessing support"""
    print("🚀 Starting Cloud Custodian Documentation Generator")
    print("=" * 60)
    
    # Get resource groups from custodian schema
    start_time = time.time()
    resource_groups = generate_resource_groups_from_schema()
    
    if not resource_groups:
        print("❌ No resource types found!")
        return
    
    # Flatten the resource list since each file has only one resource now
    all_resources = []
    for file_name, resources in resource_groups.items():
        all_resources.extend(resources)
    
    total_resources = len(all_resources)
    
    print(f"📋 Discovered {total_resources} AWS resource types")
    print(f"🏗️  Will generate {total_resources} documentation files")
    
    # Determine number of processes
    max_workers = min(cpu_count(), 8)  # Cap at 8 to avoid overwhelming the system
    print(f"🔧 Using {max_workers} parallel processes (CPU cores: {cpu_count()})")
    
    # Prepare arguments for multiprocessing
    process_args = [(resource, i % max_workers + 1, total_resources) 
                   for i, resource in enumerate(all_resources)]
    
    print(f"⏱️  Starting parallel processing...")
    processing_start = time.time()
    
    # Use multiprocessing Pool
    try:
        with Pool(processes=max_workers) as pool:
            results = pool.map(generate_markdown_for_resource, process_args)
        
        # Process results
        successful = [r for r in results if r['status'] == 'success']
        failed = [r for r in results if r['status'] == 'error']
        
        processing_time = time.time() - processing_start
        total_time = time.time() - start_time
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 PROCESSING SUMMARY")
        print("=" * 60)
        print(f"✅ Successfully processed: {len(successful)}")
        print(f"❌ Failed: {len(failed)}")
        print(f"⏱️  Processing time: {processing_time:.2f} seconds")
        print(f"🎯 Total time: {total_time:.2f} seconds")
        print(f"📈 Average time per resource: {processing_time/total_resources:.2f} seconds")
        
        if successful:
            total_actions = sum(r.get('actions_count', 0) for r in successful)
            total_filters = sum(r.get('filters_count', 0) for r in successful)
            print(f"📋 Total actions documented: {total_actions}")
            print(f"🔍 Total filters documented: {total_filters}")
        
        # Show failed resources if any
        if failed:
            print(f"\n❌ FAILED RESOURCES ({len(failed)}):")
            for failure in failed[:10]:  # Show first 10 failures
                print(f"   - {failure['resource']}: {failure.get('error', 'Unknown error')}")
            if len(failed) > 10:
                print(f"   ... and {len(failed) - 10} more failures")
        
        # Show fastest and slowest resources
        if successful:
            successful_with_time = [r for r in successful if 'process_time' in r]
            if successful_with_time:
                fastest = min(successful_with_time, key=lambda x: x['process_time'])
                slowest = max(successful_with_time, key=lambda x: x['process_time'])
                print(f"\n⚡ Fastest: {fastest['resource']} ({fastest['process_time']:.2f}s)")
                print(f"🐌 Slowest: {slowest['resource']} ({slowest['process_time']:.2f}s)")
        
        print(f"\n📁 Output directory: ./resourcetype/")
        print("✅ Documentation generation completed!")
        
        return len(successful), len(failed)
        
    except KeyboardInterrupt:
        print("\n🛑 Process interrupted by user")
        return 0, 0
    except Exception as e:
        print(f"\n❌ Fatal error during processing: {e}")
        return 0, 0

if __name__ == "__main__":
    main()
