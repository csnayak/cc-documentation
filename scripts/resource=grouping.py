import csv
from collections import defaultdict

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

# Example usage
csv_file_path = "/vagrant/shared/chatbot/resourcetype.csv"
resource_groups = generate_resource_groups_from_csv(csv_file_path)

# Print the resulting dictionary
print(resource_groups)
